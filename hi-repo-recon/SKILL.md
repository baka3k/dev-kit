---
name: hi-repo-recon
description: "Map an unfamiliar repository into an evidence-backed module inventory, entry-point map, and optional key-function catalog. Use for repository onboarding, architecture reconnaissance, handover preparation, or refactor scoping."
---

# Repository Reconnaissance

Read [dev-shared/leaf-contract.md](../dev-shared/leaf-contract.md). Produce structural evidence only. Do not own build auditing, risk synthesis, or full discovery orchestration.

## Inputs

Require an absolute, readable `repo_root`. Accept `scope`: `backend`, `frontend`, `infra`, `data`, or `all` (default). Accept `depth`: `quick`, `standard` (default), or `deep`. Accept output root; default `discovery-output/recon-data`.

Reject paths outside the requested repository and output root. Return a structured prerequisite failure when the repository cannot be read.

## Retrieval

Read [dev-shared/retrieval-protocol.md](../dev-shared/retrieval-protocol.md). Follow the first successful layer and stop when evidence is sufficient. Treat semantic hits as candidates until direct repository evidence confirms them.

Graph profile (T3 in [dev-shared/graph-function-selection.md](../dev-shared/graph-function-selection.md)): run the inventory group (`listup_symbols_matching_file_path`, `listup_class_matching_path`, `list_up_entrypoint`) for module and entry-point maps; use `plan_dependency_order`, `plan_file_dependency_order`, `plan_function_dependency_order`, and `compute_scc` for dependency waves and cycles at `deep` depth.

## Workflow

1. Validate inputs and create the output directory.
2. Record retrieval coverage and evidence gaps.
3. Identify repository roots, buildable/deployable units, source modules, generated/vendor boundaries, and ownership clues.
4. Identify CLI, API, UI route, service, worker, scheduled-job, and library entry points in scope.
5. For `standard`, add key symbols per module. For `deep`, add verified dependency, IPC, database, external-service, and file-I/O boundaries.
6. Cross-check indexed results against the filesystem. Report discrepancies; never invent unindexed modules.
7. Redact secrets, tokens, contact data, connection strings, and infrastructure endpoints.
8. Write artifacts and manifest per [output-contract.md](references/output-contract.md).
9. Validate required files and JSON shape before returning.

## Outputs

Write beneath `discovery-output/recon-data/` by default:

- `module-inventory.json` — required.
- `entry-point-map.json` — required.
- `key-functions.json` — required for `standard` and `deep`.
- `artifact-manifest.json` — required common envelope.

Complete only when required JSON parses, every claim carries evidence or explicit uncertainty, output paths remain in scope, and the manifest status matches artifacts produced.

If synthesis or build evidence is needed, return the missing prerequisite so the root can select `hi-tech-build-audit`, `hi-module-summary-report`, or an orchestrator.
