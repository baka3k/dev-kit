# Project Ingestion

Use this for adding source code or documentation to Cortex Harness config and syncing it into the graph/vector stores.

## Preflight

1. Confirm the target project path or repository URL.
2. Inspect current config:

```powershell
dev status
```

3. If no config exists, initialize it:

```powershell
dev init --project-dir <project-path>
```

Use `dev init --env prod` only when the user explicitly wants the `prod` environment.

## Add And Sync Code

Add a code project or folder:

```powershell
dev sync code add
```

Then sync:

```powershell
dev sync code
```

For all configured code folders:

```powershell
dev sync code all
```

Notes:

- The first code sync is a full sync because no baseline exists.
- Later syncs are incremental when Cortex Harness has a baseline.
- Let Cortex Harness auto-detect language analyzers unless the user has a specific parser requirement.

## Add And Sync Docs

Add a documentation project or folder:

```powershell
dev sync doc add
```

Then sync:

```powershell
dev sync doc
```

For all configured documentation folders:

```powershell
dev sync doc all
```

Supported document inputs include Markdown, text, PDF, Word, PowerPoint, and Excel files when the corresponding dependencies are installed.

## Verification

After sync:

```powershell
dev status
make doctor
```

Then verify with the consuming tools:

- `mind_mcp` for project documents and concepts.
- `graph_mcp.semantic_search` for code and relationship retrieval.

If either tool is disconnected, report the failed service or port and use the root fast-fail search fallback.
