---
name: hi-data-model-discovery
description: "Produce draft-only evidence-backed physical and logical data models, ERDs, entity and field inventories, data dictionaries, ownership, read/write access, lifecycle, sensitivity, caching, replication, and migration gaps. Do not execute schema migrations or present inferred relationships as declared constraints."
---

# Data Model Discovery

Read [dev-shared/leaf-contract.md](../dev-shared/leaf-contract.md). Operate as a draft-only leaf; lifecycle orchestrator owns refinement, review, and publication.

## Inputs

Require `repo_root`, database/module/entity scope, and `output_root`. Accept parser and project/database/collection identity, source revision, visibility (`internal` by default), and size limits.

## Evidence Gate

Read [retrieval-protocol.md](references/retrieval-protocol.md) and [dev-shared/retrieval-protocol.md](../dev-shared/retrieval-protocol.md). Distinguish database declarations, migrations, ORM mappings, domain models, DTOs, caches, and inferred usage. Reject wrong-project results. An inferred foreign key, cardinality, owner, or retention policy never becomes a declared constraint. Graph profile (T3 in [dev-shared/graph-function-selection.md](../dev-shared/graph-function-selection.md)): `search_by_code` for SQL/DDL and ORM literals, `listup_symbols_matching_file_path` for entity inventory, `get_symbol` for declared constraints.

## Workflow

1. Normalize scope, model layers, identity, visibility, and output boundary.
2. Inventory entities, fields, types, keys, constraints, indexes, relationships, migrations, readers, writers, and owners.
3. Corroborate physical declarations against ORM/domain/DTO usage; record contradictions without silently resolving them.
4. Build bounded physical and logical Mermaid ERDs, plus human and machine-readable inventories.
5. Apply [data-contract.md](references/data-contract.md), including lifecycle, retention, sensitivity, cache, replication, and migration gaps.
6. Write local manifest using `documentation-leaf-manifest-1.0` beneath `output_root`.

## Outputs

Produce physical/logical ERD sources, `data-model.json` conforming to [data-output.schema.json](references/data-output.schema.json), `data-dictionary.md`, ownership/access and lifecycle documents, contradiction/gap records, evidence index, and `artifact-manifest.json`.

Complete only when model layers and evidence statuses are explicit, verified relationships cite source evidence, and sensitive values are redacted.
