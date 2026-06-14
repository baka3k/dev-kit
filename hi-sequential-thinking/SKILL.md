---
name: hi:sequential-thinking
description: Apply step-by-step analysis for complex problems with revision capability. Use for multi-step reasoning, hypothesis verification, adaptive planning, problem decomposition, course correction.
license: MIT
argument-hint: "[problem to analyze step-by-step]"
metadata:
  author: claudekit
  version: "1.0.0"
---

# Sequential Thinking

Structured problem-solving via manageable, reflective thought sequences with dynamic adjustment.

## When to Apply

- Complex problem decomposition / adaptive planning
- Analysis needing course correction / unclear scope
- Multi-step solutions + hypothesis-driven investigation

## Core Process

Adjust thought count dynamically: **Expand** (complexity), **Contract** (simpler), **Revise** (new insight), **Branch** (alternatives).

### 1. Use Revision When Needed
```
Thought 5/8 [REVISION of Thought 2]: [Corrected understanding]
- Original: [What was stated]
- Why revised: [New insight]
- Impact: [What changes]
```

### 2. Branch for Alternatives
```
Thought 4/7 [BRANCH A from Thought 2]: [Approach A]
Thought 4/7 [BRANCH B from Thought 2]: [Approach B]
```
Compare explicitly, converge with decision rationale.

### 3. Generate & Verify Hypotheses
```
Thought 6/9 [HYPOTHESIS]: [Proposed solution]
Thought 7/9 [VERIFICATION]: [Test results]
```
Iterate until hypothesis verified.

### 4. Complete Only When Ready
Mark final: `Thought N/N [FINAL]`

Complete when:
- Solution verified
- All critical aspects addressed
- Confidence achieved
- No outstanding uncertainties

## Application Modes

**Explicit** (visible markers) when complexity warrants; **Implicit** (internal methodology) for routine problem-solving.

## Scripts (Optional)

Optional scripts for deterministic validation/tracking:
- `scripts/process-thought.js` - Validate & track thoughts with history
- `scripts/format-thought.js` - Format for display (box/markdown/simple)

See README.md for usage examples. Use when validation/persistence needed; otherwise apply methodology directly.

## References

Load when deeper understanding needed:
- `references/core-patterns.md` - Revision & branching patterns
- `references/examples-api.md` - API design example
- `references/examples-debug.md` - Debugging example
- `references/examples-architecture.md` - Architecture decision example
- `references/advanced-techniques.md` - Spiral refinement, hypothesis testing, convergence
- `references/advanced-strategies.md` - Uncertainty, revision cascades, meta-thinking
