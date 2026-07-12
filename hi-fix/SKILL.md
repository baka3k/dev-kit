---
name: hi-fix
description: "ALWAYS activate before fixing ANY bug, error, test failure, CI/CD issue, type error, lint, log error, UI issue, code problem."
argument-hint: "[issue] [--standard|--deep|--parallel|--review]  — default: Quick mode"
metadata:
  author: baka3k
  version: "2.0.0"
---
# Fix - Issue Resolution

## Mode Selection
| Flag | When |
|------|------|
| default |  1 file, type/lint, clear error |
| --standard | Standard: 2-5 files, full debug needed |
| --deep | Deep: 5+ files, architecture impact |
| --parallel | 2+ independent issues |
| --review | Human-in-the-loop at each step |

## Process Flow
`[Explorer] -> [Diagnose] -> [Fix] -> [Verify+Prevent] -> [Finalize]`

<HARD-GATE>
Do NOT fix before Explorer + Diagnose. Find ROOT CAUSE first. If 3+ fix attempts fail, STOP and question architecture with user.
</HARD-GATE>

### Step 1: Explorer (locate-only, default)
Locate affected files and  clear error. One agent is sufficient.
Standard/Deep: activate hi-explorer Or 2-3 parallel agents.

### Step 2: Diagnose (MANDATORY)
Capture pre-fix state: exact error, stack traces, logs.
Trace backward: symptom -> immediate cause -> contributing factor -> ROOT CAUSE.
If difficult: activate hi-debug. If 2+ hypotheses fail -> activate hi-problem-solving.

### Step 3: Fix
Fix ROOT CAUSE. Minimal changes. Follow existing patterns.

### Step 4: Verify + Prevent
Quick: typecheck + lint (default)
Standard: + build + test
Deep: comprehensive (edge cases, security, perf)

### Step 5: Finalize
Quick: short report -> ask commit (skip docs, skip review)
Standard/Deep: report -> review (if --review) -> docs -> commit

## Workflows

### Quick (default, 1 file, type/lint, clear error)
Explorer (locate only) -> Diagnose (read error) -> Fix -> Verify (typecheck+lint) -> Done

### Standard (--standard, 2-5 files)
Full Explorer -> Full Diagnose (call hi-debug if needed) -> Fix -> Verify (typecheck+lint+build+test) -> Review (if --review) -> Finalize

### Deep (--deep, 5+ files, architecture impact)
Parallel Explorer + Diagnose + Research -> Fix -> Comprehensive Verify -> Review -> Finalize

### Parallel (2+ independent)
Separate task tree per issue. Spawn fullstack-developer per issue.
