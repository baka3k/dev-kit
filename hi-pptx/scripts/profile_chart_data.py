#!/usr/bin/env python3
"""Profile CSV/JSON data and suggest defensible chart families.

The output is advisory. It never replaces confirmation of the analytical
question, units, denominator, source, and intended audience.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y-%m",
    "%b %Y",
    "%B %Y",
)


def load_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and isinstance(payload.get("rows"), list):
            payload = payload["rows"]
        if not isinstance(payload, list) or not all(isinstance(row, dict) for row in payload):
            raise ValueError("JSON input must be a list of objects or an object with a rows list")
        return [dict(row) for row in payload]
    raise ValueError("Input must be .csv or .json")


def is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip().lower() in {"", "na", "n/a", "null", "none", "-"})


def parse_number(value: Any) -> tuple[float | None, dict[str, Any]]:
    if isinstance(value, bool) or is_missing(value):
        return None, {}
    if isinstance(value, (int, float)):
        number = float(value)
        return (number, {}) if math.isfinite(number) else (None, {})
    text = str(value).strip()
    metadata: dict[str, Any] = {}
    if text.startswith("(") and text.endswith(")"):
        metadata["parentheses_negative"] = True
        text = "-" + text[1:-1]
    currency = "".join(symbol for symbol in "$€£¥₫" if symbol in text)
    if currency:
        metadata["currency"] = currency
    percent = text.endswith("%")
    if percent:
        metadata["percent"] = True
        text = text[:-1]
    cleaned = re.sub(r"[$€£¥₫,\s]", "", text)
    try:
        number = float(cleaned)
    except ValueError:
        return None, {}
    if not math.isfinite(number):
        return None, {}
    if percent:
        number /= 100.0
    return number, metadata


def parse_date(value: Any) -> datetime | None:
    if not isinstance(value, str) or is_missing(value):
        return None
    text = value.strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        pass
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def ordered_columns(rows: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    columns: list[str] = []
    for row in rows:
        for key in row:
            name = str(key)
            if name not in seen:
                seen.add(name)
                columns.append(name)
    return columns


def profile_column(name: str, values: list[Any]) -> dict[str, Any]:
    non_missing = [value for value in values if not is_missing(value)]
    numeric_parsed = [parse_number(value) for value in non_missing]
    numbers = [number for number, _ in numeric_parsed if number is not None]
    dates = [parsed for value in non_missing if (parsed := parse_date(value)) is not None]
    numeric_ratio = len(numbers) / len(non_missing) if non_missing else 0.0
    date_ratio = len(dates) / len(non_missing) if non_missing else 0.0

    if len(non_missing) >= 2 and numeric_ratio >= 0.8:
        kind = "numeric"
    elif len(non_missing) >= 2 and date_ratio >= 0.8:
        kind = "datetime"
    else:
        kind = "categorical"

    result: dict[str, Any] = {
        "name": name,
        "kind": kind,
        "rows": len(values),
        "non_missing": len(non_missing),
        "missing": len(values) - len(non_missing),
        "unique": len({str(value) for value in non_missing}),
    }

    if kind == "numeric" and numbers:
        metadata = [item for _, item in numeric_parsed]
        currencies = sorted({item.get("currency") for item in metadata if item.get("currency")})
        result.update(
            {
                "min": min(numbers),
                "max": max(numbers),
                "sum": sum(numbers),
                "mean": statistics.fmean(numbers),
                "median": statistics.median(numbers),
                "negative_count": sum(number < 0 for number in numbers),
                "percent_like": any(item.get("percent") for item in metadata),
                "currencies": currencies,
            }
        )
    elif kind == "datetime" and dates:
        result.update({"min": min(dates).isoformat(), "max": max(dates).isoformat()})
    else:
        counts = Counter(str(value) for value in non_missing)
        result["top_values"] = [
            {"value": value, "count": count} for value, count in counts.most_common(8)
        ]
    return result


def row_numeric_sums(rows: list[dict[str, Any]], numeric_columns: list[str]) -> list[float]:
    totals: list[float] = []
    for row in rows:
        parsed = [parse_number(row.get(column))[0] for column in numeric_columns]
        if all(value is not None for value in parsed):
            totals.append(sum(value for value in parsed if value is not None))
    return totals


def is_composition(rows: list[dict[str, Any]], numeric_columns: list[str]) -> bool:
    if len(numeric_columns) < 2:
        return False
    totals = row_numeric_sums(rows, numeric_columns)
    if not totals:
        return False
    near_one = all(abs(total - 1.0) <= 0.02 for total in totals)
    near_hundred = all(abs(total - 100.0) <= 2.0 for total in totals)
    return near_one or near_hundred


def recommend(rows: list[dict[str, Any]], columns: list[dict[str, Any]]) -> dict[str, Any]:
    numeric = [column["name"] for column in columns if column["kind"] == "numeric"]
    temporal = [column["name"] for column in columns if column["kind"] == "datetime"]
    categorical = [column["name"] for column in columns if column["kind"] == "categorical"]
    alternatives: list[str] = []
    rationale: list[str] = []

    if temporal and numeric:
        chart = "line"
        rationale.append(f"{temporal[0]} provides an ordered time axis and numeric measures provide trends")
        if len(numeric) == 1:
            alternatives.append("column")
    elif categorical and len(numeric) >= 2 and is_composition(rows, numeric):
        chart = "percent_stacked_bar"
        rationale.append("numeric series sum to approximately 100% for each category")
        alternatives.append("grouped_bar")
    elif categorical and numeric:
        chart = "horizontal_bar" if len(numeric) == 1 else "grouped_bar"
        rationale.append(f"{categorical[0]} supplies comparison categories and numeric measures supply magnitude")
        if len(numeric) == 1:
            alternatives.append("column")
    elif len(numeric) >= 2:
        chart = "scatter"
        rationale.append("two or more numeric measures can be tested for association")
        alternatives.append("table")
    elif len(numeric) == 1:
        chart = "histogram_or_kpi"
        rationale.append("one numeric measure supports a distribution or summary metric")
        alternatives.append("box_whisker")
    else:
        chart = "table"
        rationale.append("no reliable numeric measure was detected")

    return {
        "primary": chart,
        "alternatives": alternatives,
        "rationale": rationale,
        "candidate_fields": {
            "temporal": temporal,
            "categorical": categorical,
            "numeric": numeric,
        },
    }


def build_warnings(rows: list[dict[str, Any]], columns: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    if len(rows) < 2:
        warnings.append("Fewer than two rows: a chart is unlikely to show a defensible pattern")
    for column in columns:
        if column["missing"]:
            warnings.append(f"{column['name']}: {column['missing']} missing value(s)")
        if column["kind"] == "categorical" and column["unique"] > 12:
            warnings.append(f"{column['name']}: {column['unique']} categories; consider ranking, filtering, or a table")
        if column["kind"] == "numeric" and len(column.get("currencies", [])) > 1:
            warnings.append(f"{column['name']}: multiple currency symbols detected")
    categorical = [column for column in columns if column["kind"] == "categorical"]
    temporal = [column for column in columns if column["kind"] == "datetime"]
    if not temporal:
        for column in categorical:
            if column["non_missing"] > column["unique"]:
                warnings.append(f"{column['name']}: duplicate category labels detected; confirm intended aggregation")
    return warnings


def factual_insights(rows: list[dict[str, Any]], columns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    numeric = [column for column in columns if column["kind"] == "numeric"]
    categorical = [column for column in columns if column["kind"] == "categorical"]
    temporal = [column for column in columns if column["kind"] == "datetime"]
    insights: list[dict[str, Any]] = []

    if categorical and len(numeric) == 1:
        category_name = categorical[0]["name"]
        value_name = numeric[0]["name"]
        pairs = []
        for row in rows:
            value, _ = parse_number(row.get(value_name))
            if value is not None and not is_missing(row.get(category_name)):
                pairs.append((str(row.get(category_name)), value))
        if pairs:
            high = max(pairs, key=lambda item: item[1])
            low = min(pairs, key=lambda item: item[1])
            insights.append({"type": "maximum", "category": high[0], "value": high[1], "measure": value_name})
            insights.append({"type": "minimum", "category": low[0], "value": low[1], "measure": value_name})

    if temporal and numeric:
        time_name = temporal[0]["name"]
        value_name = numeric[0]["name"]
        observations = []
        for row in rows:
            moment = parse_date(row.get(time_name))
            value, _ = parse_number(row.get(value_name))
            if moment is not None and value is not None:
                observations.append((moment, value))
        observations.sort(key=lambda item: item[0])
        if len(observations) >= 2:
            start, end = observations[0][1], observations[-1][1]
            change = end - start
            percent_change = change / abs(start) if start != 0 else None
            insights.append(
                {
                    "type": "endpoint_change",
                    "measure": value_name,
                    "start": start,
                    "end": end,
                    "absolute_change": change,
                    "percent_change": percent_change,
                }
            )
    return insights


def profile(path: Path) -> dict[str, Any]:
    rows = load_rows(path)
    if not rows:
        raise ValueError("Input contains no data rows")
    names = ordered_columns(rows)
    columns = [profile_column(name, [row.get(name) for row in rows]) for name in names]
    return {
        "source": str(path.resolve()),
        "row_count": len(rows),
        "column_count": len(names),
        "columns": columns,
        "chart_recommendation": recommend(rows, columns),
        "factual_insights": factual_insights(rows, columns),
        "warnings": build_warnings(rows, columns),
        "required_human_checks": [
            "Confirm the analytical question and intended decision",
            "Confirm units, denominator, scope, source, and time period",
            "Confirm any aggregation, filtering, outlier, and rounding rules",
            "Reconcile all plotted values with the clean source table",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CSV or JSON input")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    result = profile(args.input)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
