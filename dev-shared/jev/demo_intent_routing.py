#!/usr/bin/env python3
"""Usecase demo: orchestrator intent routing with the optional Jev gate.

Exercises dev-shared/jev-contract.md end to end on the detect-intent step
(devkit.md §4). The same requests run through the fallback ladder —
J1 (Jev answers), J2 (low confidence), J3 (no Jev) — against the keyword
heuristic the orchestrator uses today. Final behavior is identical in both
worlds; only the decision source differs.

Usage:
  python3 demo_intent_routing.py                 # real mode: calls jev_ask.py
  JEV_DEMO_MOCK='<adapter JSON>' python3 ...     # canned adapter response (offline)
  JEV_MIN_CONFIDENCE=0.7                         # gate threshold, default 0.7

Always exits 0 — a demo, not a gate.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADAPTER = os.path.join(HERE, "jev_ask.py")
THRESHOLD = float(os.environ.get("JEV_MIN_CONFIDENCE", "0.7"))

# (request, the route the heuristic is expected to pick)
REQUESTS = [
    ("Users report a TypeError when clicking login — sign-in is broken", "fix"),
    ("Add a dark-mode toggle to the settings screen", "craft"),
    ("Redesign the payment module architecture for the Q4 migration", "plan"),
    ("Find where the retry logic lives in the codebase", "repo-search"),
]

QUESTIONS = {
    "route": {
        "type": "choice",
        "instructions": "Which DevKit skill should handle this developer request? "
        "Judge from intent, not keywords.",
        "criteria": {
            "craft": "Implement a new feature or change in an existing codebase",
            "fix": "Diagnose and repair a bug, error, or regression",
            "plan": "Plan architecture or a multi-phase implementation before coding",
            "repo-search": "Explore or locate existing code; no changes requested",
        },
    }
}


def heuristic(request):
    """Today's keyword routing — the unchanged fallback path (J2/J3)."""
    r = request.lower()
    if any(k in r for k in ("error", "broken", "fail", "crash", "typeerror", "bug")):
        return "fix"
    if any(k in r for k in ("plan", "architecture", "redesign", "roadmap", "estimate")):
        return "plan"
    if any(k in r for k in ("find", "where", "locate", "explore", "search", "how does")):
        return "repo-search"
    return "craft"


def ask_jev(request):
    """One adapter call per request. JEV_DEMO_MOCK substitutes a canned
    response so J1/J2 are testable without an API key."""
    mock = os.environ.get("JEV_DEMO_MOCK")
    if mock:
        return json.loads(mock)
    payload = {"state": request, "questions": QUESTIONS, "min_confidence": THRESHOLD}
    proc = subprocess.run(
        [sys.executable, ADAPTER],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
    )
    return json.loads(proc.stdout)


def route_request(request):
    """Fallback ladder (jev-contract.md §3). Returns (skill, rung, detail)."""
    fallback = heuristic(request)
    try:
        data = ask_jev(request)
    except Exception as exc:
        return fallback, "J3", "adapter error: %s" % exc
    if not data.get("available"):
        return fallback, "J3", data.get("reason", "unavailable")
    ans = data.get("answers", {}).get("route")
    if not ans:
        return fallback, "J2", "route dropped: confidence < %.2f" % THRESHOLD
    choice = ans.get("choice", "?")
    note = "agrees with heuristic" if choice == fallback else "OVERRIDES heuristic"
    return choice, "J1", "choice=%s confidence=%s (%s)" % (choice, ans.get("confidence"), note)


def main():
    mode = "MOCK" if os.environ.get("JEV_DEMO_MOCK") else "live adapter"
    print("Intent routing usecase — threshold %.2f, adapter: %s" % (THRESHOLD, mode))
    print("%-58s %-12s %-4s %s" % ("request", "heuristic", "rung", "decision"))
    print("-" * 118)
    counts = {}
    for request, _expected in REQUESTS:
        skill, rung, detail = route_request(request)
        counts[rung] = counts.get(rung, 0) + 1
        print("%-58s %-12s %-4s %s" % (request[:56] + ("…" if len(request) > 56 else ""),
                                       heuristic(request), rung, detail))
        print("%-58s %44s %s" % ("", "", "-> %s" % skill))
    print("-" * 118)
    print("rungs: %s" % ", ".join("%s=%d" % (r, n) for r, n in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
