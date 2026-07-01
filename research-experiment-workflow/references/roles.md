# Research Workflow Role Model

Use this reference only for multi-agent, delegated, or role-scoped research work. Keep role handoffs grounded in saved artifacts, not chat memory.

## Coordinator

Purpose: Coordinate multi-stage research work across hypothesis design, implementation, review, analysis, and writing.

Responsibilities:

- Translate user goals into staged work with explicit artifacts and gates.
- Assign work to role-appropriate agents when delegation is active.
- Keep the current experiment, evidence package, and paper claims consistent across stages.
- Stop or reroute execution when a gate fails, evidence is missing, or warnings are not accepted.

Out of scope:

- Owning the main implementation for a non-trivial code change.
- Providing final independent review of work it delegated or implemented.
- Writing final paper claims without reviewed analysis artifacts.

Required outputs:

- Task decomposition with owners.
- Gate decisions and rationale.
- Integrated summary that cites saved artifacts.

## Engineer

Purpose: Implement code, configuration, data, and experiment changes needed to test a hypothesis.

Responsibilities:

- Modify code, configs, scripts, and experiment setup.
- Define and run the smallest meaningful pilot before full execution.
- Save reproducible commands, configs, logs, metrics, and generated artifacts.
- Record assumptions, config overrides, environment constraints, and known risks.

Out of scope:

- Giving final approval to its own implementation or experiment package.
- Writing the main analysis interpretation.
- Drafting paper conclusions from unreviewed results.

Required outputs:

- Code or config changes when needed.
- Config or command snapshot.
- `PILOT.md` for pilot work.
- `run_notes.md` and `results/summary.json` for completed runs.
- Experiment README updates when scope or status changes.

## Reviewer

Purpose: Provide independent review for code, experiments, analysis, and evidence quality.

Responsibilities:

- Check correctness, regressions, reproducibility gaps, artifact completeness, and baseline fairness.
- Check for data leakage, metric misuse, invalid comparisons, cherry-picking, and post-hoc selection.
- Review whether claims are supported by saved artifacts and whether warnings are acceptable.
- Decide `PASS`, `WARNING`, or `FAIL` with blocking issues clearly separated from non-blocking issues.

Out of scope:

- Owning the implementation being reviewed.
- Creating post-hoc claims to justify weak evidence.
- Rewriting paper prose as the main task unless explicitly scoped as draft review.

Required outputs:

- `REVIEW.md`.
- Prioritized findings with severity and blocking status.
- Explicit sign-off state and required follow-ups.

## Analyst

Purpose: Turn saved experiment artifacts into defensible quantitative and qualitative findings.

Responsibilities:

- Load saved metrics, arrays, logs, figures, and run notes.
- Compare results against baselines or planned controls using a predefined selection rule.
- Compute summaries, uncertainty, significance tests, or qualitative case studies when appropriate.
- State what the results support, what they do not support, and what remains inconclusive.

Out of scope:

- Changing training code or experiment logic to improve results.
- Selecting only favorable runs without a documented rule.
- Writing final paper prose without reviewed numbers and cited artifacts.

Required outputs:

- `analysis.md`.
- Tables, figure references, or plot inputs as needed.
- Supported, unsupported, and inconclusive claim summary.

## Writer

Purpose: Draft paper sections, technical reports, or research summaries from confirmed evidence.

Responsibilities:

- Convert reviewed analysis, hypotheses, and literature notes into clear prose.
- Keep every quantitative or comparative claim mapped to experiment IDs, analysis artifacts, figures, tables, or citations.
- Preserve uncertainty, limitations, failed runs, and unresolved evidence gaps when they affect interpretation.
- Run the writing integrity checklist before presenting prose as paper-ready.

Out of scope:

- Inventing numbers, baselines, citations, or qualitative findings.
- Treating pilot-only or unreviewed results as final evidence.
- Performing the main implementation, analysis, or independent review work.

Required outputs:

- Draft files under the project's paper or report directory.
- Claim-to-evidence mapping.
- Open evidence gaps or TODOs when the evidence is incomplete.

## Theorist

Purpose: Support hypothesis generation, literature synthesis, novelty framing, and theoretical trade-off analysis.

Responsibilities:

- Formulate falsifiable hypotheses and alternative explanations.
- Compare design alternatives using structured reasoning.
- Identify close prior work, likely reviewer questions, and novelty risks.
- Distinguish established facts from assumptions, hypotheses, and project-specific guesses.

Out of scope:

- Owning code implementation.
- Providing final experiment review sign-off.
- Writing results claims without analysis artifacts.

Required outputs:

- Hypothesis proposals.
- Literature or novelty notes.
- Trade-off tables, assumptions, and open questions.

## Handoff Rules

- Coordinator to Engineer: provide scope, success criteria, artifact targets, budget, and write boundaries.
- Engineer to Reviewer: provide diff summary, commands, pilot or run results, artifacts, and known risks.
- Engineer to Analyst: provide `results/summary.json`, config snapshot, logs, run notes, and figure inputs.
- Analyst to Writer: provide supported claims, unsupported claims, exact numbers, figure references, and citations.
- Reviewer to Coordinator: provide `PASS`, `WARNING`, or `FAIL`, with blocking follow-ups.

Do not let a handoff rely only on chat memory. If the receiving role needs a fact, save it in an artifact or cite the existing file that contains it.
