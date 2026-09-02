---
name: hi-repository-search
description: "Gather traceable evidence from repository code and project documents. Use for codebase exploration, architecture, feature tracing, dependency or impact analysis, and questions that require verified source context."
metadata:
  author: baka3k
  version: "1.1.0"
---

# Repository Search

Retrieve and verify context; do not own planning, diagnosis, or implementation decisions.

## Modes

| Mode | Scope |
| --- | --- |
| default | Narrowest search that answers the question |
| `--code` | Code, symbols, references, and call paths |
| `--doc` | Project documents, decisions, and requirements |
| `--deep` | Reconcile code with documents and report conflicts |
| `--impact` | Callers, dependencies, affected modules, and workflows |

## Search Order

Use the first level that yields sufficient evidence:

1. `mind_mcp` for project knowledge and documents.
2. `graph_mcp` for semantic code discovery and relationships: `semantic_search`/`explore_graph` for concepts, `search_functions` for names, `search_by_code` for literals, `query_subgraph` for one-hop structure (T2 profile per [dev-shared/graph-function-selection.md](../dev-shared/graph-function-selection.md)).
3. `serena` for symbols, implementations, references, and structural search.
4. `rg` for exact-string filesystem search.

If a tool is unavailable, record it once and continue without retrying. Stop descending when evidence is sufficient; use lower levels only to close a specific gap. If all levels fail, ask the user for context.

## Workflow

1. Reuse a confirmed project; otherwise discover and activate it once.
2. Search narrowly. Treat semantic matches as candidates, not proof.
3. When only a function name is known, resolve it with `search_functions(query, parser_type)` and retain the returned node ID before graph traversal.
4. Route graph work by intent: `query_subgraph` for one-function context, `trace_flow` for relationship-filtered expansion, `find_paths` for a known start and end, and `analyze_workflow_impact` for workflow blast radius.
5. Verify important claims with direct code, symbol relationships, call paths, or document passages.
6. Trace only relationships required by the question; cap depth and result count.
7. Return an Evidence Bundle. Never fabricate missing context.

Evidence is sufficient when it identifies the relevant source, supports required relationships, separates facts from inference, and exposes conflicts or gaps.

## Evidence Bundle

Include only relevant sections:

```markdown
## Coverage
- tool: used | unavailable | no results | skipped

## Findings
- Claim — code|document — file+symbol|source_id+paragraph_id — confidence
  Evidence: concise supporting detail

## Relationships
Verified call paths, dependencies, or document relations.

## Contradictions
Conflicting sources or code-document differences.

## Inferences
Derived conclusions, explicitly labeled.

## Gaps
Unavailable, unindexed, or unanswered context.
```

## Subagents

Do not spawn by default. Use at most two investigators—code and documents—only when the user or project instructions permit delegation and the work has independent tracks, spans at least three subsystems, or needs independent conflict verification. The main agent owns synthesis and confidence.

## Tool References

Read only when exact parameters are needed:

- [Code Graph MCP](./references/code_graph.md)
- [Document Graph RAG](./references/doc_graph_rag.md)
