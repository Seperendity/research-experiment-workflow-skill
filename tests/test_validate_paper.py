from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'research-experiment-workflow/scripts/validate_paper.py'
SPEC = importlib.util.spec_from_file_location('validate_paper', SCRIPT)
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


class PaperValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / 'paper.json'
        self.paper = dict(schema_version=1, paper_id='P1', phase='PLANNING',
                          contribution_type='empirical', next_action='Diagnose baseline',
                          max_rounds=2, max_evaluations=20, artifacts=[], claims=[], candidates=[], rounds=[],
                          evaluations=[], issues=[])

    def artifact(self, identity, role='analysis', dependencies=None):
        path = self.root / (identity + '.txt')
        path.write_text('Observed evidence: ' + identity)
        item = dict(id=identity, role=role, path=path.name, sha256=V.file_digest(path),
                    status='CURRENT', depends_on=dependencies or {})
        self.paper['artifacts'].append(item)
        return item

    def ready(self):
        source = self.artifact('raw', 'results')
        analysis = self.artifact('analysis', dependencies={'raw': source['sha256']})
        manuscript = self.artifact('draft', 'manuscript')
        claim = dict(id='C1', text='Bounded observed improvement', scope='Locked benchmark',
                     central=True, status='CONFIRMED', support=['analysis'], counterevidence=[], gaps=[])
        self.paper['claims'] = [claim]
        for stage in ('META_REVIEW', 'INTEGRITY'):
            self.paper['evaluations'].append(dict(id=stage, stage=stage, subject='P1', round_id=None,
                status='CURRENT', verdict='ACCEPT', reviewer='reviewer', independence='EXTERNAL',
                inputs={a['id']: a['sha256'] for a in (analysis, manuscript)},
                claims={'C1': V.digest(claim)}, rationale='Checked evidence and scope', next_action='Ready'))
        self.paper['phase'] = 'READY'

    def errors(self):
        self.path.write_text(json.dumps(self.paper))
        return V.validate_paper(self.path, self.root)

    def assert_error(self, text):
        self.assertTrue(any(text in e for e in self.errors()), self.errors())

    def test_planning_needs_no_future_evidence(self):
        self.assertEqual([], self.errors())

    def test_ready_valid_package_and_read_only_cli(self):
        self.ready()
        self.assertEqual([], self.errors())
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        run = subprocess.run([sys.executable, str(SCRIPT), str(self.path), '--project-root', str(self.root)],
                             capture_output=True, text=True)
        self.assertEqual(0, run.returncode, run.stdout + run.stderr)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_modified_source_invalidates_derived_support(self):
        self.ready()
        (self.root / 'raw.txt').write_text('changed results')
        self.assert_error('stale evidence')

    def test_refreshing_source_hash_does_not_refresh_derivation(self):
        self.ready()
        (self.root / 'raw.txt').write_text('changed results')
        self.paper['artifacts'][0]['sha256'] = V.file_digest(self.root / 'raw.txt')
        self.assert_error('stale dependency snapshot')

    def test_changed_claim_invalidates_review(self):
        self.ready()
        self.paper['claims'][0]['scope'] = 'All tasks'
        self.assert_error('stale snapshot C1')

    def test_changed_manuscript_invalidates_review(self):
        self.ready()
        (self.root / 'draft.txt').write_text('new version')
        self.paper['artifacts'][2]['sha256'] = V.file_digest(self.root / 'draft.txt')
        self.assert_error('stale snapshot draft')

    def test_ready_needs_both_reviews(self):
        self.ready()
        self.paper['evaluations'].pop()
        self.assert_error('current INTEGRITY')

    def test_open_blocker_blocks_ready(self):
        self.ready()
        self.paper['issues'] = [dict(id='I1', blocking=True, status='OPEN', task='Check control',
                                    budget='one trial', claim_ids=['C1'], closure_evidence=[])]
        self.assert_error('open blocking issue')

    def test_closed_issue_needs_current_closure_evidence(self):
        self.ready()
        self.paper['issues'] = [dict(id='I1', blocking=True, status='CLOSED', task='Check control',
                budget='one trial', claim_ids=['C1'], resolution='Addressed', closure_evidence=[])]
        self.assert_error('closure requires evidence')

    def test_archived_missing_evidence_allowed_but_not_support(self):
        self.ready()
        old = self.artifact('old')
        old['status'] = 'STALE'
        (self.root / 'old.txt').unlink()
        self.assertEqual([], self.errors())
        self.paper['claims'][0]['support'].append('old')
        self.assert_error('stale evidence old')

    def test_paths_cannot_escape_project_including_symlinks(self):
        self.artifact('A')
        self.paper['artifacts'][0]['path'] = '../outside'
        self.assert_error('escapes project')
        with tempfile.TemporaryDirectory() as other:
            (self.root / 'link').symlink_to(other, target_is_directory=True)
            self.paper['artifacts'][0]['path'] = 'link/outside'
            self.assert_error('escapes project')

    def test_duplicate_identity_and_cycles_fail(self):
        item = self.artifact('A')
        self.paper['artifacts'].append(copy.deepcopy(item))
        self.assert_error('duplicate artifacts id')
        self.paper['artifacts'].pop()
        item['depends_on'] = {'A': item['sha256']}
        self.assert_error('dependency cycle')

    def round(self):
        trial = self.artifact('trial')
        self.paper['phase'] = 'EXPLORING'
        self.paper['candidates'] = [dict(id='H1', parents=[], hypothesis='Mechanism', prediction='A change',
            falsification='No predicted effect', selection_reason='Observed bottleneck', evidence=[], status='ACTIVE')]
        self.paper['rounds'] = [dict(id='R1', candidate_ids=['H1'], allocation_reason='First seed',
            max_trials=1, trials=['trial'], status='DONE', decision='REVISE', decision_reason='Needs control')]
        self.paper['evaluations'] = [dict(id='E1', stage='SCREEN', subject='H1', round_id='R1',
            status='CURRENT', verdict='REFINE', reviewer='scientist', independence='SELF',
            inputs={'trial': trial['sha256']}, claims={}, rationale='Alternative explanation', next_action='Run control')]

    def test_complete_round_and_resume(self):
        self.round()
        self.assertEqual([], self.errors())
        self.paper['rounds'][0]['status'] = 'RUNNING'
        self.paper['evaluations'] = []
        self.assertEqual([], self.errors())

    def test_finished_round_requires_each_candidate_evaluation(self):
        self.round()
        self.paper['evaluations'] = []
        self.assert_error('missing screening evaluation')

    def test_trial_and_round_budgets(self):
        self.round()
        self.artifact('failed_trial')
        self.paper['rounds'][0]['trials'].append('failed_trial')
        self.assert_error('trial budget exceeded')
        self.paper['max_rounds'] = 0
        self.assert_error('round budget exceeded')

    def test_round_cannot_advance_without_acceptance(self):
        self.round()
        self.paper['rounds'][0]['decision'] = 'ADVANCE'
        self.assert_error('ADVANCE requires accepted screening')
        self.paper['evaluations'][0]['verdict'] = 'ACCEPT'
        self.assertEqual([], self.errors())

    def test_evaluation_budget_includes_archived_rounds(self):
        self.ready()
        self.paper['max_evaluations'] = 1
        self.assert_error('evaluation budget exceeded')

    def test_new_rejection_cannot_hide_behind_old_acceptance(self):
        self.ready()
        rejected = copy.deepcopy(self.paper['evaluations'][0])
        rejected.update(id='new_review', verdict='REJECT')
        self.paper['evaluations'].append(rejected)
        self.assert_error('competing current evaluations')
        self.paper['evaluations'][0]['status'] = 'STALE'
        self.assert_error('current META_REVIEW')

    def test_malformed_boundaries_return_errors(self):
        for field, value in [('claims', None), ('max_rounds', True), ('artifacts', [None]),
                             ('phase', []), ('rounds', [{}])]:
            with self.subTest(field=field):
                saved = copy.deepcopy(self.paper)
                self.paper[field] = value
                self.assertTrue(self.errors())
                self.paper = saved

    def test_malformed_record_fields_never_raise(self):
        self.round()
        self.paper['claims'] = [dict(id='C', text='Claim', scope='Scope', central=False,
            status='PLANNED', support=[], counterevidence=[], gaps=[])]
        self.paper['issues'] = [dict(id='I', blocking=True, status='OPEN', task='Review',
            budget='one run', claim_ids=['C'], closure_evidence=[])]
        baseline = copy.deepcopy(self.paper)
        for collection in ('artifacts', 'claims', 'candidates', 'rounds', 'evaluations', 'issues'):
            for key in baseline[collection][0]:
                for value in (None, {}, [], True, 42):
                    with self.subTest(collection=collection, key=key, value=value):
                        self.paper = copy.deepcopy(baseline)
                        self.paper[collection][0][key] = value
                        self.errors()

    def test_unknown_reference_and_nonfinite_json(self):
        self.ready()
        self.paper['claims'][0]['support'] = ['missing']
        self.assert_error('unknown reference')
        self.path.write_text('{"schema_version": NaN}')
        self.assertIn('non-finite', V.validate_paper(self.path, self.root)[0])


if __name__ == '__main__':
    unittest.main()
