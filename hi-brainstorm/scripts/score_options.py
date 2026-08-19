#!/usr/bin/env python3
"""Validate and aggregate HI Brainstorm option scorecards."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any


class ScorecardError(ValueError):
    """Raised when a scorecard violates the input contract."""


def _number(value: Any, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ScorecardError(f"{context} must be a number")
    number = float(value)
    if not math.isfinite(number):
        raise ScorecardError(f"{context} must be finite")
    return number


def _rating_record(value: Any, context: str) -> tuple[float, dict[str, Any]]:
    if not isinstance(value, dict):
        raise ScorecardError(f"{context} must be a structured rating object")
    allowed = {"rating", "rationale", "evidence_ids", "confidence", "veto"}
    unknown = set(value) - allowed
    if unknown:
        names = ", ".join(sorted(str(item) for item in unknown))
        raise ScorecardError(f"{context} has unknown fields: {names}")
    rating = _number(value.get("rating"), f"{context}.rating")
    if rating < 1 or rating > 5:
        raise ScorecardError(f"{context}.rating must be between 1 and 5")
    rationale = value.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ScorecardError(f"{context}.rationale must be a non-empty string")
    evidence_ids = value.get("evidence_ids")
    if (
        not isinstance(evidence_ids, list)
        or not evidence_ids
        or not all(isinstance(item, str) and item.strip() for item in evidence_ids)
    ):
        raise ScorecardError(f"{context}.evidence_ids must be a non-empty array of strings")
    confidence = value.get("confidence")
    if confidence not in {"high", "medium", "low"}:
        raise ScorecardError(f"{context}.confidence must be high, medium, or low")
    veto = value.get("veto")
    if veto is not None and (not isinstance(veto, str) or not veto.strip()):
        raise ScorecardError(f"{context}.veto must be null or a non-empty string")
    return rating, {
        "rating": rating,
        "rationale": rationale,
        "evidence_ids": evidence_ids,
        "confidence": confidence,
        "veto": veto,
    }


def load_scorecard(path: str) -> dict[str, Any]:
    try:
        if path == "-":
            value = json.load(sys.stdin)
        else:
            with Path(path).open(encoding="utf-8") as handle:
                value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ScorecardError(f"cannot read scorecard: {exc}") from exc
    if not isinstance(value, dict):
        raise ScorecardError("scorecard root must be an object")
    return value


def aggregate(scorecard: dict[str, Any]) -> dict[str, Any]:
    evidence_registry = scorecard.get("evidence_registry")
    criteria = scorecard.get("criteria")
    options = scorecard.get("options")
    if not isinstance(evidence_registry, list) or not evidence_registry:
        raise ScorecardError("evidence_registry must be a non-empty array")
    if not isinstance(criteria, list) or not criteria:
        raise ScorecardError("criteria must be a non-empty array")
    if not isinstance(options, list) or not options:
        raise ScorecardError("options must be a non-empty array")

    evidence_ids: set[str] = set()
    normalized_evidence: list[dict[str, str]] = []
    for index, evidence in enumerate(evidence_registry):
        if not isinstance(evidence, dict):
            raise ScorecardError(f"evidence_registry[{index}] must be an object")
        evidence_id = evidence.get("id")
        kind = evidence.get("kind")
        evidence_text = evidence.get("text")
        if not isinstance(evidence_id, str) or not evidence_id.strip():
            raise ScorecardError(f"evidence_registry[{index}].id must be a non-empty string")
        if evidence_id in evidence_ids:
            raise ScorecardError(f"duplicate evidence id: {evidence_id}")
        if kind not in {"fact", "user_statement", "assumption", "unknown"}:
            raise ScorecardError(
                f"evidence_registry[{index}].kind must be fact, user_statement, assumption, or unknown"
            )
        if not isinstance(evidence_text, str) or not evidence_text.strip():
            raise ScorecardError(f"evidence_registry[{index}].text must be a non-empty string")
        evidence_ids.add(evidence_id)
        normalized_evidence.append({"id": evidence_id, "kind": kind, "text": evidence_text})

    criterion_map: dict[str, dict[str, Any]] = {}
    total_weight = 0.0
    for index, criterion in enumerate(criteria):
        if not isinstance(criterion, dict):
            raise ScorecardError(f"criteria[{index}] must be an object")
        criterion_id = criterion.get("id")
        label = criterion.get("label")
        if not isinstance(criterion_id, str) or not criterion_id.strip():
            raise ScorecardError(f"criteria[{index}].id must be a non-empty string")
        if criterion_id in criterion_map:
            raise ScorecardError(f"duplicate criterion id: {criterion_id}")
        if not isinstance(label, str) or not label.strip():
            raise ScorecardError(f"criteria[{index}].label must be a non-empty string")
        weight = _number(criterion.get("weight"), f"criteria[{index}].weight")
        if weight <= 0:
            raise ScorecardError(f"criteria[{index}].weight must be positive")
        criterion_map[criterion_id] = {"id": criterion_id, "label": label, "weight": weight}
        total_weight += weight

    if abs(total_weight - 100.0) > 1e-9:
        raise ScorecardError(f"criterion weights must total 100, got {total_weight:g}")

    results: list[dict[str, Any]] = []
    option_ids: set[str] = set()
    for option_index, option in enumerate(options):
        if not isinstance(option, dict):
            raise ScorecardError(f"options[{option_index}] must be an object")
        option_id = option.get("id")
        name = option.get("name")
        if not isinstance(option_id, str) or not option_id.strip():
            raise ScorecardError(f"options[{option_index}].id must be a non-empty string")
        if option_id in option_ids:
            raise ScorecardError(f"duplicate option id: {option_id}")
        option_ids.add(option_id)
        if not isinstance(name, str) or not name.strip():
            raise ScorecardError(f"options[{option_index}].name must be a non-empty string")

        gate = option.get("gate", {"status": "pass", "reasons": []})
        if not isinstance(gate, dict):
            raise ScorecardError(f"option {option_id} gate must be an object")
        gate_status = gate.get("status", "pass")
        if gate_status not in {"pass", "conditional", "fail"}:
            raise ScorecardError(f"option {option_id} gate status must be pass, conditional, or fail")
        gate_reasons = gate.get("reasons", [])
        if not isinstance(gate_reasons, list) or not all(isinstance(reason, str) for reason in gate_reasons):
            raise ScorecardError(f"option {option_id} gate reasons must be an array of strings")
        if gate_status != "pass" and not gate_reasons:
            raise ScorecardError(f"option {option_id} must explain a {gate_status} gate")

        ratings = option.get("ratings")
        if not isinstance(ratings, dict) or len(ratings) < 2:
            raise ScorecardError(f"option {option_id} requires ratings from at least two experts")

        criterion_results: list[dict[str, Any]] = []
        vetoes: list[dict[str, str]] = []
        weighted_total = 0.0
        for criterion_id, criterion in criterion_map.items():
            values: list[float] = []
            rating_details: list[dict[str, Any]] = []
            for expert, expert_ratings in ratings.items():
                if not isinstance(expert, str) or not expert.strip():
                    raise ScorecardError(f"option {option_id} has an invalid expert id")
                if not isinstance(expert_ratings, dict):
                    raise ScorecardError(f"option {option_id} ratings for {expert} must be an object")
                unknown_criteria = set(expert_ratings) - set(criterion_map)
                if unknown_criteria:
                    names = ", ".join(sorted(str(item) for item in unknown_criteria))
                    raise ScorecardError(f"option {option_id}, expert {expert} used unknown criteria: {names}")
                if criterion_id not in expert_ratings:
                    continue
                rating, record = _rating_record(
                    expert_ratings[criterion_id],
                    f"option {option_id}, expert {expert}, criterion {criterion_id}",
                )
                values.append(rating)
                rating_details.append({"expert": expert, **record})
                unresolved_evidence = set(record["evidence_ids"]) - evidence_ids
                if unresolved_evidence:
                    names = ", ".join(sorted(unresolved_evidence))
                    raise ScorecardError(
                        f"option {option_id}, expert {expert}, criterion {criterion_id} "
                        f"references unknown evidence: {names}"
                    )
                if record["veto"] is not None:
                    vetoes.append(
                        {"expert": expert, "criterion": criterion_id, "concern": record["veto"]}
                    )
            if len(values) < 2:
                raise ScorecardError(
                    f"option {option_id}, criterion {criterion_id} requires at least two expert ratings"
                )
            median = float(statistics.median(values))
            rating_range = max(values) - min(values)
            contribution = criterion["weight"] * median / 5.0
            weighted_total += contribution
            criterion_results.append(
                {
                    "id": criterion_id,
                    "label": criterion["label"],
                    "weight": criterion["weight"],
                    "median": round(median, 2),
                    "range": round(rating_range, 2),
                    "ratings_count": len(values),
                    "weighted_points": round(contribution, 2),
                    "expert_ratings": rating_details,
                }
            )

        if vetoes and gate_status == "pass":
            raise ScorecardError(f"option {option_id} has veto concerns but its gate status is pass")

        results.append(
            {
                "id": option_id,
                "name": name,
                "gate": {"status": gate_status, "reasons": gate_reasons},
                "score": round(weighted_total, 2),
                "max_rating_range": max(item["range"] for item in criterion_results),
                "vetoes": vetoes,
                "criteria": criterion_results,
                "rank": None,
                "tied": False,
            }
        )

    def substantive_ranking_key(result: dict[str, Any]) -> tuple[Any, ...]:
        medians = {criterion["id"]: criterion["median"] for criterion in result["criteria"]}
        return (
            -result["score"],
            -medians.get("goal_fit", 0),
            -medians.get("risk_safety", 0),
            -medians.get("maintainability_reversibility", 0),
            -medians.get("delivery_cost", 0),
        )

    eligible = sorted(
        (result for result in results if result["gate"]["status"] != "fail"),
        key=lambda result: (*substantive_ranking_key(result), result["id"]),
    )
    key_counts: dict[tuple[Any, ...], int] = {}
    for result in eligible:
        key = substantive_ranking_key(result)
        key_counts[key] = key_counts.get(key, 0) + 1
    previous_key: tuple[Any, ...] | None = None
    current_rank = 0
    for position, result in enumerate(eligible, start=1):
        key = substantive_ranking_key(result)
        if key != previous_key:
            current_rank = position
        result["rank"] = current_rank
        result["tied"] = key_counts[key] > 1
        previous_key = key

    results.sort(key=lambda result: (result["rank"] is None, result["rank"] or 0, result["id"]))
    return {
        "evidence_registry": normalized_evidence,
        "criteria_weight_total": total_weight,
        "ranked_options": results,
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "| Rank | Option | Score | Gate | Tie | Max rating range |",
        "|---:|---|---:|---|---|---:|",
    ]
    for option in result["ranked_options"]:
        rank = option["rank"] if option["rank"] is not None else "—"
        name = option["name"].replace("|", "\\|")
        lines.append(
            f"| {rank} | {name} (`{option['id']}`) | {option['score']:.2f} | "
            f"{option['gate']['status']} | {'yes' if option['tied'] else 'no'} | "
            f"{option['max_rating_range']:.2f} |"
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scorecard", help="Path to scorecard JSON, or - for stdin")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = aggregate(load_scorecard(args.scorecard))
    except ScorecardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
