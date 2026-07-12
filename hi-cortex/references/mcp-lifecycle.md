# MCP Lifecycle

Use this to start, stop, and verify Cortex Harness MCP servers for other skills.

## Start

From `C:\ai\cortex-harness`:

```powershell
make start
```

The default Cortex Harness workflow starts the code and document MCP services in separate terminal sessions.

If the installed CLI exposes MCP commands, inspect them first:

```powershell
dev mcp --help
```

Then run the appropriate `dev mcp` command instead of guessing subcommands.

## Stop

```powershell
make stop
```

Stop database infrastructure only when the user is done with Cortex-backed skills:

```powershell
make infra-down
```

## Health Checks

```powershell
make doctor
dev status
```

Expected service checks usually include:

- Qdrant vector database.
- FalkorDB or Neo4j-compatible graph backend, depending on the active config.
- Code MCP service.
- Document MCP service.

## Handoff To Other Skills

After MCP servers are healthy:

1. Use `hi-repo-search --doc` for document evidence.
2. Use `hi-repo-search --code` for code evidence.
3. Use `hi-repo-search --deep` when docs and code must be reconciled.
4. Use `hi-repo-search --impact` before risky changes.

If a consuming skill reports connection errors, return here, run `make doctor`, and restart MCP servers once. If the same failure repeats, report the failing endpoint instead of retrying blindly.
