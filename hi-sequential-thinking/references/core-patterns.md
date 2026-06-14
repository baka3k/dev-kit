# Core Sequential Thinking Patterns

Essential revision and branching patterns.

## Revision Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| **Assumption Challenge** | Early assumption proves invalid with new data | `1/5: Assume X is bottleneck` → `4/5 [REVISION]: Y is actual bottleneck` |
| **Scope Expansion** | Problem larger than initially understood | `1/4: Fix bug` → `4/5 [REVISION]: Architectural redesign needed` |
| **Approach Shift** | Initial strategy inadequate for requirements | `2/6: Optimize query` → `5/6 [REVISION]: + cache layer required` |
| **Understanding Deepening** | Later insight fundamentally changes interpretation | `1/5: Feature broken` → `4/5 [REVISION]: UX confusion, not bug` |

## Branching Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| **Trade-off Evaluation** | Compare approaches with different trade-offs | Branch A: simpler/less scalable vs Branch B: complex/scales better |
| **Risk Mitigation** | Prepare backup for high-risk primary approach | Primary approach + fallback contingency branch |
| **Parallel Exploration** | Investigate independent concerns separately | Branch DB + Branch API explored in parallel, then integrated |
| **Hypothesis Testing** | Test multiple explanations systematically | Test A (eliminated) + Test B (confirmed) → root cause via B |

## Adjustment Guidelines

**Expand** when complexity discovered, multiple aspects, or alternatives need exploration. **Contract** when key insight solves earlier, problem is simpler, or steps merge.

**Example**: `1/5 → 3/7 (complexity) → 5/8 (more aspects) → 8/8 [FINAL]`

## Anti-Patterns

- **Premature Completion**: Rushing without verification → Add verification thoughts.
- **Revision Cascade / Branching Explosion / Context Loss**: Identify root cause; limit to 2-3 branches; reference previous thoughts explicitly.
