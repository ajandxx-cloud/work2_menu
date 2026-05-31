"""MLPMenuNet: per-candidate MLP baseline for DRT service menu cost prediction.

A simple multi-layer perceptron that processes each candidate's 6-dim option
features independently (no set-attention, no CNN spatial encoding). Serves as
an ablation baseline to isolate the contribution of the set-attention mechanism
in CNN-SetMenuNet.

Architecture:
    Linear(6 → 64) → ReLU → Dropout → Linear(64 → 64) → ReLU → Dropout → Linear(64 → 1)

Input contract (matches SetMenuNet interface):
    option_features: Tensor[B, K, 6]  float32  per-candidate features
    option_mask:     Tensor[B, K]     bool     True for valid candidates

Output: Tensor[B, K] float32 per-candidate predicted marginal cost.
"""

import torch
import torch.nn as nn


class MLPMenuNet(nn.Module):
    """Per-candidate MLP for cost prediction (no set-attention ablation)."""

    def __init__(self, input_dim=6, hidden_dim=64, dropout=0.05):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.dropout_p = dropout

        self.mlp = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, option_features, option_mask):
        """Predict per-candidate costs from option features.

        Args:
            option_features: Tensor[B, K, 6] per-candidate features.
            option_mask: Tensor[B, K] bool — True for valid candidates.

        Returns:
            Tensor[B, K] per-candidate predicted cost.
            Padding positions (mask=False) receive zero output.
        """
        B, K = option_features.shape[0], option_features.shape[1]

        # All-masked guard
        if not option_mask.any():
            return torch.zeros(B, K, device=option_features.device,
                               dtype=option_features.dtype)

        out = self.mlp(option_features).squeeze(-1)  # [B, K]
        out = out.masked_fill(~option_mask, 0.0)
        return out

    def reset(self):
        """No-op reset for stateless model (matches CNN_2d interface)."""
        pass

    def save(self, filename):
        """Save model state dict to file (matches CNN_2d interface)."""
        torch.save(self.state_dict(), filename)

    def load(self, filename):
        """Load model state dict from file (matches CNN_2d interface)."""
        self.load_state_dict(
            torch.load(filename, map_location='cpu', weights_only=True)
        )
        self.eval()
