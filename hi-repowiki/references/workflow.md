# Repo Wiki Workflow

Detailed phases for `hi-repowiki`. The SKILL.md owns ordering and gates; this file owns the steps.

## Phase 1: Evidence Gathering

1. Validate `repo_root`, create `output_root/<lang>/` structure.
2. Load `wiki_plan.yaml` if present; otherwise derive defaults from repo analysis.
3. Run `hi-repo-recon` (deep) and `hi-tech-build-audit` (deep); may run concurrently with isolated outputs. Direct graph calls in this skill stay limited to inventory reads, `query_subgraph` spot-checks, and `reconstruct_flow` on already-verified paths per `dev-shared/graph-function-selection.md` (T3 profile, mostly delegated to leaves in step 6).
4. Build a repository-wide capability signal inventory: executable and library entry points, manifests, configuration, environment files, command registrations and help text, build targets, languages, framework bootstraps, schema/migration/model declarations, graph drivers and writers, server/tool/resource registrations, query/search indexes, change detection and synchronization, routes/events, tests, CI/CD, deployment assets, contributor guidance, diagnostics, known error paths.
5. Evaluate every baseline facet in [topic-coverage-contract.md](topic-coverage-contract.md). Never decide applicability from filenames alone; corroborate through registrations, imports, callers, configuration loading, executable declarations, tests, or runtime wiring. In `comprehensive` mode retain tests, CI, deployment, example, and contributor files in evidence scope unless the user explicitly excludes them; record such exclusions as `excluded_by_plan` or `unknown`.
6. Run applicable evidence leaves into isolated stage directories:
   - `hi-api-contract-discovery` — verified HTTP, RPC-over-HTTP, webhook, or async message surfaces.
   - `hi-data-model-discovery` — verified persistent schemas, migrations, ORM/domain mappings, caches, graph storage models.
   - `hi-usecase-discovery` — key executable modules implementing user or operator outcomes.
   - `hi-behavior-modeling` — multi-step, asynchronous, stateful, retry, sync, or ingestion flows with stable anchors.
   - `hi-command-spec-discovery` — binary/wire commands only (APDU, TLV, opcodes); not a CLI analyzer. Derive CLI reference evidence from parser registrations, dispatch tables, help output, scripts, Makefiles, task runners, tests.
7. Collect validated leaf artifacts and direct evidence. Preserve unsupported facets as `unknown` or `not_applicable`; never create a feature merely to fill the navigation tree.
8. Run `hi-module-summary-report` with validated recon + audit artifacts; join its module/risk synthesis with domain evidence.

## Phase 2: Wiki Planning

9. Create `topic-coverage.json` per [topic-coverage-contract.md](topic-coverage-contract.md); validate with `scripts/validate_topic_coverage.py`. Every baseline facet gets exactly one status: `planned`, `documented`, `merged`, `not_applicable`, `unknown`, `blocked`, or `excluded_by_plan`, with evidence and a reason. `planned` only before generation or in `plan-only` mode.
10. Build the page tree from applicable facets, module inventory, and repository terminology: two- or three-level hierarchy comparable to a technical handbook; group related child topics without flattening everything into module pages.
11. If `wiki_plan.yaml` has a `documents` allowlist, generate strictly per that list and mark otherwise-applicable facets `excluded_by_plan`. Never claim comprehensive coverage for a strict allowlist.
12. For each planned page assign: stable facet IDs, title, goal, parent page, navigation order, evidence sources, required content blocks, diagram requirements. A page may satisfy multiple closely related facets, but the mapping must be explicit.
13. Build the knowledge card module tree from the module inventory: scope, file list, dependencies, relationships, sub-modules per module.
14. `mode=plan-only`: write `wiki_plan.yaml` and `topic-coverage.json` to `output_root/`, keep applicable page mappings `planned`, validate both, stop with `succeeded`/`partial` per unresolved coverage.

## Phase 3: Page Generation

15. Generate each section's pages per [page-contract.md](page-contract.md). Each page includes: `<cite>` block of source files, Table of Contents, introduction and scope, core content (architecture, components, data flow, patterns, extension points), Mermaid diagrams where evidence supports them (architecture `graph TD`, dependencies `graph LR`), dependency analysis and integration points, troubleshooting where applicable, evidence status per claim.
16. Apply topic-specific content requirements from [topic-coverage-contract.md](topic-coverage-contract.md). Prefer verified tables for commands, configuration keys, APIs, schemas, tools, tests, deployment targets; include defaults/constraints only when evidenced.
17. Parallelize page generation across independent sections; cap workers per orchestrator contract.
18. Write pages to `content/<Section Name>/<Page Title>.md`.

## Phase 4: Knowledge Card Generation

19. Per module, generate cards per [knowledge-card-contract.md](knowledge-card-contract.md): `_module.yaml` (scope, file list, dependencies, parent/child), `overview.md` (purpose, responsibilities, boundaries), `architecture_design.md` (internal structure, patterns, key abstractions), `coding_conventions.md` (naming, style, error handling, testing patterns observed), `tech_stack.md` (languages, frameworks, libraries, tools), `unique_setup_and_commands.md` (module-specific build/run/test when applicable).
20. Nest sub-module directories under their parent module.
21. Write cards to `knowledge/<lang>/<Module Name>/`.

## Phase 5: Index Assembly and Validation

22. Build `_index.yaml` master index from all generated knowledge cards: module names, directory paths, file scopes, parent-child relationships, dependency graph.
23. Build navigation from planned parent/order fields; verify every non-root page has one reachable parent and no cycles exist.
24. Build `repowiki-metadata.json`: generation timestamp, language, template, page count, card count, source revision, evidence coverage, per-facet status counts, coverage profile.
25. Write `Getting Started.md` and `Development & Contributing.md` as root-level content pages.
26. Convert satisfied `planned` facets to `documented`/`merged`, then validate: no `planned` facet remains in `generate`/`update` mode; all planned pages and cards exist; every `documented`/`merged` facet maps to an existing page; every other facet has a reason; `_index.yaml` and `topic-coverage.json` parse; no orphaned references; Mermaid blocks parse; `<cite>` blocks reference real files; sensitive values redacted.
27. Persist `artifact-manifest.json` and final status.

## Incremental Update (`mode=update`)

1. Load existing `repowiki-metadata.json` and `_index.yaml`.
2. Detect changed files since `source_revision`: `git diff --name-only <source_revision>..HEAD`.
3. Identify affected pages (via `<cite>` source lists) and knowledge cards (via `_module.yaml` file scopes).
4. Re-run the capability signal scan for changed manifests, registrations, schemas, routes, command definitions, configuration, tests, deployment files, or documentation. Detect newly applicable or removed facets even when no existing page cites the changed file.
5. Re-run evidence gathering only for affected modules and facets.
6. Regenerate affected pages/cards, add pages for newly applicable facets, retire removed topics only after recording the transition in `topic-coverage.json`. Preserve manually-edited content flagged by the user.
7. Rebuild navigation, `_index.yaml`, `topic-coverage.json`, `repowiki-metadata.json`.
8. Keep unchanged pages/cards with their original hashes.

## wiki_plan.yaml Configuration

Accept configuration per [wiki-plan-template.yaml](wiki-plan-template.yaml):

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

Non-empty `documents` = strict generation. Empty = derive pages from evidence. `comprehensive` evaluates the full baseline taxonomy even when facets are not applicable; `focused` limits evaluation to included facets and planned documents.

## Outputs Tree

```
<output_root>/
├── wiki_plan.yaml                          # generated or copied config
├── topic-coverage.json                     # baseline facet status and page mapping
├── <lang>/
│   ├── content/
│   │   ├── Getting Started.md
│   │   ├── Development & Contributing.md
│   │   └── <Section>/<Page Title>.md
│   └── meta/repowiki-metadata.json
├── knowledge/<lang>/
│   ├── _index.yaml
│   └── <Module Name>/
│       ├── _module.yaml
│       ├── overview.md
│       ├── architecture_design.md
│       ├── coding_conventions.md
│       ├── tech_stack.md
│       └── unique_setup_and_commands.md
└── artifact-manifest.json
```
