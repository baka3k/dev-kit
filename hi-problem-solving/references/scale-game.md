# Scale Game

Test at extremes (1000x bigger/smaller, instant/year-long) to expose fundamental truths hidden at normal scales.

## Core Principle

**Extremes expose fundamentals.** What works at one scale fails at another.

## When to Use

- **"Should scale fine" (without testing)** - Test at extremes
- **Edge cases unclear** - Test minimum and maximum

## Quick Reference

| Scale Dimension | Test At Extremes | What It Reveals |
|-----------------|------------------|-----------------|
| **Volume** | 1 item vs 1B items | Algorithmic complexity limits |
| **Speed** | Instant vs 1 year | Async requirements, caching needs |
| **Users** | 1 user vs 1B users | Concurrency issues, resource limits |
| **Duration** | Milliseconds vs years | Memory leaks, state growth |
| **Failure rate** | Never fails vs always fails | Error handling adequacy |

## Process

1. **Pick dimension** - What could vary extremely?
2. **Test minimum and maximum** - What if 1000x smaller/bigger?
3. **Design for reality** - Use insights to validate architecture

## Detailed Examples

| Normal Scale | At Extreme | Reveals | Action |
|--------------|------------|---------|--------|
| Handle errors when they occur | 1B scale: error volume overwhelms logging | Need type systems or chaos engineering | Design for volume, not just occurrence |
| Sync APIs < 100ms | Global: 200-500ms network latency | Async becomes survival requirement | Design async-first from start |
| In-memory state hours/days | Years: unbounded growth, eventual crash | Need persistence or cleanup | Design for stateless or externalized state |
| Session in memory 100 users | 1M users: memory exhausted | Need distributed session store | Design for horizontal scaling from start |

## Both Directions Matter

Test smaller too: 1 user? 10 items? Instant response? Often reveals over-engineering or premature optimization.

## Red Flags

- "It works in dev" (but will it work in production?)
- No idea where limits are

## Remember

- Extremes reveal fundamentals hidden at normal scales
- Test BOTH directions (bigger AND smaller)
