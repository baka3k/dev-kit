---
name: hi-document-lifecycle
description: "Orchestrates evidence-backed document generation, human clarification, semantic/diagram refinement, and conditional review-comment resolution with pause/resume for one scoped domain. Use hi-maintenance-docs for a complete multi-domain pack."
---

# Document Lifecycle

Read [shared/orchestrator-contract.md](../shared/orchestrator-contract.md). Own the run root, checkpoint, revision ledger, pauses, joins, `current/` materialization, and final status. Never invoke another orchestrator; leaves never update global lifecycle state.

## Inputs

Required: `repo_root`, one document domain, bounded scope/anchor, `output_root`, source revision, visibility, `review_required`. Optional: prerequisite manifests, project/database/collection identity, output modes, clarification answers, review comments, limits, resume checkpoint.

Read [lifecycle-contract.md](references/lifecycle-contract.md), [transition-contract.md](references/transition-contract.md), [document-lifecycle-manifest.schema.json](references/document-lifecycle-manifest.schema.json), and [diagram-render-result.schema.json](references/diagram-render-result.schema.json) before starting.

## Generator Routing

| Domain | Generator | Optional Prerequisites |
|--------|-----------|----------------------|
| system/module summary | `hi-module-summary-report` | `hi-repo-recon`, `hi-tech-build-audit` |
| use case | `hi-usecase-discovery` | `hi-repo-recon` |
| technical behavior | `hi-behavior-modeling` | use-case or entry-point anchor |
| API/event contract | `hi-api-contract-discovery` | module/endpoint inventory |
| data model | `hi-data-model-discovery` | persistence/module inventory |
| command/protocol spec | `hi-command-spec-discovery` | module/command anchor |

Select exactly one generator per scoped lifecycle run.

## Three Phases

### Phase 1: Generate
1. Validate repository identity, output boundary, domain, review policy, source revision, and resume hashes.
2. Create `document-lifecycle/<run-id>/` with isolated stage roots, checkpoint, empty revision ledger, and root-owned manifest.
3. Run prerequisite leaves only when required validated inputs are absent.
4. Run selected generator leaf. Join local manifest as immutable `r001-generate`.

### Phase 2: Clarify/Refine
5. Run `hi-document-refinement` `analyze` against `r001`. If blocking questions lack answers → persist `waiting_for_input` and stop with resume state.
6. On resume, validate answers and run `apply` mode. Join accepted candidate as `r002-refine`; defer unanswered non-blocking items as gaps.

### Phase 3: Review/Update
7. If comments absent and review optional → `skipped_no_comments`. If review required and no comments → `waiting_for_input`. Otherwise run `hi-document-review-resolution` against base revision.
8. Join accepted changes as `r003-review`; reject stale, invalid, or unresolved blocking changes.
9. Revalidate changed dependencies, links, diagrams, redaction, evidence, hashes, and publication gate.
10. Atomically materialize accepted revision under `current/`; persist final status.

## Completion

Complete when: all transitions are legal, revisions have valid lineage and hashes, blocking items are resolved or deferred as gaps, every comment has one disposition, human inputs retain non-code provenance, navigation stays inside run root, and public visibility has explicit approval.
