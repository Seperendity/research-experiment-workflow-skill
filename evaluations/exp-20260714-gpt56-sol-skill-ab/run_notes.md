# Run Notes

## Forward execution

- Date: 2026-07-15 UTC
- Model: `gpt-5.6-sol`
- Reasoning effort: `medium`
- Surface: `codex exec --ephemeral --ignore-user-config`
- Sandbox: read-only
- Sessions: 26 fresh case-variant sessions
- Concurrency: 2 for the harness pilot, then 3 for the remaining batch
- Valid outputs: 26/26
- Infrastructure retries: 0
- Model-behavior retries: 0
- Exclusions: 0

The `implicit_research_request` pair was used only as a structural harness pilot. Both outputs were valid on their first attempt and logs confirmed the locked model and reasoning effort. The other 24 runs then completed without retry. Every final JSON, attempt JSON, stdout log, stderr log, elapsed time, and exit code is retained under `results/forward_outputs/` and `results/logs/`.

## Snapshot provenance

| Snapshot | File | SHA-256 |
|---|---|---|
| Baseline | `SKILL.md` | `7a1c5e8c4d7b501e1fc12fe62881180aa332fdc94c91d7d534407e6ac0ec977b` |
| Baseline | `agents/openai.yaml` | `ddc9eb4498223b3e4270283caa7670e5269e010a2ff403266e959efe17b0cc18` |
| Candidate | `SKILL.md` | `d896440b3b5252f9758302d7dd936bb36b80c87aa5b095b5576c2ce3bff6b1ae` |
| Candidate | `agents/openai.yaml` | `f21d35ccf4426622887758ad9c7915ef8da2f1638a1f15c0010fe2cdecff5138` |

The baseline was checked out at `1d088cd8413d2cae0aacb5ba1db3ba0bed6296a8`. Neutral package names were `pkg-amber` and `pkg-cobalt`. Neither temporary package contained behavior-test answer keys or earlier evaluation artifacts.

## Scoring deviation

Three independent external GPT-5.6 Sol blind scorers were prepared. Execution was rejected before any scorer call ran because sending the frozen workspace cases and model outputs to the external scoring service was classified as prohibited workspace-data export, including after explicit user authorization. No scorer output or retry was produced.

The materially safer fallback was one local manual audit of the anonymous packet. Variant mapping was revealed only after `results/blind_scores.json` was frozen. Invocation and profile correctness follow directly from the structured output fields; required-outcome coverage and forbidden behavior were judged against the locked answer key. This deviation is recorded as a limitation and prevents claiming independent-scorer agreement.
