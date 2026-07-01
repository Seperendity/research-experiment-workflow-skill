---
name: research-experiment-workflow
description: Artifact-gated workflow for research, machine learning, and paper-oriented experiments. Use when Codex needs to turn an idea into a scored research direction, check novelty, assess feasibility, run a pilot, execute or debug an experiment, review evidence, analyze results, plan ablations, or draft paper text with claims traceable to saved artifacts.
---

# Research Experiment Workflow

## Overview

Use this skill to keep research work artifact-driven: each stage must leave a durable file that the next stage consumes. Prefer small, falsifiable experiments over broad implementation, and do not turn observations into paper claims until the evidence package has passed the relevant gates.

For exact artifact templates, summary schema, project interface contracts, and writing integrity checks, read `references/artifact-contract.md` when creating or validating experiment artifacts.

## First Actions

1. Load the repository's project instructions if present (`AGENTS.md`, `CLAUDE.md`, `README.md`, or equivalent), then inspect relevant playbooks, templates, experiment directories, and code.
2. Identify the current stage from the user request and existing artifacts. Resume from the latest valid artifact instead of restarting.
3. Choose the smallest stage that handles the request. Use the full pipeline only when the user asks for end-to-end research execution.
4. Enforce gates: advance only when the previous gate passes, or when the user explicitly accepts a recorded warning.
5. Keep domain-specific details in project files. The reusable workflow is the stage order, artifact contract, and evidence discipline.
6. If an agent will execute generated or modified code, check the project's sandbox, dependency, network, and budget limits before running it.

## Stage Router

| User intent | Stage |
|---|---|
| Raw idea list, brainstorming, ranking directions | Idea scoring |
| New intuition, mechanism, or research question | Hypothesis |
| Prior art, related work, whether the idea is already known | Novelty check |
| "Is this worth doing?", scope, data availability, compute risk | Feasibility |
| Small proof, smoke test, minimal run, config sanity check | Pilot |
| Full run, scaled run, saved metrics, result package | Experiment run |
| Failure, NaN, shape mismatch, broken pipeline, missing artifact | Debug |
| Independent check, code review, result validation, paper evidence audit | Review |
| Metric interpretation, statistics, tables, figures, comparison | Analysis |
| Paper section, abstract claim, story, related result paragraph | Writing |
| Claim roadmap, figure plan, paper narrative | Paper story |
| Controlled comparison, one-factor removal, table row suite | Ablation |

## Canonical Pipeline

Run the standard loop as:

`idea scoring -> hypothesis -> novelty check -> feasibility -> pilot -> experiment run -> review -> analysis -> writing`

Use `debug` whenever a pilot or run fails. Use `paper story` to organize claims before writing. Use `ablation` only after the reference model or primary condition is defined.

The first two stages are lightweight. Skip `idea scoring` when the user gives a concrete hypothesis. Skip `novelty check` only for engineering-only work, local reproduction, or when the user explicitly accepts the literature risk.

## Stage Rules

### Idea Scoring

Turn raw ideas into a small ranked backlog. Record each idea with name, title, proposed experiment, interestingness, feasibility, novelty, expected evidence, and major risks. Be conservative with ratings and avoid overfitting to a single dataset, benchmark, or convenient implementation path.

Gate: one or more ideas are recorded and the chosen idea has a clear reason for selection.

### Hypothesis

Record a falsifiable statement, rationale, test method, expected outcome, alternative interpretations, priority, status, date, and linked experiments. Check whether a similar hypothesis already exists before adding a new one.

Gate: the hypothesis is recorded and has a concrete test path.

### Novelty Check

Search or inspect project literature notes for close prior work, likely baselines, and claim collisions. Record whether the idea is `NOVEL`, `PARTIAL`, `KNOWN`, or `UNCLEAR`, with citations or explicit search limits.

Gate: proceed only if the contribution remains defensible, or if the user explicitly accepts a narrowed claim or reproduction-only framing.

### Feasibility

Assess data availability, dependencies, code path, baseline, compute cost, budget limits, project interface, and scientific validity. Output a verdict: `GO`, `CONDITIONAL-GO`, or `NO-GO`.

Gate: proceed only on `GO` or on `CONDITIONAL-GO` after conditions are resolved or explicitly accepted.

### Pilot

Run the shortest meaningful test that can validate build health, forward shapes, finite loss or metric health, artifact generation, and the specific change being tested.

Gate: mark `PASS` only if the model or pipeline builds, outputs valid shapes or schemas, has no NaN/Inf or empty artifacts, and passes the change-specific sanity check.

### Experiment Run

Run the smallest scale that answers the question. Save config snapshots, metrics, logs, figures or arrays, run notes, and `results/summary.json`. Record budget limits, timeout, retry count, seeds, and stopping conditions.

Gate: training or evaluation completed, artifacts exist, and summary includes baseline comparison or an explicit explanation for why no baseline applies.

### Debug

Reproduce the failure with the smallest meaningful case. Isolate data, model, training loop, config, infrastructure, or artifact-generation causes. Fix and rerun the smallest relevant check, then update the failed pilot or run artifact.

Gate: the failure is explained and either fixed or recorded as a blocker with next action. Stop after the recorded retry or budget limit unless the user extends it.

### Review

Review as an independent reviewer: prioritize correctness, regressions, unsupported claims, missing controls, artifact gaps, reproducibility issues, novelty risk, metric misuse, leakage, and post-hoc selection. Report `PASS`, `WARNING`, or `FAIL`, plus conference-style rubric scores when the work is paper-facing.

Gate: blocking issues are fixed before downstream analysis or writing; accepted warnings must be explicitly recorded.

### Analysis

Load saved metrics and compare against baselines or planned controls. Separate supported claims, unsupported claims, inconclusive results, warnings, and next steps. Avoid selecting only favorable runs unless the selection rule was defined before evaluation.

Gate: claims are tied to metrics, figures, statistics, artifacts, or citations.

### Writing

Draft only from confirmed evidence. Every quantitative or comparative claim must point to an experiment ID, analysis artifact, figure, table, or citation. Before writing final prose, check that referenced figures, tables, citations, numbers, and section placeholders are present and consistent.

Gate: no invented numbers, unsupported baselines, missing figures, missing citations, leftover placeholders, duplicate sections, or unreviewed conclusions.

### Paper Story

Define the one-sentence contribution, core claims, planned figures, required validations, and open evidence gaps. Link each proposed claim to a completed or planned artifact.

### Ablation

Define the reference condition first. Each row changes exactly one factor, shares the same evaluation protocol, and is handed to review and analysis before writing conclusions.

## Operating Principles

- Baseline-first: do not claim improvement until the baseline is reproduced, replaced with justification, or explicitly marked unavailable.
- Novelty-first for paper claims: do not present a contribution until close prior work has been checked or the uncertainty is disclosed.
- Pilot-first: do not scale a major change until a minimal pilot passes.
- Budget-first: define timeout, retry count, run count, and stopping conditions before expensive execution.
- Evidence-first: keep claims traceable to durable artifacts.
- Compatibility-first: preserve the existing baseline path unless the task explicitly changes it.
- Artifact-first: prefer updating saved experiment files over relying on chat memory.
- Smallest-test-first: use the cheapest run that can falsify the current question.
- Safety-first: execute generated or modified code only inside the project's accepted sandbox and dependency policy.

## Role Discipline

If the user explicitly requests multi-agent or delegated work, use these roles: Coordinator, Engineer, Reviewer, Analyst, Writer, and optional Theorist. Keep Engineer and Reviewer separate for non-trivial changes; keep Analyst and Writer separate by default when making paper claims.

If no delegation is requested, still apply the same role criteria internally: implement as Engineer, then review the diff and evidence as Reviewer before presenting conclusions.
