# Project Ingestion

Use this for adding source code or documentation to Cortex Harness config and syncing it into the graph/vector stores.

## Preflight

1. Confirm the target project path or repository URL.
2. Inspect current config:

```bash
dev status
```

3. If no config exists, initialize it:

```bash
dev init --project-dir <project-path>
```

`dev init` is an interactive wizard — answer prompts only with user-provided values; Enter accepts
defaults (project id, `local` backend, falkordb provider). An agent must never guess wizard answers.
Use `dev init --env prod` only when the user explicitly wants the `prod` environment.

## Add And Sync Code

Register a code project or folder — once per root; the flagged form is non-interactive:

```bash
dev sync code add <project-path-or-repo-url> [--git <url>]
```

Then sync:

```bash
dev sync code --sync-mode both
```

For all configured code folders:

```bash
dev sync code all
```

Notes:

- The first code sync is a full sync because no baseline exists.
- Later syncs are incremental when Cortex Harness has a baseline.
- Single-phase refresh: `dev sync code --full-scan --sync-mode graph` (call graph only) or
  `--sync-mode embedding` (embeddings only) — required with `--full-scan`, and these modes do not
  move the shared incremental baseline; return to `--sync-mode both` afterwards.
- Let Cortex Harness auto-detect language analyzers unless the user has a specific parser requirement.
- Multi-language codebases (legacy C/Pro*C beside modern Java/Spring) need separate lane projects —
  read [Sync Recipes](./sync-recipes.md) before syncing.

## Add And Sync Docs

Register a documentation project or folder:

```bash
dev sync doc add <project-path-or-repo-url>
```

Then sync:

```bash
dev sync doc
```

For all configured documentation folders:

```bash
dev sync doc all
```

Supported document inputs include Markdown, text, PDF, Word, PowerPoint, and Excel files when the corresponding dependencies are installed.

## Verification

After sync:

```bash
dev status
dev doctor   # or make doctor from the Cortex Harness checkout
```

`dev status` plus the sync summary's phase results and journal state (`journal: ... pending=0
blocked=0` is healthy). Degraded or failed phases are reported to the user, never hidden.

Then verify with the consuming tools:

- `mind_mcp` for project documents and concepts.
- `graph_mcp.semantic_search`, `graph_mcp.explore_graph` for code and relationship retrieval —
  pass the lane's `project_id` and `parser_type`, and confirm a known symbol resolves.

If either tool is disconnected, report the failed service or port and use the root fast-fail search fallback.
