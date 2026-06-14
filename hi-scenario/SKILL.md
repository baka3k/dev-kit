---
name: hi-scenario
description: Generate comprehensive edge cases and test scenarios by decomposing features across 12 dimensions (user types, input extremes, timing, scale, state, environment, errors, authorization, data integrity, integration, compliance, business logic). Uses mind_mcp for feature requirements context and graph_mcp for code path discovery. Use before implementation, during code review, or when planning test coverage.
version: 1.0.0
last_updated: 2026-05-12
hooks:
  pre:
    - name: input-validation
      scope: [target_source, analysis_depth]
      enable_redaction: true
    - name: mcp-health-check
  post:
    - name: cleanup-handler
      paths: [scenario-data/]
      keep: [*.json, *.md]
---

# HI Scenario

Edge case and scenario explorer that decomposes features across 12 dimensions with MCP-assisted code path discovery and comprehensive security hardening.

## Usage

**When to use**: complex/stateful features, test authoring, planning risk assessment, API design review, refactoring critical paths, security review, onboarding to unfamiliar features.
**Avoid**: trivial/cosmetic changes, well-tested stable code, pure config changes, simple CRUD with no logic, docs-only.
**Inputs**: target (path/glob/description), depth (`quick`|`deep`), optional focus dimensions, optional severity filter.

## Input Validation & Security

- **Path**: must exist & be readable; block `../`; whitelist `[a-zA-Z0-9_\-./]`; max 1000 chars.
- **Depth**: `quick` (default, major paths) or `deep` (all branches, 12 dimensions).

## Performance & Operational Configuration

- **Timeouts**: p0=120s, p1=30s, p2=300s, p3=60s, p4=60s; total=600s.
- **Progress**: report on phase start/complete, dimension progress, and final summary (counts by severity).

---

## The 12 Decomposition Dimensions

Not all 12 apply to every feature. Filter relevant dimensions first, then generate scenarios only for those.

| # | Dimension | What to Look For |
|---|-----------|------------------|
| 1 | **User Types** | admin, guest, banned, new user, bot |
| 2 | **Input Extremes** | empty, null, max length, unicode, injection |
| 3 | **Timing** | concurrent, race, timeout, retry storms |
| 4 | **Scale** | 0, 1, 1M items, pagination wrap |
| 5 | **State Transitions** | first use, abort, resume, partial |
| 6 | **Environment** | mobile, no JS, screen reader, VPN |
| 7 | **Error Cascades** | DB down, OOM, partial write |
| 8 | **Authorization** | expired token, wrong role, CSRF |
| 9 | **Data Integrity** | duplicates, orphans, encoding mismatch |
| 10 | **Integration** | webhook replay, version mismatch, outage |
| 11 | **Compliance** | GDPR, audit gap, PII exposure |
| 12 | **Business Logic** | edge pricing, coupon stacking, refunds |

Full checklist per dimension: `references/dimension-checklist.md`

---

## Severity Criteria

| Level | Meaning |
|-------|---------|
| **Critical** | Data loss, security breach, auth bypass, silent corruption |
| **High** | Feature broken for a subset of users, data inconsistency |
| **Medium** | Degraded UX, recoverable error not surfaced to user |
| **Low** | Minor visual glitch, non-blocking warning |

---

## Orchestration Workflow

### Phase 0: Target Analysis (2min)

1. Validate target, read source files.
2. Query graph_mcp: `explore_graph` (limit 50), `trace_flow` (depth 5), `find_paths` to error handlers (max 10).
3. Query mind_mcp: `hybrid_search` for feature requirements (limit 10).
4. Identify entry points, state mutations, external calls.
5. Report: "Phase 0 complete: Target analyzed".

### Phase 1: Dimension Filtering (30s)

1. Evaluate each of 12 dimensions against target; mark applicable/skipped with reason.
2. Prioritize by risk; report "{applicable}/{total} dimensions applicable".

```yaml
dimension_applicability:
  user_types: "Applicable if feature has role-based behavior"
  input_extremes: "Applicable if feature accepts user input"
  timing: "Applicable if concurrent access or async operations"
  scale: "Applicable if feature processes collections"
  state_transitions: "Applicable if feature has multi-step flows"
  environment: "Applicable if feature runs in browser or client"
  error_cascades: "Always applicable for server-side code"
  authorization: "Applicable if feature has access control"
  data_integrity: "Applicable if feature writes to database"
  integration: "Applicable if feature calls external services"
  compliance: "Applicable if feature handles user data"
  business_logic: "Applicable if feature has pricing/rules"
```

### Phase 2: Scenario Generation (5min)

1. For each applicable dimension, generate 3-5 scenarios (concrete, reproducible, implementation-agnostic).
2. Use graph_mcp flow traces; use mind_mcp for business logic validation.
3. Prioritize high-risk dimensions first; skip skipped dimensions.
4. Report: "Phase 2 complete: {count} scenarios generated".

```yaml
scenario_template:
  - dimension: "Which of the 12 dimensions"
  - scenario: "Concrete description of the edge case"
  - trigger: "How to reproduce"
  - expected: "What should happen"
  - evidence: "mind_mcp | graph_mcp | filesystem"
```

### Phase 3: Severity Classification (1min)

Classify each scenario: **Critical** (data loss, auth bypass, silent corruption), **High** (subset broken, data inconsistency), **Medium** (degraded UX, recoverable), **Low** (visual glitch, non-blocking). Auth bypass and data exposure are always Critical; silent corruption is always Critical; UI-only = Low. Report: "Phase 3 complete: Scenarios classified".

### Phase 4: Report Generation (1min)

1. Aggregate by dimension & severity; format as table.
2. Include applicability summary, test priorities (Critical → immediate).
3. Report: "Phase 4 complete: Report generated".

---

## Output Contract

Report: `# Scenario Report — {target}` with header (date, depth, source), Dimensions Analyzed list, Skipped table, Scenarios table (#, Dimension, Scenario, Severity, Expected), Severity Summary (Critical/High/Medium/Low/Total), Test Priorities (Immediate=Critical, sprint=High, backlog=M+L), Evidence Sources (mind_mcp/graph_mcp/filesystem).

---

## Non-Negotiable Rules

- Every scenario must be concrete and reproducible
- Filter dimensions before generating — do not generate noise
- Critical findings must have specific expected behavior described
- Auth bypass or data exposure always classified as Critical
- Never skip error cascades dimension for server-side code
- Provide reason for every skipped dimension
- Graph-derived scenarios must reference actual code paths

---

## Error Handling & Fallback Strategy

- **Preflight**: validate target exists/readable (abort on fail); check graph_mcp + mind_mcp capabilities (fall back to filesystem-only on fail).
- **MCP unavailable fallback**: manual code reading — skip MCP, derive call paths from static analysis, skip business context, mark graph-derived scenarios lower confidence.
- **Recovery**: p0 MCP timeout → filesystem analysis; p2 dimension timeout → skip & continue; p4 partial data → generate partial report.

---

## Observability & Metrics

Track: total scenarios, dimensions analyzed/skipped, avg per dimension, severity distribution (Critical/High/Medium/Low), and evidence coverage (MCP-sourced vs filesystem-sourced).

---

## Version History & Changelog

v1.0.0 (2026-05-12): 12-dimension framework, MCP-assisted code path discovery, mind_mcp business context, severity classification, dimension filtering with skip reasons, structured report, MCP fallback, dimension checklist.

---

## Known Limitations

- **Analysis scope**: static analysis only (no runtime simulation); quality depends on graph_mcp paths and mind_mcp docs.
- **Dimension coverage**: not all 12 apply per feature; rare edges may be missed; concurrent access needs runtime verification.
- **MCP-dependent**: deep analysis requires graph_mcp; business context requires mind_mcp; filesystem-only mode yields simpler scenarios.

---

## Deliverables

- `scenario_report_{target}_{timestamp}.md` — Full scenario report with dimension analysis

---

## References

### Skill-Specific References

- `references/dimension-checklist.md` — Detailed checklist per dimension with example scenarios
