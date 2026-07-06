# Root Agent: Context Search Directive

**Objective:** Gather project context before executing tasks.
**Fast-Fail Rule:** If a tool is missing or disconnected -> SKIP IMMEDIATELY to the next level (Do NOT retry).

## Strict Priority Flow
*Proceed to the next step ONLY if the current step yields no results or the tool is unavailable.*

1. **`mind_mcp`**: Retrieve project docs, concepts, and foundational knowledge.
2. **`graph_mcp` (`semantic_search`)**: Find codebase relationships and logic (rely on semantics, not exact string matching).
Example:
```
 "semantic_search": {
        "query": "function that handles user authentication",
        "parser_type": "",
        "db": "neo4j",
        "top_k": "10",
        "collection": "",
    },
```
3. **`serena` (search)**: Broad codebase search.
4. **`grep`/`rg` (Native tools)**: File system sweep for exact strings (Absolute last resort).

## Mandatory Rules
- **No Hallucination:** If the entire search chain fails, stop and ask the user for details. Never fabricate context.
- **Merge Context:** Prioritize structured data from `graph_mcp` if tools return overlapping information.
- **No Assumptions:** Ask, don't guess. Highlight tradeoffs and admit confusion.
- **Minimal Code:** Solve only the target problem. No over-engineering.
- **Strict Scope:** Touch only what's necessary. Clean up your own mess.
- **Success Criteria:** Iterate until explicitly verified.
- The agent always responds in English.
