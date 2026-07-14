# Use-Case Tracing

Trace `<USE_CASE>` in `<MODULE>` from observable trigger to terminal outcome, including guards, state changes, external boundaries, and alternate/error/recovery paths. Read `GRAPH-RAG-PROTOCOL.md` first.

## Inputs

- discovery candidate or user-supplied entry/target
- module/path and validated Qdrant collection
- FalkorDB anchors, paths, and evidence ledger when available

## Mandatory Flow

1. Re-query the use case with business, state, integration, side-effect, and failure wording; do not rely only on discovery labels.
2. Use `semantic_search(expand_graph:false)` to resolve trigger, entry, handler, and outcome candidates from Qdrant.
3. Run `explore_graph` for each anchor with separate caller/trigger and callee/outcome relationship intents.
4. Run vertical graph traversal for each retained anchor: upstream callers/triggers, downstream callees/outcomes, and bidirectional context for uncertain roles.
5. Run focused graph path queries for trigger -> handler and handler -> outcome with `find_paths`/`trace_flow`, retaining direct, possible, IPC, callback, shared-state, and unknown relationships as returned.
6. At every break, query callback/virtual/function-pointer registration, IPC sender/receiver/handler, cross-module boundaries, shared state, and message IDs.
7. Run `reconstruct_flow` only on compatible path candidates already returned by graph traversal; preserve uncertainty fields.
8. Query workflow ownership and impact semantically when workflow concepts appear in Graph-RAG evidence.
9. Search cancel, invalid, timeout, retry, abort, trouble, and recovery variants; trace every retained alternate path to its outcome.
10. Repeat until two passes add no step, branch, state, message, external module, or outcome.
11. After the Falkor Graph gate, use Serena for exact symbol identity, source callers, guards, state constants, callback registration, branches, error handling, and line locations.

Do not infer a call from proximity or matching names. Mark the relationship `unknown` when FalkorDB and source references do not establish the bridge.

## Trace Step Contract

```json
{
  "order": 1,
  "node_id": "...",
  "symbol": "...",
  "location": "file:line",
  "role": "TRIGGER|GUARD|HANDLER|ADAPTER|SIDE_EFFECT|RECOVERY",
  "relation_from_previous": "direct|possible|ipc|callback|shared-state|unknown",
  "state_before": null,
  "state_after": null,
  "evidence": ["tool + query/call"],
  "uncertainty": "low|medium|high"
}
```

## Output

Write `usecase/<MODULE>/trace_<use-case>.json` with the Falkor Graph gate, retrieval trace, anchors, main path, alternate/error paths, IPC/callback bridges, evidence delta, saturation data, and unresolved gaps. A trace is complete only when its terminal outcome is established or the missing evidence is explicit.
