---
name: hi-debug
description: "Debug systematically with root cause analysis before fixes. Use for bugs, test failures, unexpected behavior, performance issues, call stack tracing, multi-layer validation, log analysis, CI/CD failures, database diagnostics, system investigation."
languages: all
argument-hint: "[error or issue description]"
metadata:
  author: claudekit
  version: "4.0.0"
---

# Debugging & System Investigation

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.** See `references/verification.md` for the Iron Law, Red Flags, and Rationalization Prevention.

## Techniques

| # | Technique | File | Load when |
|---|-----------|------|-----------|
| 1 | Systematic Debugging | `references/systematic-debugging.md` | Any bug/issue requiring investigation and fix |
| 2 | Root Cause Tracing | `references/root-cause-tracing.md` | Error deep in call stack, unclear where invalid data originated |
| 3 | Defense-in-Depth | `references/defense-in-depth.md` | After finding root cause, need comprehensive validation |
| 4 | Verification | `references/verification.md` | About to claim work complete, fixed, or passing |
| 5 | Investigation Methodology | `references/investigation-methodology.md` | Server incidents, system behavior analysis, multi-component failures |
| 6 | Log & CI/CD Analysis | `references/log-and-ci-analysis.md` | CI/CD pipeline failures, server errors, deployment issues |
| 7 | Performance Diagnostics | `references/performance-diagnostics.md` | Performance degradation, slow queries, high latency, resource exhaustion |
| 8 | Reporting Standards | `references/reporting-standards.md` | Need to produce investigation report or diagnostic summary |
| 9 | Task Management | `references/task-management-debugging.md` | Multi-component investigation (3+ steps), parallel log collection, coordinating debugger subagents |
| 10 | Frontend Verification | `references/frontend-verification.md` | Implementation touches frontend files (tsx/jsx/vue/svelte/html/css), UI bugs, visual regressions |

## Tools Integration

- **Database/CI:** `psql` for PostgreSQL; `gh` CLI for GitHub Actions logs and pipelines
- **Codebase:** `hi-docs-seeker` (package docs), `hi-repo-search` (explorer code & doc), `/hi-explorer` (search information)
- **Frontend/Problem-solving:** Chrome browser or `hi-chrome-devtools` for visual verification; `hi-problem-solving` when stuck
