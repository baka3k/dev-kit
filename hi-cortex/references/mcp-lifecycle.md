# MCP Lifecycle

Use this to start, stop, and verify Cortex Harness MCP servers for other skills.

## Start

From the Cortex Harness checkout (resolve the location from the `dev` wrapper's
`CORTEX_HARNESS_DIR` if unsure — see [Install](./install.md); never invent a path):

```bash
make start
```

The default Cortex Harness workflow starts the code and document MCP services in separate terminal sessions.

If the installed CLI exposes MCP commands, inspect them first:

```bash
dev mcp --help
```

Then run the appropriate `dev mcp` command instead of guessing subcommands.

Named instances are for hard isolation only (they double resident embedding-model memory):

```bash
dev start --name <app>-legacy --project <app>-legacy --port 8790
```

## Stop

```bash
make stop
```

When stopping a named instance, always scope it — bare `dev stop` stops every MCP on the machine:

```bash
dev stop --name <instance>
```

Stop database infrastructure only when the user is done with Cortex-backed skills:

```bash
make infra-down
```

## Health Checks

```bash
make doctor
dev status
```

`dev doctor` runs the same class of checks (embedded Qdrant/FalkorDBLite round-trips plus MCP port
diagnostics) when run outside the checkout.

Expected service checks usually include:

- Qdrant vector database.
- FalkorDB or Neo4j-compatible graph backend, depending on the active config.
- Code MCP service.
- Document MCP service.

## Handoff To Other Skills

After MCP servers are healthy:

1. Use `hi-repository-search --doc` for document evidence.
2. Use `hi-repository-search --code` for code evidence.
3. Use `hi-repository-search --deep` when docs and code must be reconciled.
4. Use `hi-repository-search --impact` before risky changes.

If a consuming skill reports connection errors, return here, run `make doctor`, and restart MCP servers once. If the same failure repeats, report the failing endpoint instead of retrying blindly.
