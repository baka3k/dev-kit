# Orchestrator Contract

## Ownership

The orchestrator owns the run directory, global manifest, checkpoint, stage transitions, final report assembly, and status. Leaf skills own only their isolated output artifacts and local manifests.

No orchestrator invokes another orchestrator. Reserve one concurrency slot; never start work with overlapping output paths.

## Worker Constraints

Cap concurrent workers at:

```
min(available_slots - 1, independent_ready_units, configured_max_workers)
```

A worker receives:
- One leaf skill assignment with required validated inputs.
- One isolated output path (no shared write targets).
- Constraints and a local completion contract.

A worker must not:
- Spawn other workers or invoke skills beyond its assigned leaf.
- Write to the global manifest, checkpoint, or run state.
- Edit another worker's output directory.

Start a worker only when: prerequisites validate, the task maps to one leaf, the output directory is unique, work is independent, and a slot exists.

## Failure Behavior

| Failure type | Action |
|-------------|--------|
| Missing or invalid input | `blocked` before delegation. |
| One leaf failure | Allow `partial` result if remaining evidence can be synthesized honestly. |
| Invalid manifest or overlapping output | Stop the affected transition. |
| Diagram renderer unavailable | Retain Mermaid source and warn. |
| Corrupt checkpoint or hash mismatch | Strict stop until reconciled. |

Log every failure with stage, leaf, artifact, and reason. Never fabricate missing evidence or invent empty successful results after a failure.

## Atomic Persistence

Write state to a temporary sibling file, fsync, and atomically replace the target. Record:

- `schema_version`, `run_id`, normalized inputs.
- Stage statuses (`pending`, `ready`, `running`, `succeeded`, `partial`, `blocked`, `failed`).
- Completed units, failures, artifact path/hash records.
- `updated_at` timestamp.

Only the root advances stages or writes the global manifest.

## Resume Semantics

On resume:
1. Validate schema, stage names, and artifact existence.
2. Verify SHA-256 hashes of completed artifacts.
3. A hash mismatch is a strict stop until the user or root reconciles.
4. Skip completed stages; revalidate only pending or failed stages.
5. Retry counts and cycles never reset on resume.

## Final Assembly

- Assemble the final report from validated stage artifacts only.
- Include: executive summary, architecture, modules, technology, risks, evidence gaps, and next steps (adapt sections to the orchestrator's domain).
- Record highest severity, evidence gaps, partial stages, and recommended next skills.
- Persist final status (`succeeded`, `partial`, `blocked`, `failed`) atomically with all supporting state.
