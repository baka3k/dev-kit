# Delegation Contract (Harness-Agnostic)

DevKit runs on multiple harnesses (Claude Code, ZCode, Zed, VS Code Copilot, ...) whose delegation primitives differ and change between versions. Skills therefore never hardcode a spawn tool name or a proprietary agent type. Every worker launch follows this contract.

## Two Verbs

- **Invoke** a skill: load its instructions into the current context. Sequential, cheap. The default.
- **Delegate** a role: run work in a separate context through the harness's delegation primitive. Costs ~10-15K tokens per unit; the only way to get true parallelism.

"Spawn a skill" is not a thing. Skills are invoked; roles are delegated.

## 1. Capability Probe (once per workflow)

Before the first delegation, probe the runtime once and cache the result for the session:

| Priority | Probe | Mode |
|----------|-------|------|
| 1 | A native subagent/delegation tool exists that accepts a generic agent type (e.g. a `Task`/`Agent` tool with a `general-purpose` type) | `spawn` |
| 2 | Only an MCP server exposing a delegation/agent tool | `spawn-mcp` |
| 3 | Neither | `inline` |

Probe the task primitive in the same pass: `TaskCreate`/`TaskUpdate` -> `TodoWrite` -> file-based checklist. Receipts (§4) use whichever exists.

Probe the tool list, not the harness name. Harness tables go stale; the tool list does not.

## 2. Roles Are Briefs, Not Agent Types

A role is a self-contained brief under `dev-shared/roles/` (or a skill's own `references/`). Delegation = generic subagent + role brief + task scope.

- `spawn` mode: read the brief, spawn the harness's generic agent type, and pass brief + scope + constraints + output path in the worker prompt.
- `inline` mode: read the brief and execute it yourself in the current context, labeling outputs `[inline:<role>]`.

## 3. Fallback Ladder

| Rung | Mode | Behavior |
|------|------|----------|
| L1 | `spawn` | True separate context. Parallel when 2+ independent units. |
| L2 | `spawn-mcp` | Same semantics through MCP. |
| L3 | `inline` | Sequential passes in the main context. Disclose the fallback in the receipt. Never describe sequential self-analysis as independent parallel agents. |

## 4. Delegation Receipt (Mandatory)

Every delegation, and every inline fallback, writes one receipt through the probed task primitive (or the workflow's log when no task primitive exists):

```
[delegate] role=<role> mode=<spawn|spawn-mcp|inline> scope=<one line> status=<done|partial|failed>
```

A workflow that ends with delegated work invisible in the task tree or log violates this contract.

## 5. Guards

- Max delegated units per workflow: 5. Document-family orchestrators use the stricter `orchestrator-contract.md` formula instead.
- Escalation depth: 1. A delegated role never delegates (see `leaf-contract.md`); a skill never escalates to itself.
- Parallel units require independent outputs (no shared write targets).
- The main agent owns synthesis: worker findings are candidates until verified against the codebase.
- Budget: each delegated unit ≈ 10-15K tokens. Prefer inline when the work is small.

## 6. Role Index

| Role | Brief | Used by |
|------|-------|---------|
| `researcher` | `dev-shared/roles/researcher.md` | `hi-plan` (`--full`/`--hard`/`--parallel`/`--two`) |
| `implementer` | `dev-shared/roles/implementer.md` (alias: `fullstack-developer`) | `hi-craft --parallel`, `hi-fix --parallel` |
| `reviewer` | `dev-shared/roles/reviewer.md` | `hi-plan red-team`, `hi-craft --review`/`--full` |
| `log-writer` | `hi-log/references/log-writer-contract.md` | `hi-log` |
| `investigator` | ad hoc — define the brief at spawn time | `hi-debug`, `hi-repository-search`, `hi-codebase-research-explorer` |

Skills may add roles; the brief must exist before the role is delegated.
