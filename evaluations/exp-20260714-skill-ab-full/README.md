# exp-20260714-skill-ab-full

- **Hypothesis**: Candidate skill instructions improve routing efficiency without weakening evidence gates across the full behavior corpus.
- **Profile**: LITE
- **Intended claim scope**: Local engineering decision for the current skill revision and runner.
- **Change**: Add the nine cases held out by `exp-20260714-skill-ab-pilot` and pool all 13 cases without editing either snapshot.
- **Config base**: `tests/skill_behavior_cases.json`
- **Config overrides**: One fresh response for each remaining case and variant; blind scoring with the locked rubric.
- **Baseline**: Git commit `1d088cd8413d2cae0aacb5ba1db3ba0bed6296a8`
- **Budget**: 18 new forward-test responses; no sampling retries; one infrastructure retry if needed.
- **Status**: DONE — candidate passed; decision is `REPLICATE` on GPT-5.6 Sol
- **Owner**: Codex

Runner identity has the same limitation as the parent pilot: local config reports `gpt-5.5` with `xhigh` reasoning, while the collaboration surface does not expose a separate model identifier.
