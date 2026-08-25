---
name: hi-repowiki
description: "Generate or update a comprehensive, evidence-backed repository wiki in Repo Wiki format (/repowiki/), including architecture, installation and configuration, CLI/build automation, languages and frameworks, data/graph schemas, protocol integrations such as MCP, query/search, incremental processing, APIs, testing, deployment, developer guidance, troubleshooting, module documentation, and knowledge cards. Use for codebase documentation, team onboarding, repository capability mapping, and persistent architecture knowledge."
---

# Repo Wiki Generator

Read [dev-shared/orchestrator-contract.md](../dev-shared/orchestrator-contract.md). Own the wiki run directory, page generation, knowledge card assembly, wiki_plan configuration, and incremental update logic.

## Inputs

Require `repo_root` and `project_id`. Accept:

- `output_root`: default `repowiki` or custom path.
- `language`: `en` (default) or `zh`. Creates language-specific subdirectory.
- `mode`: `generate` (full), `update` (incremental), or `plan-only` (emit wiki_plan.yaml without generating content).
- `wiki_plan`: path to existing `wiki_plan.yaml`, or inline configuration.
- `scope.include` / `scope.exclude`: file filters in `.gitignore` syntax.
- `template`: `architecture` (default) or `product_requirement`.
- `coverage_profile`: `comprehensive` (default) or `focused`. Comprehensive evaluates every baseline topic facet; focused evaluates only explicitly included facets and planned documents.
- `topic_overrides.include` / `topic_overrides.exclude`: baseline facet IDs to force into or remove from planning. Exclusions always remain visible in the coverage ledger.
- `notes`: list of guidance prompts to steer generation focus.
- `--resume`: continue interrupted generation.

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

### Phase 1: Evidence Gathering

1. Validate `repo_root`, create `output_root/<lang>/` structure.
2. Load `wiki_plan.yaml` if present; otherwise derive defaults from repo analysis.
3. Run `hi-repo-recon` with `deep` depth and `hi-tech-build-audit` with `deep` depth. May run concurrently with isolated outputs.
4. Build a repository-wide capability signal inventory. Inspect executable and library entry points, manifests, configuration, environment files, command registrations and help text, build targets, languages, framework bootstraps, schema/migration/model declarations, graph drivers and writers, server/tool/resource registrations, query/search indexes, change detection and synchronization, routes/events, tests, CI/CD, deployment assets, contributor guidance, diagnostics, and known error paths.
5. Evaluate every baseline facet in [topic-coverage-contract.md](references/topic-coverage-contract.md). Do not decide applicability from filenames alone; corroborate signals through registrations, imports, callers, configuration loading, executable declarations, tests, or runtime wiring.
   - In `comprehensive` mode, retain tests, CI, deployment, example, and contributor files in evidence scope unless the user explicitly excludes them. Record any user exclusion that prevents a facet decision as `excluded_by_plan` or `unknown`, as appropriate.
6. Run applicable evidence leaves into isolated stage directories:
   - Run `hi-api-contract-discovery` for verified HTTP, RPC-over-HTTP, webhook, or asynchronous message surfaces.
   - Run `hi-data-model-discovery` for verified persistent schemas, migrations, ORM/domain mappings, caches, or graph storage models.
   - Run `hi-usecase-discovery` for the key executable modules that implement user or operator outcomes.
   - Run `hi-behavior-modeling` for multi-step, asynchronous, stateful, retry, sync, or ingestion flows with stable anchors.
   - Use `hi-command-spec-discovery` only for binary/wire commands such as APDU, TLV, or opcodes; it is not a CLI analyzer. Derive CLI reference evidence directly from parser registrations, dispatch tables, help output definitions, scripts, Makefiles, task runners, and tests.
7. Collect validated leaf artifacts and direct evidence. Preserve unsupported facets as `unknown` or `not_applicable`; never create a feature merely to fill the navigation tree.
8. Run `hi-module-summary-report` with validated recon + audit artifacts and join its module/risk synthesis with the domain evidence.

### Phase 2: Wiki Planning

9. Create `topic-coverage.json` using [topic-coverage-contract.md](references/topic-coverage-contract.md) and validate it with `scripts/validate_topic_coverage.py`. Give every baseline facet exactly one status: `planned`, `documented`, `merged`, `not_applicable`, `unknown`, `blocked`, or `excluded_by_plan`, with evidence and a reason. Use `planned` only before page generation or in `plan-only` mode.
10. Build the page tree from applicable facets, module inventory, and repository terminology. Use a two- or three-level hierarchy comparable to a technical handbook; group related child topics without flattening everything into module pages.
11. If `wiki_plan.yaml` has a `documents` allowlist, generate strictly per that list and mark otherwise applicable facets `excluded_by_plan`. Never silently claim comprehensive coverage for a strict allowlist.
12. For each planned page, assign: stable facet IDs, title, goal, parent page, navigation order, evidence sources, required content blocks, and diagram requirements. A page may satisfy multiple closely related facets, but the mapping must be explicit.
13. Build the knowledge card module tree from the module inventory. Each module gets: scope, file list, dependencies, relationships, and sub-modules.
14. If `mode=plan-only`, write `wiki_plan.yaml` and `topic-coverage.json` to `output_root/`, keep applicable page mappings at `planned`, validate both, and stop with `succeeded` or `partial` according to unresolved coverage.

### Phase 3: Page Generation

15. For each section in the page tree, generate wiki pages following [page-contract.md](references/page-contract.md). Each page includes:
    - `<cite>` block listing source files referenced.
    - Table of Contents.
    - Introduction and scope.
    - Core content (architecture, components, data flow, patterns, extension points).
    - Mermaid diagrams where evidence supports them (architecture: `graph TD`, dependencies: `graph LR`).
    - Dependency analysis and integration points.
    - Troubleshooting guide where applicable.
    - Evidence status per claim.
16. Apply the topic-specific content requirements from [topic-coverage-contract.md](references/topic-coverage-contract.md). Prefer verified tables for commands, configuration keys, APIs, schemas, tools, tests, and deployment targets; include defaults and constraints only when evidenced.
17. Parallelize page generation across independent sections. Cap workers per orchestrator contract.
18. Write pages to `content/<Section Name>/<Page Title>.md`.

### Phase 4: Knowledge Card Generation

19. For each module in the module tree, generate knowledge cards following [knowledge-card-contract.md](references/knowledge-card-contract.md):
    - `_module.yaml`: scope, file list, dependencies, parent/child relationships.
    - `overview.md`: purpose, responsibilities, boundaries.
    - `architecture_design.md`: internal structure, patterns, key abstractions.
    - `coding_conventions.md`: naming, style, error handling, testing patterns observed.
    - `tech_stack.md`: languages, frameworks, libraries, tools used by this module.
    - `unique_setup_and_commands.md`: module-specific build/run/test commands when applicable.
20. Nest sub-module directories under their parent module.
21. Write cards to `knowledge/<lang>/<Module Name>/`.

### Phase 5: Index Assembly and Validation

22. Build `_index.yaml` master index from all generated knowledge cards: module names, directory paths, file scopes, parent-child relationships, dependency graph.
23. Build navigation from the planned parent/order fields; verify every non-root page has one reachable parent and no cycles exist.
24. Build `repowiki-metadata.json` with generation timestamp, language, template, page count, card count, source revision, evidence coverage, per-facet status counts, and coverage profile.
25. Write `Getting Started.md` and `Development & Contributing.md` as root-level content pages.
26. Convert satisfied `planned` facets to `documented` or `merged`, then validate: no `planned` facet remains in `generate` or `update` mode; all planned pages and cards exist; every `documented` or `merged` facet maps to an existing page; every other facet has a reason; `_index.yaml` and `topic-coverage.json` parse; no orphaned references; Mermaid blocks parse; `<cite>` blocks reference real files; sensitive values are redacted.
27. Persist `artifact-manifest.json` and final status.

## Incremental Update (`mode=update`)

1. Load existing `repowiki-metadata.json` and `_index.yaml`.
2. Detect changed files since `source_revision` using `git diff --name-only <source_revision>..HEAD`.
3. Identify affected pages (via `<cite>` source lists) and affected knowledge cards (via `_module.yaml` file scopes).
4. Re-run the capability signal scan for changed manifests, registrations, schemas, routes, command definitions, configuration, tests, deployment files, or documentation. Detect newly applicable or removed facets even when no existing page cites the changed file.
5. Re-run evidence gathering only for affected modules and facets.
6. Regenerate affected pages and cards, add pages for newly applicable facets, and retire removed topics only after recording the transition in `topic-coverage.json`. Preserve manually-edited content flagged by the user.
7. Rebuild navigation, `_index.yaml`, `topic-coverage.json`, and `repowiki-metadata.json`.
8. Keep unchanged pages/cards with their original hashes.

## Configuration: wiki_plan.yaml

Accept configuration per [wiki-plan-template.yaml](references/wiki-plan-template.yaml):

```yaml
version: 1
repowiki:
  template: architecture | product_requirement
  coverage:
    profile: comprehensive | focused
    include: ["<facet-id>"]
    exclude: ["<facet-id>"]
    max_depth: 3
  notes:
    - text: "<guidance prompt>"
      author: "<name>"
  documents:           # optional page allowlist (strict mode)
    - title: "<page title>"
      goal: "<generation goal>"
      parent: "<parent page title>"
      hints: "<additional hints>"
knowledgecard:
  notes:
    - text: "<guidance for card generation>"
scope:
  include: ["<glob>"]
  exclude: ["<glob>"]
```

When `documents` is non-empty, page generation is strict: only listed pages are produced. When empty, pages are derived automatically from evidence. `coverage.profile=comprehensive` evaluates the complete baseline taxonomy even if some facets are not applicable; `focused` limits evaluation to included facets and planned documents.

## Failure Behavior

- Missing `repo_root` or unreadable repository: `blocked`.
- Evidence gathering partial: continue with available evidence, mark affected pages/cards as `partial`.
- Page generation failure: skip affected page, continue with remaining pages.
- Knowledge card failure: skip affected card, record in manifest.
- Index assembly failure: `failed` — pages/cards may exist but navigation is broken.

## Outputs

```
<output_root>/
├── wiki_plan.yaml                          # generated or copied config
├── topic-coverage.json                     # baseline facet status and page mapping
├── <lang>/
│   ├── content/
│   │   ├── Getting Started.md
│   │   ├── Development & Contributing.md
│   │   ├── <Section>/
│   │   │   ├── <Section>.md                # section overview
│   │   │   └── <Page Title>.md             # individual pages
│   │   └── ...
│   └── meta/
│       └── repowiki-metadata.json
├── knowledge/
│   └── <lang>/
│       ├── _index.yaml
│       └── <Module Name>/
│           ├── _module.yaml
│           ├── overview.md
│           ├── architecture_design.md
│           ├── coding_conventions.md
│           ├── tech_stack.md
│           └── unique_setup_and_commands.md
└── artifact-manifest.json
```

## Completion

Complete when: all planned pages exist and parse, all planned knowledge cards exist, every evaluated topic facet has an evidence-backed status and page mapping or explicit disposition, navigation is connected and acyclic, `_index.yaml` validates, `<cite>` blocks reference real source files, Mermaid diagrams parse, sensitive values are redacted, metadata reflects actual generation state, and `artifact-manifest.json` validates. Any `unknown`, `blocked`, missing/failed page, missing/failed card, or `planned` facet outside `plan-only` mode forces `partial` with an explicit list; `planned` in `plan-only`, `not_applicable`, and user-requested `excluded_by_plan` do not by themselves force partial.
