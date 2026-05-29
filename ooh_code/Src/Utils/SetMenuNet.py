"""SetMenuNet: permutation-invariant set-attention model for DRT service menu design.

Processes candidate service option sets using a TransformerEncoder without
positional encoding, producing per-candidate cost predictions. Designed as
the set-attention backbone for the CNN-SetMenuNet hybrid model.

Input contract (from option_features.build_option_tensor):
    option_features: Tensor[B, K, 6] float32 — 6-dim per-candidate features
    option_mask:     Tensor[B, K]    bool    — True for real candidates

Architecture:
    input_proj:   Linear(6, d_model)           — per-candidate embedding
    encoder:      TransformerEncoder (2 layers, 4 heads) — set-attention
    output_head:  Linear(d_model, 1)            — per-candidate cost prediction
"""

import torch
import torch.nn as nn


class SetMenuNet(nn.Module):
    """Permutation-invariant set-attention model for candidate option sets.

    Uses nn.TransformerEncoder without positional encoding to process
    variable-size candidate sets with batch support and masking.
    """

    def __init__(self, input_dim=6, d_model=64, nhead=4, num_layers=2,
                 dim_feedforward=256, dropout=0.1):
        super().__init__()

        self.d_model = d_model
        self.nhead = nhead
        self.num_layers = num_layers
        self.input_dim = input_dim

        # Per-candidate input projection (named for Phase 4 replacement)
        self.input_proj = nn.Linear(input_dim, d_model)

        # Set-attention encoder: no positional encoding (pure feature model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(
            encoder_layer, num_layers=num_layers
        )

        # Per-candidate output head (named for Phase 4 replacement)
        self.output_head = nn.Linear(d_model, 1)

    def forward(self, option_features, option_mask):
        """Process a batch of candidate option sets.

        Args:
            option_features: Tensor[B, K, input_dim] float32 per-candidate features.
            option_mask: Tensor[B, K] bool — True for valid candidates.

        Returns:
            Tensor[B, K] float32 cost predictions. Padding positions (mask=False)
            receive zero output.
        """
        B, K = option_features.shape[0], option_features.shape[1]

        # All-masked guard: return zeros without entering the encoder
        if not option_mask.any():
            return torch.zeros(B, K, device=option_features.device,
                               dtype=option_features.dtype)

        # Project input features to d_model dimensions
        x = self.input_proj(option_features)  # [B, K, d_model]

        # Invert mask for PyTorch convention: True = ignore position
        src_key_padding_mask = ~option_mask

        # Set-attention encoding (no positional encoding)
        x = self.encoder(x, src_key_padding_mask=src_key_padding_mask)  # [B, K, d_model]

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
        """
        self.load_state_dict(
            torch.load(filename, map_location='cpu', weights_only=True)
        )
