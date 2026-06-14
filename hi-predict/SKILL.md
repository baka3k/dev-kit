---
name: hi-predict
description: Five expert personas independently analyze proposed changes before implementation to catch architectural, security, performance, and UX issues early. Uses mind_mcp for project context and graph_mcp for code impact analysis. Produces GO/CAUTION/STOP verdict with consensus agreements, conflict resolutions, and risk mitigations. Use before major features, refactors, or risky changes.
version: 1.0.0
last_updated: 2026-05-12
hooks:
  pre: mcp-health-check
  post: cleanup-handler
---

# HI Predict

Five-expert-persona pre-analysis that debates proposed changes using MCP-assisted code context before any code is written.

## When To Use / When NOT

Use: before major features, refactors, competing approaches, assumption stress-tests, implementation gates. Skip: trivial changes, already-approved work, pure dep upgrades, docs-only.

Required: change proposal, optional `--files <glob>` and concern areas, depth (`quick`|`deep`).

## The 5 Personas

| Persona | Focus | Core Question |
|---------|-------|---------------|
| **Architect** | System design, scalability, coupling | Does this fit the architecture and scale without new coupling? |
| **Security** | Attack surface, data protection, auth | What can be abused and where is data exposed? |
| **Performance** | Latency, memory, queries, resources | What is the latency / N+1 / memory / contention impact? |
| **UX** | User experience, accessibility, error states | Is it intuitive, accessible, with clear error states? |
| **Devil's Advocate** | Hidden assumptions, simpler alternatives | Why not do nothing, and which assumption could be wrong? |

## Input Validation

`proposal`: non-empty, 10-5000 chars, natural language (no code-only). `depth`: `quick` (default) or `deep`.

## Performance

Timeouts: phase 0=180s, phase 1=300s, phase 2=180s, phase 3=60s; total=720s (12min). Progress events: phase_start, persona_progress, conflict_resolving, final_summary.

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

**Phase 0 — Code Context (3min):** Parse proposal, query `mind_mcp.hybrid_search` (architecture docs) and `graph_mcp.explore_graph` + `trace_flow` (affected code/runtime path), build context package.

**Phase 1 — Independent Analysis (5min):** Each persona analyzes in isolation (no cross-reading), using MCP context + code reading. Record findings per the `persona_output_format` below.

**Phase 2 — Consensus Debate (3min):** Compare outputs side-by-side. Agreements = 4+ personas align. Conflicts = meaningful disagreement → weigh tradeoffs, document resolution with rationale per `conflict_resolution_rules`.

**Phase 3 — Verdict & Report (1min):** Synthesize findings, generate risk summary, produce recommendations, format report. `GO`: 0 Critical, <3 High, clear mitigations. `CAUTION`: 1-2 mitigatable Critical OR 3+ High. `STOP`: any unmitigatable Critical or false assumption detected.

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

  performance:
    bottlenecks: ["bottleneck 1"]
    metrics_impact: "latency +Xms, queries +N"
    alternatives: ["alternative 1"]

  ux:
    issues: ["issue 1"]
    edge_cases: ["edge case 1"]
    a11y_concerns: ["a11y concern 1"]

  devils_advocate:
    assumptions_challenged: ["assumption 1"]
    simpler_alternatives: ["alternative 1"]
    worst_case: "description of worst case"
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

Minimum report fields: title + date + depth + verdict; executive summary (2-3 sentences); agreements list; conflicts table (topic × 5 personas + resolution); risk summary table (risk/severity/persona/mitigation); per-persona detail block (concerns, threats, bottlenecks, issues, challenged assumptions + recommendations/mitigations/impact/alternatives); numbered recommendations with rationale; next steps tied to verdict (GO → hi-plan, CAUTION → address mitigations, STOP → redesign).

---

## Non-Negotiable Rules

- Personas MUST analyze independently — no cross-contamination during analysis phase
- Security persona findings always weighted higher for auth/data concerns
- Devil's Advocate must challenge at least one core assumption
- STOP verdict requires explicit documentation of what must change
- Every risk must have a concrete mitigation, not just identification
- Conflict resolutions must include rationale, not just the winner

## Error Handling & Fallback

Preflight: validate proposal, abort on failure. MCP-unavailable: skip code context, analyze proposal text only, mark code-derived findings lower confidence, note "MCP unavailable". Persona timeout: mark incomplete and continue. Unresolvable conflict: document as unresolved in report.

## Known Limitations

- Static analysis only — cannot predict runtime behavior; quality depends on proposal detail; MCP-unavailable mode is less confident.
- Personas cannot ask clarifying questions (one-pass); business nuances may be missed without domain expert input.

## Deliverables

- `prediction_report_{timestamp}.md` — Full prediction report with all persona analyses, conflicts, verdict, and recommendations

## References

- `references/persona-playbook.md` — Detailed analysis framework per persona with example prompts
