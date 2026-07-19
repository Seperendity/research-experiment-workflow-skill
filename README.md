<p align="right"><a href="./README.zh-CN.md">简体中文</a></p>

# Research Experiment Workflow Skill

An artifact-gated Codex skill for reproducible research, machine learning experiments, and evidence-grounded paper writing. It keeps claims traceable to locked protocols, saved results, review, and explicit decisions.

## Why This Skill

Coding agents can modify code and run experiments, but research can still fail through protocol drift, final-test leakage, missing baselines, lost state across sessions, or claims detached from saved results. This skill turns research state and evidence into durable, reviewable files instead of relying on chat history.

## Design Focus

- **Automatic rigor selection:** the skill infers `LITE`, `STANDARD`, `PAPER`, or `LEGACY_AUDIT` from the task, intended use, and existing artifacts.
- **The next valid artifact:** complete the current requested outcome instead of silently running an end-to-end pipeline.
- **Resumable state:** `experiment.json` records the current stage, status, checks, and artifact paths.
- **Deterministic validation:** a standard-library validator checks package structure and consistency; it does not judge scientific truth.
- **Evidence-grounded writing:** quantitative and comparative claims must trace to saved and reviewed evidence.

## Install

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## Use

Describe the task normally; you do not need to choose a profile:

```text
Use $research-experiment-workflow to compare two local training configs.
Run a small pilot and tell me which one to keep.
```

The skill infers the smallest profile that can support the requested outcome and records that choice in the experiment state.

Implicit invocation is disabled. Requests that do not name `$research-experiment-workflow` use normal Codex behavior, including experiment design, debugging, analysis, and writing.

The skill validates changed experiment artifacts automatically and reports blocking issues; users do not need to run the validator manually.

Common requests:

```text
Use $research-experiment-workflow to resume the experiment from experiment.json.

Use $research-experiment-workflow to review results/summary.json and produce the next decision.

Use $research-experiment-workflow to draft the Experiments section from reviewed evidence.
```

## Automatically Selected Profiles

These profiles are internal rigor levels; users do not need to select one before starting.

| Profile | Use | Required gates |
|---|---|---|
| `LITE` | Bounded engineering evidence or exploratory pilots | Protocol, pilot |
| `STANDARD` | Internal empirical conclusions and reproducibility | Feasibility, protocol, pilot, review |
| `PAPER` | Publication-facing novelty or scientific claims | Novelty, feasibility, protocol, pilot, review |
| `LEGACY_AUDIT` | Historical evidence without reconstructable workflow history | Record gaps; no retroactive gates |

The skill preserves an existing profile unless the claim expands, and never downgrades one to bypass missing or failed evidence.

A completed result-bearing `LITE` run uses four files: `experiment.json`, `EXPERIMENT.md`, `results/summary.json`, and `DECISION.md`. Do not precreate separate gate, run-note, or analysis files.

## Evidence Flow

```text
LITE:     protocol -> pilot -> run -> analysis -> decision
STANDARD: hypothesis -> feasibility -> protocol -> pilot -> run -> review -> analysis -> decision
PAPER:    hypothesis -> novelty -> feasibility -> protocol -> pilot -> run -> review -> analysis -> decision
```

Writing consumes reviewed evidence; it is not an experiment stage.

## Positioning

This repository is a compact evidence-control layer for existing research projects:

| Compared with | Focus here |
|---|---|
| End-to-end autonomous-scientist systems | Human-supervised progress that stops at the requested outcome or a blocked check |
| Autonomous optimization loops | General experiment state, baselines, uncertainty, invalidation, and claim boundaries rather than one fixed metric loop |
| Broad academic skill suites | A smaller contract focused on the experiment lifecycle, with progressive disclosure |
| Writing-only skills | Paper prose consumes saved experiment evidence instead of standing apart from it |

The skill does not replace experiment code, schedulers, literature databases, or scientific judgment. It adds a lightweight, auditable workflow to a project's existing tools and conventions.

## Repository

```text
research-experiment-workflow/
  SKILL.md
  agents/openai.yaml
  scripts/validate_experiment.py
  references/
tests/
```

- `SKILL.md` contains routing and the core contract.
- `references/artifact-contract.md` defines schemas and templates.
- `references/paper-writing.md` routes section-specific writing guidance.
- `tests/` contains validator tests, behavior-case contract checks, and fixtures.

## License and Attribution

This repository is licensed under the [MIT License](LICENSE).

The `paper-writing-*` references adapt MIT-licensed material from [`Master-cai/Research-Paper-Writing-Skills`](https://github.com/Master-cai/Research-Paper-Writing-Skills). That material remains subject to its upstream copyright and license notice; see [`paper-writing-attribution.md`](research-experiment-workflow/references/paper-writing-attribution.md).
