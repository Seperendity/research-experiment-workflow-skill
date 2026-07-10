#!/usr/bin/env python3
"""Validate research experiment manifests, gates, and result summaries."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 2
VALID_STAGES = {
    "IDEA",
    "HYPOTHESIS",
    "NOVELTY",
    "FEASIBILITY",
    "PROTOCOL",
    "PILOT",
    "EXPERIMENT",
    "DEBUG",
    "ABLATION",
    "REVIEW",
    "ANALYSIS",
    "DECISION",
}
VALID_STATUSES = {
    "PLANNED",
    "RUNNING",
    "INTERRUPTED",
    "BLOCKED",
    "DONE",
    "FAILED",
    "PARTIAL",
    "INVALIDATED",
}
VALID_GATE_VERDICTS = {"PASS", "WARNING", "FAIL", "PENDING"}
REQUIRED_GATES = {"novelty", "feasibility", "protocol", "pilot", "review"}
RESULT_STATUSES = {"DONE", "FAILED", "PARTIAL"}
PREREQUISITE_GATES = {
    "FEASIBILITY": ("novelty",),
    "PROTOCOL": ("novelty", "feasibility"),
    "PILOT": ("novelty", "feasibility", "protocol"),
    "EXPERIMENT": ("novelty", "feasibility", "protocol", "pilot"),
    "ABLATION": ("novelty", "feasibility", "protocol", "pilot"),
    "REVIEW": ("novelty", "feasibility", "protocol", "pilot"),
    "ANALYSIS": ("novelty", "feasibility", "protocol", "pilot", "review"),
    "DECISION": ("novelty", "feasibility", "protocol", "pilot", "review"),
}


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def exit_code(self, strict: bool = False) -> int:
        return 1 if self.errors or (strict and self.warnings) else 0


def _load_json(path: Path, result: ValidationResult, label: str) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.error(f"{label} does not exist: {path}")
        return None
    except json.JSONDecodeError as exc:
        result.error(f"{label} is invalid JSON: {exc}")
        return None
    except OSError as exc:
        result.error(f"could not read {label}: {exc}")
        return None

    if not isinstance(value, dict):
        result.error(f"{label} must contain a JSON object")
        return None
    return value


def _require_keys(
    value: dict[str, Any],
    keys: set[str],
    result: ValidationResult,
    label: str,
) -> None:
    for key in sorted(keys - value.keys()):
        result.error(f"{label} is missing required field '{key}'")


def _artifact_path(
    root: Path,
    raw_path: Any,
    result: ValidationResult,
    label: str,
    *,
    require_exists: bool,
) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path.strip():
        result.error(f"{label} must be a non-empty relative path")
        return None

    relative_path = Path(raw_path)
    if relative_path.is_absolute():
        result.error(f"{label} must be a relative path: {raw_path}")
        return None

    root = root.resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        result.error(f"{label} escapes the experiment directory: {raw_path}")
        return None

    if require_exists and not candidate.is_file():
        result.error(f"{label} does not exist: {raw_path}")
    elif candidate.exists() and not candidate.is_file():
        result.error(f"{label} must reference a file: {raw_path}")
    return candidate


def _gate_allows_progress(gate: Any) -> bool:
    if not isinstance(gate, dict):
        return False
    verdict = gate.get("verdict")
    return verdict == "PASS" or (
        verdict == "WARNING" and gate.get("accepted_warning") is True
    )


def _validate_manifest(
    root: Path,
    manifest: dict[str, Any],
    result: ValidationResult,
) -> None:
    _require_keys(
        manifest,
        {
            "schema_version",
            "experiment_id",
            "hypothesis_id",
            "stage",
            "status",
            "gates",
            "parent_experiment_id",
            "artifacts",
            "warnings",
        },
        result,
        "experiment.json",
    )

    if manifest.get("schema_version") != SCHEMA_VERSION:
        result.error(f"experiment.json schema_version must be {SCHEMA_VERSION}")

    experiment_id = manifest.get("experiment_id")
    if not isinstance(experiment_id, str) or not experiment_id:
        result.error("experiment.json experiment_id must be a non-empty string")

    parent_experiment_id = manifest.get("parent_experiment_id")
    if parent_experiment_id is not None and (
        not isinstance(parent_experiment_id, str) or not parent_experiment_id.strip()
    ):
        result.error(
            "experiment.json parent_experiment_id must be null or a non-empty string"
        )

    hypothesis_id = manifest.get("hypothesis_id")
    if not isinstance(hypothesis_id, str) or not hypothesis_id.strip():
        result.error("experiment.json hypothesis_id must be a non-empty string")

    stage = manifest.get("stage")
    if stage not in VALID_STAGES:
        result.error(f"experiment.json stage is invalid: {stage!r}")

    status = manifest.get("status")
    if status not in VALID_STATUSES:
        result.error(f"experiment.json status is invalid: {status!r}")

    if not isinstance(manifest.get("warnings"), list):
        result.error("experiment.json warnings must be a list")

    gates = manifest.get("gates")
    if not isinstance(gates, dict):
        result.error("experiment.json gates must be an object")
        gates = {}
    else:
        for missing in sorted(REQUIRED_GATES - gates.keys()):
            result.error(f"experiment.json gates is missing '{missing}'")

    for gate_name, gate in gates.items():
        label = f"gate '{gate_name}'"
        if not isinstance(gate, dict):
            result.error(f"{label} must be an object")
            continue
        _require_keys(
            gate,
            {"verdict", "artifact", "accepted_warning"},
            result,
            label,
        )
        verdict = gate.get("verdict")
        if verdict not in VALID_GATE_VERDICTS:
            result.error(f"{label} has invalid verdict: {verdict!r}")
            continue
        if not isinstance(gate.get("accepted_warning"), bool):
            result.error(f"{label} accepted_warning must be boolean")
        _artifact_path(
            root,
            gate.get("artifact"),
            result,
            f"{label} artifact",
            require_exists=verdict != "PENDING",
        )
        if verdict == "WARNING":
            if gate.get("accepted_warning") is not True:
                result.error(f"{label} warning has not been accepted")
            else:
                result.warn(f"{label} contains an accepted warning")
        if verdict == "FAIL":
            if status not in {"BLOCKED", "FAILED", "INVALIDATED"}:
                result.error(f"{label} failed but experiment status is {status!r}")
            else:
                result.warn(f"{label} records a failed gate")

    if stage in PREREQUISITE_GATES:
        for gate_name in PREREQUISITE_GATES[stage]:
            if not _gate_allows_progress(gates.get(gate_name)):
                result.error(
                    f"stage {stage} requires gate '{gate_name}' to pass "
                    "or have an accepted warning"
                )

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        result.error("experiment.json artifacts must be an object")
        return

    require_summary = stage in {"REVIEW", "ANALYSIS", "DECISION"} or (
        stage == "EXPERIMENT" and status in RESULT_STATUSES
    )
    require_analysis = stage in {"ANALYSIS", "DECISION"} and status != "RUNNING"
    require_decision = stage == "DECISION" and status != "RUNNING"
    branch_requirements = {
        "DEBUG": ("debug", "DEBUG.md"),
        "ABLATION": ("ablation", "ABLATION_PLAN.md"),
    }

    for key, required in (
        ("summary", require_summary),
        ("analysis", require_analysis),
        ("decision", require_decision),
    ):
        if key not in artifacts:
            if required:
                result.error(f"experiment.json artifacts is missing '{key}'")
            continue
        _artifact_path(
            root,
            artifacts[key],
            result,
            f"artifact '{key}'",
            require_exists=required,
        )

    if stage in branch_requirements:
        key, default_path = branch_requirements[stage]
        raw_path = artifacts.get(key, default_path)
        _artifact_path(
            root,
            raw_path,
            result,
            f"artifact '{key}'",
            require_exists=True,
        )


def _validate_summary(
    root: Path,
    summary: dict[str, Any],
    result: ValidationResult,
    manifest: dict[str, Any] | None,
) -> None:
    if "schema_version" not in summary:
        _require_keys(
            summary,
            {"experiment_id", "status", "seed", "metrics"},
            result,
            "legacy results/summary.json",
        )
        result.warn(
            "legacy results/summary.json has no schema_version; migrate new work to version 2"
        )
        if manifest and summary.get("experiment_id") != manifest.get("experiment_id"):
            result.error("manifest and legacy summary experiment_id values differ")
        return

    if summary.get("schema_version") != SCHEMA_VERSION:
        result.error(f"results/summary.json schema_version must be {SCHEMA_VERSION}")
        return

    _require_keys(
        summary,
        {
            "schema_version",
            "experiment_id",
            "hypothesis_id",
            "status",
            "protocol",
            "primary_metric",
            "config_base",
            "config_overrides",
            "runs",
            "aggregate",
            "baseline",
            "delta_vs_baseline",
            "provenance",
            "artifacts",
            "budget",
            "warnings",
        },
        result,
        "results/summary.json",
    )

    experiment_id = summary.get("experiment_id")
    if not isinstance(experiment_id, str) or not experiment_id.strip():
        result.error("results/summary.json experiment_id must be a non-empty string")
    hypothesis_id = summary.get("hypothesis_id")
    if not isinstance(hypothesis_id, str) or not hypothesis_id.strip():
        result.error("results/summary.json hypothesis_id must be a non-empty string")

    if manifest and experiment_id != manifest.get("experiment_id"):
        result.error("manifest and summary experiment_id values differ")
    if manifest and hypothesis_id != manifest.get("hypothesis_id"):
        result.error("manifest and summary hypothesis_id values differ")
    if summary.get("status") not in RESULT_STATUSES:
        result.error(f"results/summary.json status is invalid: {summary.get('status')!r}")

    protocol_path = _artifact_path(
        root,
        summary.get("protocol"),
        result,
        "results/summary.json protocol",
        require_exists=True,
    )
    if manifest and protocol_path is not None:
        gates = manifest.get("gates")
        protocol_gate = gates.get("protocol") if isinstance(gates, dict) else None
        manifest_protocol = (
            protocol_gate.get("artifact") if isinstance(protocol_gate, dict) else None
        )
        if isinstance(manifest_protocol, str):
            manifest_protocol_path = (root / manifest_protocol).resolve()
            if manifest_protocol_path != protocol_path:
                result.error("manifest and summary protocol paths differ")

    primary_metric = summary.get("primary_metric")
    if not isinstance(primary_metric, dict):
        result.error("results/summary.json primary_metric must be an object")
    else:
        if not isinstance(primary_metric.get("name"), str) or not primary_metric.get("name"):
            result.error("primary_metric.name must be a non-empty string")
        if primary_metric.get("direction") not in {"minimize", "maximize"}:
            result.error("primary_metric.direction must be 'minimize' or 'maximize'")

    for key in (
        "config_overrides",
        "aggregate",
        "baseline",
        "delta_vs_baseline",
        "provenance",
        "artifacts",
        "budget",
    ):
        if not isinstance(summary.get(key), dict):
            result.error(f"results/summary.json {key} must be an object")
    if not isinstance(summary.get("warnings"), list):
        result.error("results/summary.json warnings must be a list")

    runs = summary.get("runs")
    if not isinstance(runs, list):
        result.error("results/summary.json runs must be a list")
    else:
        for index, run in enumerate(runs):
            label = f"runs[{index}]"
            if not isinstance(run, dict):
                result.error(f"{label} must be an object")
                continue
            _require_keys(
                run,
                {"run_id", "seed", "status", "config", "metrics", "artifacts", "warnings"},
                result,
                label,
            )
            if not isinstance(run.get("run_id"), str) or not run.get("run_id"):
                result.error(f"{label}.run_id must be a non-empty string")
            if run.get("status") not in RESULT_STATUSES:
                result.error(f"{label}.status is invalid: {run.get('status')!r}")
            for key in ("config", "metrics", "artifacts"):
                if not isinstance(run.get(key), dict):
                    result.error(f"{label}.{key} must be an object")
            if not isinstance(run.get("warnings"), list):
                result.error(f"{label}.warnings must be a list")

    aggregate = summary.get("aggregate")
    if isinstance(aggregate, dict):
        _require_keys(
            aggregate,
            {"n_planned", "n_completed", "metrics"},
            result,
            "aggregate",
        )
        planned = aggregate.get("n_planned")
        completed = aggregate.get("n_completed")
        if not isinstance(planned, int) or planned < 0:
            result.error("aggregate.n_planned must be a non-negative integer")
        if not isinstance(completed, int) or completed < 0:
            result.error("aggregate.n_completed must be a non-negative integer")
        if isinstance(planned, int) and isinstance(completed, int) and completed > planned:
            result.error("aggregate.n_completed cannot exceed aggregate.n_planned")
        if not isinstance(aggregate.get("metrics"), dict):
            result.error("aggregate.metrics must be an object")

    baseline = summary.get("baseline")
    if isinstance(baseline, dict):
        _require_keys(
            baseline,
            {"experiment_id", "source", "metrics"},
            result,
            "baseline",
        )
        baseline_id = baseline.get("experiment_id")
        if baseline_id is not None and not isinstance(baseline_id, str):
            result.error("baseline.experiment_id must be null or a string")
        if not isinstance(baseline.get("source"), str) or not baseline.get("source"):
            result.error("baseline.source must be a non-empty string")
        if not isinstance(baseline.get("metrics"), dict):
            result.error("baseline.metrics must be an object")

    provenance = summary.get("provenance")
    if isinstance(provenance, dict):
        _require_keys(
            provenance,
            {"git_commit", "data_version", "environment"},
            result,
            "provenance",
        )
        provenance_keys = ("git_commit", "data_version", "environment")
        if any(provenance.get(key) is None for key in provenance_keys):
            if not summary.get("warnings"):
                result.warn("null provenance fields should be explained in warnings")

    budget = summary.get("budget")
    if isinstance(budget, dict):
        _require_keys(
            budget,
            {"max_runs", "timeout", "retries_used", "stop_reason"},
            result,
            "budget",
        )
        retries = budget.get("retries_used")
        if not isinstance(retries, int) or retries < 0:
            result.error("budget.retries_used must be a non-negative integer")


def validate_experiment(experiment_dir: Path) -> ValidationResult:
    result = ValidationResult()
    root = experiment_dir.resolve()
    if not root.is_dir():
        result.error(f"experiment directory does not exist: {experiment_dir}")
        return result

    manifest_path = root / "experiment.json"
    manifest: dict[str, Any] | None = None
    if manifest_path.is_file():
        manifest = _load_json(manifest_path, result, "experiment.json")
        if manifest is not None:
            _validate_manifest(root, manifest, result)
    else:
        result.warn("legacy experiment has no experiment.json manifest")

    summary_path = root / "results" / "summary.json"
    if manifest and isinstance(manifest.get("artifacts"), dict):
        raw_summary_path = manifest["artifacts"].get("summary")
        if isinstance(raw_summary_path, str) and raw_summary_path:
            resolved = _artifact_path(
                root,
                raw_summary_path,
                result,
                "artifact 'summary'",
                require_exists=False,
            )
            if resolved is not None:
                summary_path = resolved

    if summary_path.is_file():
        summary = _load_json(summary_path, result, "results/summary.json")
        if summary is not None:
            _validate_summary(root, summary, result, manifest)
    elif manifest is None:
        result.warn("legacy experiment has no results/summary.json")

    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a research experiment directory without modifying it."
    )
    parser.add_argument("experiment_dir", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when compatibility or accepted-warning notices exist.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    result = validate_experiment(args.experiment_dir)
    for message in result.errors:
        print(f"ERROR: {message}")
    for message in result.warnings:
        print(f"WARNING: {message}")
    if not result.errors and not result.warnings:
        print(f"PASS: {args.experiment_dir}")
    print(f"Result: {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
    return result.exit_code(args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
