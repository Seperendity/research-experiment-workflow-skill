# Protocol

- **Status**: LOCKED
- **Primary metric**: `score`, maximize
- **Unit of analysis**: evaluation item
- **Baseline**: `baseline-run`
- **Evaluation boundary**: frozen `fixture-v1` evaluation set
- **Decision rule**: prefer the candidate only when its paired mean score is higher without missing runs
- **Run budget**: one baseline and one candidate run; no retry
