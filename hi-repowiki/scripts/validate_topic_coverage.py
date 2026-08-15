#!/usr/bin/env python3
"""Validate hi-repowiki topic coverage without third-party dependencies."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = SKILL_ROOT / "references" / "topic-coverage.schema.json"


def load_json(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def resolve_scoped_path(root: Path, value: str, label: str, errors: list[str]) -> Path | None:
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        errors.append(f"{label} escapes its root: {value}")
        return None
    return candidate


def validate(data: Any, repo_root: Path, output_root: Path) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    expected_ids = schema["$defs"]["facet"]["properties"]["id"]["enum"]
    allowed_ids = set(expected_ids)
    allowed_statuses = set(schema["$defs"]["facet"]["properties"]["status"]["enum"])
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["coverage root must be a JSON object"]

    required = ("schema_version", "mode", "profile", "source_revision", "facets")
    for field in required:
        if field not in data:
            errors.append(f"missing root field: {field}")

    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    mode = data.get("mode")
    if mode not in {"generate", "update", "plan-only"}:
        errors.append("mode must be generate, update, or plan-only")
    profile = data.get("profile")
    if profile not in {"comprehensive", "focused"}:
        errors.append("profile must be comprehensive or focused")
    if not isinstance(data.get("source_revision"), str) or not data.get("source_revision", "").strip():
        errors.append("source_revision must be a non-empty string")

    facets = data.get("facets")
    if not isinstance(facets, list) or not facets:
        errors.append("facets must be a non-empty array")
        return errors

    facet_ids = [facet.get("id") for facet in facets if isinstance(facet, dict)]
    duplicates = sorted(facet_id for facet_id, count in Counter(facet_ids).items() if count > 1)
    if duplicates:
        errors.append("duplicate facet IDs: " + ", ".join(str(item) for item in duplicates))

    unknown_ids = sorted(str(item) for item in set(facet_ids) - allowed_ids)
    if unknown_ids:
        errors.append("unknown facet IDs: " + ", ".join(unknown_ids))
    if profile == "comprehensive":
        missing = sorted(allowed_ids - set(facet_ids))
        if missing:
            errors.append("comprehensive profile is missing facets: " + ", ".join(missing))

    for index, facet in enumerate(facets):
        prefix = f"facets[{index}]"
        if not isinstance(facet, dict):
            errors.append(f"{prefix} must be an object")
            continue
        facet_id = facet.get("id", "<missing>")
        prefix = f"facet {facet_id}"
        status = facet.get("status")
        reason = facet.get("reason")
        evidence = facet.get("evidence")
        checks = facet.get("checks")
        pages = facet.get("pages")
        merged_into = facet.get("merged_into")

        if status not in allowed_statuses:
            errors.append(f"{prefix}: invalid status {status!r}")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{prefix}: reason must be non-empty")
        if not isinstance(evidence, list) or any(not isinstance(item, str) or not item for item in evidence):
            errors.append(f"{prefix}: evidence must be an array of non-empty strings")
            evidence = []
        if not isinstance(checks, list) or any(not isinstance(item, str) or not item for item in checks):
            errors.append(f"{prefix}: checks must be an array of non-empty strings")
            checks = []
        if not isinstance(pages, list) or any(not isinstance(item, str) or not item for item in pages):
            errors.append(f"{prefix}: pages must be an array of non-empty strings")
            pages = []

        if status in {"planned", "documented", "merged"}:
            if not evidence:
                errors.append(f"{prefix}: {status} requires evidence")
            if not pages:
                errors.append(f"{prefix}: {status} requires page mappings")
        if status == "merged" and (not isinstance(merged_into, str) or not merged_into.strip()):
            errors.append(f"{prefix}: merged requires merged_into")
        if status in {"not_applicable", "unknown", "blocked"} and not checks:
            errors.append(f"{prefix}: {status} requires recorded checks")
        if status != "merged" and merged_into is not None:
            errors.append(f"{prefix}: merged_into must be null unless status is merged")
        if mode == "plan-only" and status in {"documented", "merged"}:
            errors.append(f"{prefix}: plan-only mode must use planned for applicable ungenerated pages")
        if mode in {"generate", "update"} and status == "planned":
            errors.append(f"{prefix}: planned is not a final status in {mode} mode")

        for value in evidence:
            candidate = resolve_scoped_path(repo_root, value, f"{prefix} evidence", errors)
            if candidate is not None and not candidate.is_file():
                errors.append(f"{prefix}: evidence file does not exist: {value}")
        if status in {"documented", "merged"}:
            for value in pages:
                candidate = resolve_scoped_path(output_root, value, f"{prefix} page", errors)
                if candidate is not None and not candidate.is_file():
                    errors.append(f"{prefix}: mapped page does not exist: {value}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("coverage", help="topic-coverage.json path, or - for stdin")
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()

    try:
        data = load_json(args.coverage)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read coverage JSON: {exc}", file=sys.stderr)
        return 2

    repo_root = args.repo_root.resolve()
    output_root = args.output_root.resolve()
    errors = validate(data, repo_root, output_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Topic coverage is valid: {len(data['facets'])} facets ({data['profile']}, {data['mode']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
