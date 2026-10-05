#!/usr/bin/env python3
"""Optional Jev adapter for DevKit sDLC judgment calls — dev-shared/jev-contract.md.

Contract: fail-open. Every failure path prints {"available": false, "reason": ...}
and exits 0, so callers fall back to their existing heuristics unchanged.
Stdlib only — no SDK dependency.

Usage:
  echo '{"state": "...", "questions": {...}, "min_confidence": 0.7}' | python3 jev_ask.py
  python3 jev_ask.py --probe

Environment:
  TYPESAFE_API_KEY  required (console.typesafe.ai/keys)
  JEV_ENABLED=0     kill-switch: always report unavailable
  JEV_TIMEOUT_S     request timeout, default 8
"""

import json
import os
import sys
import urllib.request

API_URL = "https://api.typesafe.ai/v1/systemone"


def fail(reason):
    print(json.dumps({"available": False, "reason": reason}))


def normalized_confidence(ans):
    """Choice/Score carry `confidence`; Noul carries probability `noul` where
    0.5 is a coin flip — normalize to certainty distance so callers gate
    uniformly (jev-contract.md §5)."""
    if "confidence" in ans:
        return float(ans["confidence"])
    if "noul" in ans:
        return abs(float(ans["noul"]) * 2 - 1)
    return 0.0


def call_jev(state, questions, key, timeout):
    body = json.dumps({"state": state, "model": "jev-latest", "questions": questions}).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def main():
    key = os.environ.get("TYPESAFE_API_KEY", "")
    enabled = os.environ.get("JEV_ENABLED", "1").lower() not in ("0", "false")
    timeout = float(os.environ.get("JEV_TIMEOUT_S", "8"))
    probe = len(sys.argv) > 1 and sys.argv[1] == "--probe"

    try:
        payload = {} if probe else json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        fail("bad input JSON: %s" % exc)
        return 0

    if not enabled:
        fail("JEV_ENABLED disables Jev")
        return 0
    if not key:
        fail("TYPESAFE_API_KEY not set")
        return 0

    if probe:
        payload = {
            "state": "probe",
            "questions": {"ok": {"type": "noul", "instructions": "Always answer yes."}},
        }

    state = payload.get("state")
    questions = payload.get("questions")
    if not state or not questions:
        fail("state and questions are required")
        return 0

    try:
        data = call_jev(state, questions, key, timeout)
    except Exception as exc:  # network, auth, timeout — all fail-open
        fail("jev call failed: %s" % exc)
        return 0

    threshold = float(payload.get("min_confidence", 0.0))
    answers, dropped = {}, []
    for qid, ans in (data.get("answers") or {}).items():
        out = dict(ans)
        out.setdefault("confidence", normalized_confidence(ans))
        if out["confidence"] >= threshold:
            answers[qid] = out
        else:
            dropped.append(qid)
    print(json.dumps({
        "available": True,
        "answers": answers,
        "dropped": dropped,
        "model": data.get("model"),
        "usage": data.get("usage"),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
