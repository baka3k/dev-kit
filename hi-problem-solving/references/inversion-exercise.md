# Inversion Exercise

Flip core assumptions to reveal hidden constraints and alternative approaches. "What if the opposite were true?"

## Core Principle

**Inversion exposes hidden assumptions.** Sometimes the opposite reveals the truth.

## When to Use

- **"There's only one way"** - Flip the assumption
- **Solution feels forced** - Invert the constraints

## Quick Reference

| Normal Assumption | Inverted | What It Reveals |
|-------------------|----------|-----------------|
| Cache to reduce latency | Add latency to enable caching | Debouncing patterns |
| Pull data when needed | Push data before needed | Prefetching, eager loading |
| Handle errors when occur | Make errors impossible | Type systems, contracts |
| Build features users want | Remove features users don't need | Simplicity >> addition |
| Optimize for common case | Optimize for worst case | Resilience patterns |

## Process

1. **List core assumptions** - What "must" be true?
2. **Invert each systematically** - "What if opposite were true?"
3. **Find valid inversions** - Which actually work somewhere?

## Detailed Example

**Problem:** Users complain app is slow
**Normal:** Make everything faster (cache, optimize queries, CDN, smaller bundle)
**Inverted:** Strategic slowness improves UX - debounce search (wait for full query), rate limit (friction prevents abuse), lazy load (delay reduces initial load), progressive rendering (perceived speed)
**Insight:** Strategic slowness can improve UX

## Valid vs Invalid Inversions

**Valid:** "Store data" → "Derive data on-demand" (when computation cheaper than storage)
**Invalid:** "Validate input" → "Trust all input" (security vulnerability, not context-dependent)
**Test:** Does the inversion work in ANY context? If yes, it's valid somewhere.

## Common Inversions

- **Eager → Lazy** (or vice versa)
- **Push → Pull** (or vice versa)
- **Store → Compute** (or vice versa)

## Red Flags

- "There's only one way to do this"
- Forcing solution that feels wrong
- "This is just how it's done"

## Remember

- Not all inversions work (test boundaries)
- Valid inversions reveal context-dependence
