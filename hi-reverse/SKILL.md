---
name: hi-reverse
description: "FalkorDB and Qdrant Graph-RAG-first reverse engineering of C and C++ modules into validated use-case, module, and C++-to-Java migration artifact packages. Generates evidence-backed traces, sequence/class/state/activity/architecture diagrams, entry-point/interface/data/business-rule/error/concurrency catalogs, parity mappings, risks, tests, reviews, and coverage; exhaust mind_mcp and graph_mcp before Serena, and use native source tools only as a final fallback."
---

# C++ Reverse Engineering

Reverse-engineer behavior from evidence, not symbol-name guesses. FalkorDB plus Qdrant Graph-RAG is the primary engine, Serena is source-level enrichment, native tools are the final gap filler. Run scripts from the skill directory with Node.js 18+.

## Runtime

1. Select `usecase`, `module`, or `migration`.
2. Validate the catalog: `npx --yes --offline --package=. hi-reverse-plan --check-catalog`.
3. Generate the plan: `npx --yes --offline --package=. hi-reverse-plan --profile <p> --module <m> [--use-case <slug>] [--condition <c>] --output <manifest> --summary`. Require `ARTIFACT_PLAN_GATE: PASS`. Do not read `ARTIFACT-CATALOG.yaml` directly — the script is the capability authority.
4. Activate the C++ parser, FalkorDB context, and one Qdrant collection.
5. Require `DATA_CONTEXT_GATE: PASS`.
6. Run Graph-RAG to saturation. Semantic search seeds anchors only; graph traversal must expand those anchors into caller/callee and trigger/handler/outcome paths before Serena.
7. Use Serena only for retained anchors and named gaps.
8. Rerun the plan only when discovery adds a new use-case slug or evidenced condition.
9. Generate artifacts one at a time via the loop below.
10. Require `REVERSE_PACKAGE_GATE: PASS` before delivery.

## Retrieval Order

`mind_mcp → graph_mcp/Qdrant → graph_mcp/FalkorDB → Serena → native`

- Read [GRAPH-RAG-PROTOCOL.md](references/GRAPH-RAG-PROTOCOL.md) once when retrieval starts.
- Read only the technique file returned by `--next` for the current artifact.
- Read [MCP-TOOLS.md](references/MCP-TOOLS.md) only when live metadata is ambiguous, a wrapper rejects parameters, or provider routing must be diagnosed.
- Do not read `ARTIFACT-CATALOG.yaml` unless the planner reports a catalog error.
- If a higher-priority repository instruction defines a stricter order, obey it.

## Data Context Gate

Lock the data context before any analysis query. Confirm FalkorDB is active, select one C/C++ Qdrant collection from project/repository/language metadata, and validate it with a scoped `semantic_search` probe (module-local hits required). If rejected, bind the next candidate and repeat only the probe.

```text
DATA_CONTEXT_GATE: PASS|BLOCKED
parser=cplus
graph_provider=falkordb
graph_context=active|unavailable
qdrant_collection=<validated collection or unavailable>
qdrant_context=active|unavailable
```

`PASS` is required before any discovery, tracing, mapping, glossary, or review query. Reuse it for the same repository, module, parser, and collection; re-list collections or re-run validation probes only when scope changes, context is stale, or module-local evidence fails. Every later `semantic_search`, `explore_graph`, and vertical graph traversal must use the bound collection or retained graph anchors. `BLOCKED` stops analysis instead of issuing unscoped queries.

## Falkor Graph Gate

Record before entering Serena:

```text
FALKOR_GRAPH_GATE: PASS|PARTIAL|BLOCKED
provider=falkordb
collection=<validated collection or unavailable>
semantic_search_calls=<count>
explore_graph_calls=<count>
vertical_graph_trace_calls=<count>
query_families=<completed/applicable>
graph_expansion=<available|no-evidence|unavailable>
```

`PASS` requires a validated collection, all applicable query families, vertical graph traversal for retained anchors, two saturation passes, and FalkorDB graph evidence. `PARTIAL` permits Serena only after every working Graph-RAG capability is exhausted and names the missing evidence category. `BLOCKED` means code evidence cannot be established; stop instead of guessing.

Never call `graph_mcp.list_databases`. Never hardcode or display a graph key, endpoint, port, protocol, or driver. Provider-safe calls are listed in [GRAPH-RAG-PROTOCOL.md](references/GRAPH-RAG-PROTOCOL.md) §6.

## Quiet Routing

- Fast-fail once per capability. Retry once only for `invalid_parameters`, using the callable wrapper schema.
- Never echo raw backend exceptions, host, port, graph key, protocol, driver, or other infrastructure details.
- Never narrate routing with phrases such as "I will retry", "marking traversal unavailable", "then use Serena", or equivalent fallback commentary.
- Execute the next allowed layer silently. Show completed calls and evidence in the retrieval trace, not operational detours.
- In user-facing output, summarize graph coverage only as `FalkorDB + Qdrant`, `Qdrant only`, or `Graph-RAG unavailable`.
- Keep provider failures in internal retrieval data as normalized capability statuses.

## Context Discipline

- Never read the full artifact catalog during normal execution.
- Keep at most one profile and one artifact technique active at a time.
- Keep the loaded protocol/profile/technique in working context; do not reopen unchanged files.
- Do not read templates until generating their selected artifact.
- Retain Graph results as node IDs, symbols, paths, scores, and WHY summaries.
- Move normalized evidence into `evidence-ledger.json`.
- Do not repeat full code snippets after recording source locations.
- Report deltas, not the complete accumulated frontier.
- Use compact script output (`--summary`) unless diagnosing a failure.

## Artifact Generation Loop

Generate one artifact at a time. Do not read all techniques selected by a profile at once.

1. Ask the planner for the next pending artifact:
   `npx --yes --offline --package=. hi-reverse-plan --next <manifest>`
   Compact output: `ARTIFACT_ID`, `TECHNIQUE`, `OUTPUT`, `EVIDENCE_GAPS`.
2. Read only that artifact's technique file.
3. Retrieve only the missing evidence listed in `EVIDENCE_GAPS`.
4. Generate the artifact from its template (read the template only now).
5. Validate: `npx --yes --offline --package=. hi-reverse-validate-artifact <id> <path> --summary`. Require `ARTIFACT_GATE: PASS`.
6. Release the technique details and continue to the next `--next`.

Exit 1 from `--next` means all artifacts are validated; proceed to the package gate.

### Use-Case Bundle

Every documented use case must produce: `ucXXX_<slug>.md`, `trace_<slug>.json`, `seq_<slug>_<YYYYMMDD>_v1.mmd`, `class_<slug>_<YYYYMMDD>_v1.mmd`. The Markdown must contain `## Sequence Diagram` and `## Class Diagram` sections linking the exact two Mermaid files. UC bundle link checks are enforced by `hi-reverse-validate-package` (it verifies each use-case document links its sequence and class artifacts). If native execution is forbidden, apply the checklist manually, record `ARTIFACT_GATE_MODE: manual`, and never claim the hook ran.

## Evidence Contract

Maintain one evidence ledger shared by all phases. Each claim records: `status`, `graph_provider`, `node_ids`, `symbols`, `edges`, `locations`, `retrieved_by`, `serena_support`, `uncertainties`.

- `PROVEN`: trigger, handler, and terminal side effect connected by FalkorDB path evidence and source support.
- `LIKELY`: at least two of the three connected; the missing bridge is named.
- `TENTATIVE`: semantic or source evidence exists, but the executable path is not established.
- `REJECTED`: evidence shows utility, dead path, duplicate, or unrelated module.

## Gates

- `ARTIFACT_PLAN_GATE` — catalog valid and manifest generated.
- `DATA_CONTEXT_GATE` — FalkorDB and one Qdrant collection active.
- `FALKOR_GRAPH_GATE` — query matrix and saturation complete.
- `ARTIFACT_GATE` — single artifact structurally valid.
- `REVERSE_PACKAGE_GATE` — all required profile instances validated.

Never claim completion while a required gate fails. Structural validation does not prove semantic correctness; the evidence ledger and review remain mandatory.

## User Constraints

- **No existing documents:** record `mind_mcp documents: skipped by user`; still run code Graph-RAG.
- **MCP tools only:** stop after Serena and report evidence gaps without native tools.
- **Possible use cases:** label every result; never present a name-only hit as proven behavior.
- Never claim exhaustive coverage when a collection, edge family, or source area lacks evidence.

## Script Reference

All commands run via `npx --yes --offline --package=. <command>` from the skill directory (zero dependencies, offline). Use `--summary` for compact output unless diagnosing.

| Command | Function |
|---|---|
| `hi-reverse-init <output-dir>` | Create output workspace and copy templates |
| `hi-reverse-plan --check-catalog` | Validate catalog integrity |
| `hi-reverse-plan --profile <p> --module <m> --output <f> --summary` | Generate compact manifest |
| `hi-reverse-plan --next <manifest>` | Return next pending artifact + technique + evidence gaps |
| `hi-reverse-plan --list-capabilities` | List artifact ID, status, scope, output, technique |
| `hi-reverse-validate-artifact <id> <path> --summary` | Validate one artifact |
| `hi-reverse-validate-package <manifest> --update` | Set `REVERSE_PACKAGE_GATE`; also enforces UC bundle link checks (`--verbose` for full rows) |
| `hi-reverse-metrics [usecase-dir] [metrics-file] [package-manifest]` | Append UC and profile/package coverage |

## Orchestration

`CATALOG → PROFILE → PLAN → DISCOVERY → TRACING → UC/SEQ/CLASS/ACTIVITY → MODULE MAP → OVERVIEW/ENTRYPOINTS/INTERFACES → STATE/DATA/RULES/ERRORS/CONCURRENCY → MIGRATION PARITY/MAPPINGS/WAVES/RISKS/TESTS → REVIEW → VALIDATION → PACKAGE GATE → METRICS`.

The main agent performs blocking preflight and collection validation. Sub-agents receive the repository root, module, constraints, selected collection, Graph-RAG anchors, prior artifacts, and output path. They follow the same routing, return retrieval traces and evidence deltas, and never activate the skill directory as the Serena project.
