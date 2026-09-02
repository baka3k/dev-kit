---
name: hi-module-summary-report
description: "Synthesize existing module-inventory and tech-audit artifacts into an architecture summary, per-module breakdown, risk assessment, and optional Mermaid diagrams. Do not inspect source from scratch or run full onboarding."
---

# Module Summary and Risk Report

Read [dev-shared/leaf-contract.md](../dev-shared/leaf-contract.md). Consume evidence; do not independently rediscover the repository. Lifecycle orchestrator owns refinement, review, approval, and publication.

## Inputs

Require valid `module_inventory` and `tech_audit` artifact paths. Accept `audience` (`engineering` | `management` | `mixed`), `depth` (`executive` | `standard` | `detailed`), `mermaid` (default `true`), optional `repo_root` — only to close a named evidence gap.

Missing/invalid input → return prerequisite result naming the missing producer; do not invoke it.

## Workflow

1. Validate input manifests, hashes, schemas, and producer statuses.
2. Reconcile modules, dependencies, entry points, stack, build, CI/CD, and platform evidence. Record contradictions and incomplete modules.
3. Produce per-module responsibility, technology, structure, dependency, and evidence block.
4. Prioritize risks by impact and likelihood; attach evidence and concrete mitigation.
5. Tailor detail to audience and depth without removing traceability.
6. When requested, create sanitized Mermaid source per [report-and-diagram-contract.md](references/report-and-diagram-contract.md).
7. Write `module-summary.md`, `risk-assessment.md`, optional diagrams, and `artifact-manifest.json`.
8. Validate every module is represented and every risk cites evidence.

Graph cross-check (T3 profile): validate recon-supplied dependency claims with `plan_dependency_order` and `compute_scc`, and entry-point claims with `list_up_entrypoint`; record any disagreement as a contradiction per [dev-shared/graph-function-selection.md](../dev-shared/graph-function-selection.md).

## Completion

Complete when: input coverage explicit, all modules represented, diagrams parse when requested, unsupported claims labeled as inference or gap.
