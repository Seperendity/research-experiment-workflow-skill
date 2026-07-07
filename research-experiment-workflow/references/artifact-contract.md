# Research Experiment Artifact Contract

Use this reference when creating, checking, or adapting a research experiment workflow. Keep project-specific names, paths, metrics, commands, and safety policy in the repository; keep the gate structure stable.

## Suggested Project Layout

Use existing project conventions if they exist. If a project has no research structure, propose this minimal layout before creating many files:

```text
research/
  ideas.json
  hypotheses/
    tracker.md
  experiments/
    exp-YYYYMMDD-short-name/
      README.md
      FEASIBILITY.md
      NOVELTY.md
      PILOT.md
      REVIEW.md
      analysis.md
      run_notes.md
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
- Sandbox, dependency, and network policy for generated or modified code.
- Paper or report template, citation style, and figure/table conventions if writing is expected.

## Stage Gates

| Stage | Primary artifact | Gate |
|---|---|---|
| Idea scoring | `research/ideas.json` | Candidate idea is scored and selected |
| Hypothesis | `research/hypotheses/tracker.md` entry | Falsifiable hypothesis recorded |
| Novelty check | `NOVELTY.md` or literature note | Contribution is defensible or risk is accepted |
| Feasibility | `FEASIBILITY.md` | Verdict is `GO` or resolved/accepted `CONDITIONAL-GO` |
| Pilot | `PILOT.md` | Status is `PASS` |
| Experiment run | Config snapshot, `run_notes.md`, and `results/summary.json` | Run completed and artifacts saved |
| Review | `REVIEW.md` | Status is `PASS` or accepted `WARNING` |
| Analysis | `analysis.md` | Supported and unsupported claims are explicit |
| Writing | Draft under `research/papers/drafts/` | Claims cite artifacts or literature |

## Experiment Directory Contract

Each completed or paper-relevant experiment should contain:

- `README.md`
- `FEASIBILITY.md`
- `NOVELTY.md` or a linked literature note when paper claims depend on novelty
- `PILOT.md`
- `REVIEW.md`
- Config snapshot or command snapshot
- `run_notes.md`
- `results/summary.json`
- `analysis.md`

## `results/summary.json` Minimum Fields

```json
{
  "experiment_id": "exp-YYYYMMDD-short-name",
  "hypothesis_id": "H-XXX",
  "status": "DONE | FAILED | PARTIAL",
  "config_base": "base config, command, or protocol name",
  "config_overrides": {},
  "seed": 0,
  "metrics": {},
  "baseline": {},
  "delta_vs_baseline": {},
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

Use `null` only when the field is not applicable and explain the reason in `warnings`.

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
- **Status**: PLANNED | RUNNING | DONE | FAILED
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

### Review

```markdown
# Review Report: <target>

- **Status**: PASS | WARNING | FAIL
- **Scope**: code | experiment | analysis | paper draft
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

## Next Steps

1. <next experiment or decision>
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
2. Define the smallest valid pilot and the smallest result-bearing full run.
3. Define domain metrics and acceptable sanity checks.
4. Decide where ideas, hypotheses, experiment directories, analysis artifacts, and paper drafts live.
5. Record environment assumptions and required commands in project files, not in this generic skill.
6. Keep project-specific domain facts in `AGENTS.md`, a local playbook, or a project reference file.
7. Do not migrate unsupported claims from old projects; only migrate the process.
