# Class Diagram

Build an evidence-backed Mermaid class/struct diagram for `<MODULE>` or a named use case. Read `GRAPH-RAG-PROTOCOL.md` first.

## Retrieval

1. Seed relevant types with Qdrant semantic queries for the module, use case, and architecture roles.
2. Pair each query with `explore_graph` to retrieve FalkorDB type nodes and business-relevant relationships.
3. Query retained classes separately for inheritance, owned fields, pointer/reference fields, parameters, return types, methods, and collaborators.
4. Expand types referenced by IPC payloads, state objects, adapters, and terminal side effects.
5. After Graph-RAG saturation, use Serena `get_symbols_overview` and `find_symbol(depth:1, include_body:false)` for retained files/classes.
6. Inspect declarations or bodies only when inheritance, composition, or method relationships remain unresolved.
7. Continue until two passes add no relevant type or relationship.

## Mapping

| Evidence | Mermaid |
|---|---|
| public inheritance | `Base <|-- Derived` |
| value/owned member | `Owner *-- Part` |
| pointer/reference member | `Owner o-- Part` unless lifetime proves composition |
| method parameter/return/call | `Client --> Service : uses` |
| pure virtual contract | `<<interface>>` or `<<abstract>>` |
| enum/struct/union | matching stereotype |

Do not infer ownership from a call or name. Include only business-relevant fields and methods. Preserve file/line and graph evidence in an adjacent table. Split diagrams above 20 classes by layer or subdomain. Mark unresolved relationships as dashed `uses?` links.

## Output

Write `usecase/<MODULE>/class_<use-case>_<YYYYMMDD>_v1.mmd` for every documented use case. The file must begin with the Mermaid root `classDiagram`, and the corresponding `ucXXX_<use-case>.md` must link its exact basename under `## Class Diagram`.

A module-wide class diagram is optional supplemental material and does not replace the use-case-specific diagram. Include only types that participate in the use-case trace, guards, state, payloads, adapters, or terminal effects. Return an evidence table with the Falkor Graph gate, retrieval trace, node IDs, relationship support, saturation result, and unresolved gaps.
