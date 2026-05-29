# Phase 3: SetMenuNet Model - Context

**Gathered:** 2026-05-29
**Status:** Ready for planning

<domain>
## Phase Boundary

Build a standalone set-attention nn.Module (SetMenuNet) that processes candidate sets with permutation invariance, batch support, and variable-size masking. This is the core architectural contribution — a model that understands the relationship between candidates in a set, not just individual candidates.

Input: Tensor[B, K, 6] option features + Tensor[B, K] bool mask
Output: Tensor[B, K] per-candidate predicted marginal cost

The model lives in `Src/Utils/SetMenuNet.py` as a standalone module. Phase 4 (CNN-SetMenuNet) will use it as a component. Phase 5 (Algorithm Integration) will wire it into the DSPO training loop.

</domain>

<decisions>
## Implementation Decisions

### Architecture Configuration
- **D-01:** Hidden/embedding dimension = **64**. Input projection from 6-dim to 64-dim via linear layer. Good balance for K=10 candidates with 6-dim features; not overparameterized for the dataset scale.
- **D-02:** Feed-forward expansion ratio = **4x** (64→256 inner dim). Standard transformer practice.
- **D-03:** Number of attention layers = **2**, number of heads = **4**. As specified in REQUIREMENTS (SMNET-02). Head dim = 64/4 = 16.
- **D-04:** Dropout = **0.1** on attention weights and FFN. Standard default.

### Implementation Approach
- **D-05:** Use **PyTorch `nn.TransformerEncoderLayer`** (built-in) rather than custom attention. Simpler, well-tested, automatically permutation invariant when no positional encoding is used. Two layers stacked via `nn.TransformerEncoder`.
- **D-06:** **No positional encoding**. Critical for permutation invariance (SMNET-03) — without position info, the model treats candidates as an unordered set.
- **D-07:** Permutation invariance is guaranteed by architecture (no position encoding + self-attention), but verify with a test: shuffle input → same output.

### Input/Output Contract
- **D-08:** `forward(option_features, option_mask)` signature — takes [B, K, 6] float32 features and [B, K] bool mask. Returns [B, K] cost predictions.
- **D-09:** Masking via `src_key_padding_mask` parameter of TransformerEncoder. The mask needs to be inverted for PyTorch convention (True = ignore/padding). Convert from our convention (True = valid) inside forward.
- **D-10:** Input projection: `nn.Linear(6, 64)` maps raw features to hidden dim before attention.
- **D-11:** Output head: single `nn.Linear(64, 1)` per candidate, then squeeze to [B, K]. No MLP — attention output is already rich, and multi-output (cost+ETA+IVT) is handled at algorithm level in Phase 5.

### Module Interface
- **D-12:** Inherit `nn.Module` directly (not CNN_2d — different input contract). Implement `reset()` (no-op), `save(filename)` (state_dict), `load(filename)` (load_state_dict) for compatibility with Agent base class pattern.
- **D-13:** SetMenuNet is a **pure feature processing model** — it does NOT consume spatial grid or capacity features. CNN-SetMenuNet (Phase 4) will handle the hybrid input by concatenating CNN z_t with option features before feeding to SetMenuNet.

### Variable-Size Handling
- **D-14:** Empty candidate sets (K=0 after filtering) are padded to max_k all-zeros with all-False mask by build_option_tensor. SetMenuNet receives this naturally — attention over all-masked input produces uniform output, which the mask filters downstream.
- **D-15:** Padding rows (mask=False) receive zero cost predictions via post-processing: `output[~mask] = 0.0` after the forward pass. This ensures downstream code sees clean zeros for invalid candidates.

### Testing
- **D-16:** Smoke test: synthetic [4, 10, 6] input → [4, 10] output without error (SMNET-06).
- **D-17:** Permutation test: shuffle rows of input → identical output (SMNET-03).
- **D-18:** Masking test: K=5 real + K=5 padding → padding rows output zero.

### Claude's Discretion
- Exact initialization scheme for linear layers (default PyTorch is fine)
- Whether to apply layer normalization before or after attention (PyTorch default: after)
- Gradient clipping strategy (handled at algorithm level)
- Learning rate (handled at algorithm level)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Option Feature Contract (from Phase 2)
- `ooh_code/Src/Utils/option_features.py` — normalize_features() + build_option_tensor() producing [K, 6] float32 + [K] bool mask
- `ooh_code/Src/Algorithms/DSPO_Menu.py` lines 647-714 — build_option_features() instance method producing the tensors SetMenuNet will consume

### Existing Model Patterns
- `ooh_code/Src/Utils/Predictors.py` lines 31-92 — CNN_2d: nn.Module with reset()/save()/load() interface, conv+fc architecture
- `ooh_code/Src/Algorithms/Agent.py` lines 5-65 — Agent base class: self.modules = [(name, module)], init/save/load/train_mode/eval_mode/step

### Training Infrastructure
- `ooh_code/Src/Algorithms/DSPO.py` lines 71-72, 295-301 — HuberLoss(delta=1.0), self_supervised_update pattern
- `ooh_code/Src/Utils/Utils.py` lines 240-313 — MemoryBuffer: add/sample/batch_sample for training data

### Data Structures
- `ooh_code/Environments/OOH/containers.py` — ServiceBundle, MenuOffer dataclass definitions

### Requirements and Roadmap
- `.planning/REQUIREMENTS.md` — SMNET-01 through SMNET-06
- `.planning/ROADMAP.md` — Phase 3 goal and success criteria
- `.planning/phases/02-option-feature-extractor/02-CONTEXT.md` — Phase 2 decisions (feature format, tensor shape)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `nn.TransformerEncoderLayer` / `nn.TransformerEncoder` — PyTorch built-in set-attention, handles masking via src_key_padding_mask
- `nn.Module` base — standard PyTorch module with state_dict save/load
- DSPO.py's `self_supervised_update` pattern — zero_grad → forward → loss → backward → step
- Agent.py's `self.modules` registration — model wrapped as ('supervised_ml', model) for unified save/load

### Established Patterns
- Models inherit `nn.Module`, implement `reset()` (no-op), `save()` (torch.save state_dict), `load()` (load_state_dict)
- Training: optimizer + HuberLoss created externally, model only produces differentiable output
- Predictors.py models use `forward(x, capacity)` — SetMenuNet uses different contract `forward(option_features, option_mask)` since it operates on sets not grids

### Integration Points
- Phase 4: CNN-SetMenuNet will instantiate SetMenuNet and pass concatenated [CNN_z_t, option_features] through it
- Phase 5: CNN_SetMenu algorithm will replace `self.supervised_ml` with the hybrid model, using the same Agent.modules pattern
- DSPO_Menu.build_option_features() (line 647) produces the exact tensor format SetMenuNet consumes

</code_context>

<specifics>
## Specific Ideas

- Input projection layer should be named `self.input_proj` for clarity when CNN-SetMenuNet (Phase 4) replaces it with a wider projection
- Output head should be named `self.output_head` for similar replacement flexibility
- The model should store `self.d_model = 64`, `self.nhead = 4`, `self.num_layers = 2` as attributes for easy access by downstream integration code
- Permutation invariance test should use torch.manual_seed for reproducibility: create input, clone+shuffle rows, assert allclose output

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 03-setmenunet-model*
*Context gathered: 2026-05-29*
