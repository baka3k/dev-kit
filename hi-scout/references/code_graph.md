
---

# Code Graph MCP — Code Structure Functions

MCP server using ** Neo4j/FalkorDB** (code graph: functions, classes, calls, dependencies) + **Qdrant** (vector embeddings for semantic search).

The functions are organized by usage category.

---

## Infrastructure / Discovery

### `list_databases`

Lists all available Neo4j/FalkorDB databases.

**No params**

**Returns**: `Dict` containing a list of database names.

> **Note**: Do not call this directly. The MCP server owns the FalkorDB graph selection. Use `list_mcp_functions` then `list_parsers` instead.

---

### `list_mcp_functions`

Lists all MCP tools along with their descriptions, parameters, and use cases.

**No params**

**Returns**: `Dict` with a `total_count` and a list of `functions`.

**Use when**: You want to explore the full capabilities of the code_graph MCP.

---

### `list_parsers`

Lists the supported parser types (languages/frameworks).

**No params**

**Returns**: `Dict` with available parsers (cplus, java, kotlin, android, delphi, vba, vbnet, vb6, etc.).

---

### `list_qdrant_collections`

Lists Qdrant vector collections.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `qdrant_url` | str | No | None | Qdrant server URL |
| `include_vectors` | bool | No | False | Include vector metadata |

---

### `list_parsers`

Lists supported parser profiles and their language/framework aliases. Call this after `list_mcp_functions` to discover which `parser_type` values are valid for the active server.

**No params**

**Returns**: `Dict` with available parsers (cplus, java, kotlin, android, delphi, vba, vbnet, vb6, etc.) and their aliases.

**Use when**: Before passing `parser_type` to `explore_graph` or other calls to confirm the correct alias for your codebase.

---

## Search & Discovery

### `search_functions`

Searches for functions/classes/types by name or qualified name. Returns both node details AND IDs.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Search terms separated by `|`. Case-insensitive substring match |
| `limit` | int | No | 50 | Max results |
| `project_id` | str | No | None | Project identifier — selects the graph shard via the project registry. Omit for env-default full search. |
| `content_mode` | str | No | "auto" | Output format: auto, summary, comment, code, name |
| `include_raw_fields` | bool | No | False | Include raw Nep4k/Falkor properties |
| `node_type` | str | No | "code" | Domain filter: code or doc |
| `expand_search` | bool | No | False | Cross-domain traversal |

**Returns**: `{results: [...], ids: [...], db: "..."}` (the `db` field in output is informational only)

**Use when**: You know the exact or partial name of the function/class you are looking for.

---

### `search_by_code`

Finds code snippets by matching text inside function bodies.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Code text (case-sensitive) |
| `limit` | int | No | 50 | Max results |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `content_mode` | str | No | "auto" | auto, summary, comment, code, name |
| `include_raw_fields` | bool | No | False |  |
| `node_type` | str | No | "code" | code or doc |
| `expand_search` | bool | No | False |  |

**Returns**: `Dict` containing the matching nodes that include the code snippet.

---

### ⭐ `semantic_search` — GO-TO FOR QUICK SEARCH

> **This is the most commonly used discovery function.** Start here when you don't know exact function names — describe what you're looking for in plain English and it finds semantically similar code via Qdrant vector embeddings. Much faster and more intuitive than `search_functions` for initial exploration.

**Vector semantic code search** — finds conceptually similar code using natural language.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Natural language query or code snippet |
| `mode` | str | No | "hybrid" | code, comment, hybrid |
| `top_k` | int | No | 10 | Number of results |
| `collection` | str | No | None | Qdrant collection name |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `qdrant_url` | str | No | None |  |
| `expand_graph` | bool | No | False | Expand results with call-graph neighbours from FalkorDB. Keep `false`; use `explore_graph` for graph expansion. |
| `graph_depth` | int | No | None | Traversal depth when `expand_graph` is true |
| `graph_direction` | str | No | None | `in`, `out`, or `both` when `expand_graph` is true |
| `graph_rel_types` | str | No | None | Comma-separated relationship types when `expand_graph` is true |
| `graph_limit` | int | No | None | Max graph-expanded nodes when `expand_graph` is true |

**Use when**: Describing the functionality in natural language rather than using an exact name. For example: "allocate memory safely", "how does authentication work", "error handling for database connections".

---

### `explore_graph`

**Hybrid graph explorer** — combines semantic search + BM25 keyword search + call-graph expansion. Supports both English and Vietnamese.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Natural language (keyword, sentence, or paragraph) |
| `mode` | str | No | "hybrid" | semantic, hybrid, graph_expanded |
| `top_k` | int | No | 10 | Max matched nodes |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `collection` | str | No | None | Qdrant collection |
| `debug` | bool | No | False | Include per-signal score breakdown |
| `parser_type` | str | No | None | Parser profile: cplus, java, kotlin, android, etc. Replaces session-level project activation. |

**Returns**: `{matched_nodes, entry_points, related_paths, explanation, confidence, query_analysis, mode}`

**Use when**: Querying with ambiguous or high-level natural language descriptions. This is the most powerful search tool available.

---

### `listup_symbols_matching_file_path`

Lists all symbols within files that match a specific path pattern.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `modules` | List[str] | **Yes** |  | File path patterns |
| `node_types` | List[str] | No | All symbols | Filter: ["Function"], ["Class", "Type"], etc. |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `content_mode` | str | No | "auto" |  |

**Use when**: You want an inventory of all symbols inside a specific file or module.

---

### `listup_class_matching_path`

Lists all functions/methods inside classes that match a name pattern.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `class_names` | List[str] | **Yes** |  | Class name patterns |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

### `list_up_entrypoint`

Finds entry point functions: functions within the target modules that are called from OUTSIDE those modules.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `modules` | List[str] | **Yes** |  | Module/file path patterns |
| `limit` | int | No | 200 | Max results |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

**Use when**: Identifying the public API or external interface of a module.

---

## Detail & Inspection

### `get_symbol`

Fetches detailed metadata for a specific node using its ID.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `node_id` | str | **Yes** |  | Node ID from search results |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `content_mode` | str | No | "auto" | auto, summary, comment, code, name |
| `include_raw_fields` | bool | No | False |  |
| `node_type` | str | No | "code" | code or doc |

**Returns**: `{name, qualified_name, file_path, signature, code, comment, ...}`

---

### `get_node_details`

Batch-fetches metadata for multiple nodes (significantly more efficient than calling `get_symbol` multiple times).

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `node_ids` | List[str] | **Yes** |  | List of node IDs |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `content_mode` | str | No | "auto" |  |
| `include_raw_fields` | bool | No | False |  |
| `node_type` | str | No | "code" |  |

---

### `annotate_node`

Adds an annotation (notes, tags, or severity level) to a node for code review or documentation purposes.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `node_id` | str | **Yes** |  | Node ID |
| `note` | str | No | None | Text note |
| `tags` | str | No | None | Comma-separated tags |
| `severity` | str | No | None | high, medium, low |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

## Call Graph & Tracing

### Trace routing contract

Resolve a function name to a stable graph ID before tracing:

```text
search_functions(query="<function_name>", parser_type="<type>")
```

Retain the returned `node_id`/`symbol_id`, then select the narrowest tool that answers the question:

| Intent | Tool | Key routing |
| --- | --- | --- |
| One function, all nearby callers and callees | `query_subgraph` | `direction:"all"`, default, normally `max_depth:2` |
| Callers only | `query_subgraph` | `direction:"upstream"` |
| Callees only | `query_subgraph` | `direction:"downstream"` |
| Relationship-filtered expansion, including possible calls, function pointers, or callbacks | `trace_flow` | `direction:"out"` or `"in"`, selected `rel_types`, up to `max_depth:6` |
| A known start function to a known end function | `find_paths` | pass both stable function IDs |
| Workflows affected by changing a function | `analyze_workflow_impact` | pass the stable function ID; retain severity and risk evidence |

Use `query_subgraph` for the fast neighborhood view. Use `trace_flow` when relationship selection or deeper indirect traversal is material. Do not substitute either for `find_paths` when both endpoints are known.

### `query_subgraph`

Retrieves the call graph context around a function: its callers (who calls it) and its callees (who it calls).

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `function_id` | str | **Yes** |  | Starting function node ID |
| `direction` | str | No | "all" | `all` (callers and callees), `upstream` (callers), or `downstream` (callees) |
| `max_depth` | int | No | 2 | Maximum `CALLS` hops |
| `parser_type` | str | No | None | Parser profile when known |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `content_mode` | str | No | "auto" |  |
| `include_raw_fields` | bool | No | False |  |
| `node_type` | str | No | "code" |  |
| `expand_search` | bool | No | False | Include bridge nodes from the opposite domain |

**Returns**: `{nodes: [...], edges: [...]}`

**Use when**: Understanding function dependencies — seeing what relies on this function and what this function relies on.

```text
query_subgraph(function_id="<symbol_id>", direction="all", max_depth=2, parser_type="<type>")
query_subgraph(function_id="<symbol_id>", direction="upstream", max_depth=2)
query_subgraph(function_id="<symbol_id>", direction="downstream", max_depth=2)
```

---

### `find_paths`

Finds all execution call paths between two specific functions.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `start_function_id` | str | **Yes** |  | Starting function ID |
| `end_function_id` | str | **Yes** |  | Target function ID |
| `max_depth` | int | No | 5 | Max path length |
| `relationship_types` | List[str] | No | ["CALLS"] |  |
| `parser_type` | str | No | None | Parser profile when known |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `content_mode` | str | No | "auto" |  |
| `include_raw_fields` | bool | No | False |  |
| `node_type` | str | No | "code" |  |
| `expand_search` | bool | No | False |  |

**Returns**: `{paths: [{nodes: [...], edges: [...]}]}`

**Use when**: Tracing how function A can eventually trigger or reach function B.

---

### `find_path_between_module`

Finds call paths between modules or files using file path patterns. Supports bidirectional searches.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `source_modules` | List[str] | **Yes** |  | Source file path patterns |
| `target_modules` | List[str] | **Yes** |  | Target file path patterns |
| `max_depth` | int | No | 6 | Max path length |
| `direction` | str | No | "out" | out, in, both (automatically retries with both) |
| `include_possible` | bool | No | False | Include POSSIBLE_CALLS edges |
| `include_fp` | bool | No | False | Include function pointer calls |
| `limit` | int | No | 10 | Max paths |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

**Use when**: Mapping and understanding cross-module dependencies.

---

### `trace_flow`

Performs advanced flow tracing using custom relationship types.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `start_id` | str | **Yes** |  | Start function ID |
| `end_id` | str | No | None | Optional end anchor; use `find_paths` when the question is specifically start → end |
| `direction` | str | No | None | `out` or `in`; pass explicitly |
| `rel_types` | List[str] | No | ["CALLS"] | Selected relationship types such as `CALLS` and `POSSIBLE_CALLS` |
| `max_depth` | int | No | None | Set up to 6 for deeper traversal |
| `parser_type` | str | No | None | Parser profile when known |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

Use `trace_flow` for indirect or callback-aware expansion:

```text
trace_flow(
  start_id="<symbol_id>",
  direction="out",
  rel_types=["CALLS", "POSSIBLE_CALLS"],
  max_depth=6,
  parser_type="<type>"
)
```

---

### `trace_flow_between_module`

Advanced module-to-module flow tracing utilizing custom relationships.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `source_modules` | List[str] | **Yes** |  |  |
| `target_modules` | List[str] | **Yes** |  |  |
| `rel_types` | List[str] | No | None |  |
| `max_depth` | int | No | None |  |
| `direction` | str | No | None |  |
| `limit` | int | No | None |  |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

### `list_possible_calls`

Lists `POSSIBLE_CALLS` relationships, such as function pointers, virtual calls, and callback registrations.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `limit` | int | No | 100 | Max results |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

## Planning / Dependency Ordering

### `compute_scc`

Computes Strongly Connected Components (SCC) from the dependency graph to detect dependency cycles.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `nodes` | List[str] | No | None |  |
| `edges` | List[Dict] | No | None | `[{"from": "A", "to": "B"}]` |
| `edge_semantics` | str | No | "depends_on" | depends_on or calls |
| `include_singletons` | bool | No | False |  |

**Returns**: `{components[{scc_id, nodes, size, is_cycle}], node_to_scc, cycle_summary}`

---

### `topological_sort`

Performs a topological sort on a dependency graph, ordering components into a linear sequence or parallel waves.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `nodes` | List[str] | No | None |  |
| `edges` | List[Dict] | No | None |  |
| `edge_semantics` | str | No | "depends_on" | depends_on or calls |
| `output_mode` | str | No | "both" | linear, waves, both |
| `on_cycle` | str | No | "auto_condense_scc" | auto_condense_scc or error |

---

### `plan_dependency_order`

Plans a module-level dependency order based on `CALLS` edges.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `modules` | List[str] | **Yes** |  | Module tokens matched against file_path |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `edge_semantics` | str | No | None |  |
| `on_cycle` | str | No | None |  |

**Returns**: `{waves[{wave, modules}], module_order, depends_on_map, module_dependencies, ...}`

---

### `plan_file_dependency_order`

Plans a file-level dependency order for individual modules based on `CALLS` edges.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `modules` | List[str] | **Yes** |  |  |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `edge_semantics` | str | No | None |  |
| `on_cycle` | str | No | None |  |
| `include_cross_module` | bool | No | False |  |
| `max_files_per_module` | int | No | None |  |

---

### `plan_function_dependency_order`

Plans a function-level dependency order within specified modules.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `modules` | List[str] | **Yes** |  |  |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `edge_semantics` | str | No | None |  |
| `on_cycle` | str | No | None |  |
| `include_cross_module` | bool | No | False |  |
| `include_lambdas` | bool | No | False |  |
| `max_functions_per_module` | int | No | None |  |

---

## Workflows (Frontend/Fullstack)

### `list_workflows`

Lists available predefined workflow definitions.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `project` | str | No | None | Project filter |
| `language` | str | No | None | Language filter |
| `domain` | str | No | None | Domain filter |
| `limit` | int | No | None |  |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

### `search_workflows`

Searches for workflows matching specific keywords.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Keyword search query |
| `limit` | int | No | None |  |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

### `get_workflow_steps`

Retrieves the ordered sequential function steps belonging to a workflow.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `workflow_id` | str | **Yes** |  | Workflow ID |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

### `find_screen_workflows`

Finds screen-to-screen `NAVIGATE` workflows within a React/TS project.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `project_id` | str | **Yes** |  | Project scope |
| `node_a` | str | **Yes** |  | Screen name or symbol_id. Acts as source in pair mode; anchor in single mode |
| `node_b` | str | No | None | Second screen → activates pair mode |
| `direction` | str | No | "bidirectional" | Single mode options: inbound, outbound, bidirectional |
| `max_hops` | int | No | 8 | Max NAVIGATE hops (capped at 20) |
| `max_paths` | int | No | 100 | Max workflows (capped at 1000) |
| `include_entry_function` | bool | No | False |  |
| `include_api_calls` | bool | No | False |  |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

## Fullstack / Cross-Layer

### `find_callers_of_endpoint`

Finds frontend functions or screens that call a specific backend API endpoint.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `endpoint_path` | str | **Yes** |  | e.g., "/api/users/:id" |
| `http_method` | str | No | None | GET, POST, PUT, DELETE, ALL |
| `be_project_id` | str | No | None | Backend project filter |
| `fe_project_id` | str | No | None | Frontend project filter |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

### `get_api_call_chain`

Traces a fullstack call chain across layers: from frontend components down to backend handlers (`ApiEndpoint` → `Controller` → `Service` → `Repository` → `Database`).

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `component_name` | str | No | None | Frontend component/screen name |
| `endpoint_path` | str | No | None | Backend endpoint path (used if component_name is omitted) |
| `fe_project_id` | str | No | None |  |
| `be_project_id` | str | No | None |  |
| `max_depth` | int | No | 5 | Max frontend CALLS hops |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

## Impact Analysis

### `analyze_workflow_impact`

Analyzes the potential impact of changing a function or screen, providing a risk score and modification recommendations.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `function_id` | str | **Yes** |  | Function/screen symbol_id |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `direction` | str | No | None | downstream or upstream |
| `max_depth` | int | No | 4 | Capped at 4 |

**Returns**: `{risk_score, impacted_nodes, workflow_impact}`

---

### `find_workflows_containing`

Finds workflows that include a specific function (either directly via `HAS_STEP` or indirectly through a `CALLS` chain).

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `function_id` | str | **Yes** |  | Function symbol_id or file_path |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |
| `include_indirect` | bool | No | True | Include CALLS-chain derived workflows |
| `max_depth` | int | No | 4 | Capped at 4 |

---

## IPC / Android

### `get_ipc_message`

Queries IPC/message records filtered by sender and receiver patterns (Android Intent flows).

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sender` | str | No | None | Sender component pattern |
| `receiver` | str | No | None | Receiver component pattern |
| `project_id` | str | No | None | Project identifier (omit for env-default full search) |

---

## Flow Reconstruction

### `reconstruct_flow`

Reconstructs possible execution flows from a selection of candidate graph paths. Supports backend, frontend, and hybrid environments.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `entry_context_json` | str | **Yes** |  | `{"type":"backend|frontend|hybrid", "entry_point":"...", "entry_node_id":"...", "screen":null, "trigger":null}` |
| `paths_json` | str | **Yes** |  | JSON array of path objects: `[{"path_id":"...", "nodes":[...], "edges":[...]}]` |

---

## Typical Discovery Flow

```
1. list_mcp_functions()                              → Discover capabilities
2. list_parsers()                                    → Confirm parser_type alias for your language
3. list_qdrant_collections()                         → Identify code collections
4. semantic_search(query, collection, top_k)         → Validate collection; seed query families
5. explore_graph(query, parser_type, collection)     → Semantic + graph expanded discovery
6. listup_symbols_matching_file_path([...])          → Inventory components and symbols
7. search_functions("keyword|keyword")               → Find symbols by name
8. get_symbol(node_id)                               → Inspect deep implementation details
9. query_subgraph(function_id, direction="all")      → Fast caller + callee neighbourhood
10. trace_flow(start_id, rel_types, max_depth=6)      → Filtered indirect/callback-aware traversal
11. find_paths(start_function_id, end_function_id)   → Trace an exact start → end path
12. analyze_workflow_impact(function_id)              → Assess affected workflows and risk

```

---
