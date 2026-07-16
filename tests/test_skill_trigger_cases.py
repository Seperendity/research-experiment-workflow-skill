from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = Path(__file__).with_name("skill_trigger_cases.json")
SKILL_PATH = REPO_ROOT / "research-experiment-workflow" / "SKILL.md"
OPENAI_YAML_PATH = (
    REPO_ROOT / "research-experiment-workflow" / "agents" / "openai.yaml"
)
CASE_FIELDS = {"id", "category", "prompt", "should_invoke", "rationale"}
VALID_CATEGORIES = {"explicit_skill", "durable_artifact", "implicit_design", "ordinary_task"}


class SkillTriggerCasesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    def test_native_runner_contract_is_repeated_and_trace_scored(self) -> None:
        self.assertEqual(1, self.payload["schema_version"])
        self.assertEqual("research-experiment-workflow", self.payload["skill_name"])
        contract = self.payload["runner_contract"]
        self.assertEqual("native_skill_catalog", contract["surface"])
        self.assertIsNone(contract["prompt_wrapper"])
        self.assertGreaterEqual(contract["samples_per_case"], 3)
        self.assertTrue(contract["fresh_session_per_sample"])
        self.assertEqual("runtime_skill_activation_trace", contract["scoring_signal"])

    def test_trigger_cases_are_balanced_and_well_formed(self) -> None:
        seen: set[str] = set()
        counts = {True: 0, False: 0}
        for case in self.payload["cases"]:
            with self.subTest(case=case.get("id")):
                self.assertEqual(CASE_FIELDS, set(case))
                self.assertNotIn(case["id"], seen)
                seen.add(case["id"])
                self.assertIn(case["category"], VALID_CATEGORIES)
                self.assertTrue(case["prompt"].strip())
                self.assertIsInstance(case["should_invoke"], bool)
                self.assertTrue(case["rationale"].strip())
                counts[case["should_invoke"]] += 1

        self.assertGreaterEqual(counts[True], 3)
        self.assertGreaterEqual(counts[False], 3)

    def test_key_boundary_examples_have_expected_labels(self) -> None:
        labels = {case["id"]: case["should_invoke"] for case in self.payload["cases"]}
        self.assertTrue(labels["explicit_protocol_artifact"])
        self.assertFalse(labels["implicit_experiment_design"])

    def test_metadata_exposes_the_negative_trigger_boundary(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        frontmatter = skill_text.split("---", 2)[1]
        self.assertIn("Use only when Codex is explicitly asked", frontmatter)
        self.assertIn(
            "Do not invoke merely because the user asks to discuss, brainstorm, or design an experiment",
            frontmatter,
        )

        openai_yaml = OPENAI_YAML_PATH.read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: false", openai_yaml)


if __name__ == "__main__":
    unittest.main()
