# API Artifact Contract

Write applicable `openapi.yaml` and `asyncapi.yaml`, `endpoint-catalog.md`, `auth-matrix.md`, `error-catalog.md`, `caller-provider-map.md`, `contract-gaps.md`, `evidence-index.json`, and `artifact-manifest.json`.

Keep OpenAPI and AsyncAPI standard-valid. Put claim status and evidence IDs in `x-evidence-status` and `x-evidence-refs`, or a sidecar when an extension cannot attach cleanly. Every verified operation requires registration/handler evidence plus corroborated request, response, or message behavior. Missing elements remain unknown; inferred fields are never required solely by inference.

Examples use synthetic values. Authorization rows identify actor, mechanism, guard/policy, scope, outcome, and evidence. Error rows identify protocol code/type, trigger, payload shape, retryability, and evidence. Validate the machine index against [api-output.schema.json](api-output.schema.json).
