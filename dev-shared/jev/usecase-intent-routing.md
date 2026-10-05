# Usecase: Intent Routing — With Jev vs Without Jev

Runnable proof of [jev-contract.md](jev-contract.md) on the orchestrator's detect-intent step (`devkit.md` §4): the same requests route to the same skills whether or not Jev is present — only the **decision source** (rung J1/J2/J3) changes.

## Run

```bash
cd <skills dir>/dev-shared/jev        # repo: AI/dev-kit/dev-shared/jev — installed: ~/.agents/skills/dev-shared/jev
python3 demo_intent_routing.py
```

Four requests (bug fix / feature / architecture planning / code search) go through the fallback ladder and today's keyword heuristic; the table prints the rung that decided each route.

## Test matrix

| # | Command | Rung | Expected |
| --- | --- | --- | --- |
| 1 | `python3 demo_intent_routing.py` (no `TYPESAFE_API_KEY`) | J3 ×4 | All rows: heuristic decides, `available:false`, exit 0 |
| 2 | `TYPESAFE_API_KEY=x JEV_ENABLED=0 python3 demo_intent_routing.py` | J3 ×4 | Kill-switch reason; identical decisions |
| 3 | `JEV_DEMO_MOCK='{"available": true, "answers": {}, "dropped": ["route"]}' python3 demo_intent_routing.py` | J2 ×4 | Answers dropped below threshold → heuristic decides |
| 4 | `JEV_DEMO_MOCK='{"available": true, "answers": {"route": {"type": "choice", "choice": "plan", "confidence": 0.91}}}' python3 demo_intent_routing.py` | J1 ×4 | Typed answer wins; rows where it disagrees show `OVERRIDES heuristic` |
| 5 | `TYPESAFE_API_KEY=<real key> python3 demo_intent_routing.py` | J1 | Live Jev call per request; compare its choices against the heuristic column |

## Pass criteria

- Every mode exits 0 and every request gets a route — Jev can never break routing.
- J2/J3 rows: decision equals the heuristic column exactly (the fallback is unchanged behavior).
- J1 rows: decision equals the adapter's `choice`; disagreements are visible, not hidden — that is the measured value of Jev (`hi-log` records rungs per jev-contract.md §6).

## Extending to real skills

Wire the same ladder into a skill with the one-liner recipe (jev-contract.md §4); `demo_intent_routing.py` is the reference implementation of the caller side.
