---
name: hi-behavior-modeling
description: "Produce draft-only evidence-backed technical behavior as sequence, activity, state-machine, and event-flow documentation. Do not use for business use-case catalogs, API contracts, or persistent data models."
---

# Behavior Modeling

Read [dev-shared/leaf-contract.md](../dev-shared/leaf-contract.md). Operate as a draft-only leaf; lifecycle orchestrator owns refinement, review, and publication.

## Inputs

Require `repo_root`, a module/symbol/use-case anchor, and `output_root`. Accept requested modes, project/database/collection identity, source revision, depth/path limits, and visibility (`internal` by default).

## Evidence Gate

Read [retrieval-protocol.md](references/retrieval-protocol.md) and [dev-shared/retrieval-protocol.md](../dev-shared/retrieval-protocol.md). Treat semantic matches as candidates. Confirm ordered calls, guards, state reads/writes, and terminal effects with verified graph relationships or source evidence. Reject wrong-project results. Stop the affected mode when no source evidence exists; never invent a transition.

## Workflow

1. Normalize scope, identity, limits, visibility, and requested modes.
2. Inventory entry triggers, participants, calls, branches, state access, events, and observable outcomes.
3. Trace synchronous and asynchronous paths, including retry, timeout, cancellation, error, rollback, or compensation where evidenced.
4. Reconstruct only supported sequence, activity, state, and event views. Mark every claim `verified`, `corroborated`, `inferred`, `unknown`, or `contradicted`.
5. Apply schemas and size limits in [behavior-contract.md](references/behavior-contract.md). Split oversized diagrams and report omissions.
6. Write local manifest using `documentation-leaf-manifest-1.0` beneath `output_root`.

## Outputs

Produce `behavior-index.json` conforming to [behavior-output.schema.json](references/behavior-output.schema.json), requested Mermaid sources with Markdown summaries, transition tables where state evidence exists, evidence/gap records, and `artifact-manifest.json`.

Complete only when stable IDs resolve across artifacts, every verified claim cites evidence, sensitive values are redacted, and missing modes are reported truthfully.
