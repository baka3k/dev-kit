---
name: hi-scenario
description: Generate comprehensive edge cases and test scenarios by decomposing features across 12 dimensions (user types, input extremes, timing, scale, state, environment, errors, authorization, data integrity, integration, compliance, business logic). Uses mind_mcp for feature requirements context and graph_mcp for code path discovery. Use before implementation, during code review, or when planning test coverage.
version: 1.1.0
last_updated: 2026-09-08
hooks:
  pre:
    - name: input-validation
      scope: [target_source, analysis_depth]
      enable_redaction: true
    - name: mcp-health-check
  post:
    - name: cleanup-handler
      paths: [scenario-data/]
      keep: ["*.json", "*.md"]
---

# HI Scenario

Edge case and scenario exploration that decomposes features across 12 dimensions with MCP-assisted code path discovery.

## Usage

**When**: complex/stateful features, test authoring, risk assessment, API design review, refactoring critical paths, security review, onboarding. **Avoid**: trivial/cosmetic changes, well-tested stable code, pure config changes, simple CRUD, docs-only. **Inputs**: target (path/glob/description), depth `quick` (default, major paths) | `deep` (all branches), optional focus dimensions, optional severity filter. Validate paths: must exist/readable, block `../`, whitelist `[a-zA-Z0-9_\-./]`, max 1000 chars.

Phase detail, applicability matrix, templates, fallback: [workflow.md](references/workflow.md). Full per-dimension checklist: [dimension-checklist.md](references/dimension-checklist.md).

## The 12 Decomposition Dimensions

Filter relevant dimensions first; generate scenarios only for those.

| # | Dimension | What to Look For |
| --- | --- | --- |
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

## Severity

**Critical** = data loss, security breach, auth bypass, silent corruption · **High** = feature broken for a subset, data inconsistency · **Medium** = degraded UX, recoverable · **Low** = minor glitch, non-blocking.

## Workflow

0. **Target analysis** — validate target, read source; graph_mcp for entry points, state mutations, call paths (selection per `dev-shared/graph-function-selection.md`); mind_mcp for requirements context.
1. **Dimension filtering** — mark applicable/skipped with reason; prioritize by risk.
2. **Scenario generation** — 3–5 concrete, reproducible, implementation-agnostic scenarios per applicable dimension; high-risk dimensions first.
3. **Severity classification** — per the table above; auth bypass/data exposure/silent corruption always Critical.
4. **Report generation** — table by dimension & severity, applicability summary, test priorities (Critical → immediate).

## Non-Negotiable Rules

- Every scenario must be concrete and reproducible.
- Filter dimensions before generating — do not generate noise.
- Critical findings must have specific expected behavior described.
- Auth bypass or data exposure always classified as Critical.
- Never skip error cascades dimension for server-side code.
- Provide reason for every skipped dimension.
- Graph-derived scenarios must reference actual code paths.

## Fallback

graph_mcp/mind_mcp unavailable → manual code reading (static analysis, lower confidence); dimension timeout → skip and continue; partial data → partial report.
