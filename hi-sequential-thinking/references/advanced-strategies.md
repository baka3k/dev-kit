# Advanced Sequential Thinking Strategies

Additional sophisticated patterns for complex scenarios.

## Uncertainty Management

```
Thought 2/7: Need to decide X
Thought 3/7: Insufficient data—two scenarios possible
Thought 4/7 [SCENARIO A if P true]: Analysis for A
Thought 4/7 [SCENARIO B if P false]: Analysis for B
Thought 5/7: Decision that works for both scenarios
Thought 6/7: Or determine critical info needed
Thought 7/7 [FINAL]: Robust solution or clear info requirement
```

**Strategies**: Find solution robust to uncertainty, identify minimal info needed, make safe assumptions with clear documentation.

## Revision Cascade & Meta-Thinking

| Pattern | When to Use | Approach |
|---------|-------------|----------|
| **Revision Cascade** | One revision invalidates multiple downstream thoughts | After revision, add `[REASSESSMENT]` thought checking which prior thoughts still hold, then rebuild from corrected foundation |
| **Meta-Thinking** | Stuck, circling, no progress for several thoughts | Add `[META]` thought: identify missing info, adjust strategy, research, then resume |

## Parallel Constraint Satisfaction

```
Thought 2/10: Solution must satisfy A, B, C
Thought 3/10 [CONSTRAINT A]: Solutions satisfying A: {X, Y, Z}
Thought 4/10 [CONSTRAINT B]: Solutions satisfying B: {Y, Z, W}
Thought 5/10 [CONSTRAINT C]: Solutions satisfying C: {X, Z}
Thought 6/10 [INTERSECTION]: Z satisfies all
Thought 7/10: Verify Z feasible
Thought 8/10 [BRANCH if infeasible]: Relax which constraint?
Thought 9/10: Decision on constraint relaxation if needed
Thought 10/10 [FINAL]: Optimal solution given constraints
```

Pattern: Analyze constraints independently → find intersection → verify feasibility.
