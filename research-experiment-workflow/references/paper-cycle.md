# Paper Evidence and Revision Cycle

Load for coordinating evidence across experiments, paper readiness, or review-driven research. Writing remains outside `experiment.json.stage`.

## Minimal paper record

Use an existing equivalent record or `research/papers/<paper-id>/paper.json`. Create only when coordinating a paper, not for every experiment. Use the exact version 1 schema in `research-control.md`. Validate it with `scripts/validate_paper.py`; validate referenced experiments separately. This remains a paper-level record, not an experiment manifest.

Record `paper_id`, `phase` (PLANNING, EXPLORING, CONFIRMING, DRAFTING, REVIEWING, READY, or STOPPED), contribution type, budget/round limits, claims, experiment references, review issues, and next action. Each claim needs a stable ID, text, scope, status (PLANNED, EXPLORATORY, CONFIRMED, INCONCLUSIVE, REFUTED), supporting and contradicting evidence, and remaining gaps. Artifact paths are relative to the explicit downstream project root; dependency and review references use stable artifact IDs, as defined in `research-control.md`.

Each evidence reference identifies the experiment/run, protocol version, code snapshot including uncommitted changes when relevant, data version, result/analysis artifact and immutable revision or content digest. Never invent missing provenance. Historical evidence with missing versions remains usable only within its disclosed limits.

## Review and change control

Separate run-integrity review (before interpretation) from claim-support review (after analysis, before final writing). They may share REVIEW.md with explicit scopes. Record reviewer, context independence, checked artifact versions, verdict and outstanding issues. Same-context self-review is a pre-check; fresh context alone does not establish scientific independence.

For each important issue record ID, affected claims, severity, requested evidence/change, linked task, budget, status and closure evidence. Route presentation issues to writing, evidence gaps to experiments, mechanism defects to hypothesis revision, and contribution collisions to research positioning. An issue closes only when its specific concern is addressed or the affected claim is withdrawn; a higher score is not closure.

When an input changes, identify dependent analyses, figures, claims and reviews. Preserve historical artifacts; mark affected support/reviews stale and re-check them before advancing. Content changes that do not affect evidence may retain validity with a recorded reason. Existing experiment invalidation rules still apply. The paper validator checks recorded fingerprints, dependencies, budgets and readiness conditions. Scientific support and completeness of the dependency inventory still require explicit review.

## Revision loop and readiness

Draft provisional stories early with planned-versus-observed labels. Run bounded review/rebuttal rounds. Supplementary experiments use the same feasibility, protocol, pilot and review requirements as other experiments. If feedback changes the method, return to development; never tune on protected final results.

Before READY, verify central claims against current evidence, resolve blocking issues, reproduce key results using saved commands, check method-code alignment, confirm citation existence and actual claim support, and check figures/tables against source outputs. Scale evidence to contribution type; theoretical claims require appropriate proof review. Report unresolved limitations and accepted warnings. The researcher decides contribution significance, venue fit and submission; READY does not authorize submission or guarantee acceptance.

Use existing Coordinator, Theorist, Engineer, Analyst, Reviewer and Writer roles. Coordinator owns issue routing and dependency tracking; Analyst updates claim support; Reviewer checks evidence and closure; Writer revises only supported claims. Delegation remains opt-in under the entrypoint's existing rule.
