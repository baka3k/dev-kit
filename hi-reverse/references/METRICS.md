# Reverse-Engineering Metrics

Measure evidence quality and blind spots from discovery, trace, review, and saturation manifests. Do not treat file count as coverage.

## Required Metrics

- `QUERY_FAMILY_COVERAGE`: completed applicable Qdrant + FalkorDB query families / applicable families
- `ENTRY_CANDIDATE_COVERAGE`: entry candidates assigned or rejected with reason / discovered candidates
- `ANCHOR_EXPANSION_COVERAGE`: retained anchors with caller/trigger and callee/outcome FalkorDB queries / retained anchors
- `TRIGGER_HANDLER_OUTCOME_COVERAGE`: candidates with all three connected / retained candidates
- `ALT_ERROR_COVERAGE`: traced alternate/error/recovery branches / discovered branches
- `IPC_CALLBACK_COVERAGE`: resolved IPC/callback breaks / discovered breaks
- `SOURCE_SUPPORT_COVERAGE`: executable claims with Serena source support / executable claims
- `PROVEN_UC_RATIO`: proven candidates / retained candidates
- `UNRESOLVED_GAPS`: count by missing evidence category and uninspected scope
- `SATURATION_STATUS`: final two pass deltas and pass/fail
- `GRAPH_RAG_ROUTE`: `FalkorDB + Qdrant`, `Qdrant only`, or `Graph-RAG unavailable`
- `PROFILE_ARTIFACT_COVERAGE`: validated required artifact instances / planned required instances
- `REVERSE_PACKAGE_STATUS`: package-manifest gate and failure count

Compute from manifests and ledgers first. Use Serena for missing artifact sections. Use scripts or shell counting only as a final fallback and never for MCP-only requests.

## Output

Append a dated snapshot to `usecase/<MODULE>/trace_metrics.md` with raw counts, formulas, percentages, graph route, unresolved evidence, and the highest-priority gaps. Never report 100% when required evidence or scope is unresolved.
