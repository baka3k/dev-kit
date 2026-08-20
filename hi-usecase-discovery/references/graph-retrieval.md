# Graph Retrieval Protocol

## Contents

1. Authority and safety
2. Complete read-side function set
3. Session and scope preflight
4. Module inventory calls
5. Discovery and trace calls
6. Provider and failure rules

## Authority and safety

The live `list_mcp_functions` response is authoritative. The Cortex Harness MCP README is a usage guide, but its tool count, parameter types, provider notes, and examples can lag the running server. At the start of every run, capture the live catalog and use its typed top-level parameters. Retry once only when an invalid-parameters response supplies a corrected schema.

Use read-side tools only. `annotate_node` mutates the shared graph and is intentionally excluded. Do not hard-code an endpoint, port, database, collection, provider, project ID, or obsolete parameter shape.

## Complete read-side function set

The following is the complete `graph_mcp` set used by this skill when present. “Core” means run for every module. “Conditional” means run when the corresponding graph feature or code shape exists. A missing conditional tool becomes a recorded coverage gap, not an invented result.

### Session and scope

| Function | Use | Minimum input | Mode |
| --- | --- | --- | --- |
| `list_mcp_functions` | Capture the live names, schemas, examples, and capabilities. | none | Core, first call |
| `list_parsers` | Resolve parser aliases, backend, labels, and feature gates. | none | Core |
| `list_databases` | Select the graph that contains the requested project. | parser context | Core |
| `list_qdrant_collections` | Select a semantic collection whose project identity matches the repository. | parser/database context | Core when semantic search exists |
| `activate_project` | Set parser/database session defaults after identity is verified. | `parser_type`, optional database | Core when supported |

### Broad discovery

| Function | Use | Minimum input | Mode |
| --- | --- | --- | --- |
| `semantic_search` | Seed candidates from business behavior and domain terms. | `query`, verified collection | Core when a matching collection exists |
| `explore_graph` | Fuse semantic, keyword, and graph context for vague concepts. | `query` | Conditional on provider capability |
| `search_functions` | Resolve partial class/function/type names to stable node IDs. | `query` | Core |
| `search_by_code` | Find literal SQL, routes, IDs, logs, errors, API calls, and terminal effects. | `query` | Core |

### Inventory and details

| Function | Use | Minimum input | Mode |
| --- | --- | --- | --- |
| `listup_symbols_matching_file_path` | Enumerate classes, types, functions, and methods under each module path token. | `modules`, `node_types` | Core |
| `listup_class_matching_path` | Expand every class/type name to its declared methods. | `class_names` | Core when classes/types exist |
| `list_up_entrypoint` | Find functions in the module called from outside it. | `modules` | Core |
| `get_symbol` | Fetch one retained symbol’s signature, location, code, and metadata. | `node_id` | Core for anchors |
| `get_node_details` | Batch-fetch retained nodes without broad body retrieval. | `node_ids` | Core |

### Paths and flows

| Function | Use | Minimum input | Mode |
| --- | --- | --- | --- |
| `query_subgraph` | Quickly expand one function: `all` callers/callees (default), `upstream` callers, or `downstream` callees. | `function_id`; optional direction, depth 2, parser | Core |
| `find_paths` | Prove a path between an entry/branch and a terminal symbol. | start and end IDs | Core |
| `find_path_between_module` | Discover crossings between the selected module and named neighbors. | source and target module tokens | Core when neighbors exist |
| `trace_flow` | Expand from one anchor with selected direct/possible/function-pointer/callback relationships, up to depth 6. | `start_id`, `direction` (`out`/`in`), `rel_types` | Core when indirect traversal matters |
| `trace_flow_between_module` | Validate cross-module flows and direction. | source/target module tokens | Core when crossings exist |
| `reconstruct_flow` | Convert already verified path JSON into an ordered narrative. | entry-context JSON and paths JSON | Conditional presentation step |

### Indirect and asynchronous bridges

| Function | Use | Minimum input | Mode |
| --- | --- | --- | --- |
| `list_possible_calls` | Surface callbacks, virtual dispatch, function pointers, and other `POSSIBLE_CALLS`. | optional `function_id` | Core for supported parsers |
| `get_ipc_message` | Resolve sender/receiver message, event, service, or intent bridges. | sender and/or receiver | Conditional on IPC evidence |

### Dependency shape and saturation

| Function | Use | Minimum input | Mode |
| --- | --- | --- | --- |
| `plan_dependency_order` | Inventory module-level call dependencies and cycles. | module tokens | Core when available |
| `plan_file_dependency_order` | Inventory files, internal call waves, and cross-module file edges. | module tokens | Core when available |
| `plan_function_dependency_order` | Independently enumerate function IDs and call dependencies for reconciliation. | module tokens | Core when available |
| `compute_scc` | Detect recursive/cyclic groups in collected nodes and edges. | collected nodes/edges | Conditional when cycles are present or suspected |
| `topological_sort` | Produce deterministic waves after SCC handling; use for traversal order, not proof. | collected nodes/edges | Conditional after dependency collection |

### Workflow, UI, and full-stack bridges

| Function | Use | Minimum input | Mode |
| --- | --- | --- | --- |
| `find_screen_workflows` | Enumerate React/TypeScript navigation paths around a screen. | verified `project_id`, screen node | Conditional on UI navigation |
| `find_workflows_containing` | Find direct and indirect workflows containing an anchor function. | `function_id` | Conditional; provider may be Neo4j-only |
| `analyze_workflow_impact` | Add workflow membership/blast-radius evidence for shared anchors. | `function_id` | Conditional corroboration, never sole proof |
| `find_callers_of_endpoint` | Find frontend callers of a verified backend endpoint. | endpoint path and project scopes | Conditional; provider may be Neo4j-only |
| `get_api_call_chain` | Trace UI/endpoint through controller, service, repository, and database. | component or endpoint plus scopes | Conditional; provider may be Neo4j-only |

## Session and scope preflight

1. Call `list_mcp_functions`; save the catalog/version evidence in the run ledger.
2. Call `list_parsers`, `list_databases`, and, if semantic search is available, `list_qdrant_collections`.
3. Match repository path, project ID/name, language, parser, database, and collection. Never accept a semantic hit from another repository as evidence.
4. Call `activate_project` only after the match. Echo the resolved identity into every phase artifact.
5. Run one known-symbol smoke query. Empty or cross-project results mean the scope is not proven; fall through to Serena rather than repeatedly probing the graph.

## Module inventory calls

For every canonical module path token:

1. Call `listup_symbols_matching_file_path` with the live node labels for class/type/function nodes and compact content.
2. Deduplicate by stable node ID; preserve qualified name, kind, file, start/end line, project ID, and graph source.
3. Pass every returned class/type name to `listup_class_matching_path`; reconcile declared methods with the first list.
4. Call `list_up_entrypoint`; tag external callers, framework entries, and unresolved entries separately.
5. Call the three `plan_*_dependency_order` functions. Use their module/file/function sets as independent inventory evidence, not merely planning output.
6. Batch `get_node_details` for retained IDs; use `get_symbol` with code bodies only for entry, branch, registration, indirect-call, and terminal anchors.
7. A count mismatch creates a ledger item. Resolve it using Serena, then `rg`; never silently choose the larger or smaller count.

## Discovery and trace calls

Use semantic results only as seeds. Confirm each seed through stable graph IDs and source locations.

1. Search behavior/domain queries with `semantic_search` or `explore_graph` only inside a verified project collection.
2. Search discovered names with `search_functions(query, parser_type)` and retain the returned node IDs; search routes, messages, data IDs, error strings, SQL, writes, and emitted events with `search_by_code`.
3. Add retained IDs to the tracing queue. Start with `query_subgraph(direction:"all", max_depth:2)`; use `upstream` for callers and `downstream` for callees when only one side is material.
4. Use `trace_flow` with direction `out` or `in`, `rel_types:["CALLS","POSSIBLE_CALLS"]`, and `max_depth:6` for indirect/callback-aware expansion. Use `find_paths` when both candidate endpoint IDs are known, and module variants at module boundaries.
5. Query `list_possible_calls` for every unresolved dispatch/callback site and `get_ipc_message` for every sender/receiver clue.
6. Run applicable workflow/UI/API bridge tools. Provider errors remain explicit gaps and trigger Serena/`rg` reconciliation.
7. Call `reconstruct_flow` only with path objects already retained in the evidence ledger. It formats evidence; it does not create proof.

Run relationship passes deliberately instead of relying on one provider default:

- containment/inventory: `DECLARES`, `CONTAINS`, `DEPENDS_ON`;
- executable calls: `CALLS`;
- indirect dispatch: `POSSIBLE_CALLS`, `CALLS_FUNCTION_POINTER`;
- UI/control/resource bridges when supported: `BINDS_CONTROL`, `HANDLES_CONTROL`, `OWNS_DIALOG`, `USES_RESOURCE`, `NAVIGATE`;
- workflow/full-stack bridges when supported: `HAS_STEP`, `CALLS_API`, `MATCHES`.

First inspect the live parser/provider relationship schema. Record unsupported or omitted relationships from capability diagnostics; never assume a label exists because it appears in this reference.

## Provider and failure rules

- Use typed top-level inputs from the live catalog. Arrays, strings, and numeric fields have changed historically.
- Treat empty results as valid responses until project scope, node ID type, direction, relationship types, and provider support are checked once.
- Respect `truncated`, omitted relationships, capability diagnostics, result limits, and provider-specific errors. Any unresolved truncation makes coverage partial.
- Keep compact results for breadth. Retrieve bodies only for retained anchors.
- Never infer a direct call from `POSSIBLE_CALLS`, shared state, naming similarity, or reconstructed prose.
- Fast-fail a missing/disconnected capability once. Retry only an invalid-parameters response with its supplied schema.
