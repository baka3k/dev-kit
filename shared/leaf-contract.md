# Leaf Skill Contract

## Identity

A leaf skill produces evidence-backed artifacts. It never:
- Invokes another skill or orchestrator.
- Spawns workers or delegates work.
- Writes or updates a global manifest, checkpoint, or run state owned by an orchestrator.

When a required capability belongs to another skill, return a structured prerequisite result naming the missing producer so the root can select the correct next skill.

## Draft-Only Direct Invocation

When invoked directly (not via a lifecycle orchestrator), a leaf produces **draft** artifacts only. Publication status remains `internal` or `draft` unless explicitly reviewed.

A lifecycle orchestrator (`hi-document-lifecycle` or `hi-maintenance-docs`) owns:
- Semantic refinement and clarification cycles.
- Review-comment resolution and disposition tracking.
- Approval and publication state transitions.
- Global manifest and revision lineage.

## Local Manifest

Every leaf writes a local `artifact-manifest.json` beneath its `output_root` using the shared schema `documentation-leaf-manifest-1.0` (or the skill-specific manifest schema referenced in its output contract). The manifest records:

- `producer_skill`, `created_at`, `inputs`, `status`.
- Per-artifact: path, media type, required flag, SHA-256 hash, validation result.
- Evidence references, warnings, and resume state (when applicable).

Do not substitute ad hoc manifest fields. Do not write outside the assigned `output_root`.

## Common Completion Conditions

A leaf completes only when:

1. All required output artifacts exist and validate against their schemas.
2. Every factual claim carries evidence or an explicit uncertainty marker (`inferred`, `unknown`, `contradicted`).
3. Output paths remain within the assigned `output_root`.
4. The manifest status matches the artifacts actually produced (no fabricated evidence).
5. Sensitive values (secrets, tokens, credentials, connection strings, infrastructure endpoints) are redacted.
6. The manifest hash matches the written artifacts.

A leaf returns `blocked` when required inputs are missing or invalid, `partial` when isolated evidence gaps exist with known/unknown coverage, and `succeeded` only when all required artifacts validate.

## Evidence Handling

- Record source file, symbol/document ID, retrieval layer, confidence, and source revision.
- A semantic match is a candidate, not proof. Verify through configuration, registration, exports, callers, or executable declarations.
- Separate generated, vendor, test, fixture, and production code.
- Record contradictions rather than silently resolving them.
- Reject wrong-project results and never count them toward coverage.
