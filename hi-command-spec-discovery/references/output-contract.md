# Command Documentation Output Contract

Write only beneath the caller-selected `output_root` (default recommendation: `command-docs/<module>/`):

- `commands/<command-slug>.md`: one document following the command template.
- `diagrams/<command-slug>-class.mmd`, `-sequence.mmd`, and `-state.mmd`: the same Mermaid sources embedded in the document.
- `module-inventory.json`: files, classes/types, functions/methods, entries, registrations, and reconciliation status.
- `command-inventory.json`: command seeds, opcodes/headers, handlers, codecs, status constants, and classification.
- `trace-ledger.json`: queue history, stable IDs, paths, branches, terminals, relationship types, and uncertainties.
- `evidence-index.json`: stable graph IDs and repository-relative file/line/symbol anchors.
- `coverage.json`: raw numerators/denominators, exclusions, caps, truncation, unindexed scope, and zero-delta proof.
- `documentation-gaps.md`: contradictions, runtime-only dispatch, missing bridges, unknown fields/statuses/states, and provider gaps.
- `command-index.json`: machine-readable command catalog conforming to `command-output.schema.json`.
- `artifact-manifest.json`: local `documentation-leaf-manifest-1.0` envelope with hashes, evidence refs, warnings, visibility, review state, and status.

Mark claims `verified`, `corroborated`, `inferred`, `unknown`, or `contradicted`. Only `verified` or `corroborated` facts may become normative values. Preserve variant-specific values separately when guards, versions, modes, or implementations disagree.

For each command, require evidence for the dispatch selector, framing/header, request fields, response fields, length rules, field optionality, byte order/encoding, validation order, success status, every documented error status, terminal action, sequence messages, class relationships, states, guards, and transitions. Use `{N/A}` when code proves a section is inapplicable; use `unknown` and a gap when evidence is absent.

Keep diagrams readable: at most 12 sequence lifelines, 30 messages, 20 classes, and 15 primary states per view. Split a view and link the parts when a verified flow exceeds a limit. Never omit a branch silently.
