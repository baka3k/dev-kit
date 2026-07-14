# MCP Routing Reference

This routing contract maximizes FalkorDB and Qdrant use while avoiding stale provider-specific paths. Call `graph_mcp.list_mcp_functions({})` first. The callable wrapper is the schema authority; retry once only for `invalid_parameters`.

## Required Flow

| Order | Tool | Purpose | Evidence retained |
|---|---|---|---|
| 1 | `mind_mcp.list_qdrant_collections` | Inventory project corpora | Collection candidates |
| 2 | `mind_mcp.list_source_ids` | Scope documents when allowed | Source IDs |
| 3 | `mind_mcp.query_graph_rag_langextract` | Retrieve allowed concepts and relations | Terms, actors, constraints |
| 4 | `graph_mcp.list_mcp_functions` | Discover live capabilities | Tool metadata |
| 5 | `graph_mcp.activate_project` | Activate `parser_type:"cplus"` | Configured FalkorDB context |
| 6 | `graph_mcp.list_qdrant_collections` | Inventory code vectors | Code collection candidates |
| 7 | Bind `ACTIVE_DATA_CONTEXT` | Lock active FalkorDB plus one Qdrant candidate | Permit validation probe |
| 8 | `graph_mcp.semantic_search` | Validate the bound collection, then seed query families | Qdrant symbols/files/scores |
| 9 | `graph_mcp.explore_graph` | Expand every query family using the bound collection | FalkorDB nodes, relationships, paths, WHY |
| 10 | Vertical graph traversal tools | Trace retained anchors and module pairs through graph paths | Callers, callees, trigger -> handler -> outcome paths |
| 11 | `graph_mcp.reconstruct_flow` | Normalize paths already returned | Ordered candidate flow |
| 12 | `serena...` | Enrich Graph-RAG anchors and gaps | Source symbols, references, branches |

When documents are prohibited, omit steps 2-3. Never replace steps 7-8 with broad Serena search.

## Provider-Safe Calls

### `graph_mcp.activate_project`

Use:

```json
{"parser_type": "cplus"}
```

Do not include a database or graph argument. The MCP service controls FalkorDB selection.

### Active data context

Before analysis queries, bind this session state:

```text
ACTIVE_DATA_CONTEXT
  parser=cplus
  graph_provider=falkordb
  graph_context=active
  qdrant_collection=<selected C/C++ collection>
  qdrant_context=active
```

Choose the Qdrant candidate from project/repository/language metadata. Use one scoped semantic probe to validate it; if rejected, bind the next candidate and probe again. Do not start the query matrix until `DATA_CONTEXT_GATE: PASS`, and never issue an unscoped `semantic_search` or `explore_graph` call.

### `graph_mcp.semantic_search`

Use:

```json
{
  "query": "<module-aware semantic query>",
  "top_k": 20,
  "collection": "<validated code collection>",
  "expand_graph": false
}
```

Keep `expand_graph:false`; use `explore_graph` and vertical graph traversal tools for graph expansion.

### `graph_mcp.explore_graph`

Use for every applicable query family:

```json
{
  "query": "<module + behavior + relationship intent>",
  "mode": "graph_expanded",
  "top_k": 20,
  "collection": "<validated code collection>",
  "debug": true
}
```

Use `mode:"hybrid"` when live metadata supports it and it returns richer evidence. Retain query analysis, matched nodes, WHY reasons, relationships, entry candidates, paths, and confidence.

### `graph_mcp.reconstruct_flow`

Use only with normalized path candidates already returned by `explore_graph` or vertical graph traversal. It is not a discovery tool and must not manufacture missing edges.

### Vertical graph traversal

Use after `semantic_search` and `explore_graph` have produced retained graph node IDs or module pairs:

```json
{"function_id": "<retained node id>", "max_depth": 3, "direction": "in"}
```

```json
{"start_function_id": "<trigger node id>", "end_function_id": "<handler or outcome node id>", "max_depth": 6}
```

```json
{"start_id": "<trigger node id>", "end_id": "<handler or outcome node id>", "rel_types": ["CALLS", "POSSIBLE_CALLS"], "max_depth": 6}
```

For module boundaries, use the module-path variants with retained source and target module tokens. Run upstream and downstream traversal separately for each retained anchor before moving to Serena. If a path is absent, record the gap; do not replace it with another semantic search unless the gap introduces new vocabulary.

## Quarantined Calls

Never call `graph_mcp.list_databases`.

Do not invoke the following by default because their current C++ routes may bypass the configured FalkorDB provider:

- `search_functions`, `search_by_code`, `get_node_details`
- `listup_symbols_matching_file_path`, `listup_class_matching_path`, `list_up_entrypoint`
- `list_possible_calls`, `get_ipc_message`
- `find_workflows_containing`, `analyze_workflow_impact`

Vertical traversal calls (`query_subgraph`, `find_paths`, `trace_flow`, `find_path_between_module`, `trace_flow_between_module`) are required when live metadata lists them for the active graph MCP session and retained graph anchors exist. A quarantined call becomes usable only when live metadata explicitly states that its implementation is suitable for the active parser/provider and graph evidence is already established in the current session. Do not probe it for availability.

Dependency, SCC, screen, endpoint, and API-chain tools are also conditional until live metadata confirms their provider route.

## Failure and Output Policy

- Fast-fail once per capability.
- Retry once only for wrapper-level `invalid_parameters`.
- Store failures as `available`, `no-evidence`, or `unavailable`.
- Never expose raw exception text, endpoint, host, port, graph key, protocol, or driver.
- Never narrate a retry/fallback sequence.
- User-facing coverage is only `FalkorDB + Qdrant`, `Qdrant only`, or `Graph-RAG unavailable`.

## Serena Layer

Call `serena.initial_instructions({})`, then `serena.activate_project({project:"<target repository root>"})`.

| Goal | Tool | Inputs |
|---|---|---|
| File outline | `get_symbols_overview` | `relative_path`, optional `depth` |
| Class/method lookup | `find_symbol` | returned `name_path_pattern`, optional file, `depth`, `include_body` |
| Source callers | `find_referencing_symbols` | exact returned `name_path` and defining file |
| Regex/text evidence | `search_for_pattern` | `substring_pattern`, scoped paths/globs, context lines |

`search_for_pattern` already treats `substring_pattern` as regex. Serena returns zero-based line numbers. Every call must target a Graph-RAG anchor or named gap.

## Native Layer

Use `rg` and exact file reads only after both MCP layers leave a named gap and the user permits native tools. Skip this layer for MCP-only work.
