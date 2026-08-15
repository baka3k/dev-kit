# Retrieval Protocol

## Fast-fail order

1. `mind_mcp`: retrieve project concepts, documents, and known architecture.
2. `graph_mcp`: call live tool discovery once, then use semantic search for candidates and graph relations for proof.
3. Serena: search symbols, references, and non-indexed source areas.
4. Native: use `rg --files`, `rg`, and direct file reads for exact verification.

Proceed to the next layer only when the current layer is unavailable, yields no relevant results, or leaves a named evidence gap. Do not repeat a rejected call. Retry once only when the tool reports invalid parameters and supplies a callable schema.

## Evidence rules

- Record source file, symbol or document identifier, retrieval layer, and confidence.
- A semantic match is not proof of a dependency or entry point.
- Verify entry points through configuration, registration, exports, callers, or executable declarations.
- Separate generated, vendor, test, fixture, and production code.
- Record code/document contradictions rather than choosing silently.

## Depth

- `quick`: module boundaries and basic entry points.
- `standard`: quick plus key symbols and direct dependencies.
- `deep`: standard plus verified cross-module calls, IPC, persistence, external services, and file I/O.
