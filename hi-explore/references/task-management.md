# Task Management for Parallel Agents

Lightweight patterns for spawning and tracking parallel subagents. Used by `hi-explorer` to coordinate parallel codebase scoutrs.

## When To Use

- > 2 parallel subagents
- Need to track progress / status per agent
- Need per-agent metadata (scope, index, priority)

## TaskCreate Template

```yaml
agentType: general-purpose
scope: <dir or pattern>
scale: <small|medium|large>
agentIndex: <0..N>
totalAgents: <N>
toolMode: <read|search|bash>
priority: P2
effort: 3m
```

## Lifecycle

1. `TaskList` first → reuse existing tasks if any
2. Else `TaskCreate` per agent with metadata above
3. `TaskUpdate` to `in_progress` before spawning
4. `TaskUpdate` to `completed` after agent returns
5. Skip timed-out agents (default 3m/agent)

## Notes

- Skip TaskCreate entirely if <= 2 agents or Task tools unavailable
- All agents are read-only on source code
- Output goes to consolidated report (see SKILL.md §5 Collect)
