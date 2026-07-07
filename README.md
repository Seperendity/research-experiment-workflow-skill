<p align="right">
  <a href="./README.zh-CN.md">简体中文</a>
</p>

# Research Experiment Workflow Skill

An artifact-gated Codex skill for research, machine learning, and paper-oriented experiments.

This skill helps Codex act less like an eager code generator and more like a disciplined research operator: ideas are scored, hypotheses are made falsifiable, novelty risk is checked, pilots run before full experiments, reviews happen before claims, and writing is grounded in saved artifacts.

## What It Provides

- **A staged research workflow**: idea scoring, hypothesis, novelty check, feasibility, pilot, experiment run, review, analysis, and writing.
- **Durable experiment artifacts**: templates for `ideas.json`, `NOVELTY.md`, `FEASIBILITY.md`, `PILOT.md`, `run_notes.md`, `results/summary.json`, `REVIEW.md`, and `analysis.md`.
- **Paper-aware guardrails**: baseline checks, novelty risk, leakage checks, metric misuse, post-hoc selection, review rubric, and writing integrity checks.
- **Complete paper-writing guidance**: reviewer-facing guidance for Abstract, Introduction, Related Work, Method, Experiments, Conclusion, paragraph flow, figure/table presentation, claim-evidence maps, and adversarial self-review.
- **Cross-project reuse**: project-specific commands and metrics stay in each repo; the reusable skill keeps the process consistent.

## Installation

```bash
git clone https://github.com/Seperendity/research-experiment-workflow-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R research-experiment-workflow-skill/research-experiment-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Then invoke it from any Codex session:

```text
Use $research-experiment-workflow to turn this research idea into a hypothesis, novelty check, feasibility report, and pilot plan.
```

## Workflow

```text
idea scoring
  -> hypothesis
  -> novelty check
  -> feasibility
  -> pilot
  -> experiment run
  -> review
  -> analysis
  -> writing
```

Use the whole pipeline for new research directions. For ongoing projects, resume from the latest valid artifact instead of restarting.

## Repository Layout

```text
research-experiment-workflow/
  SKILL.md
  agents/
    openai.yaml
  references/
    artifact-contract.md
    roles.md
    paper-writing.md
    paper-writing-*.md
```

- `SKILL.md` defines the stage router, gates, role discipline, and operating principles.
- `references/artifact-contract.md` defines the artifact schema, compact templates, review rubric, and writing checks.
- `references/paper-writing.md` routes paper drafting, section revision, paragraph-flow checks, figure/table presentation, claim-evidence mapping, and paper self-review.
- `references/paper-writing-*.md` contains section-specific writing guides and flattened example banks adapted from `Master-cai/Research-Paper-Writing-Skills`.
- `agents/openai.yaml` provides Codex UI metadata and a default prompt.

## Example: Starting A New Experiment Project

Suppose you start a project called `personal-knowledge-os` and want to test:

> Does hybrid retrieval, BM25 plus embedding rerank, retrieve relevant personal notes better than pure embedding retrieval for personal knowledge-base QA?

Start with process, not code:

```text
Use $research-experiment-workflow to set up the experiment workflow for this new project.

Project goal: build a personal knowledge-base QA system.
Research idea: test whether hybrid retrieval (BM25 + embedding rerank) retrieves relevant notes better than pure embedding retrieval.
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

Then run a pilot before scaling:

```text
Use $research-experiment-workflow to design and execute the smallest pilot from the current FEASIBILITY.md.

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
- Save results/summary.json and run_notes.md
- Do not write paper conclusions yet. Move to review first.
```

Finally, keep review, analysis, and writing separate:

```text
Use $research-experiment-workflow as Reviewer to check whether this experiment is trustworthy.
Focus on baseline fairness, data leakage, metric validity, cherry-picking, and artifact completeness.
```

```text
Use $research-experiment-workflow to write analysis.md from results/summary.json and run_notes.md.
Only state supported and unsupported claims. Do not draft paper prose yet.
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

- **Baseline first**: do not claim improvement until a baseline is reproduced or explicitly replaced.
- **Pilot first**: do not scale a major change until a minimal pilot passes.
- **Novelty before paper claims**: check close prior work before presenting a contribution.
- **Evidence over memory**: save artifacts that later stages can inspect.
- **Writing after review**: paper prose should consume reviewed analysis, not raw logs.

## Inspiration

The skill borrows useful workflow ideas from artifact-driven research practice and AI-Scientist-style systems, including idea scoring, novelty checks, experiment budgets, run notes, review rubrics, and writing integrity checks. Its paper-writing references adapt the MIT-licensed `Master-cai/Research-Paper-Writing-Skills` skill, whose README credits Prof. Peng Sida's open study notes as the primary source of writing methodology. This skill is intentionally a human-controlled workflow gatekeeper, not a fully automated paper generator.

## License

This repository currently has no open-source license. Add a `LICENSE` file before accepting external contributions or granting reuse rights beyond normal public viewing.

The `research-experiment-workflow/references/paper-writing-*` files include adapted material from the MIT-licensed `Master-cai/Research-Paper-Writing-Skills` repository. See `references/paper-writing-attribution.md` for the copied MIT notice and source attribution.
