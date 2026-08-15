---
name: hi-document-refinement
description: "Analyze an evidence-backed draft for ambiguity, terminology gaps, missing semantics, and under-specified Mermaid diagrams, then apply validated clarification answers to an isolated candidate revision. Do not generate initial documents, resolve review comments, invent answers, or update an orchestrator's global manifest."
---

# Document Refinement

Read [shared/leaf-contract.md](../shared/leaf-contract.md). Operate as a leaf; never invoke skills, ask on behalf of an orchestrator, spawn workers, overwrite the base revision, or update a global manifest.

## Inputs

Require `mode` (`analyze` or `apply`), base revision root and manifest, evidence index, document domain, output root, source revision, visibility. In `apply` mode also require schema-valid clarification requests and answers tied to the base revision.

Read [refinement-contract.md](references/refinement-contract.md) for both modes; read [semantic-and-diagram-review.md](references/semantic-and-diagram-review.md) when diagrams or cross-artifact terminology are in scope.

## Analyze Mode

1. Validate immutable base revision, artifact hashes, evidence refs, and output isolation.
2. Inventory ambiguous terminology, inconsistent names, missing actors/participants, guards, branches, states, relationships, constraints, contradictions, and unsupported diagram elements.
3. Separate code-resolvable gaps from questions requiring human intent or domain semantics. Use source retrieval only to close a named evidence gap.
4. Emit stable-ID blocking and non-blocking questions plus a non-mutating refinement proposal.

## Apply Mode

1. Validate question IDs, answer forms, base revision/hash, provenance, visibility, and cycle limit.
2. Reject invented, stale, conflicting, or evidence-incompatible answers; never upgrade human declarations to implementation-verified facts without corroboration.
3. Apply answered changes in deterministic artifact/anchor order to an isolated candidate root.
4. Enrich diagrams only with evidence-supported semantics; enforce size, split, render, legend, evidence, and text-summary gates.
5. Emit changed-artifact hashes, evidence impact, unresolved gaps, refinement report, candidate revision, and local manifest.

## Completion

Analyze mode succeeds without modifying the base. Apply mode succeeds when no blocking question remains unanswered, every change traces to an answer and evidence status, changed diagrams validate, redaction and path confinement pass, and the candidate is ready for orchestrator acceptance — never self-publish.
