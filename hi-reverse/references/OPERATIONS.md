# Reverse Operations Reference

Operational formats for `hi-reverse`: gate block formats, quiet-routing rules, script reference, use-case bundle checks. Routing authority stays with [GRAPH-RAG-PROTOCOL.md](GRAPH-RAG-PROTOCOL.md).

## Data Context Gate (block format)

Lock the data context before any analysis query. Confirm FalkorDB is active, select one C/C++ Qdrant collection from project/repository/language metadata, and validate it with a scoped `semantic_search`, `explore_graph` probe (module-local hits required). If rejected, bind the next candidate and repeat only the probe.

```text
DATA_CONTEXT_GATE: PASS|BLOCKED
parser=cplus
graph_provider=falkordb
graph_context=active|unavailable
qdrant_collection=<validated collection or unavailable>
qdrant_context=active|unavailable
```

`PASS` is required before any discovery, tracing, mapping, glossary, or review query. Reuse it for the same repository, module, parser, and collection; re-list collections or re-run validation probes only when scope changes, context is stale, or module-local evidence fails. Every later `semantic_search`, `explore_graph`, and vertical graph traversal must use the bound collection or retained graph anchors. `BLOCKED` stops analysis instead of issuing unscoped queries.

## Falkor Graph Gate (block format)

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

## Quiet Routing

- Fast-fail once per capability. Retry once only for `invalid_parameters`, using the callable wrapper schema.
- Never echo raw backend exceptions, host, port, graph key, protocol, driver, or other infrastructure details.
- Never narrate routing ("I will retry", "marking traversal unavailable", "then use Serena", or equivalent).
- Execute the next allowed layer silently; show completed calls and evidence in the retrieval trace, not operational detours.
- Summarize graph coverage to users only as `FalkorDB + Qdrant`, `Qdrant only`, or `Graph-RAG unavailable`.
- Keep provider failures in internal retrieval data as normalized capability statuses.

## Script Reference

All commands run via `npx --yes --offline --package=. <command>` from the skill directory (zero dependencies, offline). Use `--summary` for compact output unless diagnosing.

| Command | Function |
| --- | --- |
| `hi-reverse-init <output-dir>` | Create output workspace and copy templates |
| `hi-reverse-plan --check-catalog` | Validate catalog integrity |
| `hi-reverse-plan --profile <p> --module <m> --output <f> --summary` | Generate compact manifest |
| `hi-reverse-plan --next <manifest>` | Return next pending artifact + technique + evidence gaps |
| `hi-reverse-plan --list-capabilities` | List artifact ID, status, scope, output, technique |
| `hi-reverse-validate-artifact <id> <path> --summary` | Validate one artifact |
| `hi-reverse-validate-package <manifest> --update` | Set `REVERSE_PACKAGE_GATE`; enforces UC bundle link checks (`--verbose` for full rows) |
| `hi-reverse-metrics [usecase-dir] [metrics-file] [package-manifest]` | Append UC and profile/package coverage |

## Use-Case Bundle

Every documented use case must produce: `ucXXX_<slug>.md`, `trace_<slug>.json`, `seq_<slug>_<YYYYMMDD>_v1.mmd`, `class_<slug>_<YYYYMMDD>_v1.mmd`. The Markdown must contain `## Sequence Diagram` and `## Class Diagram` sections linking the exact two Mermaid files. Link checks are enforced by `hi-reverse-validate-package`. If native execution is forbidden, apply the checklist manually, record `ARTIFACT_GATE_MODE: manual`, and never claim the hook ran.
