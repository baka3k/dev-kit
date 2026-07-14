# Sequence Diagram

Build Mermaid sequence diagrams only from a verified trace manifest. Read `GRAPH-RAG-PROTOCOL.md` when a diagram gap requires new retrieval.

## Rules

1. Preserve trace order, relation type, state changes, and uncertainty.
2. If a participant, branch, or terminal outcome is missing, return to Graph-RAG expansion first, then Serena enrichment; do not invent the missing step.
3. Map direct calls to solid messages, asynchronous IPC/events to async messages, and uncertain/possible calls to a note or clearly labeled dotted message.
4. Put guards in `alt`/`opt` labels and tag branches `MAIN`, `ALT`, `ERROR`, `TIMEOUT`, or `RECOVERY`.
5. Show business actions in labels; retain symbols and file/line evidence in notes or the adjacent evidence table.
6. Split diagrams above 15 participants or when main and recovery paths become unreadable.

## Taxonomy

- roles: `ENTRYPOINT`, `CONTROLLER`, `SERVICE`, `ADAPTER`, `UTILITY`
- layers: `UI`, `DOMAIN`, `INFRA`, `INTEGRATION`
- sync: `SYNC`, `ASYNC`, `CALLBACK`, `INTERRUPT`
- risk: `HIGH` for money, authorization, host, persistent state, or irreversible device effects; otherwise `MED`/`LOW`

## Output

Write `usecase/<MODULE>/seq_<use-case>_<YYYYMMDD>_v1.mmd` for every documented use case. The file must begin with the Mermaid root `sequenceDiagram`, and the corresponding `ucXXX_<use-case>.md` must link its exact basename under `## Sequence Diagram`. Return the retrieval trace inherited from the trace manifest, any additional Graph/Serena calls, participant-to-node mapping, branch coverage, and unresolved gaps.
