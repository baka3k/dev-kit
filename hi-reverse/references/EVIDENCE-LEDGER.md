# Evidence Ledger

Maintain the standalone claim ledger as the traceability source for the package.

Each claim records status, Graph node IDs, symbols, relationships, locations, retrieval calls, Serena support, affected artifacts, and uncertainties. Use stable claim IDs so every document can reference the same evidence without copying it.

Merge duplicate claims by node ID and qualified symbol. Never upgrade confidence merely because multiple artifacts repeat the same unsupported statement.

Write `evidence-ledger.json` and keep `unresolved_gaps` synchronized with the open-questions log.
