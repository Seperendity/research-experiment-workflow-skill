from __future__ import annotations

import importlib.util
import json
import tempfile
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    REPO_ROOT
    / "research-experiment-workflow"
    / "scripts"
    / "validate_experiment.py"
)
SPEC = importlib.util.spec_from_file_location("validate_experiment", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


class ValidateExperimentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.experiment_dir = Path(self.temp_dir.name) / "exp-20260710-example"
        self.experiment_dir.mkdir()

        for artifact in (
            "NOVELTY.md",
            "FEASIBILITY.md",
            "PROTOCOL.md",
            "PILOT.md",
            "REVIEW.md",
            "analysis.md",
            "DECISION.md",
            "DEBUG.md",
            "ABLATION_PLAN.md",
        ):
            (self.experiment_dir / artifact).write_text(
                f"# {artifact}\n", encoding="utf-8"
            )

        self.manifest = {
            "schema_version": 2,
            "experiment_id": "exp-20260710-example",
            "hypothesis_id": "H-001",
            "stage": "DECISION",
            "status": "DONE",
            "parent_experiment_id": None,
            "gates": {
                name: {
                    "verdict": "PASS",
                    "artifact": artifact,
                    "accepted_warning": False,
                }
                for name, artifact in {
                    "novelty": "NOVELTY.md",
                    "feasibility": "FEASIBILITY.md",
                    "protocol": "PROTOCOL.md",
                    "pilot": "PILOT.md",
                    "review": "REVIEW.md",
                }.items()
            },
            "artifacts": {
                "summary": "results/summary.json",
                "analysis": "analysis.md",
                "decision": "DECISION.md",
                "debug": "DEBUG.md",
                "ablation": "ABLATION_PLAN.md",
            },
            "warnings": [],
        }
        self.summary = {
            "schema_version": 2,
            "experiment_id": "exp-20260710-example",
            "hypothesis_id": "H-001",
            "status": "DONE",
            "protocol": "PROTOCOL.md",
            "primary_metric": {"name": "score", "direction": "maximize"},
            "config_base": "baseline",
            "config_overrides": {},
            "runs": [
                {
                    "run_id": "run_0",
                    "seed": 0,
                    "status": "DONE",
                    "config": {},
                    "metrics": {"score": 1.0},
                    "artifacts": {},
                    "warnings": [],
                }
            ],
            "aggregate": {
                "n_planned": 1,
                "n_completed": 1,
                "metrics": {"score": {"mean": 1.0}},
            },
            "baseline": {
                "experiment_id": "exp-20260701-baseline",
                "source": "saved baseline artifact",
                "metrics": {"score": 0.5},
            },
            "delta_vs_baseline": {"score": 0.5},
            "provenance": {
                "git_commit": "abc123",
                "data_version": "v1",
                "environment": "env.lock",
            },
            "artifacts": {},
            "budget": {
                "max_runs": 1,
                "timeout": 60,
                "retries_used": 0,
                "stop_reason": "completed",
            },
            "warnings": [],
        }
        self._write_current()

    def _write_current(self) -> None:
        _write_json(self.experiment_dir / "experiment.json", self.manifest)
        _write_json(
            self.experiment_dir / "results" / "summary.json",
            self.summary,
        )

    def _validate(self):
        self._write_current()
        return VALIDATOR.validate_experiment(self.experiment_dir)

    def test_complete_v2_experiment_passes_strict_validation(self) -> None:
        result = self._validate()
        self.assertEqual([], result.errors)
        self.assertEqual([], result.warnings)
        self.assertEqual(0, result.exit_code(strict=True))

    def test_legacy_summary_warns_but_passes_compatibility_mode(self) -> None:
        legacy_dir = Path(self.temp_dir.name) / "legacy"
        _write_json(
            legacy_dir / "results" / "summary.json",
            {
                "experiment_id": "legacy",
                "status": "DONE",
                "seed": 0,
                "metrics": {"score": 1.0},
            },
        )

        result = VALIDATOR.validate_experiment(legacy_dir)

        self.assertEqual([], result.errors)
        self.assertGreaterEqual(len(result.warnings), 2)
        self.assertEqual(0, result.exit_code(strict=False))
        self.assertEqual(1, result.exit_code(strict=True))

    def test_missing_passed_gate_artifact_fails(self) -> None:
        (self.experiment_dir / "PROTOCOL.md").unlink()

        result = self._validate()

        self.assertTrue(
            any("gate 'protocol' artifact does not exist" in item for item in result.errors)
        )

    def test_manifest_and_summary_identity_must_match(self) -> None:
        self.summary["experiment_id"] = "exp-other"
        self.summary["hypothesis_id"] = "H-other"

        result = self._validate()

        self.assertIn("manifest and summary experiment_id values differ", result.errors)
        self.assertIn("manifest and summary hypothesis_id values differ", result.errors)

    def test_manifest_requires_parent_field_and_relative_gate_paths(self) -> None:
        del self.manifest["parent_experiment_id"]
        self.manifest["stage"] = "IDEA"
        self.manifest["status"] = "PLANNED"
        self.manifest["gates"]["novelty"] = {
            "verdict": "PENDING",
            "artifact": str(self.experiment_dir / "NOVELTY.md"),
            "accepted_warning": False,
        }

        result = self._validate()

        self.assertIn(
            "experiment.json is missing required field 'parent_experiment_id'",
            result.errors,
        )
        self.assertTrue(
            any("gate 'novelty' artifact must be a relative path" in item for item in result.errors)
        )

    def test_summary_protocol_must_exist_and_match_manifest(self) -> None:
        self.summary["protocol"] = "OTHER_PROTOCOL.md"
        (self.experiment_dir / "OTHER_PROTOCOL.md").write_text(
            "# Other protocol\n", encoding="utf-8"
        )

        result = self._validate()

        self.assertIn("manifest and summary protocol paths differ", result.errors)

    def test_interrupted_blocked_and_invalidated_states_are_recognized(self) -> None:
        for status in ("INTERRUPTED", "BLOCKED", "INVALIDATED"):
            with self.subTest(status=status):
                self.manifest["stage"] = "DEBUG"
                self.manifest["status"] = status
                result = self._validate()
                self.assertEqual([], result.errors)

    def test_debug_and_ablation_branch_artifacts_are_required(self) -> None:
        self.manifest["stage"] = "DEBUG"
        (self.experiment_dir / "DEBUG.md").unlink()
        result = self._validate()
        self.assertTrue(any("artifact 'debug' does not exist" in item for item in result.errors))

        (self.experiment_dir / "DEBUG.md").write_text("# Debug\n", encoding="utf-8")
        self.manifest["stage"] = "ABLATION"
        (self.experiment_dir / "ABLATION_PLAN.md").unlink()
        result = self._validate()
        self.assertTrue(
            any("artifact 'ablation' does not exist" in item for item in result.errors)
        )

    def test_decision_artifact_is_required_at_decision_stage(self) -> None:
        (self.experiment_dir / "DECISION.md").unlink()

        result = self._validate()

        self.assertTrue(
            any("artifact 'decision' does not exist" in item for item in result.errors)
        )

    def test_gate_warning_requires_acceptance(self) -> None:
        self.manifest["gates"]["protocol"]["verdict"] = "WARNING"
        result = self._validate()
        self.assertTrue(
            any("gate 'protocol' warning has not been accepted" in item for item in result.errors)
        )

        self.manifest["gates"]["protocol"]["accepted_warning"] = True
        result = self._validate()
        self.assertEqual([], result.errors)
        self.assertIn("gate 'protocol' contains an accepted warning", result.warnings)
        self.assertEqual(1, result.exit_code(strict=True))


if __name__ == "__main__":
    unittest.main()
