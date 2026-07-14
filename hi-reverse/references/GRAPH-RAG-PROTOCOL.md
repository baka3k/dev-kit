# FalkorDB Graph-RAG Saturation Protocol

Use this protocol for every discovery, tracing, mapping, glossary, review, or documentation phase that needs code evidence. The target is maximum relevant coverage with a reproducible evidence trail, not arbitrary call volume.

## 1. Capture Constraints

Record:

- repository root and target module/path
- C/C++ parser and configured FalkorDB provider
- user scope and requested artifact
- whether project documents are allowed
- whether native tools are allowed
- active repository search-priority and fast-fail rules

Never use a prohibited source. Store capability failures only as normalized statuses; never expose infrastructure details.

## 2. Ordered Preflight

Execute in order:

| Order | Call | Retain | Decision |
|---|---|---|---|
| 1 | `mind_mcp.list_qdrant_collections({})` | Available knowledge/code corpora | Identify project context |
| 2 | `mind_mcp.list_source_ids({limit:"200"})` when documents are allowed | Allowed document source IDs | Scope knowledge retrieval |
| 3 | `mind_mcp.query_graph_rag_langextract(...)` when documents are allowed | Passages, entities, relations, source IDs | Seed actors, concepts, and synonyms |
| 4 | `graph_mcp.list_mcp_functions({})` | Live capability metadata | Select provider-safe calls |
| 5 | `graph_mcp.activate_project({parser_type:"cplus"})` | Active parser and configured provider | Establish code context |
| 6 | `graph_mcp.list_qdrant_collections({})` | Code collections | Build collection candidates |
| 7 | Bind `ACTIVE_DATA_CONTEXT` | Active FalkorDB context plus one Qdrant candidate | Permit collection validation |

Never call `graph_mcp.list_databases`. The MCP server owns the FalkorDB graph selection. Never pass, infer, hardcode, or display a graph key.

If documents are prohibited, skip steps 2-3 and record only `skipped by user`. If metadata and the callable wrapper differ, obey the wrapper. Retry once only for `invalid_parameters`.

Before any analysis query, confirm FalkorDB activation succeeded, select one C/C++ Qdrant candidate from project/repository/language metadata, and bind both as `ACTIVE_DATA_CONTEXT`. A minimal collection-validation probe is the only query allowed before the context gate passes.

Validate the bound candidate with a small `semantic_search` using `collection:ACTIVE_QDRANT_COLLECTION`, `expand_graph:false`, the module name, and one known file/class/entry concept. Select it only after at least two hits contain module-local file paths or qualified names. If rejected, bind the next candidate and repeat only the validation probe. Never run the query matrix across multiple or unscoped collections.

Record before section 3:

```text
DATA_CONTEXT_GATE: PASS|BLOCKED
parser=cplus
graph_provider=falkordb
graph_context=active|unavailable
qdrant_collection=<validated collection or unavailable>
qdrant_context=active|unavailable
```

Proceed only on `PASS`. Every later `semantic_search`, `explore_graph`, and vertical graph traversal must explicitly pass `ACTIVE_QDRANT_COLLECTION` or use retained graph anchors from that collection.

## 3. Query Matrix

Require `DATA_CONTEXT_GATE: PASS` before starting this section.

Build multilingual queries from the request, module, known symbols, states, messages, side effects, Japanese terms, romaji, English translations, and vocabulary discovered during retrieval.

| Family | Example | Evidence sought |
|---|---|---|
| Identity/boundary | `<module> main dispatcher entry public API` | boundaries, entry candidates, main loop |
| Business intent | `<module> sell payout refund cancel settle` | business handlers |
| Lifecycle | `<module> startup start stop shutdown health` | lifecycle flows |
| State/mode | `<module> state transition mode permission enable` | guards and transitions |
| User trigger | `<module> button menu screen manual receive event` | UI/manual/event triggers |
| Integration | `<module> host IPC message device member cash printer journal` | adapters and external modules |
| Side effect | `<module> send print dispense update write commit notify` | terminal outcomes |
| Negative path | `<module> error timeout invalid cancel retry abort recover` | alternate/error/recovery |
| Domain language | `<Japanese> <romaji> <English> <prefix>` | synonyms and hidden flows |

For every applicable family, run both views:

1. `graph_mcp.semantic_search({query, top_k:20, collection, expand_graph:false})`
   - retain vector seeds, scores, qualified names, file paths, and code snippets;
2. `graph_mcp.explore_graph({query, mode:"graph_expanded", top_k:20, collection, debug:true})`
   - retain FalkorDB matches, relationships, paths, entry candidates, WHY reasons, query analysis, and confidence.

Use `mode:"hybrid"` when it produces richer provider-safe evidence. Do not enable graph expansion on `semantic_search`; FalkorDB traversal belongs to `explore_graph`.

Vary wording and use terms returned by the prior pass. Literal symbol or source search begins only after semantic retrieval supplies vocabulary.

## 4. Normalize the Frontier

Merge results by graph node ID; when absent, use qualified symbol plus file path.

Retain for each anchor:

- node ID, qualified name, kind, file, line, class/module
- exact query and query family
- semantic score and FalkorDB WHY/confidence
- role: trigger, entrypoint, guard, handler, adapter, side effect, recovery
- related nodes, relationships, paths, modules, messages, states, and terms
- source support status and named gaps

Reject cross-project or cross-module mismatches. Do not call provider-ambiguous detail/inventory tools to enrich anchors. `explore_graph` evidence and later Serena source evidence supply those details.

## 5. FalkorDB Expansion

For every retained trigger, entry candidate, business handler, adapter, side effect, and recovery anchor:

1. issue a focused `explore_graph` query naming the anchor, module, role, and desired direction;
2. run vertical graph traversal from the retained node IDs: callers/triggers with `query_subgraph(direction:"in")`, callees/outcomes with `query_subgraph(direction:"out")`, and bidirectional context with `query_subgraph(direction:"both")` when roles are unclear;
3. connect trigger -> handler and handler -> outcome anchors with `find_paths` or `trace_flow`, using `CALLS`, `POSSIBLE_CALLS`, callback/function-pointer, IPC/message, and shared-state relationship types when live metadata exposes them;
4. trace module boundaries with `find_path_between_module` or `trace_flow_between_module` for retained external modules;
5. retain all returned paths and uncertain relationships without upgrading them;
6. use `reconstruct_flow` only when graph traversal returned path candidates in a compatible shape;
7. add newly discovered vocabulary to the next semantic and graph-expanded pass.

Suggested focused query shapes:

- `<symbol> callers external entry trigger <module>`
- `<symbol> callees side effect state mutation <module>`
- `<symbol> callback virtual function pointer registration`
- `<symbol> IPC message sender receiver handler`
- `<symbol> error timeout cancel retry recovery`
- `<moduleA> to <moduleB> runtime call message shared state`

Do not expand trivial getters/setters unless they mutate state, enforce a rule, or bridge a path.

## 6. Safe Capability Boundary

The default provider-safe graph calls are:

- `list_mcp_functions`
- `activate_project` without graph/database arguments
- `list_qdrant_collections`
- `semantic_search` with `expand_graph:false`
- `explore_graph`
- `query_subgraph` for retained node IDs when live metadata lists the tool
- `find_paths` or `trace_flow` for retained start/end node IDs when live metadata lists the tool
- `find_path_between_module` or `trace_flow_between_module` for retained module pairs when live metadata lists the tool
- `reconstruct_flow` for already returned paths

Treat detail, inventory, workflow, endpoint, IPC, and dependency helper calls as quarantined unless live metadata explicitly marks them suitable for the active parser/provider and the current session already contains successful graph evidence. Do not availability-probe quarantined calls. This avoids stale provider-specific implementations while preserving the full FalkorDB-aware Graph-RAG path.

## 7. Saturation

After each pass, measure:

- new unique graph nodes and relationships
- new path variants and entry candidates
- new triggers, handlers, and outcomes
- retained anchors with upstream and downstream graph traversals
- trigger -> handler -> outcome paths connected or explicitly gapped
- new IPC/messages/external modules
- new states/modes/guards
- new use-case candidates
- remaining named gaps

Generate the next query batch from new vocabulary and gaps. Saturation passes only after two consecutive passes add no high-confidence item in any category. Stable candidate count alone is insufficient while paths, errors, messages, states, or outcomes are still growing.

Progress checkpoints report completed query families, call counts, evidence deltas, truncation, and remaining evidence gaps. They do not report raw failures, endpoints, retries, or layer-switch narration.

## 8. Serena Enrichment

Begin only after the Falkor Graph gate is `PASS` or `PARTIAL`.

1. Call `serena.initial_instructions({})` once and activate the target repository root.
2. Use `get_symbols_overview` on Graph-RAG-identified files.
3. Use `find_symbol(include_body:false, depth:1)` for retained classes.
4. Use `find_symbol(include_body:true)` only for key triggers, guards, handlers, outcomes, and unresolved bridges.
5. Use `find_referencing_symbols` for source-level callers of retained anchors.
6. Use `search_for_pattern` for states, switch cases, message IDs, callback registration, validation, timeout/error terms, multilingual synonyms, and configuration keys.

Use returned Serena `name_path` values exactly. Partition capped results by graph-identified file, class, prefix, or use-case slice. Serena line numbers are zero-based in raw evidence.

Every Serena call must map to a Graph-RAG anchor or a named completeness gap. Do not restart broad discovery from source search.

## 9. Native Fallback

Use native tools only when a specific gap remains after Graph-RAG and Serena and the user permits native tools. Record command, scope, evidence, and gap. Skip this layer for MCP-only requests.

## 10. Output Contract

Every artifact includes:

1. `retrieval_trace`: ordered completed calls, inputs, returned information, and evidence decision;
2. `active_data_context`: parser, graph provider status, and bound Qdrant collection;
3. `collection_resolution`: selected/rejected corpora and module-local proof;
4. `query_matrix`: family, exact query, vector hits, FalkorDB expansion, retained/rejected evidence;
5. `evidence_ledger`: claim-level support and uncertainty;
6. `saturation`: pass deltas and final two zero-delta passes;
7. `coverage_grid`: covered, not applicable, or unresolved dimensions;
8. `unresolved_gaps`: missing evidence categories without infrastructure details.

Never claim completeness solely because semantic hits stopped. Complete means evidence, saturation, and coverage gates all pass.

## 11. Skill Routing Contract

SKILL.md is a thin runtime router. The loading policy for this skill's files is:

| File | Loading policy |
|---|---|
| SKILL.md | Always when invoked; keep minimal |
| ARTIFACT-CATALOG.yaml | Script-only; never read directly during execution |
| GRAPH-RAG-PROTOCOL.md | Once, when retrieval starts |
| Selected profile | Once, when the plan is generated |
| Artifact technique | One at a time, returned by `hi-reverse-plan --next` |
| MCP-TOOLS.md | Only for routing/schema diagnosis |
| Templates | Only when generating that artifact |
| Validation scripts | Execute without reading source |
| Package manifest | Query through compact script commands (`--summary`, `--next`) |

This preserves all 29 capabilities while keeping baseline context under 1,200 words. The catalog is consumed by `artifact-plan.mjs`, not placed in model context.
