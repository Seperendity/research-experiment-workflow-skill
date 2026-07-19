---
name: research-experiment-workflow
description: Artifact-gated workflow for creating, resuming, validating, reviewing, and writing from durable research experiment artifacts. Use only when the user explicitly invokes `$research-experiment-workflow`; never invoke it implicitly.
---

# Research Experiment Workflow

## Goal

Produce the smallest durable research artifact that moves the requested work to its next valid state. Preserve an auditable chain from intended claim and locked protocol to runs, review, analysis, and decision. Let the model choose the efficient path within the contract below.

## Start

1. Inspect only the project files and experiment artifacts needed for the request.
2. If `experiment.json` exists, resume from its latest valid stage, gates, and artifact paths; do not restart completed work.
3. Infer the smallest profile that supports the intended claim; do not require the user to name one. Preserve an existing manifest profile unless the claim expands, and never downgrade to bypass missing or failed evidence.
4. Identify the current requested outcome, not an automatic end-to-end pipeline.
5. Load only the references routed below.
6. After changing a manifest, gate, or result package, run the validator before presenting the stage as complete.

## Profiles

| Profile | Use when | Required gates | Claim boundary |
|---|---|---|---|
| `LITE` | Bounded engineering evidence, local comparisons, or exploratory pilots | Protocol, pilot | No novelty or paper-strength claim |
| `STANDARD` | Reusable empirical conclusions or internal research decisions | Feasibility, protocol, pilot, review | Claims stay within the locked evaluation |
| `PAPER` | Publication-facing novelty, comparative, causal, or scientific claims | Novelty, feasibility, protocol, pilot, review | Full claim-evidence chain required |
| `LEGACY_AUDIT` | Compatibility review of historical work whose gates cannot be reconstructed | None; record gaps | Describes available evidence only; never implies retrospective compliance |

Infer the profile from the requested use of the results and the available artifacts. Default new empirical work to `STANDARD`; use `LITE` only for bounded non-paper work, `PAPER` for publication-facing claims, and `LEGACY_AUDIT` only for historical evidence whose workflow cannot be reconstructed. Briefly report the selected profile and reason, then proceed without asking the user to choose among profiles. Upgrade before expanding claim scope.

For a completed result-bearing `LITE` run, keep only `experiment.json`, one `EXPERIMENT.md` containing protocol, pilot, run notes, and analysis, `results/summary.json`, and `DECISION.md`. Split those sections into separate files only when the user asks or project risk requires it.

## Task Router

| Requested outcome | Primary artifact or action |
|---|---|
| Rank research directions | `research/ideas.json` |
| State or revise a falsifiable claim | hypothesis tracker entry |
| Check prior work or claim collision | `NOVELTY.md` |
| Assess data, code, compute, or validity risk | `FEASIBILITY.md` |
| Lock evaluation and statistical decisions | `PROTOCOL.md` |
| Validate the smallest meaningful execution path | `PILOT.md` |
| Run a result-bearing comparison | config snapshot, run notes, `results/summary.json` |
| Diagnose a failed research run | `DEBUG.md` and affected-artifact status |
| Audit evidence or protocol adherence | `REVIEW.md` |
| Interpret saved results | `analysis.md` |
| Select the immediate next research action | `DECISION.md` |
| Define a controlled comparison suite | `ABLATION_PLAN.md` |
| Plan a paper narrative or evidence roadmap | provisional story and claim-evidence gaps |
| Draft or revise paper prose | evidence-grounded section artifact |

Paper story and writing are consumers of experiment evidence, not values of `experiment.json.stage`. A provisional story may be planned before experiments finish when planned evidence and open gaps are labeled. Quantitative, comparative, novelty, and causal conclusions require the review demanded by the selected profile.

For `LITE`, route protocol, pilot, run-note, and analysis work to the matching sections of `EXPERIMENT.md`; the dedicated filenames above are the `STANDARD` and `PAPER` defaults.

## Core Contract

- Advance a required gate only on `PASS`, or on `WARNING` with complete acceptance metadata from an authorizing human. An agent must not infer or fabricate acceptance.
- Use `NOT_APPLICABLE` only when the selected profile does not require the gate; record why and never use it to erase missing evidence.
- Lock the intended claim, target quantity, unit of analysis, baseline or control, protected evaluation boundary, tuning/final-test separation, uncertainty method, failure handling, budget, and decision rule before result-bearing evaluation.
- Do not use protected final-test observations to tune the method or selection rule. A material change to the claim, data boundary, metric, analysis plan, or selection rule invalidates affected downstream evidence.
- Do not claim improvement without a reproduced baseline, a justified replacement, or an explicit statement that no baseline applies.
- Tie every supported claim to saved metrics, statistics, figures, experiment artifacts, or citations. Label missing evidence, protocol deviations, exploratory analyses, and inconclusive results.
- Run the smallest test that can answer the current question. Do not continue into a more expensive stage after the requested outcome is complete or while a required gate is blocked.
- Record one immediate action in `DECISION.md`: `REPLICATE`, `ABLATE`, `REVISE`, `SCALE`, `DEBUG`, or `STOP`. Additional ideas may remain as a backlog.

## Reference Router

- Read `references/artifact-contract.md` when creating or validating manifests, gates, protocols, result summaries, experiment artifacts, analysis, or decisions. Use its exact schemas and compact templates.
- For paper story, drafting, revision, paragraph flow, figure/table presentation, or paper self-review, read `references/paper-writing.md`, then only the relevant section-specific reference. Preserve planned-versus-observed evidence labels.
- If the user explicitly requests multi-agent, delegated, or role-scoped work, read `references/roles.md`. A same-context self-review is not independent sign-off.

## Finish

- Use schema version 3 for new or modified `experiment.json` files; read version 2 only in compatibility mode. `results/summary.json` remains version 2.
- Run `scripts/validate_experiment.py <experiment-dir> --strict` for current manifests. Use non-strict validation only when auditing legacy artifacts.
- Report completed artifacts, remaining evidence gaps, accepted warnings, invalidated evidence, and the next recorded action.
- If required evidence is unavailable, narrow the claim or stop at the blocked gate instead of filling the gap with assumptions.
