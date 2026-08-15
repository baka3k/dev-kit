# Use-Case Artifact Contract

Store output under `usecase/<module>/`:

- `phase1_functions.json`, `phase1_dependencies.json`.
- `phase1_module_inventory.json`, including graph/Serena/`rg` reconciliation and unindexed files.
- `keywords.txt`, `phase2_keyword_hits.txt`, `phase2_symbols.json`, `phase2_candidate_ledger.json`.
- `phase3_trace_ledger.json`, `phase3_diagrams/seq_<slug>.mmd`.
- `uc_<NNN>_<slug>.md`, `uc_list.md`, `usecase-index.json`, `coverage.json`, `artifact-manifest.json`.

Each UC document contains purpose, audience, scope, owner when known, evidence status, last verified revision, generation time, visibility, related modules/documents, known gaps, actors, permissions, business rules, preconditions, main flow, alternative flows, error flows, code references, related API/event/data/state IDs, test scenarios, concise sequence diagram, outcomes, risks, and metrics.

Mark every step and branch `verified`, `corroborated`, `inferred`, `unknown`, or `contradicted`. Verified/corroborated items cite stable symbol/node ID when available plus repository-relative file and line/symbol anchor. Keep sequences to 12 lifelines and 30 messages; link `hi-behavior-modeling` outputs when deeper technical behavior already exists, but never invoke that skill from this leaf.

Coverage reports indexed/total files, reconciled/total classes and functions, traced/total entry points, branches, error paths, business rules, authorization decisions, indirect bridges, and tests. Include raw numerators/denominators, exclusions, unindexed scope, query caps/truncation, unavailable capabilities, queue state, and zero-delta reconciliation proof. Validate `usecase-index.json` against `usecase-output.schema.json`.
