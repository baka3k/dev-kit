---
name: hi-api-contract-discovery
description: "Produce draft-only evidence-backed HTTP and asynchronous API contracts, including OpenAPI or AsyncAPI drafts, endpoints, messages, schemas, authentication, authorization, errors, consumers, and providers. Do not deploy APIs, modify implementations, or publish inferred contracts as authoritative."
---

# API Contract Discovery

Read [shared/leaf-contract.md](../shared/leaf-contract.md). Operate as a draft-only leaf; lifecycle orchestrator owns refinement, review, and publication.

## Inputs

Require `repo_root`, service/module/endpoint scope, protocol modes, and `output_root`. Accept project/database/collection identity, source revision, visibility (`internal` by default), and path/depth limits.

## Evidence Gate

Read [retrieval-protocol.md](references/retrieval-protocol.md) and [shared/retrieval-protocol.md](../shared/retrieval-protocol.md). A route or topic declaration alone is incomplete: verify registration, handler, parsing, validation, DTO/schema, auth checks, responses/errors, callers/consumers, and downstream effects. Reject wrong-project results; preserve missing elements as gaps.

## Workflow

1. Normalize scope, protocol modes, identity, visibility, and output boundary.
2. Inventory HTTP routes and event/message channels from verified registrations and source symbols.
3. Corroborate request, response, payload, validation, authentication, authorization, error, caller/provider, and dependency behavior.
4. Generate draft OpenAPI/AsyncAPI only when protocol evidence exists. Keep evidence status in standard-compatible extensions or sidecars.
5. Apply [api-contract.md](references/api-contract.md), redact examples, distinguish verified from inferred/unknown fields.
6. Write local manifest using `documentation-leaf-manifest-1.0` beneath `output_root`.

## Outputs

Produce applicable `openapi.yaml`/`asyncapi.yaml`, index conforming to [api-output.schema.json](references/api-output.schema.json), endpoint/event catalog, auth matrix, error catalog, caller/provider map, contract gaps, synthetic examples, evidence index, and `artifact-manifest.json`.

Complete only when documents parse, verified operations cite evidence, contradictions remain visible, and publication status remains internal or explicitly reviewed.
