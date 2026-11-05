# Research Design and Candidate Learning

Load for research direction selection, hypothesis design, screening, or method refinement. Keep project-specific thresholds and commands downstream.

## Research plan

Use an existing project overview or `research/RESEARCH_PLAN.md`; create it only when coordinating a research direction. Record the important question, intended contribution type, closest prior work, observed bottleneck, evidence gaps, resource budget, and stopping conditions. Distinguish author-stated limitations from reproduced failures. Contribution types may include methods, theory, empirical insight, efficiency, evaluation, and applications; improvement over SOTA is not a universal success rule.

## Candidates

Extend existing idea records with a stable ID, parent candidate IDs, bottleneck evidence, mechanism prediction, closest-work distinction, discriminating experiment, falsification condition, linked experiments, and revision reason. Keep scores as prioritization aids with evidence and uncertainty, never proof of novelty. Search terminology variants and adjacent approaches; record search date and scope. Refresh novelty when the contribution changes and before submission.

Compare credible alternatives, including a simple explanation or control. Preserve failed candidates and what they taught. Distinguish implementation failure, contradicted prediction, inconclusive evidence, and resource exhaustion. A failed implementation is not a refuted scientific hypothesis.

## Two pilot questions

1. Engineering pilot: does the implementation execute correctly, compute meaningful metrics, and save artifacts?
2. Scientific screening: on development data, does evidence support investing in the hypothesis or discriminate it from alternatives?

Keep engineering PASS separate from scientific promise. Record screening evidence and a REPLICATE, ABLATE, REVISE, SCALE, DEBUG, or STOP decision using existing artifacts. A promising pilot remains exploratory evidence.

Increase fidelity only when justified. Check that the subset contains the conditions under which the proposed mechanism should operate; use baseline or known variants to assess proxy usefulness when practical. Do not discard scale-dependent hypotheses solely on an unsuitable proxy. Record tuning and selection across all candidates, not just the winner. Allocate bounded effort to both refinement and unexplored alternatives.

## Claim-driven experiments

For each intended claim record supporting evidence needed, strongest alternative explanation, discriminating comparison, expected observation, and failure/inconclusive rule. Match data, preprocessing, evaluation, and relevant compute/tuning budgets across comparisons. Resolve unexplained baseline reproduction gaps before claiming gains.

Use removal, replacement, capacity/budget controls, and explicit interaction studies as appropriate. Component removal alone does not establish a causal mechanism. Let ablations remove unnecessary components or revise the explanation. Test generalization and efficiency only as broadly as claimed; do not impose universal dataset or seed counts. Use the protocol's independent unit, uncertainty method, and meaningful effect threshold.

## Confirmation and learning

Freeze the selected method, analysis and evaluation rules before confirmation. Development results may guide refinement; protected final-test observations may not. A changed method returns to development and requires fresh confirmation evidence or an explicitly exploratory claim. Re-locking a protocol does not make previously observed test data unseen.

Every iteration ends with one actionable decision and preserved evidence, including negative findings. Stop when the requested outcome is reached, the budget is exhausted, or further work cannot resolve a consequential uncertainty. Do not optimize indefinitely for a metric or reviewer score.

## Executing a round

Use `research-control.md` for exact candidate, round and stage-evaluation records. Complete the authorized research iteration through its decision, using recorded promotion criteria and trial/evaluation budgets. Use its shared evaluation contract for novelty checks, screening, ablation feedback and strategic meta-review.
