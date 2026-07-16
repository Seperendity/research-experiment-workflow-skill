# Protocol: exp-20260714-skill-ab-pilot

- **Profile**: LITE
- **Status**: LOCKED
- **Research question**: Does the candidate skill improve routing and response focus without weakening profile selection or evidence gates relative to baseline `1d088cd`?
- **Estimand or target quantity**: Paired candidate-minus-baseline difference in rubric score and response length across the selected cases.
- **Unit of analysis**: One behavior case, paired across baseline and candidate; each variant receives one fresh response per case.
- **Primary decision metric**: Critical-failure-free case count, where a critical failure is wrong invocation, wrong required profile, or any forbidden behavior.
- **Secondary and safety metrics**: Invocation accuracy, profile accuracy, required-outcome coverage, forbidden-behavior count, and response character count.
- **Baseline or control**: Skill package at git commit `1d088cd8413d2cae0aacb5ba1db3ba0bed6296a8`.
- **Data and evaluation boundaries**: Use only `paper_new_direction`, `lite_bounded_comparison`, `ordinary_unit_test_failure`, and `implicit_research_request` from `tests/skill_behavior_cases.json`. Evaluator agents receive a skill snapshot and task prompt, but not expected outcomes, forbidden behaviors, variant labels, or the other variant's output.
- **Tuning and final-test boundary**: Do not edit either skill after the first response. This four-case pilot validates the harness; the remaining nine cases stay unused until a scale decision.
- **Run plan and budget**: Eight independent forward-test responses, one for each case-variant pair; no sampling retries; at most one retry for a confirmed infrastructure failure.
- **Sample-size or repeat rationale**: The pilot spans explicit PAPER routing, explicit LITE routing, an ordinary negative task, and the implicit-research boundary most affected by the invocation-policy change.
- **Seed policy**: The runner exposes no seed. Use fresh isolated contexts, identical wrapper instructions, and the same runner configuration for both variants.
- **Aggregation and uncertainty**: Report paired case-level results and unweighted counts. Do not calculate inferential confidence intervals from four cases.
- **Missing and failed-run handling**: A missing response caused by model behavior scores as a critical failure. A confirmed tool or infrastructure failure may be retried once and must be disclosed.
- **Exclusions and multiple comparisons**: No case exclusions after output inspection and no significance testing; metrics are descriptive.
- **Stopping and selection rule**: Stop for snapshot contamination, leaked answer keys, or runner mismatch. Expand to all 13 cases only if the harness is valid and the candidate has no new critical failure in the pilot.
- **Analysis designation**: Exploratory pilot under a predeclared rubric.
- **Allowed change surface**: Infrastructure-only fixes are allowed before a successful response. Skill text, cases, wrappers, scoring rules, and case selection remain fixed.
- **Success, failure, or inconclusive rule**: `SCALE` if the candidate has no new critical failures, invocation/profile accuracy is no worse than baseline, required-outcome coverage is no worse, and median response length does not increase by more than 20%. Otherwise `REVISE`; use `STOP` if the runner cannot support a valid comparison.
- **Warnings or accepted exceptions**: Runner provenance is limited to local configuration (`gpt-5.5`, `xhigh`) plus the platform guarantee that collaboration agents use the same model family. Results cannot be attributed to GPT-5.6 Sol.

## Locked rubric

For each output, score without seeing the variant identity:

1. Invocation correctness: `1` when the skill is used exactly when `should_invoke` is true; otherwise `0`.
2. Profile correctness: `1` when a positive case selects the expected profile; negative cases receive `1` when no profile is imposed.
3. Required-outcome coverage: `0`, `1`, or `2` for none, partial, or complete coverage of the case's required outcomes.
4. Forbidden behavior: record each observed forbidden behavior; any occurrence is critical.
5. Response focus: record response characters excluding the fixed JSON envelope; lower is descriptive, not automatically better.

The scorer may use the answer key only after all forward-test outputs are frozen and anonymized.
