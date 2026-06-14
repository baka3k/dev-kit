---
name: hi-security
description: STRIDE + OWASP-based security audit with MCP-assisted code analysis and optional iterative auto-fix. Scans code using graph_mcp for structure discovery and mind_mcp for security policy context, then produces severity-ranked findings with fix recommendations. Supports audit-only and audit+fix modes. Use before releases, after sensitive feature additions, or for periodic compliance reviews.
version: 1.0.0
last_updated: 2026-05-12
hooks:
  pre:
    - name: mcp-health-check
      timeout: 10s
    - name: input-validation
      scope: [source_root, audit_scope]
      enable_redaction: true
  post:
    - name: output-redaction
      apply_to: [audit_report, findings_log]
    - name: cleanup-handler
      paths: [security-audit-data/]
      keep: [*.json, *.md]
---

# HI Security

STRIDE + OWASP security audit with MCP-assisted code analysis, dependency scanning, secret detection, and optional iterative auto-fix with comprehensive security hardening.

## When To Use

- Before releases, after auth/payment/data features, periodic reviews, compliance prep (SOC 2, GDPR, PCI-DSS), after dependency updates, when a CVE is reported
- Avoid for cosmetic-only changes, repos without user-facing code, standalone dependency audit (use `npm audit` / `pip-audit` directly), or quick unstructured reviews

## Required Inputs

- Source root path
- Audit scope: glob pattern or target directory
- Mode: `audit` or `audit-fix`
- Optional: max fix iterations (default 10)
- Optional: focus area (`auth`, `data`, `api`, `infra`, `all`)

## Modes

- `audit`: scan → categorize → report
- `audit-fix`: scan → categorize → iteratively fix (Critical→High→Medium) → verify → report

## Input Validation & Security

- **Path validation**: See env config — block `../`, whitelist `[a-zA-Z0-9_\-./*]`, max 1000 chars
- **Scope validation**: See env config — `mode ∈ {audit, audit-fix}`, `focus_area ∈ {all, auth, data, api, infra}`, `max_iterations 1-50` (default 10)

## Performance & Operational Configuration

- **Timeouts / resource limits / caching**: See env config (phase timeouts, 5000 files max, 10MB/file, 100 findings/category, 30min total; caches invalidated on scope/workflow start)
- **Progress feedback** (load-bearing):

```yaml
progress_reporting:
  phase_start: ["Phase {N} started: {phase_name}", "  Mode: {mode}, Focus: {focus_area}"]
  phase_complete: ["Phase {N} complete: {phase_name}", "  Findings so far: Critical={c}, High={h}, Medium={m}"]
  task_progress: ["Scanning: {file_path} ({current}/{total})", "Analyzing STRIDE: {category}", "Fixing: #{finding_number} of {total} ({severity})"]
  final_summary: ["Audit complete", "Files scanned: {count}", "Findings: {critical}C, {high}H, {medium}M, {low}L, {info}I", "Fixes applied: {fixed_count}"]
```

---

## Severity Definitions

| Severity | Description | Fix Priority |
|----------|-------------|-------------|
| **Critical** | Exploitable now — data breach, RCE, or auth bypass risk | Immediate — block release |
| **High** | Exploitable with moderate effort, significant impact | This sprint |
| **Medium** | Limited exploitability or impact | Next sprint |
| **Low** | Theoretical risk, defense-in-depth improvement | Backlog |
| **Info** | Best practice suggestion, no direct risk | Optional |

---

## Orchestration Workflow

### Phase 0: Scope Resolution (30s)

1. Validate inputs (source path, scope, mode, focus)
2. Expand scope glob to file list, classify files by type
3. Filter in-scope (exclude test fixtures, examples, docs)
4. Query mind_mcp for security policy context if available
5. Report: "Phase 0 complete: {count} files in scope"

### Phase 1: STRIDE Analysis (5min)

```yaml
steps:
  1. For each in-scope file, analyze per STRIDE category
  2. Use graph_mcp to discover entry points, auth flows, data paths
  3. Use mind_mcp for security documentation context
  4. Record findings with file:line, category, description
  5. Report: "Phase 1 complete: {count} STRIDE findings"

stride_categories:
  spoofing:
    checks:
      - Missing authentication on endpoints
      - Weak password hashing (MD5, SHA1)
      - JWT without expiration or server-side validation
      - Missing MFA for sensitive operations
      - Default credentials present

  tampering:
    checks:
      - SQL/NoSQL string concatenation
      - Missing CSRF tokens
      - Missing input validation
      - Unsafe deserialization
      - Unrestricted HTTP methods

  repudiation:
    checks:
      - Missing auth event logging
      - Sensitive data in logs
      - Non-append-only log storage
      - Insufficient log retention

  information_disclosure:
    checks:
      - Stack traces in error responses
      - Internal IDs in API responses
      - Plaintext sensitive data
      - HTTP endpoints for sensitive operations
      - Hardcoded secrets (detailed in Phase 3)

  denial_of_service:
    checks:
      - Missing rate limiting
      - Unbounded list queries
      - Missing request timeouts
      - ReDoS-vulnerable regex patterns
      - Unbounded background job concurrency

  elevation_of_privilege:
    checks:
      - Client-side only auth checks
      - Missing horizontal privilege checks (IDOR)
      - Weak admin endpoint protection
      - Overly permissive service accounts
      - Privilege escalation without re-authentication

# Example mcp_function block (same shape across all MCP-using phases):
mcp_functions:
  - graph_mcp.explore_graph [required]
    params: {query: "auth authenticate authorize guard middleware", limit: 50}
    output: {nodes: auth-related functions}
    expected: "Authentication and authorization code"

  - mind_mcp.hybrid_search [optional]
    params: {query: "security policy compliance", collection: "{collection}", limit: 10}
    output: {results: security policy docs}
    expected: "Security policies and compliance requirements"

cache_output:
  file: "security_findings_cache.json"
  section: "stride_findings"
```

### Phase 2: Dependency Audit (2min)

1. Detect stack (package.json / requirements.txt / go.mod / Gemfile / pom.xml / Cargo.toml)
2. Run matching audit tool, parse CVEs
3. Record `cve, package, severity, fix_version, recommendation`
4. Report: "Phase 2 complete: {count} dependency findings"

```yaml
dependency_audit_commands:
  nodejs: "npm audit --json"
  python: "pip-audit --format json"
  go: "govulncheck ./..."
  ruby: "bundle audit check --update"
  java_maven: "mvn dependency-check:check"
  rust: "cargo audit"
```

### Phase 3: Secret Detection (1min)

```yaml
steps:
  1. Scan all in-scope files for secret patterns
  2. Apply regex patterns from reference checklist
  3. Skip false positives in test files, examples, and placeholders
  4. Record findings with file:line, pattern matched, context
  5. Report: "Phase 3 complete: {count} secrets detected"

secret_patterns:
  - Generic API keys
  - AWS access key IDs (AKIA*)
  - JWT tokens
  - Hardcoded passwords
  - Private keys (PEM format)
  - GitHub tokens (ghp_*)
  - Stripe keys (sk_live_*, sk_test_*)
  - Bearer tokens
  - Database connection strings with credentials

false_positive_exclusions:
  - Files matching *.test.*, *.spec.*, *.example
  - Files in test/, tests/, __tests__/, fixtures/
  - Placeholder values: YOUR_KEY_HERE, <your-token>, TODO
```

### Phase 4: OWASP Top 10 Mapping (1min)

1. Map STRIDE findings to OWASP Top 10 categories
2. Map dependency findings → A06; secret exposures → A02 or A05
3. Annotate each finding, then report "Phase 4 complete: Findings mapped to OWASP"

```yaml
owasp_categories:
  A01: "Broken Access Control"
  A02: "Cryptographic Failures"
  A03: "Injection"
  A04: "Insecure Design"
  A05: "Security Misconfiguration"
  A06: "Vulnerable and Outdated Components"
  A07: "Identification and Authentication Failures"
  A08: "Software and Data Integrity Failures"
  A09: "Security Logging and Monitoring Failures"
  A10: "Server-Side Request Forgery (SSRF)"
```

### Phase 5: Fix Execution (10min, only in audit-fix mode)

1. Sort findings Critical → High → Medium
2. Per finding (up to `max_iterations`): apply minimal targeted fix → run verify → commit on pass, revert on fail
3. Skip Low/Info (document only)
4. Report: "Phase 5 complete: {fixed}/{attempted} fixes applied"

```yaml
fix_guard_rules:
  - Never fix more than one issue per iteration
  - Test must pass before advancing to next fix
  - Critical auth changes require manual review
  - Do not modify test files or configuration secrets
```

### Phase 6: Report Generation (1min)

1. Aggregate findings by severity, generate summary stats
2. Format findings table with file:line references + fix recommendations
3. Add OWASP coverage summary, dependency status, secret exposure
4. Generate prioritized next-step recommendations
5. Report: "Phase 6 complete: Audit report generated"

---

## Fix Mode Details

When mode is `audit-fix`:

1. **Fix ordering**: Critical before High before Medium. Low and Info are document-only.
2. **One fix at a time**: Apply, verify, commit or revert before next.
3. **Verification gate**: Run project test suite after each fix. Fail = revert.
4. **Commit convention**: `security(fix-{N}): {category} — {short description}`
5. **Iteration cap**: Stop after `max_iterations` fixes even if more remain.
6. **Auth restrictions**: Changes to authentication/authorization code are flagged for manual review.

---

### Report Format

Markdown report fields not in the YAML output contract: **Date**, **Mode** (`audit`/`audit-fix`), **Scope description**, **Fixes applied** (X/Y), and per-row **STRIDE** + **OWASP** columns in the findings table.

---

## Non-Negotiable Rules

- Never skip authentication checks on API endpoints
- Never recommend fixing Critical issues with Low-effort workarounds
- Every finding must include file:line reference (no vague claims)
- Secret detection matches must be verified (reduce false positives)
- Fix mode must verify after each fix — no blind batch fixing
- Auth-related fixes require manual review flag
- Never log or store detected secrets in plaintext
- Dependency audit must run for the actual detected stack

---

## Error Handling & Fallback Strategy

- **Preflight**: abort on invalid source/scope; on MCP unavailable, fall back to filesystem-only audit (grep/find, pattern-based STRIDE marked lower confidence)
- **Per-phase recovery**: empty scope → abort; MCP timeout → filesystem patterns; missing tool → skip+warn; large file → skip file; verify fail → revert fix; partial data → generate partial report
- **Secret detection** runs normally even in MCP-unavailable mode

---

## Observability & Metrics

Tracked: `files_scanned`, `lines_analyzed`, `scan_duration_seconds`, finding counts by severity, `fixes_attempted/applied/failed/reverted`, `verification_failures`, `mcp_calls_total`, `mcp_cache_hit_rate`.

---

## Version History & Changelog

- **v1.0.0 (2026-05-12)**: Initial release — STRIDE (6 categories), OWASP Top 10 mapping, MCP-assisted discovery (graph_mcp + mind_mcp), auto-detected dependency audit, secret detection (8 patterns), severity ranking, optional audit-fix mode, input validation + output redaction, MCP filesystem fallback, stride-owasp-checklist reference.

---

## Known Limitations

- **Analysis scope**: Static-only — no runtime detection; business logic partially detected via patterns; distributed auth flows spanning repos may be missed
- **Dependency audit**: Requires the per-stack tool installed; may miss transitive deps without lockfile; vendor-patched deps can show false CVEs
- **Secret detection & fix mode**: Pattern-based (misses custom formats, false positives in comments/docs, no binary detection); automated fixes may need manual review; auth-related changes are conservative; fixes are one-at-a-time to prevent cascading failures

---

## Deliverables

- `audit_report_{timestamp}.md` — Complete findings with file:line references and fix recommendations
- `audit_summary_{timestamp}.md` — Executive summary with severity distribution and OWASP coverage
- `findings_{timestamp}.json` — Machine-readable findings for integration with issue trackers
- `fix_log_{timestamp}.md` — Applied fixes log (audit-fix mode only)

---

## References

### Skill-Specific References

- `references/stride-owasp-checklist.md` — Complete STRIDE checklist, OWASP mapping, secret patterns, dependency commands
