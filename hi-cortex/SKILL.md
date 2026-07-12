---
name: cortex
description: "Set up and operate Cortex Harness for project code/doc ingestion, config updates, sync workflows, and MCP server lifecycle."
argument-hint: "[setup|status|add-code|sync-code|add-doc|sync-doc|start-mcp|stop-mcp|doctor] [project path or repo URL]"
metadata:
  author: baka3k
  version: "1.0.0"
---

# Cortex Harness

Use this skill when a task needs Cortex Harness from `https://github.com/baka3k/cortex-harness`: environment installation, project config, source-code sync, documentation sync, and MCP server startup for use with other skills.

## Operating Rules

1. Gather project context first using the root search directive: `mind_mcp`, then `graph_mcp.semantic_search`, then Serena, then `rg`.
2. Prefer the installed `dev` command. If it is not on `PATH`, use the repository-local fallback at `C:\ai\cortex-harness\.venv\Scripts\dev.exe` when present.
3. Do not invent config paths, database names, or project folders. Run `dev status` or inspect the Cortex Harness config before changing it.
4. For interactive commands, explain what they will ask for and stay with the user until config, sync, and MCP status are verified.
5. Keep Cortex Harness as the retrieval and MCP infrastructure layer. Pair it with `hi-repo-search`, `hi-plan`, `hi-craft`, `hi-fix`, `hi-debug`, `hi-scenario`, or `hi-security` for the actual engineering workflow.

## Common Tasks

| Task | Use |
| --- | --- |
| Install or repair the local environment | [Environment Setup](./references/environment-setup.md) |
| Add source code to config and sync it | [Project Ingestion](./references/project-ingestion.md) |
| Add documentation to config and sync it | [Project Ingestion](./references/project-ingestion.md) |
| Start, stop, or validate MCP servers | [MCP Lifecycle](./references/mcp-lifecycle.md) |

## Default Workflow

1. Confirm Cortex Harness is installed and current.
2. Start database infrastructure if needed.
3. Run `dev status` to inspect active config.
4. Add code folders with `dev sync code add`, then run `dev sync code` or `dev sync code all`.
5. Add doc folders with `dev sync doc add`, then run `dev sync doc` or `dev sync doc all`.
6. Start MCP servers with `make start` from the Cortex Harness repo or `dev mcp` when the installed CLI exposes the MCP subcommands.
7. Run `make doctor` or the equivalent health check and report ports, services, and any failed checks.

## Verification

A Cortex Harness task is complete only when:

- `dev status` shows the intended config.
- Code sync and doc sync finish successfully or report only documented skips.
- Database services are reachable.
- MCP servers for code and docs are running on their configured ports.
- The next skill can use `mind_mcp` and/or `graph_mcp` without connection errors.
