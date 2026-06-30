---
name: hi:scout
description: "Fast parallel codebase scoutr using multiple subagents with MCP-based external research. Use for file discovery (local), web/docs lookup, GitHub repo analysis, image/UI understanding."
argument-hint: "[search-target]"
metadata:
  author: baka3k
  version: "3.0.0"
---

# scout (Parallel Codebase + External Researcher)

Fast, token-efficient codebase intelligence + external research using parallel agents and MCP tools.

## Arguments
- Default: Parallel agents, mix of internal (Glob/Grep) + external (MCP) based on target
- `[search-target]` — what to find (path, repo URL, docs topic, image path, etc.)

## Workflow

### 1. Analyze
Parse user prompt. Detect scope:
- **Local**: target in current codebase → internal mode
- **External**: target là web docs / GitHub repo / image → external mode (MCP)
- **Hybrid**: cả hai → multi-mode parallel

Xác định SCALE (1-5 agents, >5 không khuyến khích).

### 2. Divide
Split work logically. Mỗi agent có scope riêng biệt, **không overlap**. Với external mode, mỗi agent gán 1 toolset (xem `references/external-research.md`).

### 3. Register Tasks
Skip nếu ≤2 agents hoặc Task tools unavailable.
TaskList trước → reuse. Else TaskCreate per agent với metadata:
- `agentType: general-purpose`
- `scope`, `scale`, `agentIndex`, `totalAgents`
- `toolMode: read | search | bash | web | repo | visual`
- `tools: [<mcp_tool_1>, ...]` (cho external agents)
- `priority: P2`, `effort: 3m`

Xem `references/task-management.md` cho patterns.

### 4. Spawn
TaskUpdate mỗi task → `in_progress` trước khi spawn. **3-min timeout per agent**. Skip timed-out.

- **Internal mode**: load `references/internal-scout.md` — dùng Glob/Grep
- **External mode**: load `references/external-scout.md` + `references/external-research.md` — dùng MCP tools

### 5. Collect
Aggregate: deduplicate paths/URLs, merge descriptions, note gaps/timeouts, list unresolved.

## Tool Selection (Quick Reference)

| Target | Mode | Tools |
|---|---|---|
| Local code/files | internal | Glob, Grep, Read, Bash |
| Web docs / blog | external | `mcp__MiniMax__web_search`, `mcp__web-reader__webReader` |
| GitHub repo | external | `mcp__zread__get_repo_structure`, `search_doc`, `read_file` |
| Image / UI / diagram | external | `mcp__zai-mcp-server__analyze_image`, `ui_to_artifact`, `understand_technical_diagram` |
| Error screenshot | external | `mcp__zai-mcp-server__diagnose_error_screenshot`, `extract_text_from_screenshot` |
| Hybrid (nhiều nguồn) | multi | Spawn parallel, mỗi agent 1 toolset |

Xem `references/external-research.md` cho decision matrix đầy đủ.

## Report Format

```markdown
# scout Report
## Relevant Files / Resources
- path/to/file.ts - description
- https://docs.example.com/page - description
- github.com/owner/repo/path/to/file - description
## Key Findings
- finding 1
- finding 2
## Unresolved Questions
- any gaps
```

## Configuration
MCPs phải được cấu hình ở client (Claude Code / Cursor / Copilot). Không cần config file trong repo.

Invoke /hi:project-organization để organize outputs (nếu có).
