# Phase 3: SetMenuNet Model - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-29
**Phase:** 03-setmenunet-model
**Areas discussed:** Hidden dimension, FFN ratio, Implementation approach, Output head
**Mode:** Auto (--auto flag)

---

## Hidden/Embedding Dimension

| Option | Description | Selected |
|--------|-------------|----------|
| 32 | Lightweight, may underfit for 6-dim→set interaction | |
| 64 | Good balance for K=10, 6-dim input; standard set-model scale | ✓ |
| 128 | Larger, matches CNN_2d's fc2 output dim | |

**Selected:** 64 (recommended default)
**Notes:** K=10 candidates with 6-dim features — 64 hidden dim provides enough capacity without overfitting. Phase 4 will concatenate CNN z_t [128] with option features, using a wider projection.

---

## Feed-Forward Expansion Ratio

| Option | Description | Selected |
|--------|-------------|----------|
| 2x (128 inner) | Smaller, faster training | |
| 4x (256 inner) | Standard transformer practice | ✓ |

**Selected:** 4x (recommended default)
**Notes:** Standard practice for transformer FFN layers. 64→256→64 provides sufficient non-linearity.

---

## Implementation Approach

| Option | Description | Selected |
|--------|-------------|----------|
| nn.TransformerEncoderLayer (PyTorch built-in) | Proven, well-tested, permutation invariant without position encoding | ✓ |
| Custom multi-head attention | More control, more code to debug | |

**Selected:** nn.TransformerEncoderLayer (recommended default)
**Notes:** PyTorch's built-in transformer handles masking via src_key_padding_mask. No positional encoding needed for permutation invariance. Two layers stacked via nn.TransformerEncoder.

---

## Output Head Design

| Option | Description | Selected |
|--------|-------------|----------|
| Single linear [64→1] | Simpler, attention output already rich | ✓ |
| MLP [64→32→1] | More expressive, may overfit | |

**Selected:** Single linear (recommended default)
**Notes:** Multi-output (cost+ETA+IVT) is handled at the algorithm integration level (Phase 5), not in the base SetMenuNet model. Phase 4's CNN-SetMenuNet can customize the output head if needed.

---

## Claude's Discretion

- Dropout rate: 0.1 (standard default)
- Layer normalization: PyTorch default (post-attention)
- Initialization: PyTorch default
- Gradient clipping: handled at algorithm level

## Deferred Ideas

None — all decisions within Phase 3 scope.
