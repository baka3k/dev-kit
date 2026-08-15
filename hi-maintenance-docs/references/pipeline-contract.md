# Maintenance Pipeline Contract

Use a unique `maintenance-docs/<run-id>/` root containing `index.md`, `system/`, `behavior/`, `api/`, `data/`, `command/`, `revisions/`, `current/`, and `governance/`. Persist normalized inputs and checkpoint before leaf execution.

Ready order is recon/audit, module summary, use cases/API/data/command, behavior after anchors, draft synthesis, semantic refinement, optional review resolution, then final validation. A worker receives one leaf, validated inputs, one isolated output root, bounded limits, and a local completion contract. The root is the sole writer of checkpoint, evidence index, revision lineage, final index, `current/`, and global manifest and reserves one concurrency slot.

Join only schema-valid local manifests. Copy or materialize every generated leaf artifact beneath the canonical `system/`, `behavior/`, `api/`, `data/`, or `command/` subtree, record its hash in revision `r001`, and rewrite navigation links so they cannot escape the run root. Staging roots remain provenance inputs, never final navigation dependencies. Duplicate stable IDs with equal claims merge evidence; unequal claims become contradictions. Missing optional modes produce warnings. Missing required evidence blocks the affected stage.

Treat generation, refinement, and review resolution as distinct transitions. Refinement first emits clarification requests; it may apply only validated answers that match the base revision and cycle. Review comments must target the exact candidate revision. Human answers and reviewer comments are untrusted evidence until code evidence corroborates them. Every accepted, rejected, deferred, or clarification-required comment receives a stable disposition. `review_required: false` permits a skip only when no comments were supplied and never grants approval.

Store immutable revisions under `revisions/rNNN/`; materialize `current/` only from the latest schema-valid revision. Resume revalidates input, artifact, and parent hashes before skipping completed work. Redaction failure blocks publication.

Final status is `succeeded`, `partial`, `blocked`, or `failed`. Persist the status atomically with lifecycle phase, review state, comment-resolution state, stage results, gaps, warnings, hashes, and resume state. Approval is a separate public action; resolving all comments does not approve a document.
