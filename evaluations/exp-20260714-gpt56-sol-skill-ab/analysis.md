# Analysis Report: exp-20260714-gpt56-sol-skill-ab

- **Question**: On GPT-5.6 Sol, does the candidate improve routing and focus without weakening profiles or evidence gates?
- **Analysis designation**: Confirmatory engineering replication against the frozen 13-case corpus; external generalization is exploratory
- **Unit of analysis**: Behavior case paired across baseline and candidate
- **Baseline comparison**: Candidate working-tree snapshot versus git commit `1d088cd`
- **Runner**: Exact model `gpt-5.6-sol`, medium reasoning, 26 fresh ephemeral read-only `codex exec` sessions
- **Selection rule**: All 13 predeclared cases, with no exclusions
- **Missing, failed, retried observations**: 0 / 0 / 0
- **Scoring warning**: Variant identity stayed hidden during scoring, but only one local blind audit was possible. The planned three external scorers were prohibited because the packet was classified as workspace-data export.

## Quantitative summary

| Metric | Baseline | Candidate | Candidate − baseline |
|---|---:|---:|---:|
| Critical-failure-free cases | 11/13 | 11/13 | 0 |
| Invocation accuracy | 12/13 | 12/13 | 0 |
| Profile accuracy | 11/13 | 11/13 | 0 |
| Required-outcome coverage | 22/26 | 22/26 | 0 |
| Forbidden behaviors | 2 | 2 | 0 |
| Total response characters | 13135 | 11897 | -1238 |
| Mean response characters | 1010.38 | 915.15 | -9.4% |
| Median response characters | 646 | 681 | +5.4% |

The candidate satisfies the locked non-inferiority and mean-length rule: all correctness metrics are no worse, and mean length is not more than 10% higher. It is not uniformly more concise: it is longer in 7 of 13 paired cases, and the lower mean is driven mainly by large reductions on `implicit_research_request` and `paper_story_before_results`.

## Target-model finding

The GPT-5.5/xhigh evaluation favored the candidate by one critical-failure-free case because it respected disabled implicit invocation. That advantage did not replicate on GPT-5.6 Sol/medium:

- Both variants invoked the skill for `implicit_research_request`, selected `STANDARD`, imposed protocol and pilot machinery, and proposed durable artifact capture without explicit invocation.
- The candidate response was much shorter than baseline on that case (1353 versus 2885 characters), but it still crossed the locked invocation boundary and incurred the same critical failure.
- Both variants also failed the frozen `standard_resume_existing` profile check because the prompt claimed an existing manifest but supplied none. This known fixture flaw was retained to preserve exact replication.

The supported claim is narrow: on this frozen corpus, the candidate is non-inferior to baseline and shorter on average under GPT-5.6 Sol. The stronger claim that the candidate reliably prevents implicit high-ceremony invocation on GPT-5.6 Sol is unsupported.

## Interpretation for skill design

This result supports the concern that a planning-strong model can amplify workflow ceremony when skill-level signals conflict. The package says `allow_implicit_invocation: false` and narrows its description to explicit durable-artifact work, yet the model still interpreted a generic experiment-design request as requiring `STANDARD`. Adding more lifecycle rules would not address that boundary and could increase prompt competition.

The highest-value revision is small and metadata-focused:

1. Make the negative boundary concrete in the frontmatter: merely asking to discuss or design an experiment is not invocation; require the skill name or an explicit request to create/update durable experiment files.
2. Keep the workflow body compact; do not add another planning layer, meta-controller, or conflict-resolution procedure.
3. Add a native-runtime trigger test that exercises `allow_implicit_invocation: false` without the evaluation wrapper explicitly presenting the skill path, because the wrapper may itself prime skill use.

## Evaluation-design limitations

1. One sample per pair does not estimate stochastic stability.
2. GPT-5.5/xhigh versus GPT-5.6 Sol/medium is a joint model-and-reasoning change, so the cross-model difference is descriptive rather than causal.
3. `standard_resume_existing` needs a synthetic manifest fixture in a future non-replication test.
4. Selective reference loading is not observable from response text; future testing should capture read traces.
5. The single local scorer reduces confidence in subjective outcome-coverage judgments, though invocation and profile scores are directly determined by structured fields.

## Decision input

- **Recommended action**: `REVISE`
- **Reason**: The locked A/B success rule passes, but the target-model replication does not confirm the candidate's intended implicit-invocation improvement.
- **Next test**: After one concise metadata revision, run a small trigger-only matrix on GPT-5.6 Sol with explicit invocation, implicit experiment design, ordinary debugging, and explicit durable-artifact requests; use repeated samples before another full lifecycle evaluation.
