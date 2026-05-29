"""Smoke test for SetMenuNet model.

Verifies three critical properties:
  - Permutation invariance (SMNET-03): shuffling candidate order produces
    identical cost predictions because self-attention has no positional encoding.
  - Variable-size masking (SMNET-04): padding rows (mask=False) receive
    exactly zero output.
  - Correct input/output shapes (SMNET-06): [B,K,6] input produces [B,K]
    output for various batch sizes and candidate counts.

Also validates architecture configuration (SMNET-02), the all-masked edge
case, and save/load roundtrip fidelity.

Usage:  python scripts/test_setmenunet.py
Run from ooh_code/ directory.
"""

import sys
import os
import tempfile

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from Src.Utils.SetMenuNet import SetMenuNet


def test_shape_smoke():
    """SMNET-06: [4, 10, 6] input with partial masking produces [4, 10] output."""
    model = SetMenuNet()
    model.eval()

    features = torch.randn(4, 10, 6)
    mask = torch.ones(4, 10, dtype=torch.bool)
    mask[0, 7:] = False  # partial masking in batch element 0

    with torch.no_grad():
        out = model(features, mask)

    assert out.shape == (4, 10), f"Expected (4, 10), got {out.shape}"
    return True


def test_architecture_config():
    """SMNET-02: Verify default architecture hyperparameters match spec."""
    model = SetMenuNet()

    assert model.d_model == 64, f"Expected d_model=64, got {model.d_model}"
    assert model.nhead == 4, f"Expected nhead=4, got {model.nhead}"
    assert model.num_layers == 2, f"Expected num_layers=2, got {model.num_layers}"
    assert model.input_proj.in_features == 6, \
        f"Expected input_proj.in_features=6, got {model.input_proj.in_features}"
    assert model.input_proj.out_features == 64, \
        f"Expected input_proj.out_features=64, got {model.input_proj.out_features}"
    assert model.output_head.in_features == 64, \
        f"Expected output_head.in_features=64, got {model.output_head.in_features}"
    assert model.output_head.out_features == 1, \
        f"Expected output_head.out_features=1, got {model.output_head.out_features}"
    assert len(model.encoder.layers) == 2, \
        f"Expected 2 encoder layers, got {len(model.encoder.layers)}"
    return True


def test_permutation_invariance():
    """SMNET-03: Shuffling candidate order produces identical predictions.

    Self-attention without positional encoding is permutation-invariant.
    Eval mode is critical for deterministic dropout behavior (D-07).
    """
    model = SetMenuNet()
    model.eval()

    torch.manual_seed(42)
    x = torch.randn(2, 8, 6)
    mask = torch.ones(2, 8, dtype=torch.bool)

    # Generate independent random permutations per batch element
    perm0 = torch.randperm(8)
    perm1 = torch.randperm(8)
    x_shuffled = torch.stack([x[0, perm0], x[1, perm1]])

    with torch.no_grad():
        out_orig = model(x, mask)
        out_shuffled = model(x_shuffled, mask)

    # Un-permute outputs to compare with original ordering
    out_restored = torch.stack([
        out_shuffled[0, torch.argsort(perm0)],
        out_shuffled[1, torch.argsort(perm1)],
    ])

    assert torch.allclose(out_orig, out_restored, atol=1e-5), \
        f"Permutation invariance violated, max diff: {(out_orig - out_restored).abs().max().item()}"
    return True


def test_masking():
    """SMNET-04: Padding positions (mask=False) receive exactly zero output."""
    model = SetMenuNet()
    model.eval()

    features = torch.randn(1, 10, 6)
    mask = torch.zeros(1, 10, dtype=torch.bool)
    mask[0, :5] = True  # first 5 real, last 5 padding

    with torch.no_grad():
        out = model(features, mask)

    assert (out[0, 5:] == 0).all(), "Padding outputs must be exactly zero (D-15, D-18)"
    assert (out[0, :5] != 0).any(), "Real outputs must be non-zero"
    return True


def test_all_masked():
    """Edge case (D-14): All-False mask returns all zeros without RuntimeError."""
    model = SetMenuNet()
    model.eval()

    features = torch.randn(2, 5, 6)
    mask = torch.zeros(2, 5, dtype=torch.bool)  # all False

    with torch.no_grad():
        out = model(features, mask)

    assert (out == 0).all(), "All-masked output must be all zeros"
    assert out.shape == (2, 5), f"Shape preserved even with all-masked, got {out.shape}"
    return True


def test_save_load():
    """D-12: Save and load roundtrip produces identical model outputs."""
    model = SetMenuNet()
    model.eval()

    features = torch.randn(2, 6, 6)
    mask = torch.ones(2, 6, dtype=torch.bool)

    with torch.no_grad():
        out_before = model(features, mask).clone()

    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as f:
        tmppath = f.name

    try:
        model.save(tmppath)

        model2 = SetMenuNet()
        model2.load(tmppath)
        model2.eval()

        with torch.no_grad():
            out_after = model2(features, mask)

        assert torch.allclose(out_before, out_after, atol=1e-6), \
            f"Save/load roundtrip mismatch, max diff: {(out_before - out_after).abs().max().item()}"
    finally:
        os.unlink(tmppath)

    return True


if __name__ == "__main__":
    tests = [
        ("Shape [4,10,6]->[4,10]", test_shape_smoke),
        ("Architecture config", test_architecture_config),
        ("Permutation invariance", test_permutation_invariance),
        ("Masking zeros padding", test_masking),
        ("All-masked edge case", test_all_masked),
        ("Save/load roundtrip", test_save_load),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {name}: {e}")
            failed += 1

    print(f"\n{passed}/{passed + failed} tests passed")
    if failed > 0:
        sys.exit(1)
