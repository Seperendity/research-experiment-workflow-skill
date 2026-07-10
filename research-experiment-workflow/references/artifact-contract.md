# Research Experiment Artifact Contract

Use this reference when creating, checking, or adapting a research experiment workflow. Keep project-specific names, paths, metrics, commands, and safety policy in the repository; keep the gate structure stable.

## Contents

- [Suggested Project Layout](#suggested-project-layout)
- [Project Interface Contract](#project-interface-contract)
- [Stage Gates](#stage-gates)
- [Experiment Directory Contract](#experiment-directory-contract)
- [Experiment State](#experiment-state)
- [`results/summary.json` Version 2](#resultssummaryjson-version-2)
- [Compact Templates](#compact-templates)
- [Writing Integrity Checklist](#writing-integrity-checklist)
- [Common Failure Modes to Check](#common-failure-modes-to-check)
- [Cross-Project Adaptation Checklist](#cross-project-adaptation-checklist)

## Suggested Project Layout

Use existing project conventions if they exist. If a project has no research structure, propose this minimal layout before creating many files:

```text
research/
  ideas.json
  hypotheses/
    tracker.md
  experiments/
    exp-YYYYMMDD-short-name/
      experiment.json
      README.md
      FEASIBILITY.md
      NOVELTY.md
      PROTOCOL.md
      PILOT.md
      REVIEW.md
      analysis.md
      DECISION.md
      run_notes.md
      DEBUG.md
      ABLATION_PLAN.md
      config/
      results/
        summary.json
  analysis/
  literature/
  papers/
    drafts/
    story.md
  playbooks/
  templates/
```

## Project Interface Contract

Each project should define these in `AGENTS.md`, a local playbook, or the experiment README:

- Main experiment command or entrypoint.
- Baseline command, expected baseline artifacts, and whether baseline must be rerun on the current machine.
- Plot, analysis, or report-generation command.
- Expected result schema, metric names, and artifact paths.
- Seed policy, hardware assumptions, timeout, run budget, and retry budget.
- Protected data, evaluation boundaries, stopping rules, and allowed change surface.
- Sandbox, dependency, and network policy for generated or modified code.
- Paper or report template, citation style, and figure/table conventions if writing is expected.

## Stage Gates

| Stage | Primary artifact | Gate |
|---|---|---|
| Idea scoring | `research/ideas.json` | Candidate idea is scored and selected |
| Hypothesis | `research/hypotheses/tracker.md` entry | Falsifiable hypothesis recorded |
| Novelty check | `NOVELTY.md` or literature note | Contribution is defensible or risk is accepted |
| Feasibility | `FEASIBILITY.md` | Verdict is `GO` or resolved/accepted `CONDITIONAL-GO` |
| Protocol lock | `PROTOCOL.md` | Status is `LOCKED` or an explicit warning is accepted |
| Pilot | `PILOT.md` | Status is `PASS` |
| Experiment run | Config snapshot, `run_notes.md`, and `results/summary.json` | Run completed and artifacts saved |
| Debug | `DEBUG.md` | Failure is fixed, invalidated, or recorded as blocked |
| Ablation | `ABLATION_PLAN.md` | Reference condition and controlled rows are defined |
| Review | `REVIEW.md` | Status is `PASS` or accepted `WARNING` |
| Analysis | `analysis.md` | Supported and unsupported claims are explicit |
| Decision | `DECISION.md` | Exactly one next action is selected and linked |
| Writing | Draft under `research/papers/drafts/` | Claims cite artifacts or literature |

## Experiment Directory Contract

Each new experiment should use `experiment.json` as its control-plane record. Each completed or paper-relevant experiment should contain:

- `experiment.json`
- `README.md`
- `FEASIBILITY.md`
- `NOVELTY.md` or a linked literature note when paper claims depend on novelty
- `PROTOCOL.md`
- `PILOT.md`
- `REVIEW.md`
- Config snapshot or command snapshot
- `run_notes.md`
- `results/summary.json`
- `analysis.md`
- `DECISION.md`

Add `DEBUG.md` after a failed or interrupted run. Add `ABLATION_PLAN.md` before an ablation suite. Existing experiments without `experiment.json` remain readable legacy experiments; validators should warn rather than fail unless strict mode is requested.

## Experiment State

Use this minimum `experiment.json` structure:

```json
{
  "schema_version": 2,
  "experiment_id": "exp-YYYYMMDD-short-name",
  "hypothesis_id": "H-XXX",
  "stage": "IDEA | HYPOTHESIS | NOVELTY | FEASIBILITY | PROTOCOL | PILOT | EXPERIMENT | DEBUG | ABLATION | REVIEW | ANALYSIS | DECISION",
  "status": "PLANNED | RUNNING | INTERRUPTED | BLOCKED | DONE | FAILED | PARTIAL | INVALIDATED",
  "parent_experiment_id": null,
  "gates": {
    "novelty": {"verdict": "PASS | WARNING | FAIL | PENDING", "artifact": "NOVELTY.md", "accepted_warning": false},
    "feasibility": {"verdict": "PASS | WARNING | FAIL | PENDING", "artifact": "FEASIBILITY.md", "accepted_warning": false},
    "protocol": {"verdict": "PASS | WARNING | FAIL | PENDING", "artifact": "PROTOCOL.md", "accepted_warning": false},
    "pilot": {"verdict": "PASS | WARNING | FAIL | PENDING", "artifact": "PILOT.md", "accepted_warning": false},
    "review": {"verdict": "PASS | WARNING | FAIL | PENDING", "artifact": "REVIEW.md", "accepted_warning": false}
  },
  "artifacts": {
    "summary": "results/summary.json",
    "analysis": "analysis.md",
    "decision": "DECISION.md",
    "debug": "DEBUG.md",
    "ablation": "ABLATION_PLAN.md"
  },
  "warnings": []
}
```

Keep every artifact path relative to the experiment directory. Treat an artifact as valid only when it exists, parses when structured, is referenced by the manifest, and has no failed or unaccepted upstream gate. When a material protocol or implementation change makes downstream evidence stale, set the experiment to `INVALIDATED` or reset the affected gates to `PENDING` before continuing.

## `results/summary.json` Version 2

Use the following minimum structure for new experiments:

```json
{
  "schema_version": 2,
  "experiment_id": "exp-YYYYMMDD-short-name",
  "hypothesis_id": "H-XXX",
  "status": "DONE | FAILED | PARTIAL",
  "protocol": "PROTOCOL.md",
  "primary_metric": {"name": "metric_name", "direction": "minimize | maximize"},
  "config_base": "base config, command, or protocol name",
  "config_overrides": {},
  "runs": [
    {
      "run_id": "run_0",
      "seed": 0,
      "status": "DONE | FAILED | PARTIAL",
      "config": {},
      "metrics": {},
      "artifacts": {},
      "warnings": []
    }
  ],
  "aggregate": {
    "n_planned": 1,
    "n_completed": 1,
    "metrics": {}
  },
  "baseline": {
    "experiment_id": null,
    "source": "artifact, command, citation, or not-applicable reason",
    "metrics": {}
  },
  "delta_vs_baseline": {},
  "provenance": {
    "git_commit": null,
    "data_version": null,
    "environment": null
  },
  "artifacts": {},
  "budget": {
    "max_runs": null,
    "timeout": null,
    "retries_used": 0,
    "stop_reason": null
  },
  "warnings": []
}
```

Use `runs` for repeated executions, folds, groups, or other project-defined units; keep their domain-specific fields inside each run or its artifacts. Keep aggregation methods project-defined and record them in the protocol. Use `null` only when a field is not applicable or unavailable and explain the reason in `warnings`.

Legacy summaries without `schema_version` remain valid in compatibility mode when they contain the previous top-level `seed` and `metrics` fields. Treat them as warnings so existing projects can migrate incrementally. In strict mode, require version 2.

## Compact Templates

### Ideas

```json
[
  {
    "Name": "short_descriptor",
    "Title": "Readable research title",
    "Experiment": "Implementation and evaluation outline",
    "Interestingness": 1,
    "Feasibility": 1,
    "Novelty": 1,
    "ExpectedEvidence": "metric, figure, or artifact that would support the idea",
    "Risks": ["main reason this may fail"],
    "Status": "CANDIDATE | SELECTED | REJECTED | DEFERRED"
  }
]
```

### Hypothesis

```markdown
# H-XXX: <title>

- **Statement**: <falsifiable claim>
- **Rationale**: <why this should work, with citations if available>
- **Test method**: <what changes and what metrics decide the outcome>
- **Expected outcome**: <quantitative prediction if possible>
- **Alternative interpretations**: <other explanations for the same result>
- **Priority**: HIGH | MEDIUM | LOW
- **Status**: PROPOSED | ACTIVE | DONE | REJECTED
- **Date proposed**: YYYY-MM-DD
- **Linked experiments**: <experiment IDs or TODO>
```

### Experiment README

```markdown
# exp-YYYYMMDD-<name>

- **Hypothesis**: H-XXX
- **Change**: <what differs from baseline>
- **Config base**: <base config or protocol>
- **Config overrides**: <key overrides>
- **Baseline**: <baseline artifact or command>
- **Budget**: <max runs, timeout, retry limit>
- **Status**: PLANNED | RUNNING | INTERRUPTED | BLOCKED | DONE | FAILED | PARTIAL | INVALIDATED
- **Owner**: <role or agent>
```

### Novelty

```markdown
# Novelty Check: <experiment-id or hypothesis-id>

- **Verdict**: NOVEL | PARTIAL | KNOWN | UNCLEAR
- **Search scope**: <queries, papers, local notes, databases, date>
- **Closest prior work**: <citations or none found>
- **Difference from prior work**: <specific technical or empirical distinction>
- **Claim adjustment**: <narrowed claim or none>
- **Risks**: <missed literature, weak distinction, reproduction-only framing>
```

### Feasibility

```markdown
# Feasibility Report: <experiment-id>

- **Hypothesis**: <H-XXX>
- **Decision**: GO | CONDITIONAL-GO | NO-GO
- **Estimated scope**: CONFIG-ONLY | SMALL-CODE | MAJOR-CODE
- **Pilot time**: <estimate>
- **Full run time**: <estimate>
- **Budget**: <max runs, timeout, retries>
- **Rationale**: <1-2 sentences>

## Technical Check

- [ ] Data available
- [ ] Features or inputs available
- [ ] Dependencies available
- [ ] Code path understood
- [ ] Baseline or control identified
- [ ] Result schema and artifact paths defined
- [ ] Data and evaluation boundaries can be stated before execution
- [ ] Sandbox and network policy acceptable

## Risks

| Risk | Level | Mitigation |
|---|---|---|
| Data availability | LOW/MED/HIGH | |
| Code complexity | LOW/MED/HIGH | |
| Compute cost | LOW/MED/HIGH | |
| Scientific validity | LOW/MED/HIGH | |
| Novelty or prior-art risk | LOW/MED/HIGH | |
| Safety or dependency risk | LOW/MED/HIGH | |
```

### Protocol

```markdown
# Protocol: <experiment-id>

- **Status**: DRAFT | LOCKED | INVALIDATED
- **Research question**: <question being tested>
- **Primary metric and direction**: <metric; minimize or maximize>
- **Baseline or control**: <artifact, command, citation, or not-applicable reason>
- **Data and evaluation boundaries**: <protected splits, inputs, evaluation rules>
- **Run plan and budget**: <runs, repeats, timeout, retry limit>
- **Stopping and selection rule**: <predefined rule>
- **Allowed change surface**: <what may change; what must remain fixed>
- **Success or failure rule**: <evidence threshold or decision rule>
- **Warnings or accepted exceptions**: <none or recorded rationale>
```

Keep this artifact concise. Add domain-specific audit items only in the downstream project's playbook or experiment files.

### Pilot

```markdown
# Pilot Report: <experiment-id>

- **Status**: PASS | FAIL
- **Config**: <path or summary>
- **Build**: PASS | FAIL
- **Shape or interface check**: PASS | FAIL
- **Metric or loss health**: <initial -> final, or sanity metric>
- **Artifact check**: PASS | FAIL
- **Warnings**: <none or list>

## Checks

- [ ] Pipeline builds
- [ ] Forward pass or main execution path succeeds
- [ ] Shapes, schemas, or interfaces are correct
- [ ] No NaN, Inf, empty output, or silent artifact failure
- [ ] Expected artifacts are created
- [ ] Locked protocol still applies
- [ ] Change-specific sanity check passed
```

### Run Notes

```markdown
# Run Notes: <experiment-id>

## Runs

| Run | Seed | Command/config | Status | Key metric | Notes |
|---|---:|---|---|---:|---|
| run_0 | 0 | <baseline command> | DONE | | baseline |

## Figures and Tables

| Artifact | Source data | What it shows | Used in claim |
|---|---|---|---|
| | | | |

## Decisions

- <why a run was kept, discarded, retried, or stopped>
```

### Debug

```markdown
# Debug Report: <experiment-id>

- **Status**: FIXED | BLOCKED | INVALIDATED
- **Failure class**: DATA | MODEL | TRAINING | EVALUATION | INFRASTRUCTURE | ARTIFACT
- **Smallest reproduction**: <command or case>
- **Root cause**: <evidence-backed explanation>
- **Affected artifacts**: <paths or none>
- **Retries used / limit**: <count / limit>
- **Next action**: <rerun stage, invalidate, or block>
```

### Ablation Plan

```markdown
# Ablation Plan: <experiment-id>

- **Reference condition**: <artifact or config>
- **Shared protocol**: PROTOCOL.md
- **Primary metric**: <metric>
- **Budget**: <runs, timeout, retries>

| Row | Single changed factor | Fixed factors | Expected evidence |
|---|---|---|---|
| A0 | reference | all | baseline |
| A1 | <factor> | all others | <metric or artifact> |

Declare an interaction study explicitly when a row changes more than one factor.
```

### Decision

```markdown
# Decision: <experiment-id>

- **Action**: REPLICATE | ABLATE | REVISE | SCALE | DEBUG | STOP
- **Evidence**: <reviewed analysis and artifact references>
- **Rationale**: <why this action follows>
- **Destination**: <stage or child experiment ID; none for STOP>
- **Artifact validity**: <which existing artifacts remain valid or are invalidated>
- **Owner**: <role, agent, or person>
```

### Review

```markdown
# Review Report: <target>

- **Status**: PASS | WARNING | FAIL
- **Scope**: protocol | code | experiment | analysis | paper draft
- **Reviewer**: <role or agent>

## Findings

1. <severity and issue>

## Paper-Facing Rubric

| Dimension | Score | Notes |
|---|---:|---|
| Originality | 1-10 | |
| Soundness | 1-10 | |
| Significance | 1-10 | |
| Clarity | 1-10 | |
| Reproducibility | 1-10 | |
| Confidence | 1-10 | |

## Required Follow-Ups

1. <blocking fix or none>
```

### Analysis

```markdown
# Analysis Report: <experiment-id>

- **Question**: <what this analysis answers>
- **Baseline comparison**: <ours vs baseline>
- **Selection rule**: <predefined rule for which runs are compared>
- **Supported claims**: <list>
- **Unsupported or inconclusive claims**: <list>
- **Warnings**: <list or none>

## Quantitative Summary

| Metric | Baseline | Ours | Delta |
|---|---|---|---|
| | | | |

## Decision Input

- Recommended action: REPLICATE | ABLATE | REVISE | SCALE | DEBUG | STOP
- Evidence for recommendation: <artifact references>
```

### Paper Section

```markdown
# <section title>

## Target Section Guide

- Writing reference: references/paper-writing.md
- Section-specific reference: <paper-writing-abstract.md | paper-writing-introduction.md | paper-writing-related-work.md | paper-writing-method.md | paper-writing-experiments.md | paper-writing-conclusion.md | paper-writing-flow.md>

## Mini Outline

1. <3-7 bullets covering the section logic before prose>

## Paragraph Roles

| Paragraph | Role | One-message sentence | Evidence |
|---|---|---|---|
| P1 | opening/challenge/method/advantage/evidence/limitation | | |

## Main Point

<one-sentence takeaway>

## Evidence

- Experiment IDs: <list>
- Analysis artifacts: <list>
- Figures or tables: <list>
- Citations: <list>

## Claim-Evidence Map

| Claim | Evidence | Status |
|---|---|---|
| <major claim> | <artifact, figure, table, or citation> | supported/needs evidence |

## Draft

<write the prose here>

## Self-Review Checklist

- [ ] Each paragraph has one explicit message.
- [ ] The first sentence states the paragraph role or message.
- [ ] Terminology is stable and key nouns are self-contained.
- [ ] Major Abstract/Introduction claims are mapped to evidence.
- [ ] Figure and table captions support the intended claim.

## Open Evidence Gaps

- <gap or none>
```

## Writing Integrity Checklist

Before presenting paper text as final or paper-ready, verify:

- Every number appears in `results/summary.json`, `analysis.md`, a table, or a cited artifact.
- Every figure and table reference points to an existing file or generated output.
- Every citation key or reference is present in the bibliography or literature note.
- Every major Abstract or Introduction claim appears in the claim-evidence map.
- Every paragraph has one explicit message and a topic sentence that maps to the section outline.
- Terminology is stable; key nouns are self-contained before reuse.
- Figure and table captions explain the setting, notation, and main message without hiding protocol gaps.
- Tables use readable, minimal-ink formatting with metric direction and consistent precision when applicable.
- No placeholders remain, including `TODO`, `TBD`, `XX`, `Conclusions Here`, or dummy citations.
- Sections are not duplicated and headings match the target outline.
- Negative, failed, or discarded runs are disclosed when they affect interpretation.
- The use of AI assistance is disclosed when required by venue, policy, or project rules.

## Common Failure Modes to Check

- Novelty misclassified because the search was too shallow.
- Code change is too small or unrelated to the claimed mechanism.
- Experiment failed silently but still produced partial artifacts.
- Metrics are misused, cherry-picked, or compared against a stale baseline.
- Data leakage, benchmark contamination, or post-hoc selection bias.
- Paper draft contains hallucinated numbers, missing figures, stale citations, weak paragraph flow, untracked terminology shifts, or overclaimed conclusions.

## Cross-Project Adaptation Checklist

When using this workflow in a new project:

1. Identify the project's baseline, control condition, or previous best result.
2. Lock the smallest shared protocol that makes comparisons valid.
3. Define the smallest valid pilot and the smallest result-bearing full run.
4. Define domain metrics and acceptable sanity checks.
5. Decide where ideas, hypotheses, experiment directories, analysis artifacts, and paper drafts live.
6. Record environment assumptions and required commands in project files, not in this generic skill.
7. Keep project-specific domain facts in `AGENTS.md`, a local playbook, or a project reference file.
8. Do not migrate unsupported claims from old projects; only migrate the process.
