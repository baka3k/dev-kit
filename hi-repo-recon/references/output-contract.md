# Recon Output Contract

## Manifest

Use the repository artifact envelope with:

- `schema_version`: `1.0`.
- `producer_skill`: `hi-repo-recon`.
- `created_at`: RFC 3339 timestamp.
- `inputs`: normalized repo root, scope, and depth.
- `status`: `succeeded`, `partial`, `blocked`, or `failed`.
- `artifacts`: path, media type, required flag, SHA-256, and validation status.
- `evidence_refs`: source locations or stable node/document IDs.
- `warnings`: missing indexes, contradictions, redactions, or omitted optional outputs.
- `resume_state`: omit for this stateless leaf.

## Module inventory

Each module records `name`, `path`, `kind`, `languages`, `responsibility`, `key_files`, `dependencies`, `evidence_refs`, and `confidence`. Dependencies record target, relation, and evidence.

## Entry-point map

Each entry records `name`, `kind`, `module`, `file`, optional `symbol`, trigger or registration evidence, downstream targets, evidence refs, and confidence.

## Key functions

Each item records stable symbol ID when available, name, qualified name, file, signature, role, evidence refs, and confidence. Never include full bodies unless needed to close a named gap.
