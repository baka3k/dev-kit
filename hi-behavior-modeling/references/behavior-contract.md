# Behavior Artifact Contract

Write `behavior-index.json`, `evidence-index.json`, `documentation-gaps.md`, `artifact-manifest.json`, and only requested supported views under `sequences/`, `activities/`, `states/`, and `event-flows/`.

Each view includes purpose, audience, scope, visibility, evidence status, source revision, generation time, related modules/documents, text summary, Mermaid source, legend, stable IDs, evidence links, and omissions. Use at most 12 sequence lifelines, 30 messages, or 15 primary states per view; split larger views.

Sequence records distinguish sync, async, return, retry, timeout, cancellation, error, and compensation. State records include source, trigger, guard, action, target, legality, terminal/error state, and evidence. Unknown or contradicted transitions stay explicit. Validate machine output against [behavior-output.schema.json](behavior-output.schema.json).
