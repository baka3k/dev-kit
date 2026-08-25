---
name: hi-cross-artifact-validation
description: "Validate consistency across discovery outputs (use-case, API, data-model, behavior, command-spec) by checking stable ID resolution, actor/auth alignment, state-transition lifecycle matches, schema compatibility, and cross-domain evidence coherence. Use after leaf discovery skills complete, before refinement."
---

# Cross-Artifact Validation

Read [shared/leaf-contract.md](../dev-shared/leaf-contract.md). Validate cross-domain consistency without modifying source artifacts. Operate as a read-only validation leaf.

## Inputs

Require `output_root` containing validated leaf manifests and artifacts from at least two discovery domains. Accept `domains` list to limit scope (default: all present domains), `strict` flag (default `false`), and `output_dir` (default `cross-validation`).

Block when fewer than two domain manifests are available.

## Validation Checks

| Check | Domains | Rule |
|-------|---------|------|
| Stable ID resolution | all | Every stable ID referenced across domains resolves to one entity; flag orphaned or ambiguous IDs |
| Actor/auth alignment | use-case + API | Use-case actors match API auth matrix entries; flag actors without auth or auth without actors |
| State lifecycle | behavior + data-model | Behavior state transitions match data-model lifecycle states; flag unmapped transitions |
| Schema compatibility | command-spec + API | Command-spec fields align with API request/response schemas; flag type mismatches |
| Evidence coherence | all | Evidence status across domains is consistent; flag verified-contradicted conflicts |
| Dependency coverage | all | Cross-domain dependencies cited in one artifact exist in the target domain |

## Workflow

1. Load all available domain manifests and validate their hashes.
2. Build a unified stable-ID index from all domain artifacts.
3. Run each applicable validation check from the table above.
4. Classify findings as `error` (blocks consistency), `warning` (potential issue), or `info` (observation).
5. Write `cross-validation-report.md` with findings grouped by check, `cross-validation-results.json` per [validation-contract.md](references/validation-contract.md), and `artifact-manifest.json`.

When `strict=true`, any `error` finding forces `blocked` status. When `strict=false`, errors are `warning`-level and status is `partial`.

## Completion

Complete when all applicable checks run, every finding has severity/domain/evidence/affected-IDs, the report is navigable from the index, and the manifest validates. No source artifacts are modified.
