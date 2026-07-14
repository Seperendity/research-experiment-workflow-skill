---
name: research-experiment-workflow
description: Artifact-gated workflow for research, machine learning, and paper-oriented experiments with proportional LITE, STANDARD, PAPER, and LEGACY_AUDIT rigor profiles. Use when Codex needs to turn an idea into a scored research direction, check novelty, assess feasibility, lock a statistical experiment protocol, run or debug an experiment, review evidence, analyze results, decide the next research action, plan ablations, or draft reviewer-facing paper content with claims traceable to saved artifacts.
---

# Research Experiment Workflow

## Overview

Use this skill to keep research work artifact-driven: each completed stage must leave the smallest durable artifact needed by the next stage. Match rigor to claim risk with a workflow profile, prefer small falsifiable experiments over broad implementation, and do not turn observations into paper claims until the evidence package has passed the relevant gates.

For exact artifact templates, state and result schemas, project interface contracts, and writing integrity checks, read `references/artifact-contract.md` when creating or validating experiment artifacts. For paper drafting, revision, paragraph flow, figure/table presentation, and self-review, read `references/paper-writing.md` first, then load only the section-specific writing reference needed for the current target.

## First Actions

1. Load the repository's project instructions if present (`AGENTS.md`, `CLAUDE.md`, `README.md`, or equivalent), then inspect relevant playbooks, templates, experiment directories, and code.
2. Identify the current stage from the user request and existing artifacts. When `experiment.json` exists, resume from its latest valid stage, gate records, and artifact paths instead of restarting.
3. Select the smallest valid workflow profile: `LITE`, `STANDARD`, `PAPER`, or `LEGACY_AUDIT`. Base the choice on intended claim scope and evidence risk, not convenience. Never downgrade a profile to bypass a failed gate.
4. Choose the smallest stage that handles the request. Use an end-to-end pipeline only when the user asks for end-to-end research execution.
5. Enforce the selected profile's gates. Advance on `PASS`, or on `WARNING` only when an authorizing human explicitly records who accepted it, when, and why. Never infer acceptance from silence or from the agent's own judgment.
6. Use `NOT_APPLICABLE` only for a gate the selected profile does not require; set its artifact to `null` and record a concrete rationale. Do not use it to erase missing evidence.
7. For new or modified experiment manifests, use schema version 3 and run `scripts/validate_experiment.py <experiment-dir> --strict`. Read schema version 2 only in compatibility mode.
8. Keep domain-specific details in project files. Before executing generated or modified code, check the project's sandbox, dependency, network, data, and budget limits.

## Stage Router

| User intent | Stage |
|---|---|
| Raw idea list, brainstorming, ranking directions | Idea scoring |
| New intuition, mechanism, or research question | Hypothesis |
| Prior art, related work, whether the idea is already known | Novelty check |
| "Is this worth doing?", scope, data availability, compute risk | Feasibility |
| Evaluation rules, controls, data boundaries, budget, stopping or selection policy | Protocol lock |
| Small proof, smoke test, minimal run, config sanity check | Pilot |
| Full run, scaled run, saved metrics, result package | Experiment run |
| Failure, NaN, shape mismatch, broken pipeline, missing artifact | Debug |
| Independent check, code review, result validation, paper evidence audit, paper self-review | Review |
| Metric interpretation, statistics, tables, figures, comparison | Analysis |
| Replicate, ablate, revise, scale, debug, or stop after analysis | Decision |
| Paper section, abstract claim, paragraph flow, section rewrite, related result paragraph | Writing |
| Claim roadmap, figure plan, paper narrative, section outline | Paper story |
| Controlled comparison, one-factor removal, table row suite | Ablation |

## Workflow Profiles

Select one profile before creating or updating a version 3 manifest. The profile sets the minimum evidence gates; it does not prevent optional stronger checks.

| Profile | Use when | Required gates | Claim boundary |
|---|---|---|---|
| `LITE` | Bounded engineering checks, local comparisons, smoke tests, or exploratory pilots | Protocol, pilot | No novelty or paper-strength claim |
| `STANDARD` | Reusable empirical conclusions or internal research decisions without a novelty claim | Feasibility, protocol, pilot, review | Claims stay within the locked evaluation |
| `PAPER` | Publication-facing novelty, comparative, or scientific claims | Novelty, feasibility, protocol, pilot, review | Full claim-evidence chain required |
| `LEGACY_AUDIT` | Inspecting historical work whose original gates cannot be reconstructed | None; record known gaps | Describes available evidence only; never implies retrospective compliance |

Use `NOT_APPLICABLE` only for gates outside the selected profile's required set. A lower profile is not a waiver: if the intended claim grows, upgrade the profile and complete the newly required gates before reusing downstream conclusions.

## Canonical Pipeline

Use the sequence for the selected profile:

- `PAPER`: idea scoring -> hypothesis -> novelty check -> feasibility -> protocol lock -> pilot -> experiment run -> review -> analysis -> decision
- `STANDARD`: hypothesis -> feasibility -> protocol lock -> pilot -> experiment run -> review -> analysis -> decision
- `LITE`: protocol lock -> pilot -> experiment run -> analysis -> decision
- `LEGACY_AUDIT`: inventory available artifacts -> record gaps and provenance -> analysis -> decision

After `decision`, follow exactly one recorded branch: `REPLICATE`, `ABLATE`, `REVISE`, `SCALE`, `DEBUG`, or `STOP`. Route failures through `debug`; route revised hypotheses, boundaries, or protocols back through the affected gates. Use `ablation` only after the reference condition and shared protocol are locked.

`Paper story` and `writing` are downstream authoring activities, not values of `experiment.json.stage`. Use them only after reviewed analysis. Skip idea scoring when a concrete hypothesis already exists; mark novelty `NOT_APPLICABLE` only when the profile permits it and no novelty claim is intended.

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

### Protocol Lock

Record the intended claim, estimand or target quantity, unit of analysis, primary metric and direction, baseline or control, data splits and protected evaluation boundary, and the line between tuning and final evaluation in `PROTOCOL.md`. Lock the sample or repeat rationale, seeds, uncertainty method, effect-size reporting, missing or failed-run handling, exclusion rules, multiple-comparison policy, run budget, stopping rule, allowed change surface, and success, failure, or inconclusive decision rule. Label analyses as confirmatory or exploratory before observing final results. Scale the statistical detail to the profile, but never omit the decision rule or evaluation boundary.

Keep the protocol domain-neutral; place domain-specific checks in project files. Record exceptions as warnings rather than silently changing the protocol.

Gate: proceed only when the protocol is `LOCKED`, or when an explicit `WARNING` has complete human acceptance metadata. Any material change to the claim, data boundary, metric, analysis plan, or selection rule invalidates affected downstream artifacts until those stages are rerun.

### Pilot

Run the shortest meaningful test that can validate build health, forward shapes, finite loss or metric health, artifact generation, and the specific change being tested.

Gate: mark `PASS` only if the locked protocol is still applicable, the model or pipeline builds, outputs valid shapes or schemas, has no NaN/Inf or empty artifacts, and passes the change-specific sanity check.

### Experiment Run

Run the smallest scale that answers the question. Save config snapshots, metrics, logs, figures or arrays, run notes, and `results/summary.json`. Record budget limits, timeout, retry count, seeds, and stopping conditions.

Gate: training or evaluation completed under the locked protocol, artifacts exist, and the summary includes the planned baseline comparison or the protocol's recorded reason that no baseline applies.

### Debug

Reproduce the failure with the smallest meaningful case. Isolate data, model, training loop, config, infrastructure, or artifact-generation causes. Record the diagnosis, affected artifacts, retry budget, and next action in `DEBUG.md`. Fix and rerun the smallest relevant check, then update or invalidate the failed pilot or run artifact.

Gate: the failure is explained and either fixed or recorded as a blocker with next action. Stop after the recorded retry or budget limit unless the user extends it.

### Review

Review as an independent reviewer: prioritize correctness, protocol adherence, regressions, unsupported claims, missing controls, artifact gaps, reproducibility issues, novelty risk, metric misuse, leakage, and post-hoc selection. Review the protocol before expensive or paper-relevant runs and review the evidence package after execution. For paper-facing review, also read `references/paper-writing-review.md` and check contribution, writing clarity, experimental strength, evaluation completeness, and method design soundness. Report `PASS`, `WARNING`, or `FAIL`, plus conference-style rubric scores when the work is paper-facing.

Gate: blocking issues are fixed before downstream analysis or writing; accepted warnings must include complete human acceptance metadata.

### Analysis

Load saved metrics and compare against the locked baseline or controls using the predeclared unit of analysis and statistical plan. Report effect size and uncertainty, planned run counts versus completed runs, missing or excluded observations, and sensitivity checks required by the protocol. Separate confirmatory from exploratory findings and supported, unsupported, and inconclusive claims. Do not select favorable runs, metrics, subgroups, or stopping points unless the rule was locked before final evaluation.

Gate: every claim is tied to metrics, figures, statistics, artifacts, or citations, and any deviation from the protocol is labeled with its effect on validity.

### Decision

Use analysis that has completed any review required by the selected profile to record exactly one next action in `DECISION.md`: `REPLICATE`, `ABLATE`, `REVISE`, `SCALE`, `DEBUG`, or `STOP`. Cite the evidence, name the destination stage or experiment, and state whether existing downstream artifacts remain valid.

Gate: do not start another run or present the experiment as complete until the decision and its rationale are recorded.

### Writing

Read `references/paper-writing.md` first, then load only the target section guide: Abstract, Introduction, Related Work, Method, Experiments, Conclusion, paragraph flow, review, or examples as needed. Draft only from confirmed evidence. Every quantitative, comparative, novelty, or causal claim must point to an experiment ID, analysis artifact, figure, table, or citation. Return or save a compact outline, paragraph roles, self-review checklist, and claim-evidence map. Before writing final prose, check that referenced figures, tables, citations, numbers, and section placeholders are present and consistent.

Gate: no invented numbers, unsupported baselines, missing figures, missing citations, unresolved `needs evidence` claims, leftover placeholders, duplicate sections, or unreviewed conclusions.

### Paper Story

Read `references/paper-writing.md` when the story is paper-facing. Define the one-sentence contribution, core claims, planned figures, required validations, section outline, and open evidence gaps. Link each proposed claim to a completed or planned artifact, citation, or explicit future validation. Treat missing evidence as a story gap, not as prose to smooth over.

### Ablation

Define the reference condition and rows in `ABLATION_PLAN.md` before execution. Each row changes exactly one factor unless an interaction study is explicitly declared, shares the locked evaluation protocol, and is handed to review and analysis before conclusions.

## Operating Principles

- Proportionality-first: use the smallest profile that supports the intended claim, and upgrade before expanding that claim.
- Statistics-first: define the target quantity, unit, uncertainty, multiplicity, missing-data handling, and decision rule before final evaluation.
- Baseline-first: do not claim improvement until the baseline is reproduced, replaced with justification, or explicitly marked unavailable.
- Protocol-first: lock evaluation boundaries and decision rules before running a result-bearing experiment.
- Novelty-first for paper claims: do not present a contribution until close prior work has been checked or the uncertainty is disclosed.
- Pilot-first: do not scale a major change until a minimal pilot passes.
- Budget-first: define timeout, retry count, run count, and stopping conditions before expensive execution.
- Evidence-first: keep claims traceable to durable artifacts.
- Compatibility-first: preserve the existing baseline path unless the task explicitly changes it.
- Artifact-first: prefer updating saved experiment files over relying on chat memory.
- Smallest-test-first: use the cheapest run that can falsify the current question.
- Test-boundary-first: do not change protected evaluation data or rules in response to observed results without invalidating affected evidence.
- Safety-first: execute generated or modified code only inside the project's accepted sandbox and dependency policy.

## Role Discipline

If the user explicitly requests multi-agent, delegated, or role-scoped work, use these roles: Coordinator, Engineer, Reviewer, Analyst, Writer, and optional Theorist. Read `references/roles.md` before assigning or executing role-specific work.

Keep Engineer and Reviewer separate for non-trivial changes; keep Analyst and Writer separate by default when making paper claims. A same-context self-review is a pre-check, not independent sign-off. When no fresh reviewer is available, record that limitation as a warning instead of claiming independent review.
