# Verification Before Completion

Run verification commands and confirm output before claiming success. **Canonical home for Iron Law, Red Flags, and Rationalization Prevention.**

## Core Principle

**Evidence before claims, always.** Claiming work complete without verification is dishonesty, not efficiency.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If haven't run verification command in this message, cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |

## Key Patterns

| Domain | Good (with evidence) | Bad (without evidence) |
|--------|---------------------|------------------------|
| Tests | `[Run test cmd] [See: 34/34 pass]` | "Should pass now" / "Looks correct" |
| Regression (TDD) | Write → Run(pass) → Revert → Run(MUST FAIL) → Restore → Run(pass) | "I've written regression test" (no red-green) |
| Build | `[Run build] [See: exit 0]` | "Linter passed" (linter ≠ compiler) |
| Requirements | Re-read plan → checklist → verify each → report gaps | "Tests pass, phase complete" |
| Agent delegation | Report success → check VCS diff → verify changes → report actual | Trust agent report |

## When To Apply

- ALWAYS before ANY completion claim, expression of satisfaction, or positive statement about work state
- Rule covers exact phrases, paraphrases, synonyms, and implications of success
