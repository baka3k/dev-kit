# Simplification Cascades

Find one insight eliminating multiple components. "If this is true, we don't need X, Y, Z."

## Core Principle

**Everything is a special case of...** collapses complexity dramatically. One powerful abstraction > ten clever hacks.

## When to Use

- **Same thing implemented 5+ ways** - Abstract the common pattern
- **Growing special case list** - Find the general case

## The Pattern

Look for multiple implementations, special case handling, "we need to handle A, B, C differently", complex rules with exceptions. Ask: "What if they're all the same thing underneath?"

## Examples

| Case | Before | Insight | After | Eliminated |
|------|--------|---------|-------|------------|
| Stream Abstraction | Separate handlers for batch/real-time/file/network | "All inputs are streams - just different sources" | One stream processor, multiple sources | 4 implementations |
| Resource Governance | Session tracking, rate limiting, file validation, connection pooling (separate) | "All are per-entity resource limits" | One ResourceGovernor with 4 resource types | 4 custom enforcement systems |
| Immutability | Defensive copying, locking, cache invalidation, temporal coupling | "Treat everything as immutable data + transformations" | Functional programming patterns | Entire classes of sync problems |

## Process

1. **List variations** - What's implemented multiple ways?
2. **Find essence** - What's the same underneath?
3. **Extract abstraction** - What's the domain-independent pattern?

## Red Flags

- "Just need to add one more case..." (repeating forever)
- "Don't touch that, it's complicated" (complexity hiding pattern)

## Remember

- The pattern is usually already there, just needs recognition
- Valid cascades feel obvious in retrospect
