# Interface Catalog

Generate interface contracts when the `ipc` condition is active.

## Retrieval

1. Identify inbound and outbound APIs, IPC messages, callbacks, host/device requests, shared-memory contracts, and file/database boundaries.
2. Resolve sender, receiver, registration, handler, request/response correlation, payload type, direction, synchronization, timeout, retry, and failure semantics.
3. Expand boundary anchors through Graph-RAG and verify constants, payload fields, and handlers with Serena.
4. Separate runtime contracts from compile-time includes and type dependencies.
5. Preserve unknown payload fields or timing behavior as explicit gaps.

Write `interfaces.md`. Every contract row must link to endpoint/message evidence and affected use cases.
