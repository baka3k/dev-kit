---
name: hi-reverse
description: "Reverse Engineering C and C++ modules into validated use-case, module, and C++-to-Java migration artifact packages. Generates evidence-backed traces, sequence/class/state/activity/architecture diagrams, entry-point/interface/data/business-rule/error/concurrency catalogs, parity mappings, risks, tests, reviews, and coverage; exhaust mind_mcp and graph_mcp before Serena, and use native source tools only as a final fallback."
---

# C++ Reverse Engineering

Reverse-engineer behavior from evidence, not symbol-name guesses. FalkorDB plus Qdrant Graph-RAG is the primary engine, Serena is source-level enrichment, native tools are the final gap filler. Run scripts from the skill directory with Node.js 18+. Gate block formats, quiet-routing rules, and the script table: [OPERATIONS.md](references/OPERATIONS.md).

## Runtime

1. Select `usecase`, `module`, or `migration`.
2. Validate the catalog: `npx --yes --offline --package=. hi-reverse-plan --check-catalog`.
3. For `usecase`, read [PROFILE-USECASE.md](references/PROFILE-USECASE.md); for `module`/`migration`, use the generated manifest as the profile guide.
4. Generate the plan: `hi-reverse-plan --profile <p> --module <m> [--use-case <slug>] [--condition <c>] --output <manifest> --summary`. Require `ARTIFACT_PLAN_GATE: PASS`. Never read `ARTIFACT-CATALOG.yaml` directly — the script is the capability authority.
5. Activate the C++ parser, FalkorDB context, and one Qdrant collection. Require `DATA_CONTEXT_GATE: PASS` (format: [OPERATIONS.md](references/OPERATIONS.md)).
6. Run Graph-RAG to saturation. Semantic search seeds anchors only; graph traversal must expand anchors into caller/callee and trigger/handler/outcome paths before Serena. Require `FALKOR_GRAPH_GATE: PASS` (or `PARTIAL` per rules).
7. Use Serena only for retained anchors and named gaps.
8. Rerun the plan only when discovery adds a new use-case slug or evidenced condition.
9. Generate artifacts one at a time via the loop below. Require `REVERSE_PACKAGE_GATE: PASS` before delivery.

## Retrieval Order

`mind_mcp → graph_mcp/Qdrant → graph_mcp/FalkorDB → Serena → native`

- Read [GRAPH-RAG-PROTOCOL.md](references/GRAPH-RAG-PROTOCOL.md) once when retrieval starts. Cross-check newly added read-side functions against [dev-shared/graph-function-selection.md](../dev-shared/graph-function-selection.md); GRAPH-RAG-PROTOCOL.md §6 stays authoritative for provider-safe routing.
- Read only the technique file returned by `--next` for the current artifact.
- Read [MCP-TOOLS.md](references/MCP-TOOLS.md) only when live metadata is ambiguous, a wrapper rejects parameters, or provider routing must be diagnosed.
- Never call `graph_mcp.list_databases`. Never hardcode or display a graph key, endpoint, port, protocol, or driver.
- If a higher-priority repository instruction defines a stricter order, obey it.

## Artifact Generation Loop

1. `hi-reverse-plan --next <manifest>` → compact `ARTIFACT_ID`, `TECHNIQUE`, `OUTPUT`, `EVIDENCE_GAPS`. Exit 1 = all validated; proceed to the package gate.
2. Read only that artifact's technique file.
3. Retrieve only the missing evidence listed in `EVIDENCE_GAPS`.
4. Generate the artifact from its template (read the template only now).
5. Validate: `hi-reverse-validate-artifact <id> <path> --summary`. Require `ARTIFACT_GATE: PASS`.
6. Release the technique details; continue to the next `--next`.

## Evidence Contract

One evidence ledger shared by all phases; each claim records `status`, `graph_provider`, `node_ids`, `symbols`, `edges`, `locations`, `retrieved_by`, `serena_support`, `uncertainties`.

- `PROVEN`: trigger, handler, and terminal side effect connected by FalkorDB path evidence and source support.
- `LIKELY`: at least two of the three connected; the missing bridge is named.
- `TENTATIVE`: semantic or source evidence exists, but the executable path is not established.
- `REJECTED`: evidence shows utility, dead path, duplicate, or unrelated module.

## Gates

`ARTIFACT_PLAN_GATE` (catalog valid, manifest generated) · `DATA_CONTEXT_GATE` (FalkorDB + one Qdrant collection active) · `FALKOR_GRAPH_GATE` (query matrix and saturation complete) · `ARTIFACT_GATE` (single artifact valid) · `REVERSE_PACKAGE_GATE` (all required profile instances validated). Never claim completion while a required gate fails; structural validation does not prove semantic correctness — the evidence ledger and review remain mandatory.

## User Constraints & Context Discipline

- No existing documents → record `mind_mcp documents: skipped by user`; still run code Graph-RAG.
- MCP tools only → stop after Serena; report evidence gaps without native tools.
- Label possible use cases as possible; never present a name-only hit as proven behavior. Never claim exhaustive coverage where evidence is missing.
- Never read the full catalog during normal execution; keep one profile and one technique active; do not reopen unchanged files; retain Graph results as IDs/symbols/paths/scores; move evidence into `evidence-ledger.json`; report deltas, use `--summary`.

## Orchestration

`CATALOG → PROFILE → PLAN → DISCOVERY → TRACING → UC/SEQ/CLASS/ACTIVITY → MODULE MAP → OVERVIEW/ENTRYPOINTS/INTERFACES → STATE/DATA/RULES/ERRORS/CONCURRENCY → MIGRATION PARITY/MAPPINGS/WAVES/RISKS/TESTS → REVIEW → VALIDATION → PACKAGE GATE → METRICS`.

The main agent performs blocking preflight and collection validation. Sub-agents receive repository root, module, constraints, selected collection, Graph-RAG anchors, prior artifacts, and output path; they follow the same routing, return retrieval traces and evidence deltas, and never activate the skill directory as the Serena project.
