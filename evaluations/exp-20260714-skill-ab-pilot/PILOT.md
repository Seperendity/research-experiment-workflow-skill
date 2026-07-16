# Pilot Report: exp-20260714-skill-ab-pilot

- **Status**: PASS
- **Config**: `PROTOCOL.md` and `tests/skill_behavior_cases.json`
- **Build**: PASS
- **Shape or interface check**: PASS
- **Metric or loss health**: All eight responses parsed into the locked scoring fields
- **Artifact check**: PASS
- **Warnings**: Runner identity is not exposed independently; this is not a GPT-5.6 Sol result

## Checks

- [x] Both Skill snapshots were frozen and hashed
- [x] Candidate snapshot excluded behavior-case answer keys
- [x] Every case-variant pair ran in a fresh context
- [x] All eight outputs used the required JSON envelope
- [x] The scorer saw anonymized outputs and the locked rubric only
- [x] No output was retried or excluded
- [x] Raw outputs and blind scores were saved
- [x] The locked protocol still applies

The candidate met the predeclared scale rule: no new critical failures, no regression in invocation/profile accuracy or outcome coverage, and median response length increased by 14.1%, below the 20% ceiling.
