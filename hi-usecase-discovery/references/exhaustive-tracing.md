# Exhaustive Use-Case Tracing

## Contents

1. Exhaustive boundary
2. Required ledgers
3. Module-first inventory
4. Seed construction
5. Queue and fixed-point algorithm
6. Path validation and use-case clustering
7. Coverage and stop gates

## Exhaustive boundary

“Exhaustive” means exhaustive within the declared repository revision, canonical module paths, supported source extensions, generated/vendor exclusions, graph project scope, and recorded tool capabilities. It does not mean an unbounded graph traversal.

Freeze these values before tracing:

- repository and source revision;
- canonical module path tokens and source-file universe;
- included languages/extensions and explicit exclusions;
- graph database/project/collection/parser identity;
- relationship types and provider feature gates;
- per-call limits and maximum safe depth.

A cap is a safety control. If a response reaches a cap, reports truncation, or still adds nodes at maximum depth, split the query or mark the affected denominator `partial`; never call it saturated.

## Required ledgers

Write machine-readable ledgers under `usecase/<module>/`:

- `phase1_module_inventory.json`: files, classes/types, functions/methods, entry points, registrations, exclusions, unindexed files, and source counts.
- `phase1_dependencies.json`: module/file/function dependencies, cross-module edges, SCCs, and uncertain edges.
- `phase2_candidate_ledger.json`: every candidate query/hit, retained/rejected decision, and stable ID mapping.
- `phase3_trace_ledger.json`: queue state, nodes, edges, paths, branches, terminals, indirect bridges, evidence status, and gaps.
- `coverage.json`: denominators, numerators, exclusions, truncation, unavailable capabilities, and fixed-point proof.

Use stable graph node IDs as primary keys. For source-only symbols, use `repo-relative-path::qualified-name-or-line-anchor` and mark the graph ID absent.

## Module-first inventory

Do not start with a guessed use case. Read the module as a closed inventory first.

1. Build the file universe from the canonical paths. Exclude generated, vendored, binary, fixture, and test files only through explicit policy; keep test files in a separate test-evidence set.
2. Run the graph symbol-by-path inventory for classes/types/functions, class-to-method expansion, entry-point discovery, and module/file/function dependency planners.
3. Reconcile four sets:
   - graph symbols by file path;
   - graph class methods;
   - graph function dependency inventory;
   - Serena/`rg` source inventory.
4. Classify every source file as `indexed`, `partially_indexed`, `source_only`, `excluded`, or `unreadable`.
5. Classify every symbol as entry, orchestration, rule/guard, state/data access, integration, terminal effect, utility, test, dead/unreferenced candidate, or unresolved.
6. Record counts per file and per class. Overloads remain distinct by stable ID/signature.

The Phase 1 gate passes only when every in-scope source file appears in the ledger and every graph/source count mismatch is resolved or recorded as a gap.

## Seed construction

Create a deduplicated seed queue from all of these categories:

- external module entries and public/exported functions;
- controllers, commands, handlers, listeners, jobs, schedulers, lifecycle callbacks, UI actions, and route endpoints;
- registrations in annotations, configuration, factories, dependency injection, tables, macros, and framework metadata;
- functions referenced from outside the module;
- callback, virtual-dispatch, function-pointer, IPC, event, and message endpoints;
- domain rule/guard, authorization, validation, state transition, data write, emitted event, response, error, rollback, retry, cancel, and timeout anchors;
- semantic/name/code hits that resolve to an in-scope stable symbol;
- source-only symbols found during Serena/`rg` reconciliation.

Each seed records `seed_kind`, source, stable ID/location, why it is in scope, and status `queued`, `traced`, `excluded_with_reason`, or `unresolved`.

## Queue and fixed-point algorithm

Use a deterministic FIFO queue keyed by stable ID/location:

1. Pop one unseen seed and mark it `in_progress`.
2. Expand direct outgoing and incoming graph edges at depth 1 with explicit relationship types. Add unseen nodes/edges to the ledger.
3. Increase depth in bounded waves only while the preceding wave adds relevant nodes. Split by direction or relationship type before increasing result limits.
4. For each branch/guard, enqueue every successor, including negative, default, exception, timeout, retry, cancellation, and rollback successors.
5. For each dynamic dispatch, query possible calls and validate candidates against source registrations/references. A possible edge stays `inferred` until corroborated.
6. For each module boundary, trace both module-level and symbol-level paths. Enqueue in-scope re-entry nodes and record out-of-scope dependencies as external participants.
7. For each IPC/event/API/navigation clue, run the applicable bridge query and enqueue verified counterpart nodes.
8. Identify terminal effects: state/data mutation, external call, emitted event/message, returned response/result, visible UI transition, audit/log side effect, or terminal error.
9. Prove entry-to-terminal paths with exact path/flow calls. Store ordered nodes, edges, relationship types, locations, and uncertainties.
10. Mark the seed `traced` only when all discovered branches terminate, leave scope explicitly, enter a recorded cycle/SCC, or become a named gap.
11. Add all newly found entry-like nodes, branches, registrations, and terminals to the queue.
12. After the queue empties, run one reconciliation pass over inventory counts, source references, indirect bridges, and terminal searches. If it adds anything, enqueue the delta and repeat.

The fixed point is reached only when the queue is empty and the full reconciliation pass has zero new files, symbols, entries, branches, edges, bridges, or terminals.

## Path validation and use-case clustering

Do not create one use case per function. Cluster proven paths when they share business intent, actor, trigger, authorization context, domain object/state, and terminal outcome. Split clusters when permissions, business rules, alternative outcomes, or externally visible effects differ materially.

Evidence status rules:

- `verified`: direct indexed edge or exact source call/registration with stable location.
- `corroborated`: the same bridge is supported by independent graph and source/test/config evidence.
- `inferred`: plausible indirect/dynamic/shared-state bridge with incomplete proof.
- `unknown`: required bridge cannot be resolved in the declared scope.
- `contradicted`: sources disagree; retain both claims and the conflict.

A complete use-case path needs a trigger/actor boundary, entry, relevant permissions/guards/rules, main outcome, all discovered alternative/error branches, and terminal effect. Naming similarity or a semantic hit is never a path.

## Coverage and stop gates

Report raw counts and ratios for:

- in-scope source files indexed / total source files;
- reconciled classes/types / total discovered classes/types;
- classified functions/methods / total discovered functions/methods;
- traced entry seeds / total entry seeds;
- terminated branches / total discovered branches;
- traced error/timeout/retry/cancel/rollback paths / total discovered;
- evidenced business rules and authorization decisions / total discovered;
- linked tests / total discovered test candidates;
- resolved indirect/IPC/API/navigation bridges / total discovered bridges.

Every denominator includes source-only items unless explicitly excluded with a reason. Never remove unknown or unindexed items to improve a percentage.

`succeeded` requires all of the following:

- Phase 1 file and symbol reconciliation passed;
- every seed is `traced` or `excluded_with_reason`;
- every discovered branch has a terminal, explicit scope exit/cycle, or named gap;
- the queue is empty and the reconciliation pass is zero-delta;
- no query is silently truncated and no required capability failed;
- all remaining gaps are non-critical to the documented paths.

Use `partial` when useful paths are proven but any denominator, bridge, truncation, provider gap, or critical branch remains unresolved. Use `blocked` when no validated entry-to-terminal path can be established.
