# Run Notes: exp-20260714-skill-ab-full

## Runner and snapshots

- Reused the frozen `pkg-amber` baseline and `pkg-cobalt` candidate snapshots recorded in the parent pilot.
- Local config: `gpt-5.5`, `xhigh` reasoning; collaboration runner version not separately exposed.
- New forward-test responses: 18.
- Sampling or infrastructure retries: 0.
- Missing or excluded outputs: 0.
- Held-out raw outputs: `results/heldout_raw_outputs.json`.
- Held-out blind scores: `results/heldout_blind_scores.json`.
- Parent pilot evidence: `../exp-20260714-skill-ab-pilot/results/`.

## Frozen mapping disclosed after scoring

| Case | Baseline output | Candidate output |
|---|---|---|
| `standard_resume_existing` | `resume-Q2` | `resume-Q1` |
| `material_protocol_change` | `metric-Q1` | `metric-Q2` |
| `analysis_missing_baseline` | `baseline-Q2` | `baseline-Q1` |
| `legacy_evidence_audit` | `legacy-Q1` | `legacy-Q2` |
| `paper_story_before_results` | `story-Q2` | `story-Q1` |
| `paper_draft_from_reviewed_evidence` | `draft-Q1` | `draft-Q2` |
| `generic_python_debug` | `pydebug-Q2` | `pydebug-Q1` |
| `casual_brainstorm` | `brain-Q1` | `brain-Q2` |
| `generic_document_summary` | `summary-Q2` | `summary-Q1` |

Three fresh scorers independently scored disjoint case groups. Each scorer saw answer keys and anonymized outputs, but not package identities, mappings, parent outcomes, or other scorer results.

## Execution decisions

- All nine held-out cases were retained.
- No Skill, wrapper, answer key, or rubric changed after execution began.
- The under-specified resume case and the output-unobservable reference-loading criterion were retained as locked, then reported as evaluation-design limitations.
