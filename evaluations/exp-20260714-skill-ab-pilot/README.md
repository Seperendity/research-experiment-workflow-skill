# exp-20260714-skill-ab-pilot

- **Hypothesis**: Candidate skill instructions improve routing efficiency without weakening evidence gates.
- **Profile**: LITE
- **Intended claim scope**: Local engineering decision about whether to continue the A/B evaluation.
- **Change**: Compare git baseline `1d088cd` with the current uncommitted skill package.
- **Config base**: `tests/skill_behavior_cases.json`
- **Config overrides**: Four-case stratified pilot; one fresh response per case and variant.
- **Baseline**: Git commit `1d088cd8413d2cae0aacb5ba1db3ba0bed6296a8`
- **Budget**: 8 forward-test responses, no sampling retries, one infrastructure retry if needed.
- **Status**: DONE — pilot passed; decision is `SCALE`
- **Owner**: Codex

The local Codex configuration reports `gpt-5.5` with `xhigh` reasoning. The collaboration runner does not expose a separate model identifier, so this pilot must not be reported as a GPT-5.6 Sol evaluation.
