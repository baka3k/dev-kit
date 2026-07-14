# Module Discovery

Discover all evidence-supported use-case candidates in `<MODULE>`. Read `GRAPH-RAG-PROTOCOL.md` first and expose the ordered evidence flow in the result.

## Inputs

- module/path: `<MODULE>`
- repository root, C++ parser, and validated code collection
- user constraints: documents allowed, MCP-only, requested language
- optional seed terms, files, classes, or known behavior

## Mandatory Graph-RAG Work

1. Complete the ordered preflight, activate the configured FalkorDB provider, validate the Qdrant code collection, and reject project mismatches.
2. Run the complete semantic query matrix for identity, business behavior, lifecycle, state/mode, user triggers, integrations, side effects, negative/recovery paths, and multilingual terms.
3. Pair every applicable `semantic_search(expand_graph:false)` query with `explore_graph`; retain vector seeds and FalkorDB evidence separately.
4. Build a frontier of module-local functions, classes, types, files, states, messages, and external modules returned by either view.
5. For every retained trigger, entry candidate, handler, adapter, side effect, and recovery anchor, issue focused `explore_graph` queries for callers/triggers and callees/outcomes.
6. Run vertical graph traversal for every retained anchor: upstream callers/triggers, downstream callees/outcomes, bidirectional context for unclear roles, and module-to-module paths for external boundaries.
7. Query every graph break for callback/virtual dispatch, function pointers, IPC sender/receiver/handler, shared state, and cross-module relationships.
8. Connect each candidate's trigger -> handler -> terminal outcome using `find_paths`/`trace_flow` or module path traversal when node/module anchors exist; run `reconstruct_flow` when those path results are compatible.
9. Re-query with newly discovered symbols, messages, modules, states, business terms, and error vocabulary.
10. Continue until two consecutive Graph-RAG passes add no material node, relationship, path, use case, state, message, or external module.
11. Enter Serena only after the Falkor Graph gate. Inventory Graph-RAG-identified files/classes, confirm references and branch conditions, and fill named source-detail gaps.
12. Classify the artifact conditions with evidence: `stateful`, `ipc`, `persistence`, `concurrency`, `branching`, and `distributed`.
13. Rerun `npx --yes --offline --package=. hi-reverse-plan` from the skill directory with every retained use-case slug and evidenced condition before artifact generation.

Do not availability-probe quarantined graph calls. Do not use Serena to replace the Qdrant and FalkorDB baseline.

If a response is capped or truncated, split by graph-identified file, class, symbol prefix, query family, or use-case category. Record every partition and do not pass saturation while a remainder is unprocessed.

## Candidate Clustering

Cluster by observable goal and terminal outcome, not class name. Merge handlers reached by the same trigger and producing the same outcome. Split when trigger, actor, permission, monetary effect, state transition, or side effect differs materially.

Capture for every candidate:

- use-case name and actor/trigger
- preconditions, modes, guards, and state transitions
- FalkorDB entry/handler/outcome nodes and path evidence
- terminal side effect and external systems
- alternate/error path anchors and IPC/callback bridges
- source locations and exact retrieval queries
- `PROVEN`, `LIKELY`, `TENTATIVE`, or `REJECTED` with reason

## Output

Write `usecase/<MODULE>/discovery_manifest.json`:

```json
{
  "module": "<MODULE>",
  "constraints": {},
  "falkor_graph_gate": {},
  "collection_resolution": {},
  "retrieval_trace": [],
  "query_matrix": [],
  "frontier_nodes": [],
  "entry_candidates": [],
  "classes": [],
  "use_case_candidates": [],
  "artifact_conditions": {
    "stateful": {"active": false, "evidence": []},
    "ipc": {"active": false, "evidence": []},
    "persistence": {"active": false, "evidence": []},
    "concurrency": {"active": false, "evidence": []},
    "branching": {"active": false, "evidence": []},
    "distributed": {"active": false, "evidence": []}
  },
  "package_manifest": "package-manifest.json",
  "evidence_ledger": [],
  "coverage_grid": {},
  "saturation": {"passed": false, "passes": []},
  "unresolved_gaps": []
}
```

List proven candidates first and clearly separate likely/tentative candidates and evidence gaps. Never include raw backend errors or infrastructure details.
