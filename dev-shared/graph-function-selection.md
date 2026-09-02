# Graph Function Selection (`graph_mcp`)

Shared selection layer for `graph_mcp` usage across skills: which function answers which need, and which profile each skill runs. The fast-fail order, evidence rules, and depth levels stay in [retrieval-protocol.md](retrieval-protocol.md).

## Authority

- Call `list_mcp_functions` once per session before the first graph call. The live catalog and its typed parameters are authoritative; every function name below is a candidate, not a guarantee. Historical parameter shapes (string vs numeric vs array) have changed before.
- A function missing from the live catalog becomes a recorded coverage gap, never an invented result. Fall through to Serena, then `rg`, per the retrieval protocol.

## Selection Table

| You have | Use |
| --- | --- |
| Exact or partial function/class/type name | `search_functions` |
| A stable node ID | `get_symbol` (with code body; anchors only) or `get_node_details` (batch, compact) |
| A concept, behavior, or domain description | `semantic_search`, or `explore_graph` for vague fused context |
| A literal: SQL, route, log line, error string, message/topic, opcode, API call | `search_by_code` |
| A module path token | `listup_symbols_matching_file_path` |
| A class/type name, need its methods | `listup_class_matching_path` |
| Which functions a module exposes to callers outside it | `list_up_entrypoint` |
| One function's neighborhood | `query_subgraph` (`all` default, `upstream` callers, `downstream` callees; depth 2) |
| Two known anchor IDs, need the connecting path | `find_paths` |
| Crossings between two known modules | `find_path_between_module`, `trace_flow_between_module` |
| Indirect dispatch: callbacks, virtual calls, function pointers | `trace_flow` with `rel_types:["CALLS","POSSIBLE_CALLS"]` (depth ≤ 6); per unresolved site `list_possible_calls` |
| Sender/receiver message, event, service, or intent bridge | `get_ipc_message` |
| Module/file/function build order and cycles | `plan_dependency_order`, `plan_file_dependency_order`, `plan_function_dependency_order`; `compute_scc` for cycles, `topological_sort` for waves |
| Which workflows contain a function / blast radius | `find_workflows_containing`, `analyze_workflow_impact` (corroboration, never sole proof) |
| Screen navigation paths (UI) | `find_screen_workflows` |
| Frontend callers of a verified backend endpoint | `find_callers_of_endpoint` |
| UI → controller → service → repository → database chain | `get_api_call_chain` |
| Already-verified path JSON → readable narrative | `reconstruct_flow` (formats evidence; creates nothing) |

## Session Preflight (only when graph work is expected)

1. `list_mcp_functions`; record catalog/version in the run ledger.
2. `list_parsers`, `list_databases`, and `list_qdrant_collections` when semantic search exists.
3. Match repository path, project identity, language, parser, database, and collection; only then `activate_project`.
4. Run one known-symbol smoke query. Empty or cross-project results end the graph layer; fall through to Serena.

## Tiers

| Tier | Scope | Baseline functions |
| --- | --- | --- |
| T0 | none | skill never queries the graph |
| T1 | grounding | `semantic_search` / `explore_graph`, `search_functions` |
| T2 | impact-aware | T1 + `query_subgraph`, `get_symbol` / `get_node_details`, `search_by_code` |
| T3 | full domain protocol | T2 + the inventory, flow, and domain-bridge functions listed per skill below |

## Skill Profiles

The "Additions" column lists functions beyond the tier baseline that the skill treats as core or conditional-when-shape-exists.

| Skill | Tier | Additions beyond baseline |
| --- | --- | --- |
| hi-repo-recon | T3 | inventory group; `list_up_entrypoint`; `plan_*_dependency_order`, `compute_scc` (deep depth) |
| hi-usecase-discovery | T3 | full catalog; deep operational protocol in its `references/graph-retrieval.md` |
| hi-api-contract-discovery | T3 | `search_by_code` (routes/topics); `find_callers_of_endpoint`; `get_api_call_chain`; `get_ipc_message` |
| hi-data-model-discovery | T3 | `search_by_code` (SQL/DDL/ORM); `listup_symbols_matching_file_path`; `get_symbol` (declared constraints) |
| hi-behavior-modeling | T3 | `trace_flow`; `find_paths`; `reconstruct_flow`; `list_possible_calls`; `get_ipc_message` |
| hi-command-spec-discovery | T3 | `search_by_code` (opcodes/literals/status words); `list_possible_calls`; `get_ipc_message`; `find_paths` |
| hi-reverse | T3 | own protocol: its `references/GRAPH-RAG-PROTOCOL.md` |
| hi-security | T3 | `list_up_entrypoint` (attack surface); `trace_flow` (data paths); `get_api_call_chain`; `search_by_code` (sinks/secrets) |
| hi-scenario | T3 | `trace_flow`; `find_paths`; `find_workflows_containing`; `analyze_workflow_impact` |
| hi-debug | T3 | `trace_flow` (`in`/`out`); `find_paths` (symptom → cause); `list_possible_calls`; `get_ipc_message` |
| hi-predict | T3 | `query_subgraph`; `trace_flow`; `find_paths`; `analyze_workflow_impact`; `plan_dependency_order` |
| hi-knows | T3 | `query_subgraph`; `trace_flow`; `find_paths`; `analyze_workflow_impact`; `search_by_code` |
| hi-repowiki | T3 | inventory group; `query_subgraph`; `reconstruct_flow` (mostly delegated to recon/leaf skills) |
| hi-maintenance-docs | T3 | inventory group; `get_symbol` anchors for documented behavior |
| hi-module-summary-report | T3 | `plan_*_dependency_order`; `compute_scc`; `list_up_entrypoint` (validates recon inputs) |
| hi-plan | T2 | `plan_dependency_order` (phasing); `analyze_workflow_impact` (blast radius) |
| hi-craft | T2 | pre-edit impact: `query_subgraph(downstream)` on touched symbols |
| hi-fix | T2 | `query_subgraph(upstream)` (callers of the defect); `search_by_code` (error strings) |
| hi-codebase-research-explorer | T2 | `query_subgraph`; `get_node_details` |
| hi-repository-search | T2 | `search_by_code`; `search_functions`; `query_subgraph` |
| hi-cross-artifact-validation | T2 | `search_functions` + `get_node_details` to re-resolve claimed IDs; `find_callers_of_endpoint` / `get_ipc_message` for claimed bridges |
| hi-tech-build-audit | T2 | `plan_file_dependency_order`; `search_by_code` (build/CI literals) |
| hi-project-organization | T1 | conditional `plan_file_dependency_order` for layout moves |
| hi-brainstorm, hi-problem-solving | T1 | grounding only |
| hi-document-refinement, hi-document-review-resolution, hi-document-lifecycle | T1 | `search_functions` / `get_symbol` to verify named symbols in drafts and comments |
| hi-pptx, hi-sequential-thinking, hi-docs-seeker, hi-chrome-devtools, hi-log, hi-cortex | T0 | not applicable |

## Guardrails

- Semantic hits are seeds. Confirm them through stable node IDs and source locations before they count as evidence.
- Never infer a direct call from `POSSIBLE_CALLS`, shared state, naming similarity, or `reconstruct_flow` output.
- Keep breadth passes compact; retrieve code bodies only for retained anchors.
- `annotate_node` is write-side and excluded from every read flow.
- Respect `truncated` flags and capability diagnostics; unresolved truncation means partial coverage and must be recorded.
