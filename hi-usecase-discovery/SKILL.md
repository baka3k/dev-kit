---
name: hi-usecase-discovery
description: "Produce draft-only evidence-backed business use cases for one source module by inventorying files, classes, functions, entry points, registrations, indirect calls, and terminal effects, then reconstructing actors, permissions, rules, flows, outcomes, IDs, tests, and coverage. Do not use for technical behavior diagrams, API contracts, data models, or migration execution."
---

# Use-Case Discovery

Read [dev-shared/leaf-contract.md](../dev-shared/leaf-contract.md). Operate as a draft-only leaf; lifecycle orchestrator owns refinement, review, and publication. Run four internal phases in one skill.

## Inputs

Require `repo_root`, `module_name`, and at least one canonical module path. Accept `output_dir` (default `usecase`), `parser_type` (default `cplus`), database/project/collection context, source revision, visibility (`internal` by default), and explicit query caps. Caps protect tools; they never prove completeness.

## Retrieval Gate

Read [graph-retrieval.md](references/graph-retrieval.md), [exhaustive-tracing.md](references/exhaustive-tracing.md), [serena-rg-coverage.md](references/serena-rg-coverage.md), and [dev-shared/retrieval-protocol.md](../dev-shared/retrieval-protocol.md). Stop if no code evidence can establish a module inventory.

## Phases

1. Confirm project identity and scope, build the source-file universe, then inventory every graph-visible class, type, function, method, entry point, handler, lifecycle callback, registration, dependency edge, IPC bridge, and unindexed file. Write the Phase 1 inventory and reconciliation ledger.
2. Build module/domain/romaji/kanji/field/ID keywords. Run semantic, symbol-name, code-literal, registration, and terminal-effect discovery passes; resolve retained candidates to stable IDs and add every new seed to the work queue.
3. Drain the queue in bounded graph waves. Trace each seed through direct, indirect, callback, function-pointer, IPC, navigation, API, data, error, and cross-module edges until a fixed point. Reconcile every missing bridge with Serena then `rg`. Write the trace ledger and concise Mermaid sequences; label every step and branch `verified`, `corroborated`, `inferred`, `unknown`, or `contradicted`.
4. Cluster paths by trigger, actor, permission, business rule, domain state/data, and terminal outcome. Generate documents per [usecase-contract.md](references/usecase-contract.md), validate [usecase-output.schema.json](references/usecase-output.schema.json), and write the index, evidence/gap records, coverage denominators, excluded/unindexed scope, and local `documentation-leaf-manifest-1.0` manifest.

If module inventory is missing, return a prerequisite result suggesting `hi-repo-recon`.

## Completion

Require all phase artifacts and at least one UC document only when a validated path exists. Complete when: every inventoried seed classified, trace queue empty, one zero-delta reconciliation pass, no silent truncation, and every unresolved/unindexed item recorded as a gap. A hit cap, depth cap, unavailable provider-specific bridge, or denominator mismatch forces `partial` or `blocked`, never `succeeded`.

Every UC must include actors, permissions, business rules, preconditions, main/alternative/error flows, code references, related API/event/data/state IDs, test traceability, a bounded sequence diagram, evidence status, revision, visibility, and coverage. Never convert historical percentage targets into false claims.
