# Phase 2 — Commands & Invocation reference

## Context Links
- [plan.md](./plan.md)
- [phase-01-readme-restructure.md](./phase-01-readme-restructure.md)
- Evidence: `awk '/^argument-hint:/' */SKILL.md`; `grep -n '^## Modes\|^## Subcommands\|^## Mode Matrix' */SKILL.md`

## Overview
- Priority: P1 (this is the "command section" the operator explicitly asked for)
- Status: Pending
- Size: S
- Add one README section that tells a reader how to actually invoke every skill: slash command, positional args, mode flags, subcommands.

## Key Insights
- Invocation knowledge is currently scattered inside each `SKILL.md` (argument-hint, Modes tables, Subcommands tables) and only leaked into README once (`hi-plan --fast` in Typical Workflows). The `hi-command-spec-discovery` skill is invisible in all docs.
- Real flag sets confirmed from bodies: `hi-plan --fast|--full|--hard|--parallel|--two|--no-tasks` + subcommands `archive|red-team {path}|validate {path}`; `hi-craft --full|--parallel|--review|--auto|--no-test|--test-budget=N`; `hi-fix --standard|--deep|--parallel|--review`; `hi-repository-search --code|--doc|--ask|--deep|--impact`; `hi-cortex [setup|status|add-code|sync-code|add-doc|sync-doc|start-mcp|stop-mcp|doctor]` plus `--project-dir|--name|--sync-mode|--git|--full-scan`; `hi-log [topic] [--since <ref>] [--scope <dir>]`; `hi-chrome-devtools [url or task]`; `hi-predict --files`; `hi-repowiki --resume`; `hi-reverse --module|--use-case|--package|--profile|--offline|--check-catalog|--condition|--next|--summary|--output|--yes`; `slide-kit --output-dir`.
- 19 skills have no `argument-hint` and are invoked by name + natural-language task; the section must say so explicitly instead of leaving a blank cell that looks like a defect.

## Requirements
- Functional
  - New README section `## Commands & Invocation` with a table: Skill | Invocation | Modes / Flags | Subcommands.
  - Every skill with an `argument-hint` or mode/flag set appears with its real syntax (no invented flags).
  - Skills without flags get a single explicit row group ("Invoked by name + task description: …") rather than empty cells.
  - Subcommand line for `hi-plan`: `/hi-plan archive`, `/hi-plan red-team {path}`, `/hi-plan validate {path}`.
  - Discovery/command family reachable from this table: at minimum `hi-command-spec-discovery`, `hi-usecase-discovery`, `hi-api-contract-discovery`, `hi-data-model-discovery`, `hi-behavior-modeling`, `hi-cross-artifact-validation`.
  - Note the harness contract: slash form and bare-name form both work; flags are optional unless stated.
- Non-functional
  - Table stays maintainable: one row per skill, ≤ ~110 chars per cell.
  - Any flag cited must exist in that skill's `SKILL.md` (this is the Phase 5 check's `flags-subset-of-skill` rule).

## Related Code
- Modify: `README.md` (add section after `What Is Included`; adjust Typical Workflows to reference it).
- Read-only evidence: all `*/SKILL.md`, especially the 16 with `argument-hint`.

## Implementation Steps
1. Extract flags/modes per skill mechanically (`grep -oE '\-\-[a-z][a-z-]+'` plus Modes/Subcommands tables) into a scratch table.
2. Build the README table in group order from Phase 1 so the two sections read consistently.
3. Add the trailing "invoked by name only" list for the 19 skills without flags.
4. Rewrite `## Typical Workflows` examples to use the documented syntax (e.g. `hi-plan --full`, `hi-repository-search --impact`).
5. Add a one-line pointer to `devkit.md` for the mode-selection rationale, so the table does not grow into prose.

## Success Criteria
- Every one of the 35 skills appears in the new section exactly once.
- No flag in the table is absent from the corresponding `SKILL.md`.
- `hi-command-spec-discovery` is documented with its purpose (APDU/TLV, CLA/INS/P1/P2/Lc/Le, opcode, status word drafts) and its draft-only boundary.

## Test Scope
- Mapped acceptance criteria: (a) all 35 skills present, (b) each cited flag verified against the source skill, (c) draft-only boundary stated for discovery skills.
- Expected size: S. Verification by grep cross-check + Phase 5 checker.

## Risk Assessment
- Risk: documenting flags that were renamed in a skill body but not in its `argument-hint` (already true for `hi-fix`/`hi-craft` hint wording). Mitigation: treat `SKILL.md` body as the source of truth and flag any mismatch as a Phase 4 finding.
- Risk: turning README into a second copy of every mode matrix. Mitigation: table only, rationale stays in `devkit.md`.
