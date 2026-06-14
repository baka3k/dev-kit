# Reporting Standards

Structured format for diagnostic and investigation reports. Sacrifice grammar for concision.

**Use when:** completing system investigation, summarizing debugging session, incident post-mortems, performance analysis results.

## Writing Guidelines

- **Concise** — facts and evidence, not narrative; sacrifice grammar for brevity
- **Honest** — state unknowns explicitly; "likely cause" vs "confirmed cause"

## Template

```markdown
# [Issue Title] - Investigation Report

## Executive Summary
- **Issue:**
- **Impact:**
- **Root cause:**
- **Status:**
- **Fix:**

## Timeline
- HH:MM -
- HH:MM -

## Technical Analysis
### Findings
1.
2.

### Evidence
[logs, queries, metrics]

## Recommendations
### Immediate (P0)
- [ ]

### Short-term (P1)
- [ ]

### Long-term (P2)
- [ ]

## Unresolved Questions
-
```
