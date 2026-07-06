
---

# Code Graph MCP — Code Structure Functions

MCP server using **Neo4j** (code graph: functions, classes, calls, dependencies) + **Qdrant** (vector embeddings for semantic search).

The functions are organized by usage category.

---

## Infrastructure / Discovery

### `list_databases`

Lists all available Neo4j databases.

**No params**

**Returns**: `Dict` containing a list of database names.

**Use when**: Always call this first to discover which projects are available.

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

### `activate_project`

Sets the default parser_type and database for the current session. **Must be called before querying the code graph.**

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `parser_type` | str | No | None | Parser: cplus/cpp/c++/c/clang/delphi/pascal/java/kotlin/jvm/vbnet/vb6/vba/vbscript/android/android-kotlin |
| `database_name` | str | No | None | Neo4j database name |

**Use when**: At the beginning of each session, after selecting a project.

---

## Search & Discovery

### `search_functions`

Searches for functions/classes/types by name or qualified name. Returns both node details AND IDs.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Search terms separated by `|`. Case-insensitive substring match |
| `limit` | int | No | 50 | Max results |
| `db` | str | No | Activate default | Database name |
| `content_mode` | str | No | "auto" | Output format: auto, summary, comment, code, name |
| `include_raw_fields` | bool | No | False | Include raw Neo4j properties |
| `node_type` | str | No | "code" | Domain filter: code or doc |
| `expand_search` | bool | No | False | Cross-domain traversal |

**Returns**: `{results: [...], ids: [...], db: "..."}`

**Use when**: You know the exact or partial name of the function/class you are looking for.

---

### `search_by_code`

Finds code snippets by matching text inside function bodies.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Code text (case-sensitive) |
| `limit` | int | No | 50 | Max results |
| `db` | str | No | Activate default |  |
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
| `qdrant_url` | str | No | None |  |

**Use when**: Describing the functionality in natural language rather than using an exact name. For example: "allocate memory safely", "how does authentication work", "error handling for database connections".

---

### `explore_graph`

**Hybrid graph explorer** — combines semantic search + BM25 keyword search + call-graph expansion. Supports both English and Vietnamese.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Natural language (keyword, sentence, or paragraph) |
| `mode` | str | No | "hybrid" | semantic, hybrid, graph_expanded |
| `top_k` | int | No | 10 | Max matched nodes |
| `db` | str | No | None | Database name |
| `collection` | str | No | None | Qdrant collection |
| `debug` | bool | No | False | Include per-signal score breakdown |

**Returns**: `{matched_nodes, entry_points, related_paths, explanation, confidence, query_analysis, mode}`

**Use when**: Querying with ambiguous or high-level natural language descriptions. This is the most powerful search tool available.

---

### `listup_symbols_matching_file_path`

Lists all symbols within files that match a specific path pattern.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `modules` | List[str] | **Yes** |  | File path patterns |
| `node_types` | List[str] | No | All symbols | Filter: ["Function"], ["Class", "Type"], etc. |
| `db` | str | No | Activate default |  |
| `content_mode` | str | No | "auto" |  |

**Use when**: You want an inventory of all symbols inside a specific file or module.

---

### `listup_class_matching_path`

Lists all functions/methods inside classes that match a name pattern.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `class_names` | List[str] | **Yes** |  | Class name patterns |
| `db` | str | No | Activate default |  |

---

### `list_up_entrypoint`

Finds entry point functions: functions within the target modules that are called from OUTSIDE those modules.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `modules` | List[str] | **Yes** |  | Module/file path patterns |
| `limit` | int | No | 200 | Max results |
| `db` | str | No | Activate default |  |

**Use when**: Identifying the public API or external interface of a module.

---

## Detail & Inspection

### `get_symbol`

Fetches detailed metadata for a specific node using its ID.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `node_id` | str | **Yes** |  | Node ID from search results |
| `db` | str | No | Activate default |  |
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
| `db` | str | No | Activate default |  |
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
| `db` | str | No | Activate default |  |

---

## Call Graph & Tracing

### `query_subgraph`

Retrieves the call graph context around a function: its callers (who calls it) and its callees (who it calls).

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `function_id` | str | **Yes** |  | Starting function node ID |
| `max_depth` | int | No | 2 | Graph traversal depth |
| `relationship_types` | List[str] | No | ["CALLS"] | Filter relationship types |
| `direction` | str | No | "both" | out (callees), in (callers), both |
| `db` | str | No | Activate default |  |
| `content_mode` | str | No | "auto" |  |
| `include_raw_fields` | bool | No | False |  |
| `node_type` | str | No | "code" |  |
| `expand_search` | bool | No | False | Include bridge nodes from the opposite domain |

**Returns**: `{nodes: [...], edges: [...]}`

**Use when**: Understanding function dependencies — seeing what relies on this function and what this function relies on.

---

### `find_paths`

Finds all execution call paths between two specific functions.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `start_function_id` | str | **Yes** |  | Starting function ID |
| `end_function_id` | str | **Yes** |  | Target function ID |
| `max_depth` | int | No | 5 | Max path length |
| `relationship_types` | List[str] | No | ["CALLS"] |  |
| `db` | str | No | Activate default |  |
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
| `db` | str | No | Activate default |  |

**Use when**: Mapping and understanding cross-module dependencies.

---

### `trace_flow`

Performs advanced flow tracing using custom relationship types.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `start_id` | str | **Yes** |  | Start function ID |
| `end_id` | str | **Yes** |  | End function ID |
| `rel_types` | List[str] | No | ["CALLS"] | Custom relationship types |
| `max_depth` | int | No | None |  |
| `direction` | str | No | None |  |
| `db` | str | No | Activate default |  |

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
| `db` | str | No | Activate default |  |

---

### `list_possible_calls`

Lists `POSSIBLE_CALLS` relationships, such as function pointers, virtual calls, and callback registrations.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `limit` | int | No | 100 | Max results |
| `db` | str | No | Activate default |  |

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
| `db` | str | No | Activate default |  |
| `edge_semantics` | str | No | None |  |
| `on_cycle` | str | No | None |  |

**Returns**: `{waves[{wave, modules}], module_order, depends_on_map, module_dependencies, ...}`

---

### `plan_file_dependency_order`

Plans a file-level dependency order for individual modules based on `CALLS` edges.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `modules` | List[str] | **Yes** |  |  |
| `db` | str | No | Activate default |  |
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
| `db` | str | No | Activate default |  |
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
| `db` | str | No | Activate default |  |

---

### `search_workflows`

Searches for workflows matching specific keywords.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `query` | str | **Yes** |  | Keyword search query |
| `limit` | int | No | None |  |
| `db` | str | No | Activate default |  |

---

### `get_workflow_steps`

Retrieves the ordered sequential function steps belonging to a workflow.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `workflow_id` | str | **Yes** |  | Workflow ID |
| `db` | str | No | Activate default |  |

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
| `db` | str | No | "neo4j" |  |

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
| `db` | str | No | Activate default |  |

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
| `db` | str | No | Activate default |  |

---

## Impact Analysis

### `analyze_workflow_impact`

Analyzes the potential impact of changing a function or screen, providing a risk score and modification recommendations.

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `function_id` | str | **Yes** |  | Function/screen symbol_id |
| `db` | str | No | Activate default |  |
| `direction` | str | No | None | downstream or upstream |
| `max_depth` | int | No | 4 | Capped at 4 |

**Returns**: `{risk_score, impacted_nodes, workflow_impact}`

---

### `find_workflows_containing`

Finds workflows that include a specific function (either directly via `HAS_STEP` or indirectly through a `CALLS` chain).

| Param | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `function_id` | str | **Yes** |  | Function symbol_id or file_path |
| `db` | str | No | Activate default |  |
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
| `db` | str | No | Activate default |  |

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
1. list_databases()                         → Select database
2. list_mcp_functions()                     → Discover capabilities
3. activate_project(parser_type, db)        → Set environment session context
4. listup_symbols_matching_file_path([...]) → Inventory components and symbols
5. search_functions("keyword|keyword")       → Find symbols by name
6. explore_graph("natural language query")  → Find symbols semantically
7. get_symbol(node_id)                      → Inspect deep implementation details
8. query_subgraph(function_id)              → Understand the call graph neighborhood
9. find_paths(start_id, end_id)             → Trace exact execution paths

```

---
