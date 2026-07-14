# Research Experiment Artifact Contract

Use this reference when creating, checking, or adapting a research experiment workflow. Keep project-specific names, paths, metrics, commands, and safety policy in the repository; keep the gate structure stable.

## Contents

- [Suggested Project Layout](#suggested-project-layout)
- [Project Interface Contract](#project-interface-contract)
- [Workflow Profiles](#workflow-profiles)
- [Stage Gates](#stage-gates)
- [Gate Semantics](#gate-semantics)
- [Experiment Directory Contract](#experiment-directory-contract)
- [Experiment State Version 3](#experiment-state-version-3)
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
- Intended claim scope and workflow profile.
- Expected result schema, metric names, and artifact paths.
- Estimand or target quantity, unit of analysis, and primary decision metric.
- Sample-size or repeat rationale, seed policy, aggregation method, uncertainty method, hardware assumptions, timeout, run budget, and retry budget.
- Protected data, tuning and final-evaluation boundaries, stopping and selection rules, and allowed change surface.
- Missing-data, failed-run, exclusion, and multiple-comparison policies when applicable.
- Sandbox, dependency, and network policy for generated or modified code.
- Paper or report template, citation style, and figure/table conventions if writing is expected.

## Workflow Profiles

Choose the least burdensome profile that can support the intended claim. Default new empirical work to `STANDARD`; escalate when claim risk increases and never downgrade to bypass a failed gate.

| Profile | Intended use | Required gate sequence |
|---|---|---|
| `LITE` | Engineering checks, debugging, local exploratory runs, or low-stakes reproduction not used for paper claims | `protocol -> pilot`; add feasibility or review when the project risk requires it |
| `STANDARD` | Default empirical research, internal studies, and reproducibility work | `feasibility -> protocol -> pilot -> review` |
| `PAPER` | Novelty, comparative, causal, or reviewer-facing claims | `novelty -> feasibility -> protocol -> pilot -> review` |
| `LEGACY_AUDIT` | Existing evidence that lacks current workflow history | No retroactive gate sequence; record missing evidence, provenance, and controls as limitations |

`Paper story` and `writing` are paper-level activities, not experiment lifecycle stages. They may consume several completed experiment packages and must not be written into `experiment.json.stage`.

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

## Gate Semantics

Use `PASS | WARNING | FAIL | PENDING | NOT_APPLICABLE` as the normalized gate vocabulary in schema version 3.

| Artifact verdict | Manifest gate verdict |
|---|---|
| Novelty `NOVEL` | `PASS` |
| Novelty `PARTIAL` or `UNCLEAR` with a narrowed claim or accepted literature risk | `WARNING` |
| Novelty `KNOWN` when novelty is claimed | `FAIL` |
| Feasibility `GO` | `PASS` |
| Feasibility `CONDITIONAL-GO` | `WARNING` until conditions are resolved or explicitly accepted |
| Feasibility `NO-GO` | `FAIL` |
| Protocol `DRAFT` | `PENDING` |
| Protocol `LOCKED` | `PASS` |
| Locked protocol with an accepted exception | `WARNING` |
| Protocol `INVALIDATED` | `FAIL` |
| Pilot `PASS` / `FAIL` | `PASS` / `FAIL` |
| Review `PASS` / `WARNING` / `FAIL` | Same normalized verdict |

Apply these rules:

1. Use `NOT_APPLICABLE` only when the selected profile does not require the gate. Set `artifact` to `null`, record a non-empty `rationale`, and never use it to bypass a required gate.
2. A `WARNING` requires a non-empty gate `rationale` describing the risk. It may exist before acceptance, but it blocks any stage that requires the gate. To advance, record an `acceptance` object with the authorizing human or project owner, an ISO-8601 timestamp, and a separate rationale for proceeding. An agent must not infer or fabricate acceptance.
3. `PASS`, `WARNING`, and `FAIL` require an existing artifact. `PENDING` may point to a planned artifact that does not exist yet.
4. A failed required gate requires experiment status `BLOCKED`, `FAILED`, or `INVALIDATED`.
5. Strict validation requires the current manifest schema and complete profile contract. A valid accepted warning is reported as a notice, not a strict-validation failure.

## Experiment Directory Contract

Each new experiment must use `experiment.json` as its control-plane record. Keep artifact volume proportional:

- Every result-bearing profile: `experiment.json`, `README.md`, config or command snapshot, `run_notes.md`, `results/summary.json`, `analysis.md`, and `DECISION.md`.
- `LITE`: add `PROTOCOL.md` and `PILOT.md`; add feasibility or review artifacts only when those checks are used.
- `STANDARD`: add `FEASIBILITY.md`, `PROTOCOL.md`, `PILOT.md`, and `REVIEW.md`.
- `PAPER`: use the `STANDARD` package plus `NOVELTY.md` or a linked literature note and all evidence needed for paper claims.
- `LEGACY_AUDIT`: do not create fictional historical artifacts. Preserve the source package and add only the requested review, analysis, or decision artifacts with explicit limitations.

Add `DEBUG.md` after a failed or interrupted run. Add `ABLATION_PLAN.md` before an ablation suite. Existing experiments without `experiment.json` remain readable legacy experiments; validators should warn rather than fail unless strict mode is requested.

## Experiment State Version 3

Use this minimum `experiment.json` structure for new work:

```json
{
  "schema_version": 3,
  "experiment_id": "exp-YYYYMMDD-short-name",
  "hypothesis_id": "H-XXX",
  "profile": "STANDARD",
  "stage": "IDEA | HYPOTHESIS | NOVELTY | FEASIBILITY | PROTOCOL | PILOT | EXPERIMENT | DEBUG | ABLATION | REVIEW | ANALYSIS | DECISION",
  "status": "PLANNED | RUNNING | INTERRUPTED | BLOCKED | DONE | FAILED | PARTIAL | INVALIDATED",
  "parent_experiment_id": null,
  "gates": {
    "novelty": {
      "verdict": "NOT_APPLICABLE",
      "artifact": null,
      "rationale": "STANDARD profile; no novelty claim",
      "acceptance": null
    },
    "feasibility": {"verdict": "PASS", "artifact": "FEASIBILITY.md", "rationale": null, "acceptance": null},
    "protocol": {"verdict": "PASS", "artifact": "PROTOCOL.md", "rationale": null, "acceptance": null},
    "pilot": {"verdict": "PASS", "artifact": "PILOT.md", "rationale": null, "acceptance": null},
    "review": {"verdict": "PASS", "artifact": "REVIEW.md", "rationale": null, "acceptance": null}
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

For an accepted warning, replace `acceptance: null` with:

```json
{
  "accepted_by": "authorizing human or project owner",
  "accepted_at": "YYYY-MM-DDTHH:MM:SSZ",
  "rationale": "why proceeding is acceptable"
}
```

State semantics:

- `profile` defines the minimum gate sequence; escalate it when claim risk increases and do not downgrade it to erase requirements.
- `stage` is the current resume point in the experiment lifecycle.
- `status` describes the current stage. When advancing, update `stage` to the destination and set an appropriate new status; `DONE` at `DECISION` completes the current workflow cycle.
- `hypothesis_id` may be `null` only for `LITE` or `LEGACY_AUDIT`; `STANDARD` and `PAPER` require a recorded hypothesis.
- Keep every artifact path relative to the experiment directory.
- Treat an artifact as valid only when it exists, parses when structured, is referenced by the manifest, and has no failed or unaccepted required upstream gate.
- When a material protocol or implementation change makes downstream evidence stale, set the experiment to `INVALIDATED` or reset the affected gates to `PENDING` before continuing.

Schema version 2 manifests remain readable in compatibility mode. New or migrated experiments should use version 3; strict mode rejects compatibility warnings. The result summary schema remains version 2.

## `results/summary.json` Version 2

Use the following minimum structure for new experiments:

```json
{
  "schema_version": 2,
  "experiment_id": "exp-YYYYMMDD-short-name",
  "hypothesis_id": "H-XXX",
  "status": "DONE | FAILED | PARTIAL",
  "protocol": "PROTOCOL.md",
  "primary_metric": {"name": "metric_name", "direction": "minimize | maximize | target | none"},
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

Use `runs` for repeated executions, folds, groups, or other project-defined units; keep their domain-specific fields inside each run or its artifacts. Keep aggregation methods project-defined and record them in the protocol. Use `target` or `none` when the decision rule is not monotonic and define the exact rule in `PROTOCOL.md`. The summary `hypothesis_id` may be `null` only when a version 3 `LITE` or `LEGACY_AUDIT` manifest also records it as `null`. Use other `null` values only when a field is not applicable or unavailable and explain the reason in `warnings`.

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
- **Profile**: LITE | STANDARD | PAPER | LEGACY_AUDIT
- **Intended claim scope**: <engineering check, internal result, reproducibility, or paper claim>
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

- **Profile**: LITE | STANDARD | PAPER | LEGACY_AUDIT
- **Status**: DRAFT | LOCKED | INVALIDATED
- **Research question**: <question being tested>
- **Estimand or target quantity**: <effect, quantity, or decision target>
- **Unit of analysis**: <independent sample, subject, task, seed, fold, or other unit>
- **Primary decision metric**: <metric, direction, and decision role>
- **Secondary and safety metrics**: <metrics or not applicable>
- **Baseline or control**: <artifact, command, citation, or not-applicable reason>
- **Data and evaluation boundaries**: <protected splits, inputs, contamination checks, evaluation rules>
- **Tuning and final-test boundary**: <what may guide selection; what remains untouched>
- **Run plan and budget**: <runs, repeats, timeout, retry limit>
- **Sample-size or repeat rationale**: <power, precision, coverage, convention, or budget rationale>
- **Seed policy**: <fixed or sampled seeds and how they are chosen>
- **Aggregation and uncertainty**: <summary statistic, effect size, interval or resampling method>
- **Missing and failed-run handling**: <predeclared treatment>
- **Exclusions and multiple comparisons**: <rules, correction, or not applicable>
- **Stopping and selection rule**: <predefined rule>
- **Analysis designation**: <confirmatory tests and exploratory analyses>
- **Allowed change surface**: <what may change; what must remain fixed>
- **Success, failure, or inconclusive rule**: <evidence threshold or decision rule>
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
- **Analysis designation**: confirmatory | exploratory | mixed
- **Unit of analysis**: <unit from the locked protocol>
- **Baseline comparison**: <ours vs baseline>
- **Selection rule**: <predefined rule for which runs are compared>
- **Aggregation and uncertainty**: <method from the locked protocol>
- **Missing, failed, or excluded observations**: <counts and treatment>
- **Supported claims**: <list>
- **Unsupported or inconclusive claims**: <list>
- **Warnings**: <list or none>

## Quantitative Summary

| Metric/estimand | Baseline | Ours | Effect or delta | Uncertainty |
|---|---|---|---|---|
| | | | | |

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

1. Choose the least burdensome workflow profile that supports the intended claim.
2. Identify the project's baseline, control condition, or previous best result.
3. Define the estimand, unit of analysis, primary decision metric, and tuning/final-test boundary.
4. Lock the smallest shared protocol that makes comparisons valid.
5. Define the smallest valid pilot and the smallest result-bearing full run.
6. Define domain metrics, uncertainty reporting, failure handling, and acceptable sanity checks.
7. Decide where ideas, hypotheses, experiment directories, analysis artifacts, and paper drafts live.
8. Record environment assumptions and required commands in project files, not in this generic skill.
9. Keep project-specific domain facts in `AGENTS.md`, a local playbook, or a project reference file.
10. Do not migrate unsupported claims from old projects; only migrate the process.
