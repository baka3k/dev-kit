# Jev Optional Contract

Jev (TypeSafe System One) is an **optional** judgment backend for DevKit skills: typed `Choice` / `Score` / `Noul` answers over a state, instead of prompt-and-parse LLM steps. Skills MUST work identically when Jev is absent — the fallback path is always the skill's existing heuristic, never a modified one. Background: [typesafe-ai](../typesafe-ai/SKILL.md); live docs at `https://docs.typesafe.ai`.

## 1. Capability Probe (once per workflow)

Same philosophy as [delegation-contract.md](delegation-contract.md) §1: probe once, cache the result for the session.

| Priority | Probe | Mode |
| --- | --- | --- |
| 1 | `python3 dev-shared/jev/jev_ask.py --probe` returns `"available": true` | `jev` |
| 2 | No `TYPESAFE_API_KEY`, `JEV_ENABLED=0`, or probe fails | `heuristic` (default; behavior unchanged) |

`JEV_ENABLED=0` is a kill-switch: force `heuristic` even when the key is present.

## 2. Adapter

`dev-shared/jev/jev_ask.py` is the only Jev touchpoint. Stdlib-only HTTP client — no SDK, no MCP.

- **Input (stdin):** `{"state": <text|object>, "questions": {qid: {type, instructions, criteria?}}, "min_confidence": 0.7}`
- **Output (stdout):** `{"available": true, "answers": {qid: {choice|score|noul, confidence, ...}}, "dropped": [qid], "model", "usage"}`
- **Fail-open:** every failure (bad input, missing key, network, auth, timeout `JEV_TIMEOUT_S` default 8s) prints `{"available": false, "reason": ...}` and **exits 0**. Callers never hard-fail on Jev.

The adapter normalizes certainty so callers gate uniformly (§5): `Choice`/`Score` use the model's `confidence`; `Noul` probability `p` becomes `abs(2p-1)` (a 0.5 coin flip → 0, a certain yes/no → 1). Raw fields are preserved alongside.

## 3. Fallback Ladder

| Rung | Condition | Behavior |
| --- | --- | --- |
| J1 | `jev` mode AND answer confidence ≥ threshold | The typed answer gates the branch |
| J2 | Confidence < threshold (answer in `dropped`) | Existing heuristic decides |
| J3 | Probe failed / call error / kill-switch | Existing heuristic decides; disclose in the log |

J2 and J3 are **today's behavior, byte for byte**. Skills add a fast path; they never rewrite the existing one.

## 4. Integration Recipe — one additive line per skill

Each integration point adds exactly one line of skill text:

> Optional Jev gate (see [jev-contract.md](jev-contract.md)): ask *<judgment>* via `dev-shared/jev/jev_ask.py` (state: *<what goes in>*, questions: *<qid: primitive + criteria>*); use the typed answer only when `available:true` and confidence ≥ *<threshold>*; otherwise proceed with the existing heuristic.

Candidate points (apply only where wanted):

| Skill step | Judgment | Primitive |
| --- | --- | --- |
| Orchestrator intent detection (`devkit.md` §4) | craft / fix / plan / repo-search / security / scenario | `Choice` |
| `hi-plan` Mode Selection + Scope Challenge | fast / full / hard; overlaps active plan? | `Choice` + `Noul` |
| `hi-plan` red-team / `hi-craft` review | per-dimension review score | `Score` |
| `hi-fix` stuck detection | root cause identified? | `Noul` |
| `hi-security` finding triage | true positive? + severity | `Noul` + `Choice` |
| `hi-scenario` severity classification | critical / high / medium / low | `Choice` |

## 5. Thresholds

Thresholds live in the skill's one line, are evaluated on the project's own data, and err low (J2 is free). Never adopt cookbook/demo defaults as universal rules.

## 6. Receipt

`hi-log` entries note the rung (J1/J2/J3) for each gate. This keeps Jev's actual value measurable before anyone hardens it into a dependency.
