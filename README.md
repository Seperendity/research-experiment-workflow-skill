<p align="right"><a href="./README.zh-CN.md">简体中文</a></p>

# Research Experiment Workflow Skill

An artifact-gated Codex skill for reproducible research, machine learning experiments, and evidence-grounded paper writing. It keeps claims traceable to locked protocols, saved results, review, and explicit decisions.

## Highlights

- Four rigor profiles: `LITE`, `STANDARD`, `PAPER`, and `LEGACY_AUDIT`.
- Protocol, baseline, evaluation-boundary, uncertainty, and failure-handling checks before result-bearing runs.
- Resumable `experiment.json` manifests and deterministic validation.
- Evidence-grounded analysis, decisions, and paper writing.
- Progressive disclosure: detailed schemas and writing guidance load only when needed.

## Install

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## Use

Invoke the skill explicitly:

```text
Use $research-experiment-workflow with the LITE profile for this bounded comparison.
```

Implicit invocation is disabled. Requests that do not name `$research-experiment-workflow` use normal Codex behavior, including experiment design, debugging, analysis, and writing.

The skill validates changed experiment artifacts automatically and reports blocking issues; users do not need to run the validator manually.

Common requests:

```text
Use $research-experiment-workflow to resume the experiment from experiment.json.

Use $research-experiment-workflow to review results/summary.json and produce the next decision.

Use $research-experiment-workflow to draft the Experiments section from reviewed evidence.
```

## Profiles

| Profile | Use | Required gates |
|---|---|---|
| `LITE` | Bounded engineering evidence or exploratory pilots | Protocol, pilot |
| `STANDARD` | Internal empirical conclusions and reproducibility | Feasibility, protocol, pilot, review |
| `PAPER` | Publication-facing novelty or scientific claims | Novelty, feasibility, protocol, pilot, review |
| `LEGACY_AUDIT` | Historical evidence without reconstructable workflow history | Record gaps; no retroactive gates |

Use the smallest profile that supports the intended claim. Never downgrade a profile to bypass missing or failed evidence.

A completed result-bearing `LITE` run uses four files: `experiment.json`, `EXPERIMENT.md`, `results/summary.json`, and `DECISION.md`. Do not precreate separate gate, run-note, or analysis files.

## Evidence Flow

```text
LITE:     protocol -> pilot -> run -> analysis -> decision
STANDARD: hypothesis -> feasibility -> protocol -> pilot -> run -> review -> analysis -> decision
PAPER:    hypothesis -> novelty -> feasibility -> protocol -> pilot -> run -> review -> analysis -> decision
```

Writing consumes reviewed evidence; it is not an experiment stage.

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

## Attribution and License

The `paper-writing-*` references adapt MIT-licensed material from [`Master-cai/Research-Paper-Writing-Skills`](https://github.com/Master-cai/Research-Paper-Writing-Skills). See [`paper-writing-attribution.md`](research-experiment-workflow/references/paper-writing-attribution.md) for the notice.

This repository does not currently include a project-wide open-source license. Add a `LICENSE` file before granting reuse rights or accepting external contributions.
