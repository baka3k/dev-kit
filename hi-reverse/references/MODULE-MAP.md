# Module Map

Map runtime calls, possible calls, IPC, shared data, and dependency relationships around `<MODULE>`. Read `GRAPH-RAG-PROTOCOL.md` first.

## Mandatory Graph-RAG Work

1. Run Qdrant semantic queries for host, IPC, events, devices, database/files, member services, cash, printer, journal, configuration, and known neighboring modules.
2. Pair every query with `explore_graph` and retain FalkorDB module nodes, relationships, paths, messages, and WHY evidence.
3. Extract external module names from returned paths, symbols, files, messages, and adapters.
4. For every retained module pair, issue focused queries in both directions for direct calls, possible calls, callbacks, IPC, shared state, and terminal effects.
5. Expand boundary functions toward internal handlers/outcomes and external senders/receivers.
6. Query dependency ordering and cycle concepts through `explore_graph`; invoke specialized dependency/SCC tools only when live metadata explicitly confirms FalkorDB routing.
7. Repeat with newly discovered module/message names until two zero-delta passes.
8. Use Serena only after Graph-RAG saturation to confirm message IDs, callback registration, include/type relationships, shared state, and line context.

A shared header or include is not automatically a runtime dependency. Keep compile-time, shared-data, direct-call, possible-call, callback, and IPC relationships distinct.

## Output

Write `usecase/<MODULE>/module-map.md` with:

- Falkor Graph gate, retrieval trace, and selected code collection
- inbound and outbound modules
- direct/possible/callback path evidence
- IPC messages with sender, receiver, payload, and handler
- shared-state/config dependencies
- dependency ordering and cycles when evidenced
- source locations and confidence for every edge
- saturation result and unresolved boundaries
