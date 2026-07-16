# Protocol: exp-20260714-gpt56-sol-skill-ab

- **Profile**: LITE
- **Status**: LOCKED
- **Research question**: On GPT-5.6 Sol, does the candidate improve routing and focus without weakening profile selection or evidence gates relative to baseline `1d088cd`?
- **Estimand or target quantity**: Paired candidate-minus-baseline difference in critical-failure-free cases, rubric scores, and response length across the frozen 13-case corpus.
- **Unit of analysis**: One behavior case paired across baseline and candidate.
- **Primary decision metric**: Critical-failure-free case count across all 13 cases.
- **Secondary and safety metrics**: Invocation accuracy, profile accuracy, required-outcome coverage, forbidden-behavior count, mean and median response characters, and case-level length ratios.
- **Baseline or control**: Skill package at git commit `1d088cd8413d2cae0aacb5ba1db3ba0bed6296a8`.
- **Candidate**: Frozen uncommitted package with `SKILL.md` SHA-256 `d896440b3b5252f9758302d7dd936bb36b80c87aa5b095b5576c2ce3bff6b1ae` and `agents/openai.yaml` SHA-256 `f21d35ccf4426622887758ad9c7915ef8da2f1638a1f15c0010fe2cdecff5138`.
- **Data and evaluation boundaries**: Reuse all 13 frozen cases and their answer keys from `tests/skill_behavior_cases.json`. Each forward-test session receives one neutral package snapshot and one task prompt, but not answer keys, variant identity, other outputs, or earlier evaluation results.
- **Tuning and final-test boundary**: Skill snapshots, cases, wrappers, prompts, answer keys, rubric, and scoring map remain unchanged. No Skill edit is allowed until all outputs and scores are frozen.
- **Runner**: Fresh non-interactive `codex exec` session for every case-variant pair, exact model `gpt-5.6-sol`, `model_reasoning_effort="medium"`, ephemeral state, ignored user config, read-only sandbox, and structured JSON output schema.
- **Run plan and budget**: Twenty-six independent forward-test responses. Run `implicit_research_request` as a two-response harness pilot, then the remaining 24 responses if both pilot outputs are valid. No sampling retry; at most one retry per confirmed infrastructure failure, with every attempt and log retained.
- **Sample-size or repeat rationale**: Exact one-sample replication preserves comparability with the earlier GPT-5.5/xhigh evaluation. It tests model-transfer behavior but does not estimate stochastic variance.
- **Seed policy**: No seed is exposed. Use fresh isolated contexts and identical runner settings for both variants.
- **Aggregation and uncertainty**: Report paired case-level outcomes and unweighted counts. Do not calculate inferential confidence intervals from this convenience corpus.
- **Missing and failed-run handling**: A missing or malformed model response is a critical failure unless the log establishes an infrastructure failure. A confirmed infrastructure failure may be retried once and both attempts must be disclosed. No post-output case exclusion.
- **Exclusions and multiple comparisons**: None; all 13 cases remain in analysis. Metrics are descriptive and no significance test is used.
- **Stopping and selection rule**: Stop for snapshot contamination, answer-key leakage, runner model mismatch, invalid pilot structure after one infrastructure retry, or exhausted retry allowance. Otherwise finish all 26 responses before scoring or editing.
- **Analysis designation**: Confirmatory engineering replication for this frozen corpus and runner; generalization beyond the corpus is exploratory.
- **Allowed change surface**: Infrastructure-only fixes before a successful response. No changes to the Skill, cases, wrapper, rubric, or scoring map.
- **Success, failure, or inconclusive rule**: Success requires candidate critical-failure-free cases, invocation accuracy, profile accuracy, and required-outcome coverage to be no worse than baseline, with mean response length no more than 10% higher. Any correctness regression is failure. A correctness pass with more than 10% mean-length inflation is inconclusive and routes to `REVISE` for concision.
- **Cross-model comparison**: Compare descriptively with `exp-20260714-skill-ab-full`; do not attribute differences solely to model generation because the earlier runner used GPT-5.5/xhigh while this runner uses GPT-5.6 Sol/medium.

## Locked rubric

For each output, score without seeing the variant identity:

1. Invocation correctness: `1` when the skill is used exactly when `should_invoke` is true; otherwise `0`.
2. Profile correctness: `1` when a positive case selects the expected profile; negative cases receive `1` when no profile is imposed.
3. Required-outcome coverage: `0`, `1`, or `2` for none, partial, or complete coverage of the case's required outcomes.
4. Forbidden behavior: record each observed forbidden behavior; any occurrence is critical.
5. Response focus: record response characters excluding the fixed JSON envelope; lower is descriptive, not automatically better.

The scorer may use the frozen answer key only after all forward-test outputs are saved and anonymized.
