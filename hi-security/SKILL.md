---
name: hi-security
description: STRIDE + OWASP-based security audit with MCP-assisted code analysis and optional iterative auto-fix. Scans code using graph_mcp for structure discovery and mind_mcp for security policy context, then produces severity-ranked findings with fix recommendations. Supports audit-only and audit+fix modes. Use before releases, after sensitive feature additions, or for periodic compliance reviews.
version: 1.1.0
last_updated: 2026-09-08
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
      keep: ["*.json", "*.md"]
---

# HI Security

STRIDE + OWASP security audit with MCP-assisted analysis, dependency audit, secret detection, and optional iterative auto-fix.

## When To Use / Avoid

Use before releases, after auth/payment/data features, periodic reviews, compliance prep (SOC 2, GDPR, PCI-DSS), after dependency updates, on CVE reports. Avoid for cosmetic-only changes and standalone dependency audits (`npm audit` / `pip-audit` directly).

## Inputs

Source root path; audit scope (glob or directory); mode `audit` (scan → categorize → report) or `audit-fix` (… → iterative fix Critical→High→Medium → verify → report); optional max fix iterations (default 10); optional focus (`auth`|`data`|`api`|`infra`|`all`). Validate paths: block `../`, whitelist `[a-zA-Z0-9_\-./*]`, max 1000 chars. Redact outputs.

## Workflow

Phase detail and MCP call blocks: [workflow.md](references/workflow.md). Checklists (STRIDE checks, OWASP mapping, secret patterns, dependency commands): [stride-owasp-checklist.md](references/stride-owasp-checklist.md).

0. **Scope resolution** — validate inputs, expand glob, filter test/fixtures/docs, mind_mcp policy context.
1. **STRIDE analysis** — per-file 6-category scan; graph_mcp for entry points, auth flows, data paths; findings with file:line.
2. **Dependency audit** — detect stack, run matching tool, record CVEs.
3. **Secret detection** — pattern scan, skip test/placeholder false positives.
4. **OWASP mapping** — STRIDE→Top 10; dependencies→A06; secrets→A02/A05.
5. **Fix execution** (audit-fix only) — Critical→High→Medium, one fix per iteration, verify then commit or revert, cap at `max_iterations`.
6. **Report** — severity table with file:line + recommendations, OWASP coverage, next steps.

## Fix Guard Rules

- Never fix more than one issue per iteration.
- Tests must pass before advancing to the next fix.
- Critical auth changes require manual review.
- Do not modify test files or configuration secrets.

## Non-Negotiable Rules

- Never skip authentication checks on API endpoints.
- Never recommend fixing Critical issues with Low-effort workarounds.
- Every finding must include file:line reference (no vague claims).
- Secret detection matches must be verified (reduce false positives).
- Fix mode must verify after each fix — no blind batch fixing.
- Auth-related fixes require manual review flag.
- Never log or store detected secrets in plaintext.
- Dependency audit must run for the actual detected stack.

## Fallback

MCP unavailable → filesystem-only audit (pattern-based STRIDE, lower confidence); secret detection always runs. Fix verification failure → revert. Partial data → partial report.

## Deliverables

`audit_report_{timestamp}.md`, `audit_summary_{timestamp}.md`, `findings_{timestamp}.json`, plus `fix_log_{timestamp}.md` in audit-fix mode.
