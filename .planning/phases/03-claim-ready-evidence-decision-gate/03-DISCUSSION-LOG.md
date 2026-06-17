# Phase 3: Claim-Ready Evidence Decision Gate - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-17T10:08:09.1788059+08:00
**Phase:** 3-Claim-Ready Evidence Decision Gate
**Areas discussed:** Frozen Settings Gap, Final Replay Legitimacy Threshold, Claim Classification Rule, Failure And Second-Attempt Rule

---

## Frozen Settings Gap

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Missing freeze/protocol handling | Strict no-go | Missing `FROZEN_FINAL_SETTINGS.md` / `CALIBRATION_PROTOCOL.md` directly locks diagnostic path. | No |
| Missing freeze/protocol handling | Allow controlled reconstruction | Reconstruct a freeze/protocol record from current files or history. | No |
| Missing freeze/protocol handling | Write blocked freeze decision | Record `blocked_pending_gate_cleanup`; final replay is not authorized until gates are satisfied. | Yes |
| Missing freeze/protocol handling | Agent decides | Agent chooses the conservative research-integrity boundary. | No |

**User's choice:** Write blocked freeze decision.
**Notes:** Phase 3 should classify the current final path as blocked pending gate cleanup, not immediate authorization.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Allowed sources for later gap closure | Only current manifest and current file state | Use current manifests and current filesystem facts only. | Yes |
| Allowed sources for later gap closure | Allow git-history old files | Restore or cite named old freeze/protocol files from git history. | No |
| Allowed sources for later gap closure | Allow writing a new protocol | Write a new protocol from current evidence for future rerun. | No |
| Allowed sources for later gap closure | Agent decides | Agent chooses the conservative source rule. | No |

**User's choice:** Only current manifest and current file state.
**Notes:** Do not restore or mine old legacy planning files for Phase 3 authorization.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Missing protocol reference interpretation | Treat as unverified statement | Manifest intent exists, but missing protocol means no replay authorization. | Yes |
| Missing protocol reference interpretation | Treat as temporary freeze candidate | Use current manifest as a candidate starting point after later freeze record creation. | No |
| Missing protocol reference interpretation | Invalidate final manifest | Treat final manifest as unusable because referenced protocol is missing. | No |
| Missing protocol reference interpretation | Agent decides | Agent chooses the interpretation. | No |

**User's choice:** Treat as unverified statement.
**Notes:** `selected_runtime_knobs.source` cannot prove pre-run selection while `CALIBRATION_PROTOCOL.md` is absent.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Where to write blocked finding | Only M3_CLAIM_READY_DECISION.md | Keep Phase 3 as a decision gate and do not create freeze/protocol docs. | Yes |
| Where to write blocked finding | Also create blocked FROZEN_FINAL_SETTINGS.md | Create a blocked freeze file for later tests. | No |
| Where to write blocked finding | Create both protocol and freeze files | Rebuild missing protocol and freeze docs in Phase 3. | No |
| Where to write blocked finding | Agent decides | Agent chooses output scope. | No |

**User's choice:** Only M3_CLAIM_READY_DECISION.md.
**Notes:** Phase 3 should not expand into protocol reconstruction.

---

## Final Replay Legitimacy Threshold

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Phase 4 replay authorization | No-go until all gates already passed | Phase 4 cannot touch replay until gates are already complete. | No |
| Phase 4 replay authorization | Conditional go after gates | Phase 4 may perform gate cleanup/readiness, then replay only if gates pass. | Yes |
| Phase 4 replay authorization | Allow replay attempt then guard decides | Permit replay attempt and let later guard outcome decide claims. | No |
| Phase 4 replay authorization | Agent decides | Agent chooses authorization rule. | No |

**User's choice:** Conditional go after gates.
**Notes:** Phase 3 does not authorize immediate final replay.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Required pre-replay gates | Only provenance gates | Require clean git, freeze/protocol, checkpoint, and dependency evidence. | No |
| Required pre-replay gates | Provenance plus manifest/paired replay gates | Also require stable manifest, seven policy tags, fixed splits/seeds, and valid paired/varied fields. | Yes |
| Required pre-replay gates | Provenance plus manifest plus package gates | Also require package/artifact builders before replay. | No |
| Required pre-replay gates | Agent decides | Agent chooses gate set. | No |

**User's choice:** Provenance plus manifest/paired replay gates.
**Notes:** Package gates determine post-replay claim status, but replay start requires provenance and manifest fairness gates.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Legitimate cleanup changes | Only path/metadata repairs | Allow only evidence-chain repair, not result-affecting setting changes. | Yes |
| Legitimate cleanup changes | Allow runtime scale changes | Permit resource-related scale changes while keeping policy family. | No |
| Legitimate cleanup changes | Allow parameter changes if recorded | Permit broader setting changes if pre-recorded. | No |
| Legitimate cleanup changes | Agent decides | Agent chooses cleanup boundary. | No |

**User's choice:** Only path/metadata repairs.
**Notes:** Changing policies, split/seed, metrics, or frozen runtime knobs invalidates final replay path.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Post-replay claim decision | Strictly by generated CLAIM_GUARD.json | Artifact gates and strict claim guard are the claim authority. | Yes |
| Post-replay claim decision | Human judgment may override guard | Allow narrative judgment to override guard output. | No |
| Post-replay claim decision | Completed replay is claim-ready | Treat completion as sufficient for claim readiness. | No |
| Post-replay claim decision | Agent decides | Agent chooses post-replay authority. | No |

**User's choice:** Strictly by generated `CLAIM_GUARD.json`.
**Notes:** Replay creates candidate evidence only.

---

## Claim Classification Rule

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Evidence classification unit | Claim-by-claim classification | Each claim ID is governed by its own strict guard status. | Yes |
| Evidence classification unit | Whole-paper classification | A major passing claim can upgrade the whole paper. | No |
| Evidence classification unit | Central-claim-first classification | Only central claim determines claim-ready status. | No |
| Evidence classification unit | Agent decides | Agent chooses classification unit. | No |

**User's choice:** Claim-by-claim classification.
**Notes:** No unrelated claim upgrade by association.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| If C1 remains blocked but local claims pass | Conditional regime-specific manuscript | Allow local guard-authorized results without central superiority. | Yes |
| If C1 remains blocked but local claims pass | Diagnostic-only | Central claim failure downgrades all content to diagnostic. | No |
| If C1 remains blocked but local claims pass | Claim-ready empirical | Any passing positive claim makes the paper claim-ready. | No |
| If C1 remains blocked but local claims pass | Agent decides | Agent chooses manuscript path. | No |

**User's choice:** Conditional regime-specific manuscript.
**Notes:** No adaptive-menu central superiority language unless C1 passes.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Diagnostic/provisional material use | Diagnostic boundary or appendix only | Use Phase 8/9/no-filter/case scaffold as boundary evidence only. | Yes |
| Diagnostic/provisional material use | Main results with conservative language | Put diagnostics in main results with careful wording. | No |
| Diagnostic/provisional material use | Exclude from manuscript body | Do not use diagnostic/provisional material. | No |
| Diagnostic/provisional material use | Agent decides | Agent chooses diagnostic material placement. | No |

**User's choice:** Diagnostic boundary or appendix only.
**Notes:** Diagnostic material cannot support positive main claims.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| `manuscript_allowed=true` when overall `claim_ready=false` | Use local allowed content by claim ID | Use only with claim status, source, and allowed-use labeling. | Yes |
| `manuscript_allowed=true` when overall `claim_ready=false` | Do not use any allowed claims | Keep the whole manuscript diagnostic only. | No |
| `manuscript_allowed=true` when overall `claim_ready=false` | Treat allowed claims as main findings | Promote allowed content to main positive findings. | No |
| `manuscript_allowed=true` when overall `claim_ready=false` | Agent decides | Agent chooses allowed-use rule. | No |

**User's choice:** Use local allowed content by claim ID.
**Notes:** Allowed content is not the same as positive claim-ready evidence.

---

## Failure And Second-Attempt Rule

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Pre-replay gate failure | Direct diagnostic lock | If gates fail, do not run final replay; switch to Path B. | Yes |
| Pre-replay gate failure | Allow repair then recheck once | Permit another gate cleanup cycle. | No |
| Pre-replay gate failure | Continue replay as diagnostic | Run replay despite blocked gates, but label diagnostic. | No |
| Pre-replay gate failure | Agent decides | Agent chooses failure branch. | No |

**User's choice:** Direct diagnostic lock.
**Notes:** Blocked gates cannot be used to probe final results.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| First final replay technical failure | Allow one technical rerun | Same manifest, git SHA, checkpoint/hash, seeds, splits, policies, and settings. | Yes |
| First final replay technical failure | No second attempt | Any failure locks diagnostic path. | No |
| First final replay technical failure | Multiple attempts until complete | Keep rerunning until final completion. | No |
| First final replay technical failure | Agent decides | Agent chooses rerun rule. | No |

**User's choice:** Allow one technical rerun.
**Notes:** The rerun may address runtime failure or environment interruption only.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Second final replay failure | Immediate diagnostic lock | Stop v1 claim-ready path. | Yes |
| Second final replay failure | Reduce scale and rerun | Change runtime scale for completion. | No |
| Second final replay failure | Delete failed rows | Manually remove failed evidence rows. | No |
| Second final replay failure | Agent decides | Agent chooses second-failure branch. | No |

**User's choice:** Immediate diagnostic lock.
**Notes:** No scale reduction, row deletion, or continued reruns.

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Completed replay but guard remains false | Diagnostic or conditional path | Do not tune manifest after guard failure. | Yes |
| Completed replay but guard remains false | Recalibrate in new milestone | Future v2 could revisit, but v1 stops pursuing claim-ready path. | No |
| Completed replay but guard remains false | Continue tuning in this phase | Adjust settings and try again for claim readiness. | No |
| Completed replay but guard remains false | Agent decides | Agent chooses post-guard branch. | No |

**User's choice:** Diagnostic or conditional path.
**Notes:** Guard failure is an evidence result, not a technical failure.

## The Agent's Discretion

None. The user selected explicit options throughout.

## Deferred Ideas

None. Discussion stayed within Phase 3 scope.
