"""Smoke tests for CNNSetMenuNet model.

Verifies seven critical properties:
  - Shape correctness (CSMNET-06): grid [4,2,11,11] + options [4,10,6] -> [4,10].
  - CNN_Encoder output dimension (CSMNET-02): 128-dim embedding from grid input.
  - Warm-start from CNN_2d checkpoint (CSMNET-05): conv+fc weights transfer, fc3 skipped.
  - Permutation invariance (CSMNET-04): shuffling option order produces identical costs.
  - Variable-size masking (CSMNET-04): padding positions zeroed out.
  - All-masked edge case (D-19): returns zeros without RuntimeError.
  - Save/load roundtrip (D-13, D-15, D-16): identical outputs after save/load cycle.

Usage:  python scripts/test_cnnsetmenunet.py
Run from ooh_code/ directory.
"""

import sys
import os
import tempfile

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from Src.Utils.CNNSetMenuNet import CNNSetMenuNet, CNN_Encoder
from Src.Utils.Predictors import CNN_2d


def test_shape_smoke():
    """CSMNET-06: [4,2,11,11]+[4,4]+[4,10,6]+[4,10]bool -> [4,10] output."""
    model = CNNSetMenuNet()
    model.eval()

    grid = torch.randn(4, 2, 11, 11)
    capacity = torch.randn(4, 4)
    options = torch.randn(4, 10, 6)
    mask = torch.ones(4, 10, dtype=torch.bool)
    mask[0, 7:] = False  # partial masking in batch element 0

    with torch.no_grad():
        out = model(grid, capacity, options, mask)

    assert out.shape == (4, 10), f"Expected (4, 10), got {out.shape}"
    return True


def test_encoder_output_dim():
    """CSMNET-02: CNN_Encoder produces [B, 128] from grid + capacity input."""
    encoder = CNN_Encoder(dim=11, n_layers=2, n_filters=32, dropout=0.1, aux_dim=4)
    encoder.eval()

    grid = torch.randn(4, 2, 11, 11)
    capacity = torch.randn(4, 4)

    with torch.no_grad():
        out = encoder(grid, capacity)

    assert out.shape == (4, 128), f"Expected (4, 128), got {out.shape}"
    return True


def test_warm_start():
    """CSMNET-05: CNN_2d weights load into CNN_Encoder; fc3 skipped gracefully."""
    cnn2d = CNN_2d(dim=11, n_layers=2, n_filters=32, dropout=0.1, aux_dim=4, output_dim=3)
    model = CNNSetMenuNet()

    cnn2d_state_dict = cnn2d.state_dict()
    model.load_cnn_weights(cnn2d_state_dict)

    # Verify conv1 weights were transferred
    assert torch.equal(model.encoder.conv1.weight, cnn2d.conv1.weight), \
        "conv1 weights must match after warm-start"
    assert torch.equal(model.encoder.conv1.bias, cnn2d.conv1.bias), \
        "conv1 bias must match after warm-start"

    # Verify conv2 weights were transferred
    assert torch.equal(model.encoder.conv2.weight, cnn2d.conv2.weight), \
        "conv2 weights must match after warm-start"

    # Verify fc1 and fc2 were transferred
    assert torch.equal(model.encoder.fc1.weight, cnn2d.fc1.weight), \
        "fc1 weights must match after warm-start"
    assert torch.equal(model.encoder.fc2.weight, cnn2d.fc2.weight), \
        "fc2 weights must match after warm-start"

    # Verify CNN_Encoder has no fc3 key (it should not exist)
    encoder_keys = set(model.encoder.state_dict().keys())
    assert "fc3.weight" not in encoder_keys, \
        "CNN_Encoder should not have fc3.weight"
    assert "fc3.bias" not in encoder_keys, \
        "CNN_Encoder should not have fc3.bias"

    return True


def test_permutation_invariance():
    """CSMNET-04: Shuffling option order produces identical cost predictions.

    TransformerEncoder without positional encoding is permutation-invariant.
    Eval mode ensures deterministic dropout behavior.
    """
    model = CNNSetMenuNet()
    model.eval()

    torch.manual_seed(42)
    grid = torch.randn(2, 2, 11, 11)
    capacity = torch.randn(2, 4)
    options = torch.randn(2, 8, 6)
    mask = torch.ones(2, 8, dtype=torch.bool)

    # Generate independent random permutations per batch element
    perm0 = torch.randperm(8)
    perm1 = torch.randperm(8)
    options_shuffled = torch.stack([options[0, perm0], options[1, perm1]])

    with torch.no_grad():
        out_orig = model(grid, capacity, options, mask)
        out_shuffled = model(grid, capacity, options_shuffled, mask)

    # Un-permute outputs to compare with original ordering
    out_restored = torch.stack([
        out_shuffled[0, torch.argsort(perm0)],
        out_shuffled[1, torch.argsort(perm1)],
    ])

    assert torch.allclose(out_orig, out_restored, atol=1e-5), \
        f"Permutation invariance violated, max diff: {(out_orig - out_restored).abs().max().item()}"
    return True


def test_masking():
    """CSMNET-04: Padding positions (mask=False) receive exactly zero output."""
    model = CNNSetMenuNet()
    model.eval()

    grid = torch.randn(1, 2, 11, 11)
    capacity = torch.randn(1, 4)
    options = torch.randn(1, 10, 6)
    mask = torch.zeros(1, 10, dtype=torch.bool)
    mask[0, :5] = True  # first 5 real, last 5 padding

    with torch.no_grad():
        out = model(grid, capacity, options, mask)

    assert (out[0, 5:] == 0).all(), "Padding outputs must be exactly zero"
    assert (out[0, :5] != 0).any(), "Real outputs must be non-zero"
    return True


def test_all_masked():
    """D-19 edge case: All-False mask returns zeros without RuntimeError."""
    model = CNNSetMenuNet()
    model.eval()

    grid = torch.randn(2, 2, 11, 11)
    capacity = torch.randn(2, 4)
    options = torch.randn(2, 5, 6)
    mask = torch.zeros(2, 5, dtype=torch.bool)  # all False

    with torch.no_grad():
        out = model(grid, capacity, options, mask)

    assert (out == 0).all(), "All-masked output must be all zeros"
    assert out.shape == (2, 5), f"Shape preserved even with all-masked, got {out.shape}"
    return True


def test_save_load():
    """D-13, D-15, D-16: Save and load roundtrip produces identical outputs."""
    model = CNNSetMenuNet()
    model.eval()

    grid = torch.randn(2, 2, 11, 11)
    capacity = torch.randn(2, 4)
    options = torch.randn(2, 6, 6)
    mask = torch.ones(2, 6, dtype=torch.bool)

    with torch.no_grad():
        out_before = model(grid, capacity, options, mask).clone()

    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as f:
        tmppath = f.name

    try:
        model.save(tmppath)

        model2 = CNNSetMenuNet()
        model2.load(tmppath)

        with torch.no_grad():
            out_after = model2(grid, capacity, options, mask)

        assert torch.allclose(out_before, out_after, atol=1e-6), \
            f"Save/load roundtrip mismatch, max diff: {(out_before - out_after).abs().max().item()}"
    finally:
        os.unlink(tmppath)

    return True


if __name__ == "__main__":
    tests = [
        ("Shape [B,2,11,11]+[B,10,6]->[B,10]", test_shape_smoke),
        ("CNN_Encoder output dim 128", test_encoder_output_dim),
        ("Warm-start from CNN_2d", test_warm_start),
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
