"""CNNSetMenuNet: hybrid CNN + set-attention model for DRT service menu design.

Combines a CNN_Encoder (derived from CNN_2d, warm-startable) with a
TransformerEncoder set-attention module to predict per-candidate marginal
costs for dynamic service menu construction.

Architecture:
    1. CNN_Encoder extracts 128-dim spatial context z_t from grid state
       (mirrors CNN_2d conv1..fc2, omits fc3 output head).
    2. Fusion layer broadcasts z_t across candidates and concatenates with
       per-candidate 6-dim option features, producing [B, K, 134] embeddings
       projected to [B, K, d_model].
    3. TransformerEncoder processes fused embeddings with permutation-invariant
       set-attention (same hyperparams as SetMenuNet).
    4. Output head produces per-candidate cost predictions [B, K].

Input contract:
    grid_input:     Tensor[B, n_layers, dim, dim]  e.g. [B, 2, 11, 11]
    capacity:       Tensor[B, aux_dim]              e.g. [B, 4]
    option_features: Tensor[B, K, 6]  float32  per-candidate features
    option_mask:     Tensor[B, K]     bool     True for valid candidates

Output: Tensor[B, K] float32 per-candidate predicted marginal cost.

Relationships:
    CNN_Encoder mirrors ooh_code/Src/Utils/Predictors.CNN_2d through fc2.
    Set-attention mirrors ooh_code/Src/Utils/SetMenuNet with separate instance.
"""

import numpy as np
import torch
import torch.nn as nn


class CNN_Encoder(nn.Module):
    """CNN spatial state encoder derived from CNN_2d (Predictors.py).

    Mirrors CNN_2d's conv1, conv2, avgpool1, flatten, fc1, fc2 layers exactly,
    but omits fc3. Outputs a 128-dim embedding z_t for downstream fusion.

    Constructor signature matches CNN_2d for warm-start compatibility.
    """

    def __init__(self, dim, n_layers, n_filters, dropout, aux_dim=1):
        super().__init__()

        kernel1 = (3, 3)
        kernel2 = (2, 2)
        dilation = 1
        stride = (1, 1)
        padding = (1, 1)
        out_channels = n_filters

        # Calculate output shape of conv and pool layers (matches CNN_2d exactly)
        h1 = np.floor(((dim + 2 * padding[0] - dilation * (kernel1[0] - 1) - 1) / stride[0]) + 1)
        w1 = np.floor(((dim + 2 * padding[1] - dilation * (kernel1[1] - 1) - 1) / stride[1]) + 1)
        h2 = np.floor(((h1 + 2 * padding[0] - dilation * (kernel1[0] - 1) - 1) / stride[0]) + 1)
        w2 = np.floor(((w1 + 2 * padding[1] - dilation * (kernel1[1] - 1) - 1) / stride[1]) + 1)
        h3 = np.floor(((h2 + 2 * padding[0] - kernel2[0]) / stride[0]) + 1)
        w3 = np.floor(((w2 + 2 * padding[1] - kernel2[1]) / stride[0]) + 1)

        self.conv1 = nn.Conv2d(
            in_channels=n_layers, dilation=dilation,
            out_channels=out_channels, kernel_size=kernel1, padding=padding,
        )
        self.conv2 = nn.Conv2d(
            in_channels=out_channels, dilation=dilation,
            out_channels=2 * out_channels, kernel_size=kernel1, padding=padding,
        )
        self.avgpool1 = nn.AvgPool2d(
            kernel_size=kernel2, stride=stride, padding=padding,
        )

        self.flatten = nn.Flatten(start_dim=1)

        self.fc1 = nn.Linear(
            in_features=int(aux_dim + 2 * out_channels * h3 * w3),
            out_features=256,
        )
        self.fc2 = nn.Linear(256, 128)
        # No fc3 — this encoder produces a 128-dim embedding, not task output.

        self.dropout = nn.Dropout(p=dropout)

        # Store hyperparameters as instance attributes for downstream inspection
        self.dim = dim
        self.n_layers = n_layers
        self.n_filters = n_filters
        self.aux_dim = aux_dim
        self.dropout_p = dropout

    def forward(self, x, capacity):
        """Encode grid state + aux features into 128-dim embedding.

        Args:
            x: Tensor[B, n_layers, dim, dim] grid state input.
            capacity: Tensor[B, aux_dim] auxiliary features (capacity, etc.).

        Returns:
            Tensor[B, 128] spatial context embedding z_t.
        """
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = self.avgpool1(x)
        x = self.flatten(x)
        if capacity.dim() == 1:
            capacity = capacity.unsqueeze(1)
        x = torch.cat((x, capacity), dim=1)
        x = self.dropout(nn.functional.relu(self.fc1(x)))
        x = self.dropout(nn.functional.relu(self.fc2(x)))
        return x


class CNNSetMenuNet(nn.Module):
    """Hybrid CNN + set-attention model for DRT service menu design.

    Combines CNN_Encoder global state encoding with TransformerEncoder
    set-attention over candidate option features. CNN_Encoder produces a
    128-dim spatial context embedding z_t that is fused with per-candidate
    6-dim option features via concatenation + projection. The fused embeddings
    are processed by set-attention to produce per-candidate cost predictions.
    """

    def __init__(self, dim=11, n_layers=2, n_filters=32, dropout=0.1,
                 aux_dim=4, d_model=64, nhead=4, num_layers=2,
                 dim_feedforward=256):
        super().__init__()

        # Store all hyperparameters as instance attributes
        self.dim = dim
        self.n_layers = n_layers
        self.n_filters = n_filters
        self.aux_dim = aux_dim
        self.d_model = d_model
        self.nhead = nhead
        self.num_layers = num_layers
        self.dim_feedforward = dim_feedforward
        self.dropout_p = dropout

        # CNN global state encoder (warm-startable from CNN_2d checkpoint)
        self.encoder = CNN_Encoder(dim, n_layers, n_filters, dropout, aux_dim)

        # Fusion projection: z_t [B,128] + option [B,K,6] -> [B,K,134] -> [B,K,d_model]
        self.fusion_proj = nn.Linear(6 + 128, d_model)

        # Set-attention encoder (same architecture as SetMenuNet)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
        )
        self.set_encoder = nn.TransformerEncoder(
            encoder_layer, num_layers=num_layers,
        )

        # Per-candidate output head
        self.output_head = nn.Linear(d_model, 1)

    def forward(self, grid_input, capacity, option_features, option_mask):
        """Process grid state + candidate options to predict per-candidate costs.

        Args:
            grid_input: Tensor[B, n_layers, dim, dim] spatial grid state.
            capacity: Tensor[B, aux_dim] auxiliary features.
            option_features: Tensor[B, K, 6] float32 per-candidate features.
            option_mask: Tensor[B, K] bool — True for valid candidates.

        Returns:
            Tensor[B, K] float32 per-candidate predicted marginal cost.
            Padding positions (mask=False) receive zero output.
        """
        B, K = option_features.shape[0], option_features.shape[1]

        # All-masked guard: return zeros without entering encoders
        if not option_mask.any():
            return torch.zeros(B, K, device=option_features.device,
                               dtype=option_features.dtype)

        # CNN path: extract 128-dim global state embedding
        z_t = self.encoder(grid_input, capacity)  # [B, 128]

        # Fusion: broadcast z_t to each candidate and concatenate with option features
        z_t_expanded = z_t.unsqueeze(1).expand(-1, K, -1)  # [B, K, 128]
        fused = torch.cat([z_t_expanded, option_features], dim=-1)  # [B, K, 134]
        x = self.fusion_proj(fused)  # [B, K, d_model]

        # Set-attention: process fused embeddings with permutation invariance
        src_key_padding_mask = ~option_mask  # PyTorch convention: True = ignore
        x = self.set_encoder(x, src_key_padding_mask=src_key_padding_mask)  # [B, K, d_model]

        # Per-candidate cost prediction
        out = self.output_head(x).squeeze(-1)  # [B, K]

        # Zero out padding positions
        out = out.masked_fill(~option_mask, 0.0)

        return out

    def reset(self):
        """No-op reset for stateless model (matches CNN_2d interface)."""
        pass

    def save(self, filename):
        """Save model state dict to file (matches CNN_2d interface)."""
        torch.save(self.state_dict(), filename)

    def load(self, filename):
        """Load model state dict from file (matches CNN_2d interface).

        Uses weights_only=True for safe deserialization (PyTorch 2.x).
        Calls self.eval() to disable dropout after loading.
        """
        self.load_state_dict(
            torch.load(filename, map_location='cpu', weights_only=True)
        )
        self.eval()

    @torch.no_grad()
    def load_cnn_weights(self, state_dict):
        """Load CNN_2d checkpoint weights into CNN_Encoder (skip fc3 and non-matching keys).

        Logs which keys were loaded and which were skipped for debugging.
        fc3 mismatch is handled gracefully — it is absent from CNN_Encoder.

        Args:
            state_dict: dict of CNN_2d checkpoint weights (from torch.load).
        """
        encoder_dict = self.encoder.state_dict()
        loaded_keys = []
        skipped_keys = []
        for key in encoder_dict:
            if key in state_dict:
                encoder_dict[key] = state_dict[key]
                loaded_keys.append(key)
            else:
                skipped_keys.append(key)
        self.encoder.load_state_dict(encoder_dict)
        print(f"CNN_Encoder warm-start: loaded {len(loaded_keys)} keys, skipped {len(skipped_keys)} keys")
        if skipped_keys:
            print(f"  Skipped: {skipped_keys}")
