# Entry-Point Catalog

Catalog every evidenced way control enters the target module.

## Entry Types

- public/API function
- external module call
- IPC or message handler
- callback or virtual dispatch target
- timer, signal, interrupt, or event
- lifecycle hook
- UI/manual trigger

## Retrieval

1. Seed candidates through identity, trigger, lifecycle, event, callback, and message queries.
2. Expand each candidate toward callers/triggers and handlers/outcomes with `explore_graph`.
3. Use Serena references and registration patterns to confirm source locations.
4. Reject internal helpers, unused declarations, duplicate overloads, and unrelated homonyms with reasons.
5. Record actor, trigger, preconditions, synchronization, first handler, reachable use cases, and evidence status.

Write `entrypoints.json`. Do not label a symbol as an entry point without inbound evidence or explicit registration.
