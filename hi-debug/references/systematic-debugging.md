# Systematic Debugging

Four-phase debugging framework that ensures root cause investigation before attempting fixes. For Iron Law, Red Flags, and Rationalizations, see `verification.md`.

## The Four Phases

Must complete each phase before proceeding to next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:** Read errors carefully (don't skip stack traces), reproduce consistently, check recent changes (git diff, commits, deps), gather evidence at each component boundary (log data in/out, verify env propagation), trace data flow up the call stack to the source (see root-cause-tracing.md).

### Phase 2: Pattern Analysis

**Find pattern before fixing:** Find working examples in same codebase, read reference implementation completely, identify every difference (no "that can't matter"), understand dependencies (components, config, env).

### Phase 3: Hypothesis and Testing

**Scientific method:** Form a single specific hypothesis ("X is root cause because Y"), test minimally (smallest change, one variable), verify before continuing (worked → Phase 4; didn't → new hypothesis, don't pile fixes), say "I don't understand X" when stuck (don't pretend).

### Phase 4: Implementation

**Fix root cause, not symptom:** Create a failing test case first (MUST have before fixing), implement a single fix (one change, no "while I'm here"), verify (passes, no regressions, issue resolved). **If fix doesn't work:** count attempts; if <3 return to Phase 1 with new info; **if ≥3: STOP and question architecture** (each fix reveals new shared-state/coupling problem — discuss with human partner before more fixes).
