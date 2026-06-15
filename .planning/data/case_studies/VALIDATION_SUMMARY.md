# Phase 7 Case Contract Validation Summary

status: scaffolding_only_blocked_execution
case_execution_allowed: false
result_artifacts_allowed: false
manuscript_claim_upgrade_allowed: false

Labels: semi-real geography/network, simulated demand, simulated choice.

Validation scope: planning-side metadata contracts only. No external data, road graphs, matrices, demand rows, replay outputs, or runtime manifests were inspected or created.

## blocking

None.

## warning

None.

## info

- code: `source_contract_scope`
  message: Source contracts checked at metadata level only; no real source availability was inspected.
  evidence_location: `.planning\data\case_studies\source_contracts.yaml`
  minimal_fix: No action needed.
  rerun_command: `python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary`

- code: `runtime_manifest_absent`
  message: No work2_coding/Experiments/studies/case_* runtime manifest was found.
  evidence_location: `C:\Users\39583\Desktop\4_Publication\2.paper_2_menu optimization-7分_trE\work2_coding\Experiments\studies`
  minimal_fix: No action needed.
  rerun_command: `python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary`

## Machine-Readable Findings

```json
[
  {
    "code": "source_contract_scope",
    "evidence_location": ".planning\\data\\case_studies\\source_contracts.yaml",
    "message": "Source contracts checked at metadata level only; no real source availability was inspected.",
    "minimal_fix": "No action needed.",
    "rerun_command": "python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary",
    "severity": "info"
  },
  {
    "code": "runtime_manifest_absent",
    "evidence_location": "C:\\Users\\39583\\Desktop\\4_Publication\\2.paper_2_menu optimization-7\u5206_trE\\work2_coding\\Experiments\\studies",
    "message": "No work2_coding/Experiments/studies/case_* runtime manifest was found.",
    "minimal_fix": "No action needed.",
    "rerun_command": "python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary",
    "severity": "info"
  }
]
```
