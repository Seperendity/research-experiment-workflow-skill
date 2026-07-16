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
Use $research-experiment-workflow to create and lock PROTOCOL.md for this comparison.
```

Implicit invocation is disabled. Ordinary experiment discussion, brainstorming, debugging, and generic analysis should use normal Codex behavior unless the user names the skill or requests durable experiment artifacts.

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

## Evidence Flow

```text
hypothesis -> protocol -> pilot -> run -> review -> analysis -> decision
```

`STANDARD` adds feasibility and review; `PAPER` also adds novelty. `LITE` omits gates that its claim scope does not require. Writing consumes reviewed evidence; it is not an experiment stage.

## Validate

New manifests use schema version 3. Result summaries use schema version 2.

```bash
python research-experiment-workflow/scripts/validate_experiment.py path/to/experiment --strict
python -m unittest discover -s tests -v
```

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
- `tests/` contains validator, behavior, trigger, and fixture tests.

## Attribution and License

The `paper-writing-*` references adapt MIT-licensed material from [`Master-cai/Research-Paper-Writing-Skills`](https://github.com/Master-cai/Research-Paper-Writing-Skills). See [`paper-writing-attribution.md`](research-experiment-workflow/references/paper-writing-attribution.md) for the notice.

This repository does not currently include a project-wide open-source license. Add a `LICENSE` file before granting reuse rights or accepting external contributions.
