# Meta-Pattern Recognition

Spot patterns appearing in 3+ domains to find universal principles.

## Core Principle

**Find patterns in how patterns emerge.** When the same pattern appears in 3+ domains, it's likely a universal principle worth extracting.

## When to Use

- **Same issue in different places** - Extract the abstract form
- **Déjà vu in problem-solving** - Find the universal pattern

## Quick Reference

| Pattern Appears In | Abstract Form | Where Else? |
|-------------------|---------------|-------------|
| CPU/DB/HTTP/DNS caching | Store frequently-accessed data closer | LLM prompt caching, CDN |
| Layering (network/storage/compute) | Separate concerns into abstraction levels | Architecture, org structure |
| Queuing (message/task/request) | Decouple producer from consumer with buffer | Event systems, async |
| Pooling (connection/thread/object) | Reuse expensive resources | Memory mgmt, governance |

## Process

1. **Spot repetition** - See same shape in 3+ places
2. **Extract abstract form** - Describe independent of any domain
3. **Document pattern** - Make it reusable

## Detailed Example

**Pattern:** Rate limiting appears in API throttling, traffic shaping, circuit breakers, admission control
**Abstract form:** Bound resource consumption to prevent exhaustion
**Variation points:** What resource, what limit, what happens when exceeded
**New application:** LLM token budgets - bound context window consumption (truncate or reject)

## 3+ Domain Rule

1 occurrence = coincidence, 2 = possible pattern, 3+ = likely universal. Test: can you describe the pattern without mentioning specific domains?

## Red Flags

- "This problem is unique" (probably not)
- Multiple teams solving "different" problems identically

