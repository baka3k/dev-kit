# Phase 1 — README restructure and catalog

## Context Links
- [plan.md](./plan.md)
- `/Users/hieplq1.aip/AI/dev-kit/README.md` (568 lines, current target)
- Verified inventory: `ls -d */` ∩ `*/SKILL.md` at repo root

## Overview
- Priority: P1 (foundation — later phases reference this catalog)
- Status: Pending
- Size: M
- Rewrite README so it describes the kit that actually exists: correct skill count, complete catalog, correct folder tree, no duplicated sections.

## Key Insights
- README is two documents concatenated: the old layer (lines ~60-135: `## Install Other skills from github`, `## Usage`, `## Manifest files`, `## AGENTS.md`, `## Supported agents`, `## What Is Included`) and a newer layer (lines ~198+: `## Installation`, `## Supported Agents`, `## Manifest Files`, `## Custom Sources`, `## How Installation Works`). They contradict each other on skill names (`knows` vs `hi-knows`, `hi-explore/` vs `hi-codebase-research-explorer/`, `cortex/` vs `hi-cortex/`).
- The old layer re-prints the whole AGENTS.md content inside README — content that already ships as `AGENTS.md` and is auto-installed. Remove the copy, link the file.
- Two `## Supported agents` tables differ: the older one omits the `Set CLAUDE_CONFIG_DIR...` note but includes Antigravity/Hermes; the newer adds the note. Merge into one.

## Requirements
- Functional
  - Header states 35 skills + `dev-shared` support package.
  - Six catalog groups exactly as defined in `plan.md` → Target Catalog Taxonomy; each row: directory, skill name, purpose (one line, reuse frontmatter `description` intent, not verbatim copy of long ones).
  - `dev-shared` listed as support package with its sibling-install explanation.
  - Folder Structure tree regenerated from the real tree, including `dev-shared/`, `wiki/`, `docs/`, `slide-kit/`, `typesafe-ai/`.
  - `hi-command-spec-discovery` and the whole Discovery & Artifact group present.
  - Single `Installation`, single `Supported Agents`, single `Manifest Files`, single `Custom Sources`, single `How Installation Works`.
  - `wiki/` documented and linked (currently unreferenced).
  - Cross-link to the new Commands & Invocation section (Phase 2) and to `devkit.md`.
- Non-functional
  - No content duplication with `devkit.md` beyond a short pointer; README = catalog + install, devkit.md = workflows.
  - Markdown renders on GitHub: no ragged tables, no broken relative links.

## Related Code
- Modify: `README.md` (full rewrite, keep `## License` and the MIT block).
- Read-only evidence: every `*/SKILL.md` frontmatter (name, description, argument-hint), `dev-shared/SKILL.md`.

## Implementation Steps
1. Draft the ordered section skeleton: Title/intro → Advanced Capabilities → Installation → Manifest files → Supported agents → What Is Included (6 groups) → Repository Search Integration → Commands & Invocation (pointer) → Typical Workflows → Workflow Diagrams (pointer to devkit.md) → Folder Structure → Key Conventions → Adding A Skill → Reference Docs → License.
2. Regenerate the skill inventory table from frontmatter (script in Phase 5 will later enforce it; do it manually now).
3. Assign each of the 35 skills to its group; verify total = 35 against the tree.
4. Merge the two `Supported agents` tables; keep Antigravity and Hermes rows plus the `CLAUDE_CONFIG_DIR`/`CODEX_HOME`/`XDG_CONFIG_HOME` note.
5. Merge the two manifest sections into one; delete the inline AGENTS.md dump, keep the routing table (`AGENTS.md` → `~/.agents/AGENTS.md`, `CLAUDE.md` → `~/.claude/CLAUDE.md`, others → `~/.agents/`).
6. Regenerate Folder Structure from `find . -maxdepth 1 -type d` (exclude dot dirs) and annotate each entry.
7. Delete the duplicated Workflow Diagrams / Cross-Skill Integration / HARD-GATEs blocks that duplicate `devkit.md`; leave one-line pointers.
8. Re-read the file top to bottom and delete any surviving repeated heading.

## Success Criteria
- `grep -c '^## ' README.md` yields no duplicate heading text.
- Every directory from the tree appears exactly once in the catalog or the Folder Structure.
- Skill count in prose = 35 and matches the catalog row count.
- No `hi-explore/` or bare `cortex/` reference remains except in a clearly labeled "renamed" note if one is kept.

## Test Scope
- Mapped acceptance criteria: (a) catalog covers 35 skills, (b) no duplicate H2, (c) folder tree matches dirs, (d) all relative links resolve, (e) `hi-command-spec-discovery` present.
- Expected size: M. Verification is a read + the Phase 5 checker in dry-run; no unit tests (docs-only change, per test-budget "Never" tier for prose).

## Risk Assessment
- Risk: silently dropping a skill during regrouping. Mitigation: build the table from a script-generated list, not from memory; diff row count before/after.
- Risk: over-trimming — deleting content that only existed in README (e.g. `Repository Search Integration`, `Key Conventions`). Mitigation: keep those sections, only dedupe what genuinely repeats.
- Risk: `devkit.md` also duplicates README's HARD-GATEs table; resolve in Phase 3, not by deleting README's copy now.
