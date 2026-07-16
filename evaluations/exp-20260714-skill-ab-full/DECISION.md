# Decision: exp-20260714-skill-ab-full

- **Action**: REPLICATE
- **Evidence**: `analysis.md`, `results/summary.json`, `results/heldout_raw_outputs.json`, `results/heldout_blind_scores.json`, and the parent pilot artifacts
- **Rationale**: The candidate passes the locked full-corpus rule on the current runner and is preferred to baseline, but the user-relevant GPT-5.6 Sol claim and stochastic stability remain untested.
- **Destination**: A GPT-5.6 Sol replication with corrected fixtures and repeated samples
- **Artifact validity**: Current A/B artifacts remain valid only for the frozen snapshots, prompts, scorer rubric, and runner limitations stated in the protocol
- **Owner**: Codex
