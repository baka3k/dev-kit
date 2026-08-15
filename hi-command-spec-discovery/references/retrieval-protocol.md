# Command Retrieval Protocol

## Contents

1. Authority and evidence rules
2. Complete graph_mcp call catalog
3. Module-first inventory
4. Exhaustive command tracing
5. Serena reconciliation
6. Native rg fallback
7. Coverage and failure gates

## Authority and evidence rules

Use the live `graph_mcp.list_mcp_functions` response as the authority for names, typed top-level inputs, outputs, provider limits, and examples. The Cortex Harness MCP README is a usage guide and may lag the running server. Retry once only when an `invalid_parameters` result supplies the corrected schema.

Never confuse a symbol name with its stable graph ID. Copy IDs from search or inventory results before calling symbol, path, subgraph, workflow, or impact tools. Verify repository path, project ID, parser, database, and Qdrant collection before accepting results. Reject cross-project hits.

Use read-only functions. Do not call `annotate_node`: it mutates the shared graph and is not needed to generate command documentation.

## Complete graph_mcp call catalog

“Core” means call for every run when the live server provides it. “Conditional” means call when the indexed language, provider, or command shape makes it applicable. A missing conditional function becomes a coverage gap.

### Session, routing, and scope

| Function | Purpose | Mode |
| --- | --- | --- |
| `list_mcp_functions` | Capture the live catalog and schemas; call first. | Core |
| `list_parsers` | Resolve parser alias, backend, labels, relationships, and feature gates. | Core |
| `list_databases` | Discover the graph/database containing the target repository. | Core |
| `list_qdrant_collections` | Find a semantic collection whose project identity matches the repository. | Core when semantic search exists |
| `activate_project` | Set verified parser/database defaults for the session. | Core when supported |

### Broad discovery

| Function | Purpose | Mode |
| --- | --- | --- |
| `semantic_search` | Seed behavior, command, validation, and protocol candidates from natural language. | Core with a verified collection |
| `explore_graph` | Combine semantic, keyword, and graph-expanded discovery for vague command concepts. | Conditional on provider capability |
| `search_functions` | Resolve partial command, dispatcher, class, type, and method names to stable IDs. | Core |
| `search_by_code` | Find opcodes, CLA/INS/P1/P2, TLV tags, lengths, status words, errors, logs, registrations, and terminal effects. | Core |

### Module, class, and function inventory

| Function | Purpose | Mode |
| --- | --- | --- |
| `listup_symbols_matching_file_path` | Enumerate functions, methods, classes, and types beneath every module path token. | Core |
| `listup_class_matching_path` | Expand every inventoried class/type into its declared methods. | Core when classes/types exist |
| `list_up_entrypoint` | Find symbols called from outside the selected module. | Core |
| `get_node_details` | Batch-fetch compact metadata for retained stable IDs. | Core |
| `get_symbol` | Fetch signatures, source, comments, and code for command anchors and unresolved branches. | Core for retained anchors |

### Call paths and execution flows

| Function | Purpose | Mode |
| --- | --- | --- |
| `query_subgraph` | Expand callers and callees around each queued symbol in bounded waves. | Core |
| `find_paths` | Prove dispatcher/entry-to-validator/terminal paths between stable IDs. | Core |
| `find_path_between_module` | Prove command paths that cross module/file boundaries. | Conditional when neighbors exist |
| `trace_flow` | Trace selected direct and indirect relationship types for a command path. | Core |
| `trace_flow_between_module` | Trace cross-module command execution with provider-aware relationships. | Conditional when crossings exist |
| `reconstruct_flow` | Format already verified path JSON into ordered, uncertainty-aware flows. | Conditional presentation aid; never proof by itself |

### Indirect, asynchronous, workflow, and full-stack bridges

| Function | Purpose | Mode |
| --- | --- | --- |
| `list_possible_calls` | Surface callbacks, virtual dispatch, function pointers, and `POSSIBLE_CALLS`. | Core when supported |
| `get_ipc_message` | Resolve sender/receiver, service, intent, message, or event bridges. | Conditional on IPC evidence |
| `find_screen_workflows` | Enumerate navigation paths that trigger or consume a command. | Conditional on UI commands |
| `find_workflows_containing` | Find direct or indirect workflows containing a command anchor. | Conditional on workflow data/provider |
| `analyze_workflow_impact` | Corroborate shared-anchor blast radius and regression scope. | Conditional; never sole evidence |
| `find_callers_of_endpoint` | Find frontend callers when the command is exposed through an API endpoint. | Conditional on endpoint evidence |
| `get_api_call_chain` | Trace component/endpoint through controller, service, repository, and database. | Conditional on full-stack evidence |

### Dependency shape and saturation

| Function | Purpose | Mode |
| --- | --- | --- |
| `plan_dependency_order` | Independently inventory module dependencies and cycles. | Core when available |
| `plan_file_dependency_order` | Inventory files, internal waves, and cross-module file edges. | Core when available |
| `plan_function_dependency_order` | Independently enumerate function IDs and call dependencies for reconciliation. | Core when available |
| `compute_scc` | Detect recursive/cyclic dispatcher, parser, retry, and state groups. | Conditional when cycles exist or are suspected |
| `topological_sort` | Produce deterministic traversal waves after SCC handling. | Conditional planning aid; never call-path proof |

### Existing-document corroboration

Use this family only when the live catalog exposes Living Docs and existing specifications are explicitly in scope. Existing text can corroborate code but cannot override it.

| Function | Purpose | Mode |
| --- | --- | --- |
| `livingdoc_get_links_for_symbol` | Find documents linked to a retained command symbol. | Conditional |
| `livingdoc_get_links_for_document` | Find code linked to an existing command document. | Conditional |
| `livingdoc_get_links_by_anchor` | Inspect all links touching one code/document anchor. | Conditional |
| `livingdoc_list_documents` | List documents that already have code links. | Conditional |
| `livingdoc_list_ingested_documents` | Detect ingested but unlinked specifications. | Conditional |
| `livingdoc_get_link_stats` | Record link health and orphan statistics. | Conditional |
| `livingdoc_trace_path` | Walk multi-hop code-document relationships. | Conditional |
| `livingdoc_derive_anchors_for_file` | Diagnose missing anchors for one existing spec file. | Conditional diagnostic |
| `livingdoc_validate_links` | Revalidate sampled links before citing them. | Conditional completion gate |

## Module-first inventory

Do not begin from a command handler alone. First build the complete source-file universe for each canonical module path, excluding only generated/vendor/build paths with recorded rules.

1. Call `listup_symbols_matching_file_path` separately for class/type and function/method labels reported by `list_parsers`.
2. Deduplicate by stable node ID while preserving qualified name, kind, file, lines, project ID, and graph source.
3. Pass every class/type to `listup_class_matching_path`; reconcile its method set against the file inventory.
4. Call `list_up_entrypoint` and tag external entries, framework callbacks, registrations, and unresolved entries.
5. Call all available `plan_*_dependency_order` functions. Treat their file/function sets as independent inventory evidence.
6. Batch `get_node_details`; retrieve full bodies with `get_symbol` only for entries, dispatchers, field parsers/encoders, branches, registrations, indirect calls, state writes, and terminal effects.
7. Compare graph file/class/function counts with Serena and `rg`. A mismatch remains a ledger item until explained.

## Exhaustive command tracing

Maintain deterministic `unseen`, `queued`, `traced`, `excluded`, and `gap` sets keyed by stable ID plus source anchor.

1. Seed from command names, opcodes, headers, tag/status constants, dispatch tables, serializers, parsers, registrations, error strings, and terminal effects.
2. Resolve names with `search_functions` and literals with `search_by_code`; use semantic functions only inside a verified project collection.
3. Expand each queued symbol with `query_subgraph` in increasing depth waves and explicit relationship types. Add every new in-scope symbol to the queue.
4. Prove candidate paths with `find_paths` and `trace_flow`; use module variants at boundaries.
5. Query `list_possible_calls` for each unresolved callback/dynamic dispatch and `get_ipc_message` for every sender/receiver clue.
6. Run applicable workflow, endpoint, and full-stack bridge calls. Provider failures trigger Serena/`rg` reconciliation.
7. Trace every branch to a terminal outcome: success response/status, protocol error, validation rejection, retry, abort, timeout, cancellation, persistence/action, or explicit fall-through.
8. Stop only when the queue is empty and a complete repeat of semantic/name/literal/registration/terminal-effect searches produces zero new stable IDs and zero new paths.

## Serena reconciliation

Activate the repository and read Serena’s instructions before symbolic work. Use these functions in order:

| Function | Purpose |
| --- | --- |
| `initial_instructions` | Load Serena’s operating rules once per session. |
| `activate_project` | Bind Serena to the requested `repo_root`. |
| `get_current_config` | Verify the active project when identity is uncertain. |
| `get_symbols_overview` | Inventory top-level symbols and immediate children for each relevant file. |
| `find_symbol` | Resolve classes/functions and retrieve children with `depth=1`; retrieve bodies only for retained anchors. |
| `find_referencing_symbols` | Find callers, registrations, constant uses, and cross-file references. |
| `search_for_pattern` | Find dispatch tables, macros, tags, opcodes, status words, and non-symbol text across code/non-code files. |

Use Serena to cover graph omissions, never to silently replace a mismatched graph inventory. Record graph-only, Serena-only, reconciled, excluded, and unresolved items.

## Native rg fallback

Use native search only after Serena yields no sufficient result or is unavailable:

```text
rg --files <module> -g '<source-glob>' -g '!<generated/vendor/build-glob>'
rg -n --hidden -g '<source-glob>' '<command|opcode|tag|status|registration-pattern>' <module>
rg -n '<resolved-symbol-or-literal>' <repo_root>
rg -l '<dispatcher-or-command-id>' <repo_root>
```

Prefer literal searches for exact hex values and escaped regex for alternations. Capture command, scope, exclusions, result count, and truncation in the ledger. Do not treat text co-occurrence as a call edge.

## Coverage and failure gates

Report raw numerators and denominators for files, classes/types, functions/methods, entry points, command seeds, request/response fields, status words, branches, indirect bridges, terminal outcomes, and diagram elements.

Respect result caps, `truncated`, omitted relationships, capability diagnostics, provider-specific errors, and runtime-only behavior. A missing/disconnected function fast-fails once. Empty results are valid only after identity, ID shape, direction, relationships, and provider support are checked once. Unresolved gaps force `partial` or `blocked`.
