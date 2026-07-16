# Decision: exp-20260714-skill-ab-pilot

- **Action**: SCALE
- **Evidence**: `PILOT.md`, `analysis.md`, `results/summary.json`, `results/raw_outputs.json`, and `results/blind_scores.json`
- **Rationale**: The candidate passed the locked pilot rule and removed the tested implicit-invocation failure, while the LITE verbosity regression warrants broader measurement rather than immediate acceptance.
- **Destination**: Full 13-case A/B evaluation using the frozen snapshots
- **Artifact validity**: All pilot artifacts remain valid for the frozen snapshots and current runner limitation; none supports a GPT-5.6 Sol claim
- **Owner**: Codex
