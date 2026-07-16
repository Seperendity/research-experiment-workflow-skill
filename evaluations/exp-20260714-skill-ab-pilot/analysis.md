# Analysis Report: exp-20260714-skill-ab-pilot

- **Question**: Does the candidate improve routing and focus without weakening profile selection or evidence gates?
- **Analysis designation**: Exploratory pilot under a predeclared rubric
- **Unit of analysis**: Behavior case paired across baseline and candidate
- **Baseline comparison**: Candidate versus git commit `1d088cd`
- **Selection rule**: All four predeclared pilot cases; no exclusions
- **Aggregation and uncertainty**: Unweighted paired counts and response-character summaries; no inferential interval for four cases
- **Missing, failed, or excluded observations**: 0 / 0 / 0
- **Supported claims**: Candidate removed the tested implicit-invocation failure without introducing a critical failure in the other three pilot cases
- **Unsupported or inconclusive claims**: Overall quality across all 13 cases; stochastic stability; any claim about GPT-5.6 Sol
- **Warnings**: Candidate response length was heterogeneous and increased sharply on the LITE case

## Quantitative Summary

| Metric | Baseline | Candidate | Effect or delta |
|---|---:|---:|---:|
| Critical-failure-free cases | 3/4 | 4/4 | +1 case |
| Invocation accuracy | 3/4 | 4/4 | +25 percentage points |
| Profile accuracy | 3/4 | 4/4 | +25 percentage points |
| Required-outcome coverage | 5/8 | 8/8 | +3 rubric points |
| Forbidden behaviors | 2 | 0 | -2 |
| Mean response characters | 1307.00 | 1292.25 | -1.1% |
| Median response characters | 1084.00 | 1237.00 | +14.1% |

## Case-level interpretation

- `paper_new_direction`: Both versions selected PAPER and stopped before code or result-bearing work. The candidate more explicitly left novelty and feasibility behind future gates.
- `lite_bounded_comparison`: Both versions protected the protocol and pilot gates. The candidate was substantially more verbose (2481 versus 1318 characters), so concision is not yet demonstrated for this route.
- `ordinary_unit_test_failure`: Both versions correctly avoided the research workflow.
- `implicit_research_request`: Baseline implicitly selected STANDARD and expanded into a ten-step artifact-heavy workflow. Candidate did not invoke the Skill and still gave a useful ordinary experiment-design answer, reducing the response from 2841 to 1670 characters.

## Decision Input

- Recommended action: SCALE
- Evidence for recommendation: `PILOT.md`, `results/raw_outputs.json`, and `results/blind_scores.json`
- Scale focus: Run the remaining nine cases, preserve blind scoring, and add a targeted verbosity check for LITE and protocol-heavy prompts
