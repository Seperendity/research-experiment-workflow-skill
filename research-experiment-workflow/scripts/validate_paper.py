#!/usr/bin/env python3
"""Read-only validation of paper evidence, bounded rounds and stage evaluations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

PHASES = {'PLANNING', 'EXPLORING', 'CONFIRMING', 'DRAFTING', 'REVIEWING', 'READY', 'STOPPED'}
STAGES = {'POSITION', 'NOVELTY', 'BASELINE', 'SCREEN', 'CONFIRM', 'ABLATE',
          'DRAFT', 'PEER_REVIEW', 'META_REVIEW', 'INTEGRITY'}
VERDICTS = {'ACCEPT', 'REFINE', 'REJECT', 'INCONCLUSIVE'}


def digest(value):
    """Canonical structured snapshot; stable across JSON whitespace/key ordering."""
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_digest(path):
    checksum = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(chunk)
    return checksum.hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


class PaperValidator:
    def __init__(self, project_root):
        self.root = Path(project_root).resolve()
        self.errors = []

    def check(self, condition, message):
        if not condition:
            self.errors.append(message)
        return bool(condition)

    def text(self, record, key, label):
        self.check(nonempty(record.get(key)), f'{label}.{key} must be non-empty text')

    def choice(self, record, key, options, label):
        value = record.get(key)
        self.check(isinstance(value, str) and value in options, f'{label}.{key} is invalid')

    def records(self, record, key):
        values = record.get(key)
        if not self.check(isinstance(values, list), f'{key} must be a list'):
            return {}
        indexed = {}
        for item in values:
            if not self.check(isinstance(item, dict), f'{key} entries must be objects'):
                continue
            identity = item.get('id')
            if not self.check(nonempty(identity), f'{key} entries require an id'):
                continue
            self.check(identity not in indexed, f'duplicate {key} id: {identity}')
            indexed[identity] = item
        return indexed

    def refs(self, value, targets, label):
        if not self.check(isinstance(value, list), f'{label} must be a list'):
            return []
        seen = set()
        valid = []
        for ref in value:
            if not self.check(isinstance(ref, str) and ref in targets, f'{label}: unknown reference {ref!r}'):
                continue
            self.check(ref not in seen, f'{label}: duplicate reference {ref}')
            seen.add(ref)
            valid.append(ref)
        return valid

    def path(self, value, label):
        if not self.check(nonempty(value), f'{label}: missing path'):
            return None
        raw = Path(value)
        path = (self.root / raw).resolve()
        if not self.check(not raw.is_absolute() and self.root in path.parents,
                          f'{label}: path escapes project root'):
            return None
        return path

    def acyclic(self, graph, label):
        visiting, done = set(), set()
        def visit(node):
            if node in visiting:
                self.errors.append(f'{label}: dependency cycle at {node}')
                return
            if node in done:
                return
            visiting.add(node)
            for child in graph.get(node, []):
                visit(child)
            visiting.remove(node)
            done.add(node)
        for node in graph:
            visit(node)

    def validate(self, paper):
        if not self.check(isinstance(paper, dict), 'paper must be an object'):
            return self.errors
        self.check(type(paper.get('schema_version')) is int and paper['schema_version'] == 1,
                   'paper schema_version must be 1')
        for field in ('paper_id', 'contribution_type', 'next_action'):
            self.text(paper, field, 'paper')
        self.choice(paper, 'phase', PHASES, 'paper')
        artifacts = self.records(paper, 'artifacts')
        claims = self.records(paper, 'claims')
        candidates = self.records(paper, 'candidates')
        rounds = self.records(paper, 'rounds')
        evaluations = self.records(paper, 'evaluations')
        issues = self.records(paper, 'issues')
        max_rounds = paper.get('max_rounds')
        self.check(type(max_rounds) is int and max_rounds >= 0, 'max_rounds must be a non-negative integer')
        if type(max_rounds) is int:
            self.check(len(rounds) <= max_rounds, 'round budget exceeded')

        max_evaluations = paper.get('max_evaluations')
        self.check(type(max_evaluations) is int and max_evaluations >= 0, 'max_evaluations must be a non-negative integer')
        if type(max_evaluations) is int:
            self.check(len(evaluations) <= max_evaluations, 'evaluation budget exceeded')

        current = self.validate_artifacts(artifacts)
        self.validate_claims(claims, artifacts, current)
        self.validate_candidates(candidates, artifacts)
        self.validate_rounds(rounds, candidates, artifacts, evaluations)
        self.validate_evaluations(evaluations, paper, rounds, candidates, artifacts, claims, current)
        self.validate_issues(issues, claims, artifacts, current)
        self.validate_readiness(paper, claims, issues, rounds, artifacts, evaluations, current)
        return self.errors

    def validate_artifacts(self, artifacts):
        graph, current = {}, {}
        for identity, item in artifacts.items():
            label = f'artifact {identity}'
            self.choice(item, 'status', {'CURRENT', 'STALE'}, label)
            self.text(item, 'role', label)
            dependencies = item.get('depends_on')
            if not self.check(isinstance(dependencies, dict), label + '.depends_on must be an object'):
                dependencies = {}
            graph[identity] = self.refs(list(dependencies), artifacts, label + '.depends_on')
            for ref in graph[identity]:
                self.check(isinstance(dependencies[ref], str) and re.fullmatch('[0-9a-f]{64}', dependencies[ref]) is not None,
                           label + ': invalid dependency fingerprint')
                if item.get('status') == 'CURRENT':
                    self.check(dependencies[ref] == artifacts[ref].get('sha256'), label + ': stale dependency snapshot ' + ref)
            fingerprint = item.get('sha256')
            self.check(isinstance(fingerprint, str) and re.fullmatch('[0-9a-f]{64}', fingerprint) is not None,
                       label + ': invalid sha256')
            path = self.path(item.get('path'), label)
            valid = False
            if item.get('status') == 'CURRENT' and path is not None:
                try:
                    valid = file_digest(path) == fingerprint
                    self.check(valid, label + ': fingerprint mismatch')
                except OSError as exc:
                    self.errors.append(f'{label}: cannot read file: {exc}')
            current[identity] = valid
        self.acyclic(graph, 'artifacts')
        # Propagate stale state without recursion so broken graphs still produce diagnostics.
        for _ in artifacts:
            for identity, dependencies in graph.items():
                if any(not current.get(dep, False) for dep in dependencies):
                    current[identity] = False
        for identity, item in artifacts.items():
            if item.get('status') == 'CURRENT':
                self.check(current[identity], f'artifact {identity}: stale evidence or dependency')

        return current

    def live_refs(self, value, artifacts, current, label):
        refs = self.refs(value, artifacts, label)
        for ref in refs:
            self.check(current.get(ref, False), f'{label}: stale evidence {ref}')
        return refs

    def validate_claims(self, claims, artifacts, current):
        for identity, item in claims.items():
            label = f'claim {identity}'
            for key in ('text', 'scope'):
                self.text(item, key, label)
            self.choice(item, 'status', {'PLANNED', 'EXPLORATORY', 'CONFIRMED', 'INCONCLUSIVE', 'REFUTED', 'WITHDRAWN'}, label)
            self.check(type(item.get('central')) is bool, label + '.central must be boolean')
            support = self.refs(item.get('support'), artifacts, label + '.support')
            self.refs(item.get('counterevidence'), artifacts, label + '.counterevidence')
            self.check(isinstance(item.get('gaps'), list) and all(nonempty(x) for x in item['gaps']), label + '.gaps must be a text list')
            if item.get('status') in ('CONFIRMED', 'EXPLORATORY'):
                self.check(bool(support), label + ': supported claim needs evidence')
                self.live_refs(item.get('support'), artifacts, current, label)
            if item.get('status') == 'WITHDRAWN':
                self.text(item, 'withdrawal_reason', label)

    def validate_candidates(self, candidates, artifacts):
        candidate_graph = {}
        for identity, item in candidates.items():
            label = f'candidate {identity}'
            candidate_graph[identity] = self.refs(item.get('parents'), candidates, label + '.parents')
            for key in ('hypothesis', 'prediction', 'falsification', 'selection_reason'):
                self.text(item, key, label)
            self.refs(item.get('evidence'), artifacts, label + '.evidence')
            self.choice(item, 'status', {'UNTESTED', 'ACTIVE', 'PROMISING', 'REJECTED', 'INCONCLUSIVE'}, label)
        self.acyclic(candidate_graph, 'candidates')

    def validate_rounds(self, rounds, candidates, artifacts, evaluations):
        all_trials = set()
        for identity, item in rounds.items():
            label = f'round {identity}'
            selected = self.refs(item.get('candidate_ids'), candidates, label + '.candidate_ids')
            self.check(bool(selected), label + ': select at least one candidate')
            self.text(item, 'allocation_reason', label)
            self.choice(item, 'status', {'PLANNED', 'RUNNING', 'DONE', 'STOPPED'}, label)
            trials = self.refs(item.get('trials'), artifacts, label + '.trials')
            self.check(not all_trials.intersection(trials), label + ': trial reused across rounds')
            all_trials.update(trials)
            limit = item.get('max_trials')
            self.check(type(limit) is int and limit > 0, label + ': max_trials must be positive integer')
            if type(limit) is int:
                self.check(len(trials) <= limit, label + ': trial budget exceeded')
            if item.get('status') in ('DONE', 'STOPPED'):
                self.choice(item, 'decision', {'ADVANCE', 'REVISE', 'STOP'}, label)
                self.text(item, 'decision_reason', label)
                if item.get('status') == 'STOPPED':
                    self.check(item.get('decision') == 'STOP', label + ': stopped round requires STOP')
                if item.get('status') == 'DONE':
                    self.check(bool(trials), label + ': completed screening round needs trial evidence')
                    if item.get('decision') == 'ADVANCE':
                        latest = {}
                        for evaluation in evaluations.values():
                            subject = evaluation.get('subject')
                            if evaluation.get('round_id') == identity and subject in selected and evaluation.get('stage') == 'SCREEN':
                                latest[subject] = evaluation
                        self.check(any(e.get('verdict') == 'ACCEPT' for e in latest.values()),
                                   label + ': ADVANCE requires accepted screening')
                    for candidate in selected:
                        self.check(any(e.get('round_id') == identity and e.get('subject') == candidate
                                       and e.get('stage') == 'SCREEN' and isinstance(e.get('inputs'), dict)
                                       and set(trials).intersection(e['inputs']) for e in evaluations.values()),
                                   label + f': missing screening evaluation for {candidate}')

    def validate_evaluations(self, evaluations, paper, rounds, candidates, artifacts, claims, current):
        current_evaluations = set()
        for identity, item in evaluations.items():
            label = f'evaluation {identity}'
            self.choice(item, 'stage', STAGES, label)
            self.choice(item, 'verdict', VERDICTS, label)
            self.choice(item, 'status', {'CURRENT', 'STALE'}, label)
            self.choice(item, 'independence', {'SELF', 'FRESH_CONTEXT', 'EXTERNAL'}, label)
            for key in ('reviewer', 'rationale', 'next_action'):
                self.text(item, key, label)
            subject = item.get('subject')
            self.check(isinstance(subject, str) and (subject == paper.get('paper_id') or subject in candidates), label + ': unknown subject')
            round_id = item.get('round_id')
            if round_id is not None:
                self.check(isinstance(round_id, str) and round_id in rounds, label + ': unknown round')
            if all(isinstance(value, str) for value in (item.get('stage'), subject)) and (round_id is None or isinstance(round_id, str)) and item.get('status') == 'CURRENT':
                key = (item['stage'], subject, round_id)
                self.check(key not in current_evaluations, label + ': competing current evaluations; archive superseded evaluation')
                current_evaluations.add(key)
            if item.get('stage') == 'SCREEN':
                self.check(isinstance(round_id, str) and round_id in rounds
                           and isinstance(rounds[round_id].get('candidate_ids'), list)
                           and subject in rounds[round_id]['candidate_ids'], label + ': screen subject must belong to round')
            for key, targets in (('inputs', artifacts), ('claims', claims)):
                snapshots = item.get(key)
                if not self.check(isinstance(snapshots, dict), label + f'.{key} must be an object'):
                    continue
                if key == 'inputs':
                    self.check(bool(snapshots), label + ': evaluation requires input evidence')
                for ref, fingerprint in snapshots.items():
                    if not self.check(ref in targets, label + f': unknown {key} reference {ref}'):
                        continue
                    self.check(isinstance(fingerprint, str) and re.fullmatch('[0-9a-f]{64}', fingerprint) is not None,
                               label + ': invalid snapshot fingerprint')
                    if item.get('status') == 'CURRENT':
                        expected = artifacts[ref].get('sha256') if key == 'inputs' else digest(claims[ref])
                        self.check(fingerprint == expected, label + ': stale snapshot ' + ref)
                        if key == 'inputs':
                            self.check(current.get(ref, False), label + ': stale input ' + ref)

    def validate_issues(self, issues, claims, artifacts, current):
        for identity, item in issues.items():
            label = f'issue {identity}'
            self.check(type(item.get('blocking')) is bool, label + '.blocking must be boolean')
            self.choice(item, 'status', {'OPEN', 'CLOSED'}, label)
            for key in ('task', 'budget'):
                self.text(item, key, label)
            self.refs(item.get('claim_ids'), claims, label + '.claim_ids')
            self.refs(item.get('closure_evidence'), artifacts, label + '.closure_evidence')
            if item.get('status') == 'CLOSED':
                self.text(item, 'resolution', label)
                self.check(bool(self.live_refs(item.get('closure_evidence'), artifacts, current, label)), label + ': closure requires evidence')

    def validate_readiness(self, paper, claims, issues, rounds, artifacts, evaluations, current):
        if paper.get('phase') == 'READY' and not self.errors:
            central = {key: claim for key, claim in claims.items() if claim.get('central') is True}
            self.check(bool(central), 'READY requires central claims')
            for identity, item in central.items():
                self.check(item.get('status') == 'CONFIRMED' and item.get('gaps') == [], 'READY: unresolved central claim ' + identity)
            self.check(not any(i.get('blocking') and i.get('status') != 'CLOSED' for i in issues.values()), 'READY: open blocking issue')
            self.check(not any(r.get('status') in {'PLANNED', 'RUNNING'} for r in rounds.values()), 'READY: unfinished research round')
            manuscripts = {key for key, value in artifacts.items() if value.get('role') == 'manuscript' and current.get(key)}
            self.check(bool(manuscripts), 'READY requires current manuscript')
            for stage in ('META_REVIEW', 'INTEGRITY'):
                self.check(any(e.get('stage') == stage and e.get('subject') == paper.get('paper_id')
                               and e.get('status') == 'CURRENT' and e.get('verdict') == 'ACCEPT'
                               and set(central).issubset(e.get('claims', {}))
                               and manuscripts.intersection(e.get('inputs', {}))
                               and all(set(c.get('support', [])).issubset(e.get('inputs', {})) for c in central.values())
                               for e in evaluations.values()
                               if isinstance(e.get('claims'), dict) and isinstance(e.get('inputs'), dict)),
                           'READY requires current ' + stage + ' covering manuscript and central claims/evidence')



def validate_paper(path, project_root):
    validator = PaperValidator(project_root)
    try:
        paper = json.loads(Path(path).read_text(encoding='utf-8'),
                           parse_constant=lambda value: (_ for _ in ()).throw(ValueError('non-finite JSON: ' + value)))
        return validator.validate(paper)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        return ['cannot validate paper: ' + str(exc)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paper', type=Path)
    parser.add_argument('--project-root', type=Path, required=True)
    args = parser.parse_args()
    errors = validate_paper(args.paper, args.project_root)
    for error in errors:
        print('ERROR:', error)
    print(f'Result: {len(errors)} error(s); scientific validity requires review')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
