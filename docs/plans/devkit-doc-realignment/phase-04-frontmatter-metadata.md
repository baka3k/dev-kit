# Phase 4 — Frontmatter metadata standardization

## Context Links
- [plan.md](./plan.md)
- Evidence: frontmatter key scan across `*/SKILL.md` (see plan.md Findings)

## Overview
- Priority: P2
- Status: Pending
- Size: M
- One version convention, `argument-hint` wherever modes exist, and a decision on the unexplained `hooks:` blocks.

## Key Insights
- Three states today: top-level `version:` + `last_updated:` (`hi-brainstorm`, `hi-knows`, `hi-predict`, `hi-scenario`, `hi-security`), `metadata.version` (`hi-chrome-devtools`, `hi-codebase-research-explorer`, `hi-cortex`, `hi-craft`, `hi-debug`, `hi-fix`, `hi-log`, `hi-plan`, `hi-problem-solving`, `hi-repository-search`, `hi-sequential-thinking`), and none (21 skills, mostly the newer families).
- `hi-sequential-thinking` and `hi-chrome-devtools` carry `license:` at top level; `typesafe-ai` too. Keep `license` where present; do not invent licenses for other skills.
- 19 skills lack `argument-hint`, including every Discovery & Artifact and Documentation Lifecycle skill — the exact skills a reader cannot guess how to call. Phase 2 documents them as "name + task"; the hint should match that reality rather than stay empty.
- `hooks:` appears in `hi-predict`, `hi-scenario`, `hi-security` (`mcp-health-check`, `input-validation`, `cleanup-handler`, `output-redaction`) with scopes and cleanup paths. Nothing in the kit, README, or installer consumes them. They are either a contract with an external harness or dead metadata.
- `dev-shared/SKILL.md` already uses `metadata.support: true`; keep the support marker and give it a version only if the convention requires uniform versioning.

## Requirements
- Functional
  - Decide one convention. Recommendation: keep the existing majority pattern — `name`/`description` at top level, `version` + `last_updated` under `metadata`, since 11 of 16 versioned skills already do this and it groups authorship with authorship.
  - Migrate the 5 top-level-version skills to the chosen convention (or the reverse, if the operator prefers top-level — decide once in step 1 and record it in `README.md` "Adding A Skill").
  - Add `argument-hint` to every skill with documented modes/flags: the 6 discovery skills, the 3 lifecycle/refinement/review skills, plus `hi-docs-seeker`, `hi-project-organization`, `hi-repo-recon`, `hi-repowiki`, `hi-tech-build-audit`, `hi-module-summary-report`, `hi-reverse`, `slide-kit`, `hi-knows`, `hi-brainstorm`, `hi-predict`, `hi-scenario`, `hi-security`, `typesafe-ai` — hint text must match the real modes (e.g. `hi-repository-search` style: `[question|symbol|path|SQL|impact] [--code|--doc|--deep|--impact]`).
  - Add `version` to skills that currently have none, starting at `1.0.0`.
  - Resolve `hooks:`: either document the contract (what consumes it, when) in `README.md`/`dev-shared/`, or remove the keys. No third option.
- Non-functional
  - Do not add `version`/`last_updated` churn unrelated to this change; no other frontmatter fields touched.
  - `description` keeps its existing draft-only / boundary language untouched (it drives skill routing).

## Related Code
- Modify: `*/SKILL.md` frontmatter only (35 files + `dev-shared/SKILL.md` decision).
- Modify: `README.md` "Adding A Skill" (document the convention + required fields).
- Read-only evidence: `hi-repository-search/SKILL.md`, `hi-cortex/SKILL.md` (good `argument-hint` exemplars).

## Implementation Steps
1. Pick and record the version convention; state it in `README.md`.
2. Script the migration (Python/YAML-lite frontmatter rewrite, preserving description text and quoting style) rather than hand-editing 35 files; keep a dry-run diff before writing.
3. Write `argument-hint` per skill from its actual Modes/Subcommands section and flags — read each file, do not template.
4. Add `version: 1.0.0` (+ `last_updated: 2026-10-18`) to skills missing both.
5. Decide `hooks:` (document or delete) and apply.
6. Re-run the Phase 5 checker in dry-run to confirm frontmatter parse + hint presence.

## Success Criteria
- Zero skills with two competing version styles.
- Every skill with modes/flags has a non-empty `argument-hint` matching its body.
- No `hooks:` key without a documented consumer.
- All 36 `SKILL.md` files still parse as YAML frontmatter and `name` still equals the directory name.

## Test Scope
- Mapped acceptance criteria: (a) single version convention, (b) hint coverage for all mode-bearing skills, (c) hooks resolved, (d) frontmatter parses and `name == dir`.
- Expected size: M. Verification: frontmatter parse script (Phase 5) + spot read of 5 migrated files. No unit tests (metadata tier).

## Risk Assessment
- Risk: a bad script corrupts 35 files at once. Mitigation: dry-run diff, git-clean tree before the run, one commit per convention step so a revert is cheap.
- Risk: `argument-hint` text drifting from mode tables. Mitigation: hints are copied from the file being edited in the same pass.
- Risk: deleting `hooks:` breaks an external harness the operator uses. Mitigation: default to *document*, and only delete on explicit confirmation.
