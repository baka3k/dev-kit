# Security Audit Workflow Detail

Phase-level detail for `hi-security`. Checklists live in [stride-owasp-checklist.md](stride-owasp-checklist.md).

## Severity Definitions

| Severity | Description | Fix Priority |
| --- | --- | --- |
| **Critical** | Exploitable now — data breach, RCE, or auth bypass risk | Immediate — block release |
| **High** | Exploitable with moderate effort, significant impact | This sprint |
| **Medium** | Limited exploitability or impact | Next sprint |
| **Low** | Theoretical risk, defense-in-depth improvement | Backlog |
| **Info** | Best practice suggestion, no direct risk | Optional |

## Phase 0: Scope Resolution

1. Validate inputs (source path, scope, mode, focus).
2. Expand scope glob to file list; classify files by type.
3. Filter in-scope (exclude test fixtures, examples, docs).
4. Query mind_mcp for security policy context if available.
5. Report: "Phase 0 complete: {count} files in scope".

## Phase 1: STRIDE Analysis

Per in-scope file, analyze per STRIDE category (checks: [stride-owasp-checklist.md](stride-owasp-checklist.md)). Use graph_mcp for entry points (`list_up_entrypoint`), auth flows, and data paths (`trace_flow` with `rel_types:["CALLS","POSSIBLE_CALLS"]`; `get_api_call_chain` for endpoint-to-database chains) — selection per `dev-shared/graph-function-selection.md`. Use mind_mcp for security documentation context. Record findings with file:line, category, description. Cache to `security_findings_cache.json` section `stride_findings`.

```yaml
mcp_functions:
  - graph_mcp.semantic_search [required]
    params: {query: "auth authenticate authorize guard middleware", limit: 50}
    expected: "Authentication and authorization code"
  - graph_mcp.explore_graph [required]
    params: {start_nodes: auth-related functions, depth: 5}
    expected: "Call paths for auth flows"
  - graph_mcp.search_by_code [required]
    params: {query: "password secret token hash encode base64"}
    expected: "Hardcoded secret and crypto sink locations"
  - graph_mcp.list_up_entrypoint [required]
    params: {modules: "{in-scope modules}"}
    expected: "Attack surface: externally reachable entry points"
  - mind_mcp.hybrid_search [optional]
    params: {query: "security policy compliance", collection: "{collection}", limit: 10}
    expected: "Security policies and compliance requirements"
```

## Phase 2: Dependency Audit

Detect stack (`package.json` / `requirements.txt` / `go.mod` / `Gemfile` / `pom.xml` / `Cargo.toml`), run the matching audit tool, parse CVEs; record `cve, package, severity, fix_version, recommendation`. Commands per stack in [stride-owasp-checklist.md](stride-owasp-checklist.md) §Dependency Audit Commands.

## Phase 3: Secret Detection

Scan all in-scope files for secret patterns ([stride-owasp-checklist.md](stride-owasp-checklist.md) §Secret Patterns to Detect). Skip false positives in test files, examples, placeholders (`YOUR_KEY_HERE`, `<your-token>`, TODO; `*.test.*`, `*.spec.*`, `*.example`, `tests/`, `fixtures/`). Record file:line, pattern matched, context.

## Phase 4: OWASP Top 10 Mapping

Map STRIDE findings to OWASP Top 10; dependency findings → A06; secret exposures → A02 or A05. OWASP quick reference: [stride-owasp-checklist.md](stride-owasp-checklist.md).

## Phase 5: Fix Execution (audit-fix only)

Sort findings Critical → High → Medium (Low/Info document-only). Per finding, up to `max_iterations`: minimal targeted fix → verify → commit on pass, revert on fail.

## Phase 6: Report Generation

Aggregate findings by severity; format the findings table with file:line references + fix recommendations + STRIDE and OWASP columns; add OWASP coverage, dependency status, secret exposure, prioritized next steps. Report fields not in the JSON contract: Date, Mode, Scope description, Fixes applied (X/Y).

## Progress Reporting

Report on phase start/complete with running severity counts (`Critical={c}, High={h}, Medium={m}`), per-task progress (scanning/analyzing/fixing with counters), and a final summary (files scanned, findings by severity, fixes applied).

## Fallback & Error Handling

- Preflight: abort on invalid source/scope; MCP unavailable → filesystem-only audit (grep/find, pattern-based STRIDE, lower confidence); secret detection runs regardless.
- Per-phase: empty scope → abort; MCP timeout → filesystem patterns; missing tool → skip+warn; oversized file → skip; verify fail → revert fix; partial data → partial report.

## Observability

Track: `files_scanned`, `lines_analyzed`, `scan_duration_seconds`, findings by severity, `fixes_attempted/applied/failed/reverted`, `verification_failures`, `mcp_calls_total`, `mcp_cache_hit_rate`.

## Known Limitations

Static analysis only — no runtime detection; distributed auth flows spanning repos may be missed. Dependency audit requires per-stack tooling and may miss transitive deps without lockfiles; vendor-patched deps can show false CVEs. Secret detection is pattern-based (misses custom formats, possible false positives, no binary detection). Automated fixes may need manual review; auth changes are conservative; fixes are one-at-a-time.

## Version History

- v1.1.0 (2026-09-08): SKILL.md compressed to router; phase detail moved here.
- v1.0.0 (2026-05-12): Initial release — STRIDE (6 categories), OWASP Top 10 mapping, MCP-assisted discovery, dependency audit, secret detection, severity ranking, audit-fix mode, MCP filesystem fallback.
