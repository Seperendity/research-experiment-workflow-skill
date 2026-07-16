<p align="right">
  <a href="./README.zh-CN.md">简体中文</a>
</p>

# Research Experiment Workflow Skill

An artifact-gated Codex skill for research, machine learning, and paper-oriented experiments.

This skill helps Codex act less like an eager code generator and more like a disciplined research operator: ideas are scored, hypotheses are made falsifiable, evaluation protocols are locked before result-bearing runs, and reviewed analysis ends in an explicit next decision.

## What It Provides

- **Proportional workflow profiles**: `LITE`, `STANDARD`, `PAPER`, and `LEGACY_AUDIT` match evidence burden to the intended claim instead of forcing every task through one pipeline.
- **Durable experiment artifacts**: a resumable version 3 `experiment.json` manifest plus protocol, run, review, analysis, debug, ablation, and decision templates.
- **Explicit gate semantics**: profile-specific prerequisites, justified `NOT_APPLICABLE` gates, and human-attributed warning acceptance replace ambiguous skip behavior.
- **Statistical and evaluation guardrails**: estimands, units of analysis, uncertainty, multiple comparisons, failed-run handling, protected evaluation boundaries, baseline checks, and invalidation rules are locked before final evaluation.
- **Complete paper-writing guidance**: reviewer-facing guidance for Abstract, Introduction, Related Work, Method, Experiments, Conclusion, paragraph flow, figure/table presentation, claim-evidence maps, and adversarial self-review.
- **Cross-project reuse**: project-specific commands and metrics stay in each repo; the reusable skill keeps the process consistent.

## Installation

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Then invoke it explicitly from any Codex session:

```text
Use $research-experiment-workflow to turn this idea into a hypothesis, novelty check, feasibility report, locked protocol, and pilot plan.
```

Implicit invocation is disabled because this workflow creates durable research state and evidence gates. A request to discuss, brainstorm, or design an experiment should use ordinary Codex behavior unless the user explicitly names the skill or asks to create, update, validate, analyze, or resume durable experiment artifacts. The same ordinary behavior applies to routine code debugging, unit tests, generic analysis, and writing that does not depend on experiment artifacts.

## Workflow Profiles

Choose the smallest profile that can support the intended claim. Upgrade before broadening a claim; never downgrade to bypass failed evidence.

| Profile | Typical use | Required gates |
|---|---|---|
| `LITE` | Bounded engineering checks and exploratory pilots | Protocol, pilot |
| `STANDARD` | Internal empirical conclusions and reproducibility work | Feasibility, protocol, pilot, review |
| `PAPER` | Publication-facing novelty, comparative, or scientific claims | Novelty, feasibility, protocol, pilot, review |
| `LEGACY_AUDIT` | Honest inspection of incomplete historical evidence | No retroactive gates; record gaps and provenance |

The resulting paths are:

```text
PAPER:         idea/hypothesis -> novelty -> feasibility -> protocol -> pilot -> run -> review -> analysis -> decision
STANDARD:      hypothesis -> feasibility -> protocol -> pilot -> run -> review -> analysis -> decision
LITE:          protocol -> pilot -> run -> analysis -> decision
LEGACY_AUDIT:  artifact inventory -> gap/provenance record -> analysis -> decision
```

Paper story and writing are not values of `experiment.json.stage`. A provisional story may be planned before experiments finish when planned evidence and open gaps are labeled; paper-ready quantitative, comparative, novelty, and causal claims consume reviewed evidence. For ongoing projects, resume from the latest valid artifact instead of restarting.

## Repository Layout

```text
research-experiment-workflow/
  SKILL.md
  agents/
    openai.yaml
  scripts/
    validate_experiment.py
  references/
    artifact-contract.md
    roles.md
    paper-writing.md
    paper-writing-*.md
```

- `SKILL.md` defines profile selection, the core evidence contract, reference routing, and stopping rules.
- `references/artifact-contract.md` defines the artifact schema, compact templates, review rubric, and writing checks.
- `scripts/validate_experiment.py` validates manifests, gates, and result summaries without modifying the experiment.
- `references/paper-writing.md` routes paper drafting, section revision, paragraph-flow checks, figure/table presentation, claim-evidence mapping, and paper self-review.
- `references/paper-writing-*.md` contains section-specific writing guides and flattened example banks adapted from `Master-cai/Research-Paper-Writing-Skills`.
- `agents/openai.yaml` provides Codex UI metadata and a default prompt.

New manifests use `experiment.json` schema version 3; `results/summary.json` remains schema version 2. Non-strict validation reads version 2 manifests and schema-less legacy summaries with compatibility warnings. Strict mode rejects warnings, while a complete, human-attributed version 3 warning acceptance is reported as a notice.

```bash
python research-experiment-workflow/scripts/validate_experiment.py path/to/experiment
python research-experiment-workflow/scripts/validate_experiment.py path/to/experiment --strict
```

## Example: Starting A New Experiment Project

Suppose you start a project called `personal-knowledge-os` and want to test:

> Does hybrid retrieval, BM25 plus embedding rerank, retrieve relevant personal notes better than pure embedding retrieval for personal knowledge-base QA?

Start with process, not code:

```text
Use $research-experiment-workflow to set up the experiment workflow for this new project.

Project goal: build a personal knowledge-base QA system.
Research idea: test whether hybrid retrieval (BM25 + embedding rerank) retrieves relevant notes better than pure embedding retrieval.
Workflow profile: PAPER, because the intended output includes a novelty claim and paper-facing prose.
Do not write code yet. Start with idea scoring, hypothesis, novelty check, and feasibility.
```

The first pass should create or propose artifacts like:

```text
research/
  ideas.json
  hypotheses/
    tracker.md
  experiments/
    exp-20260701-hybrid-retrieval/
      experiment.json
      README.md
      NOVELTY.md
      FEASIBILITY.md
```

Next, give the skill the project interface:

```text
Use $research-experiment-workflow to add a minimal project interface contract.

Available commands:
- Retrieval evaluation: python scripts/eval_retrieval.py
- Dataset: data/eval_queries.jsonl
- Output: outputs/retrieval_metrics.json
- Baseline: pure_embedding
- Metrics: recall@5, recall@10, MRR, latency_ms
```

Before execution, lock only the comparison rules that must not drift after results are observed:

```text
Use $research-experiment-workflow to lock the minimal protocol for this experiment.
Record the intended claim, estimand, unit of analysis, primary metric and direction, baseline,
protected evaluation and tuning boundaries, sample/repeat and seed rationale, uncertainty method,
failed-run and multiple-comparison handling, run budget, stopping/selection rule, allowed changes,
and success, failure, or inconclusive rule in PROTOCOL.md.
```

Then run a pilot before scaling:

```text
Use $research-experiment-workflow to design and execute the smallest pilot under the locked PROTOCOL.md.

Requirements:
- Use only 20 eval queries
- Compare only pure_embedding and hybrid_retrieval
- Save PILOT.md and run_notes.md
- Do not proceed to the full experiment until the pilot passes
```

If the pilot passes, move to the full experiment:

```text
Use $research-experiment-workflow. The pilot passed. Execute the full experiment.

Requirements:
- Use the complete eval_queries.jsonl
- Fix the seed
- Compare pure_embedding, hybrid_retrieval, and hybrid_with_rerank
- Save a version 2 results/summary.json and run_notes.md
- Do not write paper conclusions yet. Move to review first.
```

Finally, keep review, analysis, decision, and writing separate:

```text
Use $research-experiment-workflow as Reviewer to check whether this experiment is trustworthy.
Focus on baseline fairness, data leakage, metric validity, cherry-picking, and artifact completeness.
```

```text
Use $research-experiment-workflow to write analysis.md from results/summary.json and run_notes.md.
Only state supported and unsupported claims. Do not draft paper prose yet.
```

```text
Use $research-experiment-workflow to record DECISION.md from the reviewed analysis.
Choose exactly one action: REPLICATE, ABLATE, REVISE, SCALE, DEBUG, or STOP.
```

```text
Use $research-experiment-workflow to draft the experiment section for a paper or technical report from the reviewed analysis.md.
Every number must cite the experiment id, summary.json, or analysis.md.
```

For reviewer-facing paper prose, ask for the specific section and keep evidence constraints explicit:

```text
Use $research-experiment-workflow to draft the Abstract and Introduction from the reviewed analysis.md and NOVELTY.md.
Use the paper-writing guidance. Include a mini-outline, paragraph roles, claim-evidence map, and open evidence gaps.
Do not invent numbers, baselines, citations, figures, or conclusions.
```

## Design Principles

- **Proportionality first**: use the smallest profile that supports the intended claim, then upgrade before expanding the claim.
- **Statistics first**: lock the target quantity, unit, uncertainty, multiplicity, missing-data handling, and decision rule before final evaluation.
- **Baseline first**: do not claim improvement until a baseline is reproduced or explicitly replaced.
- **Protocol first**: lock evaluation boundaries and decision rules before result-bearing execution.
- **Pilot first**: do not scale a major change until a minimal pilot passes.
- **Novelty before paper claims**: check close prior work before presenting a contribution.
- **Evidence over memory**: save artifacts that later stages can inspect.
- **Decision after analysis**: record whether to replicate, ablate, revise, scale, debug, or stop.
- **Claims after review**: provisional story planning may precede experiments, but paper-ready quantitative, comparative, novelty, and causal claims must consume reviewed analysis.

## Inspiration

The skill borrows useful workflow ideas from artifact-driven research practice and AI-Scientist-style systems, including idea scoring, novelty checks, experiment budgets, run notes, review rubrics, and writing integrity checks. Its paper-writing references adapt the MIT-licensed `Master-cai/Research-Paper-Writing-Skills` skill, whose README credits Prof. Peng Sida's open study notes as the primary source of writing methodology. This skill is intentionally a human-controlled workflow gatekeeper, not a fully automated paper generator.

## License

This repository currently has no open-source license. Add a `LICENSE` file before accepting external contributions or granting reuse rights beyond normal public viewing.

The `research-experiment-workflow/references/paper-writing-*` files include adapted material from the MIT-licensed `Master-cai/Research-Paper-Writing-Skills` repository. See `references/paper-writing-attribution.md` for the copied MIT notice and source attribution.
