# DevKit

A token-efficient agent skills kit for software engineering workflows. 13 composable skills, designed for Claude Code / Cursor / Continue / Copilot.
## Installation

Just simple in terminal

```
npx skill-dev
```
## Advanced Capabilities

For complex codebases exceeding millions of lines of code (LOC) and massive documentation scale (tens of gigabytes), integrate cortex-harness (https://github.com/baka3k/cortex-harness).

The pre-configured skills natively support hybrid querying across both Graph Databases (GraphDB) and Vector Databases (VectorDB). 

By combining graph-based relational queries with semantic search, the system optimizes context retrieval and dramatically accelerates project onboarding and codebase understanding.

## Skills

### Orchestrators (drive end-to-end work)

| Skill | Purpose | Default mode |
|-------|---------|--------------|
| `hi:cook` | Implement features (plan → code → test → finalize) | `fast` |
| `hi:fix` | Fix bugs (explorer → diagnose → fix → verify → finalize) | `quick` |
| `hi:plan` | Multi-mode planning (fast / full / hard / parallel) | `fast` |

### Leaf skills (called by orchestrators)

| Skill | Purpose |
|-------|---------|
| `hi:explorer` | Parallel codebase explore (multi-agent file discovery) |
| `hi:debug` | Systematic debugging + root cause tracing + verification gate |
| `hi:knows` | Evidence retrieval (Git → MCP → memory) |
| `hi:log` | Write session log entries to `./docs/logs/` |
| `hi:problem-solving` | Stuck-unsticking techniques (inversion, collision-zone, scale-game) |

### Analysis & methodology

| Skill | Purpose |
|-------|---------|
| `hi:scenario` | 12-dimension edge case explore before implementation |
| `hi:predict` | 5-persona pre-analysis debate |
| `hi:security` | STRIDE + OWASP security audit with iterative auto-fix |
| `hi:sequential-thinking` | Sequential reasoning with revision / branching / hypothesis testing |

## Typical Workflows

```
Implement feature:  hi:cook (fast) → hi:plan inline → code → test → hi:log → commit
Implement complex:  hi:cook (full) → hi:explorer → hi:plan (full) → code → review → commit
Fix bug:            hi:fix (quick) → explorer → diagnose → fix → verify → commit
                    hi:fix (deep)  → hi:explorer (parallel) → hi:debug → hi:problem-solving
Pre-flight chehi:   hi:scenario (12 dim) → hi:predict (5 personas) → ship
Security audit:     hi:security (STRIDE phases 0-6) → fix mode → re-verify
```

## Quick Start

```bash
# Skills are picked up automatically by Claude Code / Cursor / Continue.
# Trigger via slash command or natural language.
```

**Install on Cursor (global)**: copy `.cursorrules` + skill folders to `~/.cursor/skills/`.
**Install on Claude Code**: copy skill folders to `~/.claude/skills/`.

See [USAGE_GUIDE.md](USAGE_GUIDE.md) for per-skill usage, inputs, and outputs.

## Folder Structure

```
dev-kit/
├── hi-cook/          SKILL.md + references/ + agents/
├── hi-fix/
├── hi-plan/
├── hi-explorer/       (renamed from hi-ciu)
├── hi-debug/         SKILL.md + references/ + scripts/
├── hi-knows/
├── hi-log/
├── hi-problem-solving/  SKILL.md + references/ (7 techniques)
├── hi-scenario/      SKILL.md + references/
├── hi-predict/
├── hi-security/      SKILL.md + references/ + scripts/
├── hi-sequential-thinking/  SKILL.md + references/ (5 files)
├── knows/            Standalone evidence retrieval
├── .cursorrules      Cursor auto-load rules
├── AGENTS.md         Agent harness instructions
├── CLAUDE.md         Project-level Claude instructions
├── devkit.md         Workflow diagrams (mermaid) + HARD-GATEs
├── dependency.md     Skill-to-skill call graph + missing skills
```

## Key Conventions

- **HARD-GATE** — non-negotiable rules per skill (e.g. `hi:fix` blocks before Explorer + Diagnose complete)
- **Inline > Spawn** — only spawn sub-skills when really needed (>2 fail, scope too large)
- **Mode flags** — every orchestrator has `--fast` / `--full` / `--review`; default = lightest
- **Evidence over assumption** — every claim cites `file:line` or `commit:sha`
- **Vietnamese by default** — human-readable outputs (logs, plans) are Vietnamese; technical artifacts keep English

## Token Economy

Designed for minimum token burn:
- Default modes skip heavy sub-skill spawns (~80% reduction vs naive workflow)
- Parallel subagents only when 3+ files / 2+ independent issues
- Verification gates prevent over-fixing (typecheck+lint beats full test suite when not needed)

See [optimize.md](optimize.md) for the full token-burn analysis.

## Adding a Skill

1. Create `your-skill/SKILL.md` with frontmatter: `name`, `description`, `argument-hint`, `metadata`
2. Add `references/` for supporting docs (optional)
3. Add `agents/openai.yaml` for Cursor / Copilot picker (optional)
4. Run `python scripts/sync_manifest.py` (auto-regenerates MANIFEST.json)

## Reference Docs

| Doc | What's in it |
|-----|--------------|
| [devkit.md](devkit.md) | Mermaid workflow diagrams + HARD-GATEs + cross-skill integration |
| [dependency.md](dependency.md) | Skill call graph, missing skills, external refs to fix |
## License

MIT
