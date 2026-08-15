# Topic Coverage Contract

Use this contract to turn repository evidence into a comprehensive, navigable wiki rather than a module-only inventory.

## Coverage Ledger

Write `topic-coverage.json`, validate it against [topic-coverage.schema.json](topic-coverage.schema.json), and use this shape:

```json
{
  "schema_version": "1.0",
  "mode": "generate",
  "profile": "comprehensive",
  "source_revision": "<revision>",
  "facets": [
    {
      "id": "installation.database",
      "status": "documented",
      "reason": "Database configuration is loaded at runtime.",
      "evidence": ["path/to/config-loader.ts", "path/to/schema.sql"],
      "checks": [],
      "pages": ["en/content/Installation & Configuration/Database Configuration.md"],
      "merged_into": null
    }
  ]
}
```

Use exactly one status per evaluated facet:

- `planned`: the facet is applicable and mapped to a future page, but the page has not been generated. Use only during planning or in `plan-only` mode.
- `documented`: one or more dedicated pages satisfy the facet.
- `merged`: a broader page satisfies the facet; set `merged_into` and `pages`.
- `not_applicable`: sufficient evidence shows the repository does not implement or own the concern.
- `unknown`: available evidence cannot determine applicability or behavior.
- `blocked`: required evidence or retrieval failed.
- `excluded_by_plan`: the user or strict document allowlist omitted an otherwise applicable facet.

Require a non-empty reason for every status. Require repository-relative evidence for `planned`, `documented`, and `merged`. Use `checks` to record inventories, expected locations, retrieval queries/layers, and gaps used to decide `not_applicable`, `unknown`, or `blocked`; require at least one check for those statuses. Treat page paths as output-root-relative. Never use an empty page to convert `unknown` into `documented`.

## Baseline Facets

Evaluate all facets for the `comprehensive` profile. Use repository-specific titles, split large facets, and merge small related facets while preserving IDs in the ledger.

### Core Concepts & Architecture

- `core.overview`: purpose, users, boundaries, principal capabilities, and vocabulary.
- `core.architecture`: deployable units, modules, dependency direction, runtime topology, and primary data/control flows.
- `core.extension_points`: plugins, adapters, providers, hooks, registries, or other supported customization mechanisms.

### Installation & Configuration

- `installation.prerequisites`: runtimes, package managers, external services, and supported versions.
- `installation.platforms`: OS-, architecture-, container-, or cloud-specific setup differences.
- `installation.database`: database or graph-store setup, migrations, connection-key names, and initialization flow; redact values.
- `installation.environment`: configuration files, environment variable names, precedence, defaults, validation, reload behavior, and examples with safe placeholders.
- `installation.security_production`: authentication bootstrap, secret handling, TLS/network assumptions, hardening, and production configuration.

### Command Line Interface & Automation

- `cli.commands`: executable names, command/subcommand tree, arguments, flags, defaults, examples, exit behavior, and registration/handler mapping.
- `cli.build_automation`: Makefile/task-runner targets, package scripts, generators, lint/test/build/package commands, prerequisites, and artifacts.
- `cli.context_projects`: profiles, workspaces, repositories, tenants, projects, contexts, or multi-project selection.
- `cli.scripting`: non-interactive use, stdin/stdout formats, shell integration, batch workflows, and automation-safe error handling.

### Language Support & Analyzers

- `languages.supported`: detected and explicitly supported languages, parser/analyzer selection, file extensions, limitations, and version constraints.
- `languages.legacy`: legacy languages, compatibility layers, fallbacks, and unsupported constructs.
- `languages.scripting_web`: scripting, template, markup, and web languages with their analysis depth.
- `languages.custom_analyzers`: analyzer interfaces, registration, lifecycle, contracts, examples, and tests for extension authors.

### Framework Analysis & Overlays

- `frameworks.detected`: each evidenced framework and how it is detected, bootstrapped, modeled, or overlaid.
- `frameworks.generic`: generic fallback behavior when a framework-specific adapter is absent.
- `frameworks.custom_overlays`: rules for adding framework adapters, overlays, mappings, or conventions.

Create framework-specific child pages when a framework has distinct registration, lifecycle, data, routing, or build behavior. Do not create pages for popular frameworks that the repository does not support.

### Data, Graph Operations & Schema

- `data.schema`: physical/logical models, entities or node/edge types, keys, indexes, constraints, ownership, and migrations.
- `data.drivers`: database/graph drivers, connection lifecycle, pooling, transactions, retry, and supported backends.
- `data.operations_api`: read/write/traversal/query operations and their public or internal contracts.
- `data.ingestion`: writers, importers, parsing/normalization, batching, idempotency, validation, failure handling, and terminal storage effects.

Use graph-specific page titles only when graph concepts are evidenced; otherwise use repository terminology such as Data Model, Persistence, or Storage.

### Protocol & Model Context Protocol Integration

- `protocol.server_architecture`: protocol server entry points, transports, sessions, lifecycle, routing, and dependencies.
- `protocol.capabilities`: registered tools, resources, prompts, methods, schemas, handlers, terminal effects, and capability negotiation.
- `protocol.clients_sdk`: client setup, SDK use, transport configuration, compatibility, retries, and integration examples.
- `protocol.security`: authentication, authorization, scope, secret handling, transport security, validation, rate limits, and trust boundaries.

When MCP is evidenced, title this section `Model Context Protocol Integration` and explicitly inventory MCP tools, resources, prompts, transports, schemas, and client configuration. For other protocols, retain the facet IDs but use the protocol's real name. Do not infer MCP from a generic server or a dependency name alone; verify registrations and handlers.

### Query Interface & Search

- `query.interfaces`: user/programmatic query entry points, syntax, parameters, result shapes, pagination, errors, and handler mapping.
- `query.search`: indexes, tokenization/embedding, filters, ranking, traversal, caching, limits, and fallback behavior.

### Incremental Analysis & Sync

- `incremental.change_detection`: revision tracking, file watching, hashing, invalidation, dependency impact, and deletion/rename handling.
- `incremental.sync`: synchronization direction, checkpoints, resumability, conflict resolution, idempotency, retries, and consistency guarantees.

### API Reference

- `api.http_events`: verified HTTP endpoints, webhooks, events, or message channels with schemas, auth, errors, consumers/providers, and terminal effects.
- `api.internal_extensions`: stable public library interfaces, plugin contracts, SDK surfaces, or extension APIs.

Separate API reference pages by protocol or bounded surface when this improves navigation. A symbol list without contracts and evidence does not satisfy this facet.

### Testing & Validation

- `testing.strategy`: test levels, directory layout, fixtures, mocks, coverage configuration, and ownership.
- `testing.commands`: verified commands, prerequisites, selectors, expected outputs/artifacts, and CI mapping.
- `testing.validation`: schema validators, linters, formatters, static analysis, quality gates, and failure diagnostics.

### Deployment & Operations

- `operations.deployment`: packaging, containers, services, environments, infrastructure definitions, promotion, rollback, and health checks.
- `operations.observability`: logs, metrics, traces, diagnostics, alerting, audit records, and operator entry points.
- `operations.scaling_recovery`: concurrency, capacity, persistence/backup, failure recovery, retry, and disaster assumptions.

### Developer Guide

- `developer.workflow`: local setup, build/test loop, repository layout, branching/contribution evidence, code generation, and common change paths.
- `developer.extension`: how to add a module, command, analyzer, framework adapter, protocol capability, API, schema migration, or test where applicable.

### Troubleshooting & FAQ

- `troubleshooting.failures`: evidenced failure modes, symptoms, causes, diagnostics, and safe resolutions.
- `troubleshooting.faq`: recurring ambiguities or operational questions supported by code, tests, issue templates, or existing docs.

Do not invent frequently asked questions. Prefer a troubleshooting matrix keyed by emitted errors, validation messages, health checks, and known failure branches.

## Applicability and Evidence Rules

1. Start with broad file and symbol inventories, then verify candidate signals through runtime wiring or authoritative configuration.
2. Treat README claims and comments as candidates until code/config/tests corroborate them. Keep contradictions visible.
3. Use absence claims only after checking expected source, configuration, tests, and build/deployment locations, and record those checks in the ledger. Otherwise use `unknown`, not `not_applicable`.
4. Map every generated page to at least one facet and every `documented` or `merged` facet to at least one page.
5. Keep navigation depth at three levels by default. Split oversized pages by user task or bounded technical surface, not by arbitrary file count.
6. Prefer repository vocabulary. The baseline labels are coverage prompts, not mandatory literal titles.
7. Redact secret values, credentials, connection strings, private endpoints, personal data, and production identifiers while retaining safe key names and structural evidence.

## Page Planning Quality Gate

Before generating pages, verify:

- Every baseline facet required by the selected profile appears once in the ledger.
- Applicable CLI/API/protocol items trace registrations to handlers and observable effects.
- Configuration items trace declaration to loading, precedence, validation, and consumers where available.
- Data/graph items distinguish declared schema from inferred relationships.
- Incremental/sync items cover create, update, delete, rename, retry, resume, and conflict behavior when evidenced.
- Testing and deployment claims distinguish verified commands from conventional guesses.
- Unknown, blocked, excluded, and contradictory areas remain visible in the final metadata and gaps summary.
