# Internal Explore
Use this when the target is within the local codebase (single repo). Each subagent must follow the **Tool Priority Flow** before falling back to native tools.
## Tool Priority Flow

1. **`mind_mcp`**: Retrieve project docs, concepts, and foundational knowledge.
2. **`graph_mcp` (`semantic_search`)**: Find codebase relationships and logic (rely on semantics, not exact string matching).
3. **`serena` (search)**: Broad codebase search.
4. **`grep`/`rg` (Native tools)**: File system sweep for exact strings (Absolute last resort).

**Fast-Fail Rule:** If a tool is missing or unavailable → skip immediately to the next tool (DO NOT retry). Continue until results are found or all tools have been exhausted.
## Prompt Template
```
Quickly explore {DIRECTORY} for: {TARGET}
Use Glob/Grep. List files with descriptions. Timeout 3m.
Report: ## Found Files + path/file.ext - description
```
## Directory Division
src/ | lib/ | tests/ | config/ | api/ | types/
No overlap. Spawn all in a single message.
## File Chunking
* <500 lines: Read entire file.
* 500–1500 lines: 2–3 chunks via Bash `sed`.
* > 1500 lines: ceil(lines/500) chunks.
## Timeout
3 minutes per agent. Skip non-responders. Deduplicate paths.
---
