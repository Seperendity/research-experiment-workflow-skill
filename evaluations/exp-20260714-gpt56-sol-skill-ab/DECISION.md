# Decision: exp-20260714-gpt56-sol-skill-ab

- **Action**: REVISE
- **Evidence**: `analysis.md`, `results/summary.json`, `results/raw_outputs.json`, `results/blind_scores.json`, `results/scored_outputs.json`, and archived per-attempt outputs and logs
- **Rationale**: The candidate passes the locked non-inferiority and mean-length rule on GPT-5.6 Sol, but its GPT-5.5 implicit-invocation advantage did not replicate. Both variants injected the high-ceremony STANDARD workflow for a generic experiment-design request.
- **Revision boundary**: Change only trigger metadata and its tests. Do not add another planner, lifecycle layer, or meta-control mechanism.
- **Destination**: A repeated GPT-5.6 Sol trigger-only evaluation using both the current wrapper and a native-runtime invocation surface
- **Artifact validity**: These artifacts remain valid for the exact frozen snapshots, 13 prompts, GPT-5.6 Sol/medium runner, and stated single-scorer limitation
- **Owner**: Codex
