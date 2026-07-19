from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = Path(__file__).with_name("skill_behavior_cases.json")
SKILL_PATH = REPO_ROOT / "research-experiment-workflow" / "SKILL.md"
README_PATH = REPO_ROOT / "README.md"
README_ZH_PATH = REPO_ROOT / "README.zh-CN.md"
OPENAI_YAML_PATH = (
    REPO_ROOT / "research-experiment-workflow" / "agents" / "openai.yaml"
)
VALIDATOR_PATH = (
    REPO_ROOT
    / "research-experiment-workflow"
    / "scripts"
    / "validate_experiment.py"
)
VALID_PROFILES = {"LITE", "STANDARD", "PAPER", "LEGACY_AUDIT"}
REQUIRED_CASE_FIELDS = {
    "id",
    "prompt",
    "should_invoke",
    "expected_profile",
    "required_outcomes",
    "forbidden_behaviors",
}
OPTIONAL_CASE_FIELDS = {"workspace_fixture"}


class SkillBehaviorCasesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    def test_case_file_has_current_shape(self) -> None:
        self.assertEqual(2, self.payload.get("schema_version"))
        self.assertRegex(self.payload.get("baseline_ref", ""), r"^[0-9a-f]{7,40}$")
        self.assertIsInstance(self.payload.get("cases"), list)
        self.assertGreaterEqual(len(self.payload["cases"]), 12)

    def test_cases_are_unique_and_well_formed(self) -> None:
        case_ids: set[str] = set()
        for case in self.payload["cases"]:
            with self.subTest(case=case.get("id")):
                fields = set(case)
                self.assertTrue(REQUIRED_CASE_FIELDS <= fields)
                self.assertTrue(fields <= REQUIRED_CASE_FIELDS | OPTIONAL_CASE_FIELDS)
                self.assertIsInstance(case["id"], str)
                self.assertTrue(case["id"])
                self.assertNotIn(case["id"], case_ids)
                case_ids.add(case["id"])
                self.assertIsInstance(case["prompt"], str)
                self.assertTrue(case["prompt"].strip())
                self.assertIsInstance(case["should_invoke"], bool)
                self.assertIsInstance(case["required_outcomes"], list)
                self.assertIsInstance(case["forbidden_behaviors"], list)
                self.assertTrue(case["forbidden_behaviors"])

                fixture = case.get("workspace_fixture")
                if fixture is not None:
                    fixture_path = Path(fixture)
                    self.assertFalse(fixture_path.is_absolute())
                    self.assertNotIn("..", fixture_path.parts)
                    self.assertTrue(
                        (REPO_ROOT / fixture_path / "experiment.json").is_file()
                    )

                if case["should_invoke"]:
                    self.assertIn(case["expected_profile"], VALID_PROFILES)
                    self.assertTrue(case["required_outcomes"])
                    self.assertIn("$research-experiment-workflow", case["prompt"])
                else:
                    self.assertIsNone(case["expected_profile"])
                    self.assertEqual([], case["required_outcomes"])

    def test_skill_requires_explicit_invocation(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        frontmatter = skill_text.split("---", 2)[1]
        openai_yaml = OPENAI_YAML_PATH.read_text(encoding="utf-8")

        self.assertIn("explicitly invokes `$research-experiment-workflow`", frontmatter)
        self.assertIn("never invoke it implicitly", frontmatter)
        self.assertIn("allow_implicit_invocation: false", openai_yaml)

    def test_skill_infers_profile_without_user_selection(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        openai_yaml = OPENAI_YAML_PATH.read_text(encoding="utf-8")
        readme = README_PATH.read_text(encoding="utf-8")
        readme_zh = README_ZH_PATH.read_text(encoding="utf-8")

        self.assertIn("Infer the smallest profile", skill_text)
        self.assertIn("do not require the user to name one", skill_text)
        self.assertIn("proceed without asking the user to choose", skill_text)
        self.assertIn("infer the appropriate rigor profile", openai_yaml)
        self.assertIn("you do not need to choose a profile", readme)
        self.assertIn("无需选择配置", readme_zh)
        self.assertNotIn("with LITE", readme)
        self.assertNotIn("的 LITE 配置", readme_zh)

        inferred_case_ids = {
            "paper_new_direction",
            "lite_bounded_comparison",
            "standard_unspecified_empirical",
            "legacy_evidence_audit",
        }
        inferred_cases = {
            case["id"]: case
            for case in self.payload["cases"]
            if case["id"] in inferred_case_ids
        }
        self.assertEqual(inferred_case_ids, set(inferred_cases))
        for case_id, case in inferred_cases.items():
            with self.subTest(case=case_id):
                for profile in VALID_PROFILES:
                    self.assertNotIn(profile, case["prompt"])

    def test_resume_fixture_passes_strict_validation(self) -> None:
        resume_case = next(
            case
            for case in self.payload["cases"]
            if case["id"] == "standard_resume_existing"
        )
        fixture_dir = REPO_ROOT / resume_case["workspace_fixture"]
        manifest = json.loads(
            (fixture_dir / "experiment.json").read_text(encoding="utf-8")
        )
        self.assertEqual("STANDARD", manifest["profile"])
        self.assertEqual("ANALYSIS", manifest["stage"])
        self.assertEqual("RUNNING", manifest["status"])

        completed = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), str(fixture_dir), "--strict"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
