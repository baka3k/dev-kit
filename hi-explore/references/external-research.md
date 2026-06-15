# External Research (MCP-based)

When the target is **outside the local codebase** (web docs, GitHub repos, images, UI), use MCP tools to gather information. All tools listed below run **within the same agent process**—no additional installation required.

> If the target is **within the local codebase** → use `internal-explore.md` (Glob/Grep) instead.

## Tool Categories

### 1. Web Search

| Tool | When |
| --- | --- |
| `mcp__MiniMax__web_search(query)` | Quick lookup, short queries (1-2 keywords) |
| `mcp__web-search-prime__web_search_prime(query, recency, content_size)` | In-depth search, with time filters (`oneDay`/`oneWeek`/`oneMonth`/`oneYear`) |

**Example:**

```
MiniMax__web_search("Next.js 15 app router caching")
web_search_prime("TypeScript 5.5 satisfies operator", recency="oneYear", content_size="high")

```

### 2. Web Reading

| Tool | When |
| --- | --- |
| `mcp__web-reader__webReader(url, return_format="markdown")` | Read content of a specific URL (docs page, blog post, GitHub issue) |

**Example:**

```
webReader("https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config")

```

### 3. Visual Analysis (zai-mcp-server)

| Tool | When |
| --- | --- |
| `mcp__zai-mcp-server__analyze_image(image_source, prompt)` | General images (dashboards, error screenshots, mockups) |
| `mcp__zai-mcp-server__ui_to_artifact(image_source, output_type, prompt)` | UI screenshot → generate code / prompt / spec |
| `mcp__zai-mcp-server__understand_technical_diagram(image_source, prompt)` | Architecture / flowchart / UML / ER diagram |
| `mcp__zai-mcp-server__diagnose_error_screenshot(image_source, prompt)` | Error visible in image → diagnose + fix |
| `mcp__zai-mcp-server__extract_text_from_screenshot(image_source, prompt)` | OCR (code, terminal output, docs) |
| `mcp__zai-mcp-server__analyze_data_visualization(image_source, prompt)` | Charts, graphs, metrics dashboards |

`output_type` for `ui_to_artifact`: `code` | `prompt` | `spec` | `description`

### 4. Repo Lookup (Zread)

| Tool | When |
| --- | --- |
| `mcp__zread__get_repo_structure(owner/repo, dir_path="/")` | View GitHub repo file tree quickly |
| `mcp__zread__search_doc(owner/repo, query, language)` | Search within repo docs/issues/commits |
| `mcp__zread__read_file(owner/repo, file_path)` | Read a specific file in the repo |

**Example:**

```
zread__get_repo_structure("vercel/next.js", dir_path="/packages/next/src")
zread__search_doc("vercel/next.js", "route segment config", language="en")
zread__read_file("vercel/next.js", "packages/next/src/server/config.ts")

```

---

## Decision Matrix

| User Intent | Primary Tools | Notes |
| --- | --- | --- |
| Find docs about X | `web_search` → `webReader(url)` | Search first, read top 1-3 results |
| Find error message / known bug | `web_search` | Prioritize recency filter |
| Understand GitHub repo structure | `zread.get_repo_structure` | One call is enough for an overview |
| Find function/class in repo | `zread.search_doc` → `zread.read_file` | Search doc first, read specific file later |
| Read a specific docs page | `webReader(url)` | If URL is known, skip search |
| Analyze UI screenshot | `zai.ui_to_artifact` (output=code/spec) | Generate code when requested |
| Analyze dashboard/chart image | `zai.analyze_data_visualization` | Specialized in trends/anomalies |
| Analyze error screenshot | `zai.diagnose_error_screenshot` | Providing "during X" context improves accuracy |
| Analyze architecture diagram | `zai.understand_technical_diagram` | Spec for system design |
| OCR text/code from image | `zai.extract_text_from_screenshot` | Spec `programming_language` if it is code |
| General image | `zai.analyze_image` | Fallback for any image type |
| Mix multiple sources | Spawn parallel agents, one toolset per agent | Refer to `external-explore.md` |

---

## Spawn Pattern (parallel agents)

```yaml
# Example: 3 parallel agents for 1 explore task
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

Each agent runs with a **3-min timeout**, skip non-responders, and deduplicate results during the Collect step.

---

## Limits

* **Timeout**: 3min/agent (same as internal mode)
* **Concurrency**: max parallel = SCALE (user config)
* **Cache**: rely on client-side MCP cache (no app-level cache)
* **Secrets**: redact before sending URL/query

## Failure Modes

| Symptom | Action |
| --- | --- |
| `web_search` returns 0 results | Refine query, try `web_search_prime` with recency filter |
| `webReader` timeout | Try shorter URL or fetch snippet manually via `web_search` |
| `zread` repo not found | Verify `owner/repo` is correct, check public/private access |
| `zai` image format unsupported | Convert to PNG/JPG/WebP, max 8MB (for video) |
| MCP tool not in agent's toolset | Fall back to an alternative tool in the same category |
