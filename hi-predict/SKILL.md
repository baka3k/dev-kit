---
name: hi-predict
description: Five expert personas independently stress-test one proposed change before implementation to catch architectural, security, performance, and UX issues early. Grounds findings in code impact evidence (hi-scout --impact over mind_mcp and graph_mcp) and produces a GO/CAUTION/STOP verdict with consensus agreements, conflict resolutions, and risk mitigations. Use before major features, refactors, or risky changes once an approach is chosen; use hi-brainstorm first when competing options still need selection.
argument-hint: "<change proposal> [--files <glob>] [quick|standard|deep]  — default: standard"
metadata:
  author: baka3k
  version: "1.1.0"
  last_updated: "2026-10-24"
hooks:
  pre: mcp-health-check
  post: cleanup-handler
---

# HI Predict

Five-persona pre-mortem that stress-tests one chosen proposal with evidence-grounded code context before any code is written. The outcome is a verdict with mitigations — not a choice between competing options, and not authorization to implement.

## When To Use / When NOT

Use: before major features, refactors, assumption stress-tests, and implementation gates — once a single approach is on the table. Skip: trivial changes, already-approved work with unchanged scope, pure dependency upgrades, docs-only changes.

Boundary with `hi-brainstorm`: this skill stress-tests one proposal; it does not select among alternatives. When competing options still need selection, run `hi-brainstorm` first and feed its selected option and conditions here (`hi-brainstorm` already hands high-risk selections to this skill). A `STOP` that invalidates the core approach returns the decision to `hi-brainstorm`.

Required: change proposal, optional `--files <glob>` and concern areas, depth (`quick`|`standard`|`deep`).

Depth never drops a persona — all five always run; it controls context coverage and debate rounds, following the depth levels in [dev-shared/retrieval-protocol.md](../dev-shared/retrieval-protocol.md). `quick`: module boundaries and direct callers/callees only, one debate pass, condensed report. `standard` (default): full impact evidence (callers, dependencies, affected workflows), full four-phase pipeline. `deep`: standard + verified cross-module and runtime paths, a second challenge round against the draft consensus, and explicit flip conditions.

## The 5 Personas

| Persona | Focus | Core Question |
|---------|-------|---------------|
| **Architect** | System design, scalability, coupling | Does this fit the architecture and scale without new coupling? |
| **Security** | Attack surface, data protection, auth | What can be abused and where is data exposed? |
| **Performance** | Latency, memory, queries, resources | What is the latency / N+1 / memory / contention impact? |
| **UX** | User experience, accessibility, error states | Is it intuitive, accessible, with clear error states? |
| **Devil's Advocate** | Hidden assumptions, simpler alternatives | Why not do nothing, and which assumption could be wrong? |

## Input Validation

`proposal`: non-empty, 10-5000 chars, natural language (no code-only). `depth`: `quick`, `standard` (default), or `deep`.

## Performance

Timeouts (`standard`): phase 0=180s, phase 1=300s, phase 2=180s, phase 3=60s; total=720s (12min). `quick` should finish well inside these; `deep` adds one extra 180s Phase 2 round. Progress events: phase_start, persona_progress, conflict_resolving, final_summary.

---

## Verdict Levels

| Verdict | Meaning |
|---------|---------|
| **GO** | All personas aligned, no critical risks, proceed with confidence |
| **CAUTION** | Concerns exist but manageable — mitigations identified, proceed carefully |
| **STOP** | Critical unresolved issue found — redesign or more information needed |

### STOP Triggers (any one is sufficient)

- Security persona identifies auth bypass or data exposure with no viable mitigation
- Architect identifies fundamental design incompatibility requiring significant rework
- Performance persona identifies unacceptable latency or query explosion with no workaround
- Devil's Advocate exposes a false assumption that invalidates the entire approach

---

## Orchestration Workflow

**Phase 0 — Code Context (3min):** Parse the proposal into named symbols, scoped files (`--files`), and affected workflows. Gather impact evidence with `hi-scout --impact` at the chosen depth, or follow [dev-shared/retrieval-protocol.md](../dev-shared/retrieval-protocol.md) directly when delegation is unavailable: resolve named functions first, then collect callers/callees, indirect or callback-aware paths, affected workflows with severity, and dependency-ordering risk; route graph intents per [dev-shared/graph-function-selection.md](../dev-shared/graph-function-selection.md) and discover live tool schemas before use. Build one neutral, evidence-scoped context packet per the shared council contract ([dev-shared/expert-council.md](../dev-shared/expert-council.md); predict-specific sections in [references/persona-playbook.md](references/persona-playbook.md)) that separates verified facts, user statements, assumptions, and unknowns with stable IDs. It must contain no verdict, preferred mitigation, or persona conclusion.

**Phase 1 — Independent Analysis (5min):** Every persona receives the same packet and analyzes in isolation. When collaboration agents are available and delegation is allowed, run one persona brief per subagent (isolated forks, same packet, concurrently); personas never see each other's output before Phase 2. If isolated contexts are unavailable, run clearly separated sequential passes, disclose the fallback in the report, and lower confidence — never describe sequential self-analysis as independent parallel agents. Each finding cites packet evidence IDs or is marked as an assumption. Record findings per `persona_output_format` below.

**Phase 2 — Consensus Debate (3min):** Compare outputs side-by-side. Agreements = 4+ personas align. Conflicts = meaningful disagreement → weigh tradeoffs, document resolution with rationale per `conflict_resolution_rules`. In `deep`, run a second challenge round (playbook: [references/persona-playbook.md](references/persona-playbook.md)): each persona rebuts the draft consensus, names the assumption most likely to flip the verdict, and proposes a mitigation or concedes; revise only on evidence and record what changed.

**Phase 3 — Verdict & Report (1min):** Synthesize findings, generate risk summary, produce recommendations, format report. `GO`: 0 Critical, <3 High, clear mitigations. `CAUTION`: 1-2 mitigatable Critical OR 3+ High. `STOP`: any unmitigatable Critical or false assumption detected. In `deep`, also list flip conditions: the evidence that would move the verdict up or down.

```yaml
persona_output_format:
  architect:
    concerns: ["concern 1", "concern 2"]
    recommendations: ["action 1", "action 2"]
    confidence: "high|medium|low"

  security:
    threats: ["threat 1", "threat 2"]
    severity: "critical|high|medium|low"
    mitigations: ["mitigation 1"]
    confidence: "high|medium|low"

  performance:
    bottlenecks: ["bottleneck 1"]
    metrics_impact: "latency +Xms, queries +N"
    alternatives: ["alternative 1"]
    confidence: "high|medium|low"

  ux:
    issues: ["issue 1"]
    edge_cases: ["edge case 1"]
    a11y_concerns: ["a11y concern 1"]
    confidence: "high|medium|low"

  devils_advocate:
    assumptions_challenged: ["assumption 1"]
    simpler_alternatives: ["alternative 1"]
    worst_case: "description of worst case"
    confidence: "high|medium|low"
```

```yaml
conflict_resolution_rules:
  - "Security vs Performance → Security wins unless performance makes system unusable"
  - "Architect vs UX → Defer to UX for user-facing features, Architect for backend"
  - "Devil's Advocate vs Everyone → If assumption is unvalidated, CAUTION"
  - "Any persona at Critical severity → cannot be GO"
```

---

## Output Contract

Minimum report fields: title + date + depth + isolation mode (parallel subagents | sequential fallback) + verdict; executive summary (2-3 sentences); context coverage (tools used or unavailable, evidence IDs); agreements list; conflicts table (topic × 5 personas + resolution); risk summary table (risk/severity/persona/mitigation/evidence); per-persona detail block (concerns, threats, bottlenecks, issues, challenged assumptions + recommendations/mitigations/impact/alternatives); numbered recommendations with rationale; flip conditions (`deep`); next steps tied to verdict (GO → hi-plan, CAUTION → address mitigations, STOP → redesign, or return to hi-brainstorm when the approach itself must be re-selected).

---

## Non-Negotiable Rules

- Personas MUST analyze independently — no cross-contamination during analysis phase; the isolation mode actually used is reported honestly
- Depth never removes a persona
- Security persona findings always weighted higher for auth/data concerns
- Devil's Advocate must challenge at least one core assumption
- STOP verdict requires explicit documentation of what must change
- Every risk must have a concrete mitigation, not just identification
- Conflict resolutions must include rationale, not just the winner

## Error Handling & Fallback

Preflight: validate proposal, abort on failure. Code context unavailable (hi-scout or every retrieval layer fails): analyze proposal text only, mark code-derived findings lower confidence, note "code context unavailable". Persona timeout: mark incomplete and continue. Unresolvable conflict: document as unresolved in report.

## Known Limitations

- Static analysis only — cannot predict runtime behavior; quality depends on proposal detail; the no-code-context mode is less confident.
- Personas cannot ask clarifying questions (one-pass); business nuances may be missed without domain expert input.

## Deliverables

- `prediction_report_{timestamp}.md` — Full prediction report with all persona analyses, conflicts, verdict, and recommendations. Write it when the user wants a persistent artifact (location per `hi-project-organization`); otherwise return the report inline.

## References

- [references/persona-playbook.md](references/persona-playbook.md) — Predict packet sections, isolated persona brief with example prompts, per-persona focus/questions/red flags, and the `deep` challenge round
- [dev-shared/expert-council.md](../dev-shared/expert-council.md) — Shared council contract: evidence ledger, packet neutrality, independence, debate discipline
