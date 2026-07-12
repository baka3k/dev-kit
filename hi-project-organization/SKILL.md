---
name: hi-project-organization
description: Organize project files, directories, output paths, names, and Markdown structure. Use when creating files, choosing where outputs belong, reorganizing existing assets, or standardizing a project layout.
---

# Project Organization

Place files consistently without overriding established project conventions.

## Modes

- **Advisory:** Return the recommended path and name when another skill or task needs an output location.
- **Organize:** When asked to reorganize targets, scan, propose a migration, obtain approval, execute, and verify.

## Priority

1. Preserve explicit user requirements.
2. Follow existing repository and ecosystem conventions.
3. Apply this skill's defaults only where the project has no convention.

## Path Rules

| Content | Default location |
| --- | --- |
| Source | `src/` or the ecosystem-standard project root |
| Tests | Existing `test/` or `tests/`, mirroring source where practical |
| Documentation | `docs/` |
| Technical logs | `docs/logs/` |
| Architecture decisions | `docs/decisions/` |
| Plans | `plans/{timestamp}-{slug}/` |
| Plan-scoped research/reports | `plans/{plan}/research/`, `plans/{plan}/reports/` |
| Standalone research/reports | `plans/research/`, `plans/reports/` |
| Scripts | `scripts/` |
| Assets | `assets/{type}/` |
| User guides | Existing `guide/` or `guides/`; otherwise `docs/guides/` |
| Configuration | Ecosystem-standard root path; `.config/` only when supported |

Read [references/directory-patterns.md](references/directory-patterns.md) only when detailed layout guidance is needed.

## Naming Rules

- Use a lowercase kebab-case, self-documenting slug, at most 50 characters.
- Timestamp time-sensitive plans, reports, logs, sessions, and generated content as `{YYMMDD-HHmm}-{slug}`.
- Leave evergreen docs, configs, guides, scripts, and source files untimestamped.
- Name variants `{slug}-{variant}.{ext}`.
- Follow the repository or language convention for code files instead of forcing kebab-case.
- Use `$HI_PLAN_DATE_FORMAT` when set; otherwise use `YYMMDD-HHmm`.

Read [references/naming-conventions.md](references/naming-conventions.md) only for slug normalization and variant examples.

## Nesting Rules

- Keep a single output flat in its category directory.
- Give a multi-file output a self-contained directory.
- Nest artifacts under their owning plan or feature context.
- Keep variants flat with suffixes; use platform subdirectories only for collections.
- Add `.gitkeep` only when an intentionally empty directory must be tracked.

## Markdown Rules

- Use one H1 title.
- Add frontmatter only when a tool or workflow consumes it.
- Order content as context, main content, then next steps or unresolved questions.
- Use tables for structured comparisons and lists for sequences.
- Prefer concise, scannable prose.

Read [references/markdown-body-templates.md](references/markdown-body-templates.md) only when creating a plan, phase, report, log, ADR, changelog, README, guide, or specification.

## Resolve a New Output

1. Detect the file type and the project's existing convention.
2. Select the base path from the table above.
3. Choose timestamped, evergreen, or variant naming.
4. Choose flat or nested placement from the output count and ownership.
5. Apply a Markdown template when relevant.
6. Check for path conflicts before writing.

## Organize Existing Files

1. Scan only the requested targets and categorize their files.
2. Identify misplaced files, naming violations, and inconsistent structure.
3. Present a `from -> to` migration table, including conflicts and tradeoffs.
4. Obtain user approval before moving or renaming anything.
5. Apply only approved changes.
6. Verify the final tree and report unresolved issues.

## Safety

- Never overwrite an existing file; surface conflicts.
- Never modify `.git/`, dependency directories, secrets, or `.env` files.
- Respect `.gitignore` and preserve repository history with normal moves.
- Do not create categories or directories that the requested output does not need.

