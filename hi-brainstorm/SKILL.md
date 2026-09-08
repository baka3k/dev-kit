---
name: hi-brainstorm
description: Convene an adaptive panel of independent experts to generate competing solutions, challenge assumptions, debate tradeoffs, and select an evidence-backed option with weighted scoring before implementation. Use for ambiguous, consequential, or multi-path decisions; skip trivial work with one obvious reversible solution.
version: 1.1.0
last_updated: 2026-09-08
---

# HI Brainstorm

Run a structured expert council before implementation. The outcome is a decision and handoff, not permission to perform work beyond the user's request.

## Required Input

Establish: the problem or decision; desired outcomes and measurable success criteria; constraints and non-negotiables; known evidence, affected scope, and candidate options. Ask only when a missing answer could materially change the selected solution; otherwise state bounded assumptions and lower confidence.

Modes: `quick` (3 lenses, 2–3 options, one rebuttal round — omit non-decision-relevant lenses, always keep the skeptic plus a domain or architecture lens, record omissions), `standard` (default: 5 lenses, 3–5 options, initial + final scoring), `deep` (standard + broader evidence, validation experiments, second rebuttal round).

## Council

Moderator frames the decision, protects independence, consolidates options, calculates results, writes the decision; never invents a preferred option or silently changes scores. Lenses: Domain, Systems architect, Delivery engineer, User/value, Risk skeptic (always retain the skeptic; adapt/split as needed).

Independence: when collaboration agents are available and delegation allowed, one expert brief per subagent (isolated forks, same neutral context packet, run concurrently); experts never see each other's initial conclusions. If isolated contexts are unavailable, run clearly separated passes, disclose the fallback, lower confidence — never describe sequential self-analysis as independent parallel agents.

## Workflow

1. **Frame and ground** — normalize goal, measures, constraints, deadline, evidence gaps; gather repository context per the project's search order; distinguish verified facts, user statements, assumptions.
2. **Generate independently** — each expert proposes ≥1 solution (mechanism, benefits, costs, assumptions, failure modes, falsification test).
3. **Form the candidate set** — merge duplicates, preserve distinct mechanisms (3–5 options; never drop a user-mandated candidate for count); same decision horizon and scope; merge hybrids whose near-term mechanism matches a base option; include status quo or a reversible experiment when credible; anonymize origins.
4. **Apply hard gates** — `fail` any option that violates a non-negotiable/verified constraint, has an unresolved critical security/privacy/legal issue, is infeasible under verified limits, or intrinsically depends on an excluded action. Use `conditional` when a blocker has a concrete mitigation. Never average a failure away. Lack of post-council authorization is not an option failure.
5. **Score independently** — 1–5 (1 unacceptable, 5 excellent). Weighted score = `sum(weight × median rating / 5)`, 0–100. Preserve dispersion and dissent. Use `scripts/score_options.py` when multiple experts and options exist.

| Criterion | Weight | High score means |
|---|---:|---|
| Goal fit | 25 | Directly satisfies the desired outcome |
| Evidence and feasibility | 20 | Supported and realistically implementable |
| Risk and safety | 20 | Low residual risk with credible controls |
| Delivery cost | 15 | Lower effort, complexity, disruption |
| Maintainability and reversibility | 10 | Easy to own, change, roll back |
| User value and time to value | 10 | Valuable results arrive quickly |

Customize weights only when the decision requires it, explaining why; total stays 100. Every rating needs evidence or a marked assumption, confidence, and veto concerns.

6. **Debate and rebut** (panel playbook: [references/panel-playbook.md](references/panel-playbook.md)) — each expert objects to the leader, names a ranking-reversing assumption, steelmans a rival, proposes a mitigation or concedes. Revise only on evidence; re-check horizons and merge sequencing-only variants; re-score and record material changes.
7. **Decide** — `SELECT`: top ≥75, lead ≥5, all gates pass, no unresolved critical objection. `CONDITIONAL`: top ≥65 but narrow lead, low confidence, or required mitigations. `NO DECISION`: gates fail, top <65, decisive information missing, or critical conflict unresolved. Ties: goal fit → lower risk → reversibility → lower cost. Consensus not required; preserve principled dissent.
8. **Handoff** — produce the output contract (decision + confidence, frame, panel + fallback, options + gates, scorecards + deltas, objections/mitigations/dissent, selected solution or exact missing evidence, conditions + handoff). If implementation was already authorized, pass the option and conditions into planning; otherwise stop — selection never grants authorization. For a high-risk selected change, follow with `hi-predict`.

## Non-Negotiable Rules

- Independent generation happens before cross-reading or debate.
- Compare materially distinct solutions, not cosmetic variants.
- Every rating has evidence or an explicitly marked assumption.
- A critical gate cannot be overruled by voting or a high average.
- The moderator documents score changes, tie-breaks, and dissent.
- Stop with `NO DECISION` instead of manufacturing certainty.

Save a report file only when the user requests a persistent artifact.
