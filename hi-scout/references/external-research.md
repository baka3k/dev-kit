# External Research (MCP-based)

Use when the target is outside the local codebase: web docs, GitHub repos, images, UI. All tools run inline within the agent process — no external CLI installation is required.

If the target is **within the local codebase**, stay on the search order in `SKILL.md` and use `rg`/`serena` instead.

## Tool Categories

### 1. Web Search

| Tool | When |
| --- | --- |
| `mcp__MiniMax__web_search(query)` | Quick lookup, short queries (1-2 keywords) |
| `mcp__web-search-prime__web_search_prime(query, recency, content_size)` | In-depth search, with time filters (`oneDay`/`oneWeek`/`oneMonth`/`oneYear`) |

```text
MiniMax__web_search("Next.js 15 app router caching")
web_search_prime("TypeScript 5.5 satisfies operator", recency="oneYear", content_size="high")
```

### 2. Web Reading

| Tool | When |
| --- | --- |
| `mcp__web-reader__webReader(url, return_format="markdown")` | Read a specific URL (docs page, blog post, GitHub issue) |

```text
webReader("https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config")
```

### 3. Visual Analysis (zai-mcp-server)

| Tool | When |
| --- | --- |
| `mcp__zai-mcp-server__analyze_image(image_source, prompt)` | General images (dashboards, error screenshots, mockups) |
| `mcp__zai-mcp-server__ui_to_artifact(image_source, output_type, prompt)` | UI screenshot → code / prompt / spec |
| `mcp__zai-mcp-server__understand_technical_diagram(image_source, prompt)` | Architecture / flowchart / UML / ER diagram |
| `mcp__zai-mcp-server__diagnose_error_screenshot(image_source, prompt)` | Error visible in image → diagnose + fix |
| `mcp__zai-mcp-server__extract_text_from_screenshot(image_source, prompt)` | OCR (code, terminal output, docs) |
| `mcp__zai-mcp-server__analyze_data_visualization(image_source, prompt)` | Charts, graphs, metrics dashboards |

`output_type` for `ui_to_artifact`: `code` | `prompt` | `spec` | `description`.

### 4. Repo Lookup (Zread)

| Tool | When |
| --- | --- |
| `mcp__zread__get_repo_structure(owner/repo, dir_path="/")` | View a GitHub repo file tree quickly |
| `mcp__zread__search_doc(owner/repo, query, language)` | Search within repo docs/issues/commits |
| `mcp__zread__read_file(owner/repo, file_path)` | Read a specific file in the repo |

```text
zread__get_repo_structure("vercel/next.js", dir_path="/packages/next/src")
zread__search_doc("vercel/next.js", "route segment config", language="en")
zread__read_file("vercel/next.js", "packages/next/src/server/config.ts")
```

## Decision Matrix

| User Intent | Primary Tools | Notes |
| --- | --- | --- |
| Find docs about X | `web_search` → `webReader(url)` | Search first, read the top 1-3 results |
| Find an error message / known bug | `web_search` | Prefer the recency filter |
| Understand GitHub repo structure | `zread.get_repo_structure` | One call is enough for an overview |
| Find a function/class in a repo | `zread.search_doc` → `zread.read_file` | Search first, read the specific file later |
| Read a specific docs page | `webReader(url)` | Skip search when the URL is known |
| Analyze a UI screenshot | `zai.ui_to_artifact` (`output=code/spec`) | Generate code when requested |
| Analyze a dashboard/chart image | `zai.analyze_data_visualization` | Specialized in trends/anomalies |
| Analyze an error screenshot | `zai.diagnose_error_screenshot` | "during X" context improves accuracy |
| Analyze an architecture diagram | `zai.understand_technical_diagram` | Spec for system design |
| OCR text/code from an image | `zai.extract_text_from_screenshot` | Pass `programming_language` when it is code |
| General image | `zai.analyze_image` | Fallback for any image type |
| Mix multiple sources | Spawn parallel agents, one toolset per agent | See the spawn pattern below |

## SCALE → Spawn Count

| SCALE | Agent Count | Use Case |
| --- | --- | --- |
| 1 | 1 | Single repo lookup, one docs page |
| 2-3 | 2-3 | Multi-source research (repo + web + image) |
| 4-5 | 4-5 | Comprehensive research with multiple queries |
| 6+ | 6+ | **Not recommended** — split into batches instead |

## Spawn Pattern

Each agent owns one toolset. Spawn them in a single message for parallel execution.

```yaml
# TaskCreate metadata (per agent)
agentType: general-purpose
scope: <short description, e.g. "GitHub repo structure">
tools: [<mcp_tool_1>, <mcp_tool_2>]
scale: small|medium|large
agentIndex: 0..N
totalAgents: N
priority: P2
effort: 3m
```

```text
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

Timeout: 3 min. Skip if a tool is unavailable, propose a fallback.
```

Example: 3 parallel agents for one scout task.

```yaml
agents:
  - id: agent-1
    scope: "GitHub repo structure"
    tools: [mcp__zread__get_repo_structure, mcp__zread__search_doc, mcp__zread__read_file]
    scope_target: "vercel/next.js /packages/next/src"

  - id: agent-2
    scope: "Web docs"
    tools: [mcp__MiniMax__web_search, mcp__web-reader__webReader]
    scope_target: "Next.js 15 app router caching strategies"

  - id: agent-3
    scope: "Visual analysis"
    tools: [mcp__zai-mcp-server__analyze_image]
    scope_target: "user-provided screenshot of architecture"
```

## Collect

Aggregate reports from all agents:

- Deduplicate URLs/repo paths.
- Merge key findings by topic.
- Note gaps/timeouts under "Unresolved Questions".
- Output according to the Report Format in `SKILL.md`.

## Limits And Failure Modes

- **Timeout**: 3 min per agent; skip non-responders, do not retry.
- **Concurrency**: max parallel = SCALE.
- **Cache**: rely on client-side MCP cache (no app-level cache).
- **Secrets**: redact before sending a URL or query.
- If 2+ agents fail with the same tool, record "tool degraded". If all agents fail, mark the result "incomplete" and recommend internal search or manual research.

| Symptom | Action |
| --- | --- |
| `web_search` returns 0 results | Refine the query, try `web_search_prime` with a recency filter |
| `webReader` timeout | Try a shorter URL or fetch a snippet through `web_search` |
| `zread` repo not found | Verify `owner/repo` and public/private access |
| `zai` image format unsupported | Convert to PNG/JPG/WebP, max 8MB (for video) |
| MCP tool not in the agent's toolset | Fall back to another tool in the same category |
