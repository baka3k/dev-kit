---
name: hi-maintenance-docs
description: "Orchestrate a complete, navigable, evidence-backed maintenance documentation pack spanning system overview, architecture, modules, use cases, technical behavior, API contracts, data models, command specifications, gaps, and freshness. Use for end-to-end documentation — not one bounded domain."
---

# Maintenance Documentation

Read [dev-shared/orchestrator-contract.md](../dev-shared/orchestrator-contract.md). Own the run directory, global manifest, joins, contradiction handling, index, freshness, and final status. Leaves own only their isolated outputs.

## Inputs

Require `repo_root`, scope, audience, visibility, requested modes. Accept module inventory, tech audit, use-case/API/data/command artifacts, project/database/collection identity, output root, limits, incremental baseline, render preference, `review_required` (default `true`), clarification answers, review comments.

Read [pipeline-contract.md](references/pipeline-contract.md), [evidence-contract.md](references/evidence-contract.md), [readability-and-security.md](references/readability-and-security.md), and `hi-document-lifecycle/references/lifecycle-contract.md`.

## Stage Dependencies

| Order | Stage | Skill | Prerequisites | Skippable? |
|-------|-------|-------|--------------|-----------|
| 1 | recon/audit | `hi-repo-recon` + `hi-tech-build-audit` | inputs | Yes, if validated inputs provided |
| 2 | module summary | `hi-module-summary-report` | recon + audit | No |
| 3 | use cases | `hi-usecase-discovery` | module roots | No |
| 4 | API/data/command | `hi-api-contract-discovery` + `hi-data-model-discovery` + `hi-command-spec-discovery` | requested modes only | Yes, if not requested |
| 5 | behavior | `hi-behavior-modeling` | use-case/entry-point anchor | Yes, if no anchor |
| 6 | cross-validation | `hi-cross-artifact-validation` | all leaf manifests | Optional |
| 7 | synthesis | internal | all local manifests | No |
| 8 | refinement | `hi-document-refinement` | r001 | No |
| 9 | review | `hi-document-review-resolution` | r002 + comments | If no comments + not required |

## Workflow

1. Create unique `maintenance-docs/<run-id>/` with normalized inputs, checkpoint, and empty manifest.
2. Run `hi-repo-recon` + `hi-tech-build-audit` only when validated inputs absent. Allow concurrency for disjoint stage roots.
3. Join required manifests, run `hi-module-summary-report` for system/module views.
4. Run `hi-usecase-discovery` across independent module roots.
5. Run `hi-api-contract-discovery`, `hi-data-model-discovery`, `hi-command-spec-discovery` only for requested, supported modes.
6. Run `hi-behavior-modeling` only after a use-case/entry-point anchor exists.
7. Optionally run `hi-cross-artifact-validation` for cross-domain consistency checks.
8. Validate and join local manifests; copy every leaf artifact into its canonical domain subtree (`system/`, `behavior/`, `api/`, `data/`, `command/`). Rewrite links to stay inside run root; reconcile stable IDs; retain contradictions; classify gaps; compute freshness. Persist as immutable `r001`.
9. Run `hi-document-refinement` `analyze` against `r001`. If blocking questions unanswered → persist, stop in `waiting_for_input`. Otherwise run `apply` with validated answers → immutable `r002`.
10. If comments anchored to `r002` exist → invoke `hi-document-review-resolution` → `r003` + disposition ledger. If absent and `review_required=true` → wait. If absent and `review_required=false` → skip.
11. Build final index from [index-template.md](assets/index-template.md), materialize `current/` from latest validated revision, validate pack, persist status with resume state.

Graph evidence comes from the leaf skills above; run no direct inventory. When validating a claimed anchor during joins, verify it once with `search_functions` or `get_symbol` per [dev-shared/graph-function-selection.md](../dev-shared/graph-function-selection.md) (T3 profile, delegated execution).

**Resume**: Revalidate input, artifact, and parent hashes before skipping completed work. Retry counts never reset.

## Completion

Require all requested artifacts navigable, `governance/evidence-index.json` valid, `governance/documentation-gaps.md`, `governance/freshness-report.md`, manifest valid, legal lifecycle transitions, revision lineage, artifact hashes, clarification/review coverage. Block on redaction failure. Missing evidence, stale inputs, skipped review, omitted optional modes must remain visible.
