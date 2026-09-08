---
name: hi-cortex
description: "Set up and operate Cortex Harness for project code/doc ingestion, config updates, sync workflows, and MCP server lifecycle."
argument-hint: "[setup|status|add-code|sync-code|add-doc|sync-doc|start-mcp|stop-mcp|doctor] [project path or repo URL]"
metadata:
  author: baka3k
  version: "1.1.0"
---

# Cortex Harness

Use this skill when a task needs Cortex Harness from `https://github.com/baka3k/cortex-harness`: environment installation, project config, source-code sync, documentation sync, and MCP server startup for use with other skills.

## Operating Rules

1. Gather project context first using the root search directive: `mind_mcp`, then `graph_mcp` (`semantic_search`, `explore_graph` — resolve the live catalog with `list_mcp_functions` first), then Serena, then `rg`.
2. Prefer the installed `dev` command. Preflight first: `command -v dev || [ -x "$HOME/.local/bin/dev" ]`. If both miss, follow [Install](./references/install.md); if `dev` exists but errors, run `dev doctor` first — never reinstall over a working installation. The wrapper at `~/.local/bin/dev` may pin its own checkout (`CORTEX_HARNESS_DIR`) — read it before assuming the repository location.
3. Do not invent config paths, database names, checkout locations, or project folders. Run `dev status` or inspect the Cortex Harness config before changing it.
4. Prefer fully flagged, non-interactive commands. Wizard prompts (`dev init`, `dev sync code add` without arguments, bare `dev sync code`) may only be answered with user-provided values — an agent never guesses wizard answers.
5. Keep Cortex Harness as the retrieval and MCP infrastructure layer. Pair it with `hi-repository-search`, `hi-plan`, `hi-craft`, `hi-fix`, `hi-debug`, `hi-scenario`, or `hi-security` for the actual engineering workflow.

## `dev` Command Surface

| Command | Purpose |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `dev status` | Show resolved config: graph path, Qdrant directory, vector collection, embedding model, registered source/doc folders. Run before and after every change. |
| `dev doctor` | Health check: embedded Qdrant/FalkorDBLite round-trips plus MCP port diagnostics. |
| `dev init --project-dir <project-root>` | One-time interactive config wizard per project root. Enter accepts defaults (project id, `local` backend, falkordb provider). Choose `remote` only on explicit user instruction. |
| `dev sync code add <root> [--git <url>]` | Register a code root — once per root. The flagged form is non-interactive. |
| `dev sync code --sync-mode both` | Incremental code ingest (graph + embeddings; first run is a full scan). `--full-scan --sync-mode graph` or `embedding` refreshes one phase only and does not move the incremental baseline. |
| `dev sync doc add <root>` then `dev sync doc` | Register and sync knowledge-base documents (`.md` `.txt` `.pdf` `.docx` `.pptx` `.xlsx`). `all` variants cover every registered folder. |
| `dev mcp` / `make start` | Start MCP servers. Inspect `dev mcp --help` first; never guess subcommands. |
| `dev start --name <instance> ...` / `dev stop --name <instance>` | Named instances for hard isolation only. Never run bare `dev stop` — it stops every MCP on the machine. |

Hygiene: `.cortext-harness/config/{env}.json` stores settings — and remote credentials — in plaintext: never commit populated configs or echo their contents. `CORTEX_DATA_HOME` / `CORTEX_STORAGE_INSTANCE` give an isolated data root for tests.

## Common Tasks

| Task                                       | Use                                                     |
| ------------------------------------------ | ------------------------------------------------------- |
| Install the environment / `dev` command    | [Install](./references/install.md)                      |
| Add source code to config and sync it      | [Project Ingestion](./references/project-ingestion.md)  |
| Add documentation to config and sync it    | [Project Ingestion](./references/project-ingestion.md)  |
| Legacy/modern lane split for dual codebases | [Sync Recipes](./references/sync-recipes.md)           |
| Start, stop, or validate MCP servers       | [MCP Lifecycle](./references/mcp-lifecycle.md)          |

## Default Workflow

1. Preflight `dev`; install only if missing ([Install](./references/install.md)).
2. Run `dev status` to inspect the active config; `dev init --project-dir <root>` if none exists.
3. Add code folders with `dev sync code add <root>`, then `dev sync code --sync-mode both` (or `dev sync code all`).
4. Add doc folders with `dev sync doc add <root>`, then `dev sync doc` (or `dev sync doc all`).
5. Start MCP servers with `make start` from the Cortex Harness checkout, or the appropriate `dev mcp` subcommand after checking `--help`.
6. Run `dev doctor` or `make doctor`; report ports, services, and any failed checks.
7. Verify retrieval end to end: `graph_mcp` queries must return known symbols from the intended project (pass `project_id` and the matching `parser_type`); documents via `mind_mcp`.

Multi-language codebases (e.g. C/Pro*C legacy beside Java/MyBatis/Spring modern) must use separate lane projects, graphs, and collections — read [Sync Recipes](./references/sync-recipes.md) before running any sync for them.

## Verification

A Cortex Harness task is complete only when:

- `dev status` shows the intended config and the sync journal is healthy (`journal: ... pending=0 blocked=0`).
- Code sync and doc sync finish successfully or report only documented skips.
- Database services are reachable (`dev doctor` / `make doctor` passes).
- MCP servers for code and docs are running on their configured ports.
- The next skill can use `mind_mcp` and/or `graph_mcp` without connection errors.
