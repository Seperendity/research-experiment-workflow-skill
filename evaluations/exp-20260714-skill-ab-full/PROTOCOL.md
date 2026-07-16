# Protocol: exp-20260714-skill-ab-full

- **Profile**: LITE
- **Status**: LOCKED
- **Research question**: Across the full 13-case behavior corpus, does the candidate improve routing and focus without weakening profile selection or evidence gates relative to baseline `1d088cd`?
- **Estimand or target quantity**: Paired candidate-minus-baseline difference in critical-failure-free cases, rubric scores, and response length.
- **Unit of analysis**: One behavior case paired across baseline and candidate.
- **Primary decision metric**: Critical-failure-free case count across all 13 cases.
- **Secondary and safety metrics**: Invocation accuracy, profile accuracy, required-outcome coverage, forbidden-behavior count, mean response characters, median response characters, and case-level length ratios.
- **Baseline or control**: Skill package at git commit `1d088cd8413d2cae0aacb5ba1db3ba0bed6296a8`.
- **Data and evaluation boundaries**: Reuse the four frozen parent-pilot case pairs and run only the nine previously unused cases from `tests/skill_behavior_cases.json`. Forward-test agents receive one neutral Skill snapshot and one raw task prompt, but not answer keys, variant identity, other outputs, or parent results.
- **Tuning and final-test boundary**: Skill snapshots, wrappers, prompts, answer keys, and rubric remain unchanged. No Skill edit is allowed until all outputs and scores are frozen.
- **Run plan and budget**: Eighteen new independent responses, one for each held-out case-variant pair. Pool them with the eight parent-pilot responses for a 13-case paired summary. No sampling retries; at most one retry for confirmed infrastructure failure.
- **Sample-size or repeat rationale**: The corpus is the complete predeclared behavior set. One response per pair measures deterministic routing behavior under the current runner but not stochastic stability.
- **Seed policy**: No seed is exposed. Use fresh isolated contexts, identical wrappers, and the same runner configuration for both variants.
- **Aggregation and uncertainty**: Report paired case-level outcomes and unweighted counts. Do not calculate inferential confidence intervals from the convenience corpus.
- **Missing and failed-run handling**: A missing model response is a critical failure. A confirmed infrastructure failure may be retried once and disclosed. No post-output case exclusion.
- **Exclusions and multiple comparisons**: None; all 13 cases remain in the pooled analysis. Metrics are descriptive and no significance test is used.
- **Stopping and selection rule**: Stop for snapshot contamination, answer-key leakage, or runner mismatch. Otherwise finish all 18 held-out responses before scoring or editing.
- **Analysis designation**: Confirmatory engineering evaluation against the predeclared corpus and rubric; external generalization remains exploratory.
- **Allowed change surface**: Infrastructure-only fixes before a successful response. No changes to the Skill, cases, wrapper, rubric, or scoring map.
- **Success, failure, or inconclusive rule**: Success requires candidate critical-failure-free cases, invocation accuracy, profile accuracy, and required-outcome coverage to be no worse than baseline, with mean response length no more than 10% higher. Any correctness regression is failure. A correctness pass with more than 10% mean-length inflation is inconclusive and routes to `REVISE` for concision.
- **Warnings or accepted exceptions**: This evaluation cannot be attributed to GPT-5.6 Sol, and one response per pair does not estimate stochastic variance.

## Locked scoring

Reuse the parent protocol's five-field rubric. For positive cases, score invocation, expected profile, required-outcome coverage, and forbidden behavior. For negative cases, correct ordinary behavior receives complete outcome coverage when it avoids all forbidden behavior. Compute response characters from the frozen raw string after scoring.
