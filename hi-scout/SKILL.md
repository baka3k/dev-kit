---
name: hi-scout
description: "Gather traceable evidence from repository code, project documents, and external sources. Use for codebase exploration, architecture, feature tracing, dependency or impact analysis, file discovery, web/docs lookup, GitHub repo analysis, and image or UI understanding."
argument-hint: "<question | symbol | path | SQL | impact target | repo URL | docs topic | image> [--code|--doc|--ask|--deep|--impact] [--external] [--parallel]"
metadata:
  author: baka3k
  version: "4.0.0"
  last_updated: "2026-10-20"
---

# Scout

Retrieve and verify context; do not own planning, diagnosis, or implementation decisions. Sequential evidence gathering is the default; parallel agents and external research are explicit modes.

## Modes

| Mode | Scope |
| --- | --- |
| default | Narrowest search that answers the question |
| `--code` | Code, symbols, references, and call paths |
| `--doc` | Project documents, decisions, and requirements |
| `--ask` | Short question answered from the nearest sufficient evidence |
| `--deep` | Reconcile code with documents and report conflicts |
| `--impact` | Callers, dependencies, affected modules, and workflows |
| `--external` | Web docs, GitHub repos, and image/UI analysis via MCP tools |
| `--parallel` | Split an independent-scope target across 1-5 subagents |

Modes combine: `--external --parallel` runs one toolset per agent; `--deep --parallel` verifies code and document tracks independently.

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

## External And Parallel Modes

- External targets (web docs, GitHub repo, image/UI) use MCP tools; read [references/external-research.md](./references/external-research.md) for tool selection, the decision matrix, and failure handling.
- `--parallel` splits a target into 1-5 non-overlapping agent scopes; read [references/task-management.md](./references/task-management.md) for task registration, timeouts, and collection.
- Spawn only when a mode requests it, never more than 5 units.
- Each agent has a 3-minute timeout; skip non-responders instead of retrying.
- The main agent owns synthesis: deduplicate paths/URLs, merge findings by topic, and record gaps.
- When `--deep` needs only code/document conflict verification, at most two investigators (code, documents) are allowed.

## Evidence Bundle

Include only relevant sections:

```markdown
## Coverage
- tool: used | unavailable | no results | skipped

## Findings
- Claim — code|document|external — file+symbol|source_id+paragraph_id|url — confidence
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

## Report Format (parallel mode)

```markdown
# Scout Report
## Relevant Files / Resources
- path/to/file.ts - description
- https://docs.example.com/page - description
- github.com/owner/repo/path/to/file - description
## Key Findings
- finding 1
## Unresolved Questions
- any gaps
```

## Tool References

Read only when exact parameters are needed:

- [Code Graph MCP](./references/code_graph.md)
- [Document Graph RAG](./references/doc_graph_rag.md)

## Configuration

MCPs must be configured at the client (Claude Code / Cursor / Copilot). No config file is needed in the repository. When outputs are written to disk, follow `hi-project-organization`.
