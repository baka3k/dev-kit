# Scenario Workflow Detail

Phase-level detail for `hi-scenario`. The SKILL.md owns the dimension table, severity table, and rules.

## Phase 0: Target Analysis

1. Validate target, read source files.
2. Query graph_mcp: `semantic_search`/`explore_graph` for candidates; `search_functions(query, parser_type)` when only a function name is known. For retained IDs: `query_subgraph(direction:"all", max_depth:2)` for nearby callers/callees; `trace_flow` (direction `out`/`in`, `rel_types:["CALLS","POSSIBLE_CALLS"]`, `max_depth:6`) for indirect/callback paths; `find_paths` when both trigger and error-handler IDs are known (max 10 paths). Add `find_workflows_containing` and `analyze_workflow_impact` for blast radius of edge-case anchors (matrix: `dev-shared/graph-function-selection.md`).
3. Query mind_mcp: `hybrid_search` for feature requirements (limit 10).
4. Identify entry points, state mutations, external calls.
5. Report: "Phase 0 complete: Target analyzed".

## Phase 1: Dimension Filtering

Evaluate each of the 12 dimensions against the target; mark applicable/skipped with reason; prioritize by risk; report "{applicable}/{total} dimensions applicable".

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

## Phase 2: Scenario Generation

For each applicable dimension, generate 3–5 concrete, reproducible, implementation-agnostic scenarios. Use graph_mcp flow traces; mind_mcp for business logic validation. Prioritize high-risk dimensions first. Report: "Phase 2 complete: {count} scenarios generated".

```yaml
scenario_template:
  - dimension: "Which of the 12 dimensions"
  - scenario: "Concrete description of the edge case"
  - trigger: "How to reproduce"
  - expected: "What should happen"
  - evidence: "mind_mcp | graph_mcp | filesystem"
```

## Phase 3: Severity Classification

Classify each scenario: **Critical** (data loss, auth bypass, silent corruption), **High** (subset broken, data inconsistency), **Medium** (degraded UX, recoverable), **Low** (visual glitch, non-blocking). Auth bypass, data exposure, and silent corruption are always Critical; UI-only is Low. Report: "Phase 3 complete: Scenarios classified".

## Phase 4: Report Generation

Aggregate by dimension and severity; format as table; include applicability summary and test priorities (Critical → immediate). Report: "Phase 4 complete: Report generated".

## Output Contract

`# Scenario Report — {target}` with header (date, depth, source), Dimensions Analyzed list, Skipped table, Scenarios table (#, Dimension, Scenario, Severity, Expected), Severity Summary (Critical/High/Medium/Low/Total), Test Priorities (Immediate=Critical, sprint=High, backlog=M+L), Evidence Sources (mind_mcp/graph_mcp/filesystem). Deliverable: `scenario_report_{target}_{timestamp}.md`.

## Error Handling & Fallback

- Preflight: validate target exists/readable (abort on fail); check graph_mcp + mind_mcp capabilities (fall back to filesystem-only on fail).
- MCP unavailable: manual code reading — skip MCP, derive call paths from static analysis, skip business context, mark graph-derived scenarios lower confidence.
- Recovery: p0 MCP timeout → filesystem analysis; p2 dimension timeout → skip & continue; p4 partial data → partial report.

## Performance & Operational Configuration

Timeouts: p0=120s, p1=30s, p2=300s, p3=60s, p4=60s; total=600s. Report on phase start/complete, dimension progress, final summary.

## Observability & Metrics

Total scenarios, dimensions analyzed/skipped, avg per dimension, severity distribution, evidence coverage (MCP-sourced vs filesystem-sourced).

## Known Limitations

Static analysis only (no runtime simulation); quality depends on graph_mcp paths and mind_mcp docs; rare edges may be missed; concurrent access needs runtime verification; filesystem-only mode yields simpler scenarios.

## Version History

- v1.1.0 (2026-09-08): SKILL.md compressed to router; phase detail moved here.
- v1.0.0 (2026-05-12): 12-dimension framework, MCP-assisted code path discovery, mind_mcp business context, severity classification, dimension filtering with skip reasons, structured report, MCP fallback, dimension checklist.
