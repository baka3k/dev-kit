---
name: hi:log
description: "Write log entries analyzing recent changes and session reflections."
argument-hint: "[topic] [--since <ref>] [--scope <dir>]"
metadata:
  author: baka3k
  version: "1.2.0"
---
# Log

Spawn log-writer subagent to scout memories and recent code changes, write concise log entries to ./docs/logs/.
Focus on key events, changes, impacts, and decisions. Run /hi:project-organization to organize outputs.

## Arguments
- Default: summarize last session (claude-mem + recent diffs)
- `[topic]` - focus log on a specific area (e.g. `auth`, `ci`, `release`)
- `--since <ref>` - only changes after git ref/sha/date (default: last 24h)
- `--scope <dir>` - limit exploration to a directory (e.g. `src/api/`)

## Workflow

### 1. Discover
Pull context from claude-mem (recent observations) and git diff/log.
Use hi:scout if scope is ambiguous. Honor `--since` / `--scope` filters.

### 2. Filter
Keep entries that change behavior, fix risk, or capture a decision.
Drop noise: trivial formatting, regenerate-only commits, no-op refactors.

### 3. Write
Spawn log-writer subagent per `references/log-writer-contract.md`.
One file per logical event. Filename: `YYYY-MM-DD-<slug>.md`.

### 4. Organize
Run /hi:project-organization to index logs under ./docs/logs/.
Ensure cross-links to plans (`./plans/`) and journal entries.

## Non-Negotiable Rules
- Do NOT log empty sessions. If no material change -> abort with notice.
- Always include **Impact** section in every entry.
- Tie each entry to concrete references: `path/to/file.ts:LINE` or `commit:sha`.
- One event = one file. No monolithic daily dumps.
- Preserve decision rationale, not just the outcome.

## Output Format
```markdown
# <Title> — YYYY-MM-DD
## Context
What triggered this work (bug, request, plan link).
## Change
What changed, with `file:line` references.
## Impact
Who/what is affected. Risk level (low/med/high).
## Decision
Why this approach. Alternatives considered.
## References
- plan: ./plans/<id>/plan.md
- commit: <sha>
- memory: <obs-id>
```

## References
- Subagent contract: `references/log-writer-contract.md`
- Output: `./docs/logs/`
- Indexer: `/hi:project-organization`
