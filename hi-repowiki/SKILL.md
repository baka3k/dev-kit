---
name: hi-repowiki
description: "Generate or update a comprehensive, evidence-backed repository wiki in Repo Wiki format (/repowiki/), including architecture, installation and configuration, CLI/build automation, languages and frameworks, data/graph schemas, protocol integrations such as MCP, query/search, incremental processing, APIs, testing, deployment, developer guidance, troubleshooting, module documentation, and knowledge cards. Use for codebase documentation, team onboarding, repository capability mapping, and persistent architecture knowledge."
---

# Repo Wiki Generator

Read [dev-shared/orchestrator-contract.md](../dev-shared/orchestrator-contract.md). Own the wiki run directory, page generation, knowledge card assembly, wiki_plan configuration, and incremental update logic.

## Inputs

Require `repo_root`, `project_id`. Accept: `output_root` (default `repowiki`), `language` (`en` default | `zh`), `mode` (`generate` | `update` | `plan-only`), `wiki_plan` (path or inline), `scope.include/exclude` (gitignore syntax), `template` (`architecture` default | `product_requirement`), `coverage_profile` (`comprehensive` default | `focused`), `topic_overrides.include/exclude` (facet IDs; exclusions stay visible in the ledger), `notes`, `--resume`.

## Stage Pipeline

| Order | Stage | Skill/Action | Depends On | Outputs |
|-------|-------|-------------|-----------|---------|
| 1 | recon | `hi-repo-recon` (deep) | inputs | module inventory, entry points |
| 2 | audit | `hi-tech-build-audit` (deep) | inputs | tech stack, build, CI/CD |
| 3 | facet scan | internal | recon + audit | capability signals, baseline topic coverage |
| 4 | domain evidence | applicable leaf skills | facet scan | API, data, use-case, behavior evidence |
| 5 | summary | `hi-module-summary-report` | recon + audit | per-module breakdown, risks |
| 6 | plan | internal | all evidence | coverage ledger, wiki tree, page list, module tree |
| 7 | pages | internal (parallel per section) | plan + evidence | content/*.md pages |
| 8 | cards | internal (parallel per module) | plan + evidence | knowledge/**/*.md cards |
| 9 | index | internal | pages + cards | navigation, metadata, manifests |

Read [dev-shared/retrieval-protocol.md](../dev-shared/retrieval-protocol.md) for evidence gathering.

## Workflow

Execute the five phases (evidence gathering → wiki planning → page generation → knowledge cards → index assembly & validation) exactly as specified in [workflow.md](references/workflow.md). Contracts: [topic-coverage-contract.md](references/topic-coverage-contract.md) (facet statuses; validate with `scripts/validate_topic_coverage.py`), [page-contract.md](references/page-contract.md), [knowledge-card-contract.md](references/knowledge-card-contract.md), [wiki-plan-template.yaml](references/wiki-plan-template.yaml).

Hard rules: corroborate facet applicability through registrations, imports, callers, configuration, or runtime wiring — never filenames alone; comprehensive mode retains tests/CI/deployment/contributor files unless the user excludes them; a strict `documents` allowlist generates only listed pages and marks other facets `excluded_by_plan`; never create a feature merely to fill the navigation tree — unsupported facets stay `unknown`/`not_applicable`.

## Failure Behavior

Missing/unreadable `repo_root` → `blocked`. Partial evidence → affected pages/cards `partial`. Page/card failure → skip and record in manifest. Index assembly failure → `failed` (navigation broken).

## Outputs

Tree per [workflow.md](references/workflow.md): `wiki_plan.yaml`, `topic-coverage.json`, `<lang>/content/` pages, `<lang>/meta/repowiki-metadata.json`, `knowledge/<lang>/` cards + `_index.yaml`, `artifact-manifest.json`.

## Completion

Complete only when: all planned pages and cards exist and parse, every evaluated facet has an evidence-backed status with a valid page mapping or explicit disposition, navigation is connected and acyclic, `_index.yaml` and `topic-coverage.json` validate, `<cite>` blocks reference real files, Mermaid parses, sensitive values redacted, manifest validates. Any `unknown`, `blocked`, failed artifact, or `planned` facet outside `plan-only` forces `partial` with an explicit list; `planned` in `plan-only`, `not_applicable`, and user-requested `excluded_by_plan` do not.
