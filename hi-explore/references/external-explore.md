# External scout (MCP-based)

When the target is outside the local codebase (web docs, GitHub repos, images), use parallel agents with MCP tools. All tools run inline within the agent process—no external CLI installation required.

## When To Use

* Target is a **GitHub repo** that hasn't been cloned yet.
* Target is a **docs/blog post** on the web.
* Target is a **screenshot/image** that needs analysis.
* Mixed: Multiple sources outside the local environment.

If the target is **within the local codebase** → use `internal-scout.md` (Glob/Grep).

## Tool Selection

Refer to `external-research.md` for:

* A full list of MCP tools (4 categories).
* Decision matrix: user intent → tool combination.
* Examples for each tool.

## SCALE → Spawn count

| SCALE | Agent Count | Use Case |
| --- | --- | --- |
| 1 | 1 | Single repo lookup, 1 docs page |
| 2-3 | 2-3 | Multi-source research (repo + web + image) |
| 4-5 | 4-5 | Comprehensive research with multiple queries |
| 6+ | 6+ | **Not recommended** — split into multiple batches instead of spawning too many agents |

## Spawn Pattern

Each agent is assigned a **toolset** (one or more MCP tools). Spawn them in **a single message** for parallel execution.

```yaml
# TaskCreate metadata (per agent)
agentType: general-purpose
scope: <short description, e.g., "GitHub repo structure">
tools: [<mcp_tool_1>, <mcp_tool_2>]
scale: small|medium|large
agentIndex: 0..N
totalAgents: N
priority: P2
effort: 3m

```

## Prompt Template (per agent)

```
You are agent {agentIndex}/{totalAgents} in a parallel hi-scout batch.
Scope: {scope}
Tools available: {tools}
Target: {target}

Use your tools to gather relevant information.
Report format:
## Found Resources
- <url|repo:path|image> - <description>

## Key Findings
- <bullet 1>
- <bullet 2>

## Unresolved
- <gap 1>

Timeout: 3 min. Skip if tool is unavailable, propose a fallback.

```

## Collect

Aggregate reports from all agents:

* Deduplicate URLs/repo paths.
* Merge key findings by topic.
* Note gaps/timeouts in "Unresolved Questions".
* Output according to the Report Format in `SKILL.md` §5.

## Timeout & Failure

* 3-minute timeout per agent.
* Skip non-responders (do not retry).
* If 2+ agents fail with the same tool → note "tool degraded" in the report.
* If all agents fail → mark scout result as "incomplete", and recommend internal mode or manual research.
