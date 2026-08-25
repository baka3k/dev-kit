# Shared Retrieval Protocol

## Fast-Fail Order

Follow layers in order. Proceed to the next only when the current layer is unavailable, yields no relevant results, or leaves a named evidence gap. Do not repeat a rejected call.

1. **mind_mcp**: Retrieve project concepts, documents, and known architecture.
2. **graph_mcp**: Call live tool discovery once, then use semantic search for candidates and verified graph relationships for proof.
3. **Serena**: Search symbols, references, and non-indexed source areas.
4. **Native (rg)**: Use `rg --files`, `rg`, and direct file reads for exact verification.

Retry once only when the tool reports invalid parameters and supplies a callable schema. Fast-fail an unavailable layer once; do not retry it with guessed parameters. The live tool schema overrides historical examples and documentation.

## Evidence Rules

- Record source file, symbol or document identifier, retrieval layer, and confidence.
- A semantic match is not proof of a dependency, entry point, or relationship.
- Verify entry points through configuration, registration, exports, callers, or executable declarations.
- Separate generated, vendor, test, fixture, and production code.
- Record code/document contradictions rather than choosing silently.
- Treat names, comments, and existing documents as candidates until implementation paths corroborate them.
- Reject wrong-project graph results; warn and never count toward coverage.

## Depth Levels

| Depth | Coverage |
|-------|----------|
| `quick` | Module boundaries and basic entry points. |
| `standard` | Quick plus key symbols and direct dependencies. |
| `deep` | Standard plus verified cross-module calls, IPC, persistence, external services, and file I/O. |

## Required Retrieval Intents

Adapt the intent list to the skill's domain:

- Symbol inventory and details (classes, functions, types, entry points).
- Dependency relationships (direct, indirect, callback, IPC, cross-module).
- Registration and dispatch sites.
- Terminal effects (state writes, external calls, file I/O).
- Project-document retrieval (configs, schemas, contracts).

Never hard-code provider endpoints or obsolete call names. Discover live graph functions before use.
