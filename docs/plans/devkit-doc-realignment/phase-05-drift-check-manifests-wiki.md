# Phase 5 — Drift-check tooling, manifests, wiki

## Context Links
- [plan.md](./plan.md)
- [phase-01-readme-restructure.md](./phase-01-readme-restructure.md) … [phase-04-frontmatter-metadata.md](./phase-04-frontmatter-metadata.md)

## Overview
- Priority: P2
- Status: Pending
- Size: M
- Make drift impossible to reintroduce: a checker wired into `make`, a single manifest source, and a decision + execution for the 18 skills missing wiki pages.

## Key Insights
- Nothing validates docs against the tree, which is exactly how README fell 19 skills behind.
- No CI in this repo's root (`.github/` is gitignored for everything except workflows/hooks/agents), so the practical entry point is a `Makefile` target alongside the existing `doctor`.
- Node is already a hard dependency (`npx skill-dev` in `Makefile`, `node dist/cli.js` for the local installer), so a dependency-free Node script needs no new tooling.
- Link check found only 4 broken refs and all are illustrative placeholders — the checker should allow a documented allowlist rather than force edits to examples.
- Manifests: `AGENTS.md`, `CLAUDE.md`, `.cursorrules` are near-identical; the installer copies only `AGENTS.md` and `CLAUDE.md`. Divergence already exists (`.cursorrules` drops the "params invalid → retry twice" rule and the Decision section; AGENTS.md/CLAUDE.md add a "When any decision is needed" block). `AGENTS.md`'s "always responds in English" also conflicts with the operator's Vietnamese preference.
- `docs/logs/` has one entry while `hi-log` is mandatory at finalize — a process gap worth flagging, not fixing through a doc phase.

## Requirements
- Functional (checker — `scripts/check-kit-docs.mjs`)
  - `catalog-complete`: every dir with `SKILL.md` (excluding `dev-shared`) appears in the README catalog.
  - `catalog-count`: skill count stated in README prose equals the real count.
  - `no-duplicate-heading`: no repeated `^## ` heading text in `README.md`/`devkit.md`.
  - `tree-matches`: every backticked `xyz/` path in the Folder Structure block resolves to a real directory.
  - `links-resolve`: relative `.md` links in `*.md` resolve, with an allowlist for placeholder examples (`phase-01-setup.md`, `phase-01-name.md`, `jev-contract.md`, `system/system-overview.md`).
  - `frontmatter-valid`: `SKILL.md` frontmatter parses; `name` == directory name; version convention respected (from Phase 4's decision).
  - `hint-present`: skills whose body has a `Modes`/`Subcommands`/`Mode Matrix` section have a non-empty `argument-hint`.
  - `flags-known`: every `--flag` listed in the README Commands & Invocation table also appears in that skill's `SKILL.md`.
  - `hardgate-parity`: HARD-GATE tables in README and `devkit.md` have identical rows.
  - Output: per-rule pass/fail + offending path; non-zero exit on any failure; `--json` flag for CI.
- Functional (Makefile)
  - `make check-docs` runs the checker; `make doctor` gains one `[ OK ]/[FAIL] docs drift` line so health-check covers it.
- Functional (manifests)
  - Recommend: `AGENTS.md` is the single source of truth; `CLAUDE.md` and `.cursorrules` are generated from it (or `.cursorrules` is deleted, since the installer never ships it — needs confirmation).
  - Resolve the language-policy line: state the policy explicitly (docs English, replies follow operator language) or drop the blanket English rule.
- Functional (wiki)
  - Recommendation: do not bulk-regenerate — add pages only for the 18 missing skills, keeping `en`/`vi` parity (currently 18 files each, same skill set).
  - Verify with the checker: every skill dir has `wiki/en/<skill>-skill.md` and `wiki/vi/<skill>-skill.md`, or is on an explicit allowlist.
  - Document in `README.md` how the wiki is regenerated (`hi-repowiki`) instead of leaving the folder unexplained.
- Functional (process note, no code)
  - Record the `docs/logs/` gap (1 entry vs mandatory finalize logging) in `README.md` Key Conventions or as a follow-up plan item.

## Related Code
- Create: `scripts/check-kit-docs.mjs`.
- Modify: `Makefile` (add `check-docs` target, extend `help` and `doctor`), `README.md` (Adding A Skill, wiki note, manifest policy), `AGENTS.md` + `CLAUDE.md` (+ `.cursorrules` decision), `wiki/en|vi/*` for the 18 missing skills.

## Implementation Steps
1. Write the checker with the 9 rules above; run it against the current (post-Phase 1-4) tree and fix real findings, not rules.
2. Add the allowlist file/constant for the 4 placeholder links with a comment explaining why they are allowed.
3. Wire `make check-docs`; add the docs line to `make doctor`; update `make help`.
4. Manifest consolidation: diff the three files, produce the merged canonical `AGENTS.md`, regenerate `CLAUDE.md`, and either regenerate `.cursorrules` or delete it after confirmation.
5. Resolve the language-policy line in all manifest copies at once (single generation step prevents re-drift).
6. Wiki: list the 18 missing skills, generate `en` + `vi` pages (delegate to `hi-repowiki` if it is the sanctioned generator; otherwise write from each `SKILL.md`), then re-run the checker with the wiki rule enabled.
7. Add the wiki regeneration note + logging-gap note to README.
8. Run `make check-docs` and `make doctor` to confirm both pass on a clean tree.

## Success Criteria
- `make check-docs` exits 0 on the fixed tree.
- Injecting one drift (remove a skill row from README, rename a dir, break a link) makes it exit non-zero — prove each of the 9 rules can fail.
- One canonical manifest source; no contradictory language rules across `AGENTS.md`/`CLAUDE.md`/`.cursorrules`.
- Wiki covers all 35 skills in both languages, or the gaps are explicitly allowlisted.

## Test Scope
- Mapped acceptance criteria: one passing run on the clean tree + one deliberate failure proven per rule (13 rules), manifest parity, wiki coverage.
- Expected size: M. Verification: script output matrix (rule × clean/dirty), `make doctor` output, spot check of 3 generated wiki pages.

## Execution Notes (as delivered)

- The checker shipped with **13 rules**, not 9: `commands-coverage` and `wiki-fresh` were added, and `frontmatter-valid` grew author/quoting/indentation/`support` checks. Two review rounds found rules that could pass vacuously (renamed section, a skill dropped from the Commands table but mentioned in prose, valueless keys, `support: true` self-exemption, empty `argument-hint`, emptied wiki page) — each was closed and pinned by a test case.
- `scripts/gen-wiki-pages.mjs` was added (not in the original file list) so the 36 compact pages are regenerable rather than hand-written. Hand-written pages are only replaced on an explicit `--adopt`; `--force` cannot destroy them (verified by test).
- `wiki-coverage` also verifies generator-owned page structure (title, source link, marker); legacy hand-written pages are only checked for mentioning their skill.
- Verified by 34 drift injections against byte-identical copies, each caught by its intended rule: `/private/tmp/.../scratchpad/test_drift_rules.py` (session scratch, not committed), plus a `--force`-protection test.
- Also fixed while in scope: a broken relative link in `dev-shared/jev/usecase-intent-routing.md` and a stale `devkit.md` section reference in the same file, plus two broken `references/install.md` links in `wiki/{en,vi}/hi-cortex-skill.md` that only became visible once the link rule started scanning `wiki/`.

## Risk Assessment

- Risk: checker becomes a maintenance burden and gets ignored. Mitigation: 13 rules max, no new dependencies, `make doctor` integration so it fires during normal setup.
- Risk: generating 36 wiki pages by hand is large and error-prone. Mitigation: prefer `hi-repowiki`; otherwise script the extraction from `SKILL.md`.
- Risk: deleting `.cursorrules` breaks a Cursor user's setup. Mitigation: default to regenerating it; delete only on explicit confirmation.
- Risk: frontmatter `version` bumps in Phase 4 make the checker fail if the convention wasn't recorded. Mitigation: Phase 5 reads the convention from README, not from a hardcoded list.
