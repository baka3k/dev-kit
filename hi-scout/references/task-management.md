# Task Management for Parallel Agents

Lightweight patterns for spawning and tracking parallel subagents in `--parallel` mode.

## When To Use

- More than 2 parallel subagents
- Progress or status must be tracked per agent
- Per-agent metadata is needed (scope, index, priority)

## TaskCreate Template

```yaml
agentType: general-purpose
scope: <dir or pattern>
scale: <small|medium|large>
agentIndex: <0..N>
totalAgents: <N>
toolMode: <read|search|bash|web|repo|visual>
tools: [<mcp_tool_1>, ...]
priority: P2
effort: 3m
```

## Lifecycle

1. `TaskList` first → reuse existing tasks if any
2. Else `TaskCreate` per agent with the metadata above
3. `TaskUpdate` to `in_progress` before spawning
4. `TaskUpdate` to `completed` after the agent returns
5. Skip timed-out agents (default 3 min/agent)

## Internal Prompt Template

```text
Quickly explore {DIRECTORY} for: {TARGET}
Use the search order from SKILL.md (mind_mcp, graph_mcp, serena, rg).
List files with descriptions. Timeout 3 min.
Report: ## Found Files + path/file.ext - description
```

## Directory Division

`src/` | `lib/` | `tests/` | `config/` | `api/` | `types/`

Scopes must not overlap. Spawn all agents in a single message.

## File Chunking

- <500 lines: read the entire file.
- 500-1500 lines: 2-3 chunks.
- >1500 lines: `ceil(lines/500)` chunks.

## Notes

- Skip TaskCreate entirely if <= 2 agents or task tools are unavailable.
- All agents are read-only on source code.
- Output goes to the consolidated report (see `SKILL.md`).
