# Run Notes: exp-20260714-skill-ab-pilot

## Runner

- Local Codex config: `model = "gpt-5.5"`, `model_reasoning_effort = "xhigh"`.
- Forward-test runner: fresh Codex collaboration agents; the platform does not expose a separate model identifier.
- Sampling seed: unavailable.
- Infrastructure retries: 0.
- Raw outputs: `results/raw_outputs.json`.
- Blind scores: `results/blind_scores.json`.

## Frozen snapshots

| Variant | Neutral package | Source | `SKILL.md` SHA-256 | `agents/openai.yaml` SHA-256 |
|---|---|---|---|---|
| baseline | `pkg-amber` | `1d088cd8413d2cae0aacb5ba1db3ba0bed6296a8` | `7a1c5e8c4d7b501e1fc12fe62881180aa332fdc94c91d7d534407e6ac0ec977b` | `ddc9eb4498223b3e4270283caa7670e5269e010a2ff403266e959efe17b0cc18` |
| candidate | `pkg-cobalt` | current working-tree snapshot | `d896440b3b5252f9758302d7dd936bb36b80c87aa5b095b5576c2ce3bff6b1ae` | `f21d35ccf4426622887758ad9c7915ef8da2f1638a1f15c0010fe2cdecff5138` |

The scorer received anonymized IDs and did not receive the neutral-package mapping. The mapping was disclosed only after all eight outputs were frozen.

## Runs

| Case | Baseline output | Candidate output | Status |
|---|---|---|---|
| `paper_new_direction` | `paper-X2` | `paper-X1` | DONE |
| `lite_bounded_comparison` | `lite-X1` | `lite-X2` | DONE |
| `ordinary_unit_test_failure` | `unit-X2` | `unit-X1` | DONE |
| `implicit_research_request` | `implicit-X1` | `implicit-X2` | DONE |

## Decisions during execution

- No output was retried, excluded, or edited.
- No Skill text, wrapper, case, or scoring rule changed after the first response.
- The candidate's longer LITE response was retained and scored as observed.
