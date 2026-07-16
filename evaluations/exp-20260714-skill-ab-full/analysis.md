# Analysis Report: exp-20260714-skill-ab-full

- **Question**: Across all 13 cases, does the candidate improve routing and focus without weakening profiles or evidence gates?
- **Analysis designation**: Confirmatory engineering evaluation against the predeclared corpus; external generalization is exploratory
- **Unit of analysis**: Behavior case paired across baseline and candidate
- **Baseline comparison**: Candidate working-tree snapshot versus git commit `1d088cd`
- **Selection rule**: All 13 predeclared cases, with no exclusions or retries
- **Aggregation and uncertainty**: Unweighted paired counts and character summaries; no inferential interval
- **Missing, failed, or excluded observations**: 0 / 0 / 0
- **Supported claims**: On this runner and corpus, the candidate improved trigger correctness and rubric coverage without increasing mean response length
- **Unsupported or inconclusive claims**: Stochastic stability, behavior on realistic artifact fixtures, generalization beyond these prompts, and performance on GPT-5.6 Sol
- **Warnings**: One positive case is under-specified and one rubric item is not directly observable from final output

## Pooled quantitative summary

| Metric | Baseline | Candidate | Effect or delta |
|---|---:|---:|---:|
| Critical-failure-free cases | 11/13 | 12/13 | +1 case |
| Invocation accuracy | 12/13 | 13/13 | +1 case |
| Profile accuracy | 11/13 | 12/13 | +1 case |
| Required-outcome coverage | 20/26 | 24/26 | +4 rubric points |
| Forbidden behaviors | 2 | 0 | -2 |
| Total response characters | 10405 | 10375 | -30 |
| Mean response characters | 800.38 | 798.08 | -0.3% |
| Median response characters | 648 | 510 | -21.3% |

The candidate satisfies the locked success rule: correctness metrics are no worse and mean length is not more than 10% higher.

## What improved

- `implicit_research_request`: Candidate respected disabled implicit invocation, avoided the heavy STANDARD workflow, and remained useful as an ordinary experiment-design assistant.
- `paper_new_direction`: Candidate covered the unresolved feasibility and novelty boundary more completely.
- `legacy_evidence_audit`: Candidate explicitly included missing controls and unverifiable provenance links.
- Several task-focused responses were shorter, including resume (-33.5%), paper drafting (-13.1%), and the implicit research request (-41.2%).

## What did not improve uniformly

- `lite_bounded_comparison`: Candidate was 88.2% longer, expanding a compact request into a detailed protocol template.
- `legacy_evidence_audit` and `paper_story_before_results` were 30.1% and 26.5% longer, respectively.
- The candidate is therefore better routed and lower-median, but not consistently more concise on every positive task.

## Evaluation-design findings

1. `standard_resume_existing` withholds the claimed `experiment.json` while expecting `STANDARD`. Both versions correctly refused to invent the manifest profile and were nevertheless scored as profile failures. Replace this case with a synthetic manifest in the next replication; do not reinterpret the frozen score.
2. `paper_draft_from_reviewed_evidence` scores whether only the relevant writing guide was loaded, but final text does not reliably reveal context loading. A future harness should capture read traces or replace this with an observable outcome.
3. One response per pair cannot separate Skill effects from sampling noise.
4. Local config identifies `gpt-5.5/xhigh`, not GPT-5.6 Sol.

## Decision Input

- Recommended action: REPLICATE
- Evidence: Parent and full raw outputs, blind scores, and `results/summary.json`
- Replication target: Actual GPT-5.6 Sol runner, corrected resume fixture, observable reference-loading metric, and at least three samples per case-variant pair
