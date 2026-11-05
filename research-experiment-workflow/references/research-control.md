# Research Control Record, Version 1

Load when coordinating a bounded research iteration or paper across experiments. This contract owns `paper.json`; `artifact-contract.md` continues to own experiment manifests. Do not require this record for LITE work or a single bounded experiment.

## Authorized unit of work

If asked for one artifact, stop at that artifact. If asked to complete a research iteration, continue through the authorized selection, engineering pilot, development screening, analysis and decision without stopping merely because a file is finished. Respect existing gates, resource authorization and the requested endpoint. Exhausted budgets, missing required evidence or unaccepted warnings stop dependent work; save the resume state and immediate next action.

## Shared stage evaluation

Every stage evaluation records the candidate/artifact examined, reviewer and context independence, frozen input fingerprints, verdict, evidence-based rationale and immediate next action. Use ACCEPT, REFINE, REJECT or INCONCLUSIVE; these are research decisions, not replacements for experiment PASS/WARNING/FAIL gates. ACCEPT never bypasses a required experiment gate.

| Stage | Acceptance question | REFINE route |
|---|---|---|
| POSITION | Does observed evidence establish a meaningful bottleneck and contribution target? | Reframe question or collect diagnostic evidence |
| NOVELTY | Is the distinction defensible against close prior work? | Search or narrow the contribution |
| BASELINE | Is the reproduced comparison trustworthy under the shared protocol? | Fix reproduction or resolve mismatch |
| SCREEN | Is development evidence sufficient for the predeclared promotion rule? | Diagnose, revise candidate, or obtain discriminating evidence |
| CONFIRM | Does frozen evaluation support the selected claim? | Narrow claims or return to development with fresh confirmation boundaries |
| ABLATE | Do controls distinguish the proposed explanation from alternatives? | Simplify method or revise explanation, then repeat affected validation |
| DRAFT | Does the manuscript accurately describe the evidence and implementation? | Revise text, figures or claim scope |
| PEER_REVIEW | Have concrete scientific and presentation concerns been identified/addressed? | Route each concern to an issue/task |
| META_REVIEW | Does the contribution remain defensible as a whole? | Reposition, revise method, or request decisive evidence |
| INTEGRITY | Are key results reproducible, evaluation rules respected, citations supported and method/code aligned? | Repair the affected artifacts and re-review |

Use only applicable stages. Theory may substitute proof checks for empirical controls; explain applicability in the evaluation rationale. Meta-review is a strategic assessment, not an average reviewer score. Its ACCEPT is an internal readiness judgment, not a conference decision. Same-context evaluation stays SELF.

## Candidate rounds

Before running a round, select candidates, record the mix of evolved and untested ideas (or why only one category is appropriate), define project-specific promotion/revision/rejection/inconclusive criteria and reserve trial/evaluation budgets. Reference that plan as an evaluation input. Criteria cover meaningful effect, uncertainty, relevant secondary metrics, cost and proxy validity; never invent universal thresholds.

Record every launched trial, including failures/retries, as a unique artifact ID with its log or result path. A round completes after each selected candidate has a SCREEN evaluation and a decision. ADVANCE needs accepted screening; REVISE starts a new bounded round; STOP preserves lessons. Implementation failure does not refute a hypothesis. Do not promote a candidate from engineering pilot success alone.

Use immutable candidate IDs for materially changed hypotheses; link parents and evidence from successful and failed attempts. Avoid repeatedly optimizing one early winner without considering remaining alternatives. Select the best defensible candidate using the predeclared multi-metric rule, not a newly chosen favorable metric.

The round record preserves a historical decision; it is not authorization to reuse stale evidence. After interruptions resume RUNNING rounds and reuse completed trials. Do not reset counters by deleting history. Scientific refinement must retain tuning/final-test separation. New budget authorization is recorded in project notes before increasing caps.

## Minimal paper.json

Use `research/papers/<paper-id>/paper.json` or a project-equivalent location. Existing unversioned notes remain historical notes; migrate explicitly without inventing provenance. All artifact paths below are relative to the explicit project root supplied to the validator, including paths to experiments outside the paper directory. Absolute paths and symlink escapes are rejected. The paper record must not fingerprint itself.

```json
{
  "schema_version": 1,
  "paper_id": "P-001",
  "phase": "PLANNING",
  "contribution_type": "empirical method",
  "next_action": "Diagnose the baseline failure conditions",
  "max_rounds": 2,
  "max_evaluations": 20,
  "artifacts": [],
  "claims": [],
  "candidates": [],
  "rounds": [],
  "evaluations": [],
  "issues": []
}
```

Caps are project choices, not defaults imposed by the skill. `max_rounds` counts all retained candidate rounds; `max_evaluations` counts all retained evaluations, including superseded ones. These caps do not measure GPU hours or money; record and monitor those through project job logs. Do not precreate future-stage files.

Each array has unique non-empty string `id` values. References use these IDs, not free-text names. Fields below are required unless stated otherwise; empty collections are allowed unless a gate requires evidence.

| Record | Fields |
|---|---|
| Artifact | `id`, `path`, `role` (e.g. protocol, code_snapshot, data_manifest, results, analysis, manuscript), `status` CURRENT/STALE, `sha256`, `depends_on` mapping artifact IDs to their SHA-256 at derivation time |
| Claim | `id`, `text`, `scope`, `central` boolean, `status` PLANNED/EXPLORATORY/CONFIRMED/INCONCLUSIVE/REFUTED/WITHDRAWN, `support` artifact IDs, `counterevidence` artifact IDs, `gaps` text list; WITHDRAWN also requires `withdrawal_reason` |
| Candidate | `id`, `parents` candidate IDs, `hypothesis`, `prediction`, `falsification`, `selection_reason`, `evidence` artifact IDs, `status` UNTESTED/ACTIVE/PROMISING/REJECTED/INCONCLUSIVE |
| Round | `id`, `candidate_ids`, `allocation_reason`, `max_trials` positive integer, `trials` artifact IDs, `status` PLANNED/RUNNING/DONE/STOPPED; DONE/STOPPED also require `decision` ADVANCE/REVISE/STOP and `decision_reason` |
| Evaluation | `id`, `stage` from stage table, `subject` candidate ID or paper ID, `round_id` (null outside a candidate round), `status` CURRENT/STALE, `verdict`, `reviewer`, `independence` SELF/FRESH_CONTEXT/EXTERNAL, `inputs` artifact-ID-to-SHA-256 mapping, `claims` claim-ID-to-canonical-SHA-256 mapping, `rationale`, `next_action` |
| Issue | `id`, `blocking` boolean, `status` OPEN/CLOSED, `task`, `budget` text, `claim_ids`, `closure_evidence` artifact IDs; CLOSED also requires `resolution` |

When using this control record, `candidates` is authoritative for active candidate lineage; an existing ideas.json may remain an unselected backlog. Do not maintain competing copies of candidate state.

Artifacts and candidate parents must be acyclic. A CURRENT artifact must exist, match its bytes fingerprint, and depend on current artifacts with matching derivation-time fingerprints. STALE history may refer to unavailable files but cannot support confirmed/exploratory claims or close issues. Mark affected claims INCONCLUSIVE or WITHDRAWN until revalidated. Retain counterevidence and explain its interpretation in the analysis; the validator cannot decide whether it defeats a claim.

For large data/code collections, fingerprint a reproducible manifest listing immutable versions or content checksums; include uncommitted code changes. The validator hashes that manifest, not every referenced external object. Verify external data identity separately. Do not silently refresh digests to hide changes.

## Fingerprints and evaluations

File fingerprints use SHA-256 of file bytes. Claim snapshots use the helper `digest(claim)` in `scripts/validate_paper.py`: SHA-256 of UTF-8 JSON with sorted keys, ensure_ascii=False, separators=(',', ':'), and no non-finite values. Capture snapshots when reviewing, never retrospectively refresh an old signature. Example generation using the standard library:

```python
import hashlib, json
file_sha = hashlib.sha256(path.read_bytes()).hexdigest()
claim_sha = hashlib.sha256(json.dumps(
    claim, sort_keys=True, ensure_ascii=False,
    separators=(',', ':'), allow_nan=False
).encode('utf-8')).hexdigest()
```

An evaluation needs at least one input artifact. SCREEN must reference its round and selected candidate; completed rounds require screening evidence drawn from their recorded trials. Preserve superseded evaluations as STALE; only one CURRENT evaluation per stage/subject/round is allowed. Refreshing a source hash does not refresh dependent analyses or reviews. A changed manuscript or claim requires review of that version.

## Phase routing and readiness

PLANNING → EXPLORING → CONFIRMING → DRAFTING → REVIEWING → READY is a usual route, not a mandatory linear sequence. Drafting may overlap development when unobserved evidence is labeled. Method-changing feedback returns to EXPLORING; supplementary confirmation returns to CONFIRMING; budget exhaustion can enter STOPPED. Review the latest valid artifacts when choosing a phase. The validator checks current consistency and READY conditions, not historical authorization or all possible phase transitions.

READY requires at least one central claim; every central claim must be CONFIRMED with no open gaps. There must be a current manuscript, no unfinished candidate rounds and no open blocking issues. Current ACCEPT evaluations for both META_REVIEW and INTEGRITY must cover the current manuscript, every central claim snapshot and its direct supporting artifacts. Transitive source validity is checked through dependencies. A readiness pass certifies record consistency, not scientific truth, actual reviewer independence, adequate study power or publication acceptance.

Run `python <skill-dir>/scripts/validate_paper.py <paper.json> --project-root <project-root>` after updating the paper control record or its evidence and before reporting readiness. Also run the existing experiment validator with `--strict` on each changed or relied-upon experiment package; paper validation does not replace experiment validation or reproduce experiments. Both commands are read-only. Do not label a failing package ready; report diagnostics and the repair action.
