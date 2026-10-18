---
title: "Realign dev-kit documentation, invocation reference, and metadata"
description: "Fix documentation drift across README/devkit.md/wiki, add a Commands & Invocation reference covering all 35 skills, standardize skill frontmatter, and add drift-check tooling."
status: pending
priority: P2
effort: 10h
branch: main
tags: [docs, tech-debt, infra]
blockedBy: []
blocks: []
created: 2026-10-18
---

# Plan

## Overview
The kit ships 35 skills + 1 support package (`dev-shared`), but README claims "16 composable skills", omits 18 skills entirely, lists non-existent directories (`hi-explore/`, `cortex/`), and contains two duplicated document layers. `devkit.md` still documents only 3 core skills. Skill frontmatter has two competing version conventions, 19 skills lack `argument-hint`, and nothing validates docs against the real tree. Target state: docs match the tree, every skill is discoverable and invocable from README, metadata follows one convention, and `make check-docs` fails on future drift.

## Verified Findings (evidence)
- 36 dirs carry `SKILL.md` = 35 skills + `dev-shared` (`metadata.support: true`).
- README catalog covers 17 skills; missing 18: `hi-api-contract-discovery`, `hi-behavior-modeling`, `hi-command-spec-discovery`, `hi-cross-artifact-validation`, `hi-data-model-discovery`, `hi-docs-seeker`, `hi-document-lifecycle`, `hi-document-refinement`, `hi-document-review-resolution`, `hi-maintenance-docs`, `hi-module-summary-report`, `hi-repo-recon`, `hi-repowiki`, `hi-reverse`, `hi-tech-build-audit`, `hi-usecase-discovery`, `slide-kit`, `typesafe-ai`.
- README duplicates `Installation`, `Supported agents`, `Manifest files` (lines ~60-135 vs ~198-231), with contradictory content.
- `devkit.md` covers craft/fix/plan only; no discovery/document-lifecycle/recon/slide-kit nodes.
- 19 skills have no `argument-hint`; version exists as top-level `version:` in 5 skills and `metadata.version` in 9 skills; 21 skills have none.
- `hooks:` present in `hi-predict`, `hi-scenario`, `hi-security` but no harness or doc describes them.
- `wiki/{en,vi}` documents 17 skills each; 18 skills undocumented; `wiki/` itself is unmentioned in README.
- `docs/logs/` holds a single entry despite `hi-log` being a mandatory finalize step.
- Manifests `AGENTS.md`, `CLAUDE.md`, `.cursorrules` are near-duplicates; the installer only copies the first two, so `.cursorrules` drifts. `AGENTS.md` ends with "The agent always responds in English", which conflicts with the operator's Vietnamese preference.
- Internal link check: 4 broken references, all placeholder examples (`phase-01-setup.md`, `phase-01-name.md`, `jev-contract.md` from `dev-shared/jev/`, `system/system-overview.md`).

## Phases
| Phase | Name | Size | Status |
|-------|------|------|--------|
| 1 | [README restructure and catalog](./phase-01-readme-restructure.md) | M | Pending |
| 2 | [Commands & Invocation reference](./phase-02-commands-invocation.md) | S | Pending |
| 3 | [devkit.md workflow expansion](./phase-03-devkit-workflows.md) | M | Pending |
| 4 | [Frontmatter metadata standardization](./phase-04-frontmatter-metadata.md) | M | Pending |
| 5 | [Drift-check tooling, manifests, wiki](./phase-05-drift-check-manifests-wiki.md) | M | Pending |

## Target Catalog Taxonomy (6 groups, 35 skills)
| Group | Skills |
|-------|--------|
| Core Workflow (4) | hi-plan, hi-craft, hi-fix, hi-debug |
| Evidence & Exploration (5) | hi-repository-search, hi-codebase-research-explorer, hi-knows, hi-docs-seeker, hi-repo-recon |
| Discovery & Artifact (7) | hi-usecase-discovery, hi-behavior-modeling, hi-api-contract-discovery, hi-data-model-discovery, hi-command-spec-discovery, hi-reverse, hi-cross-artifact-validation |
| Documentation Lifecycle (6) | hi-maintenance-docs, hi-document-lifecycle, hi-document-refinement, hi-document-review-resolution, hi-repowiki, hi-module-summary-report |
| Analysis & Review (6) | hi-scenario, hi-brainstorm, hi-predict, hi-security, hi-sequential-thinking, hi-problem-solving |
| Utilities & Integrations (7) | hi-log, hi-project-organization, hi-tech-build-audit, hi-chrome-devtools, hi-cortex, slide-kit, typesafe-ai |
| Support (1) | dev-shared (support package, never activated directly) |

## Decisions Locked
- Catalog = 6 groups (user asked "e.g. add a command section"; group count derived from the tree, not from the old "16 skills" claim).
- "Command" covers both meanings: a README Commands & Invocation reference (Phase 2) and full catalog coverage of `hi-command-spec-discovery` (Phase 1 + 2).
- Docs stay English to match the repo; chat replies stay Vietnamese.
- `docs/plans/` is the plan home (no `docs/development-rules.md` exists in this repo).

## Open Questions
- Manifest consolidation: keep 3 files or generate `CLAUDE.md`/`.cursorrules` from `AGENTS.md`? Proposal in Phase 5; confirm before deleting anything.
- Wiki: regenerate all skill pages via `hi-repowiki`, or only add the 18 missing ones? Proposal in Phase 5.

## Success Criteria
- README count, catalog, and Folder Structure match the tree; zero duplicate sections.
- Every skill is discoverable in README and its invocation documented.
- One version convention across all skills; `argument-hint` present where modes exist.
- `make check-docs` exits 0 and fails on injected drift.
- No broken internal links.
