# DevKit Documentation Realignment — 2026-10-18

## Context

The kit shipped 35 skills plus the `dev-shared` support package, but its own documentation had drifted far behind the tree. `README.md` claimed "16 composable skills", omitted 18 skills entirely, listed directories that no longer existed (`hi-explore/`, `cortex/`), and contained two contradictory document layers (duplicate `Installation`, `Supported agents`, and `Manifest files` sections). `devkit.md` documented only `hi-craft`, `hi-fix`, and `hi-plan`, so the discovery-to-documentation pipelines that ship today were invisible. Nothing verified any of this, which is how the gap accumulated.

## Change

- **README rewritten** as a catalog: 35 skills in six groups plus the support package (`README.md:168`), a new **Commands And Invocation** table giving every skill its invocation, modes/flags, and subcommands (`README.md:245`), a regenerated Folder Structure tree (`README.md:342`), one manifest section with the routing table (`README.md:106`), one Supported Agents table (`README.md:152`), and a Development section documenting the new targets (`README.md:444`). Duplicated sections and the inlined AGENTS.md dump were removed in favour of references to [devkit.md](../../devkit.md).
- **devkit.md rewritten** around the real surface: orchestrator/leaf/standalone role tables, the core pipelines, the discovery artifact pipeline (`devkit.md:197`), the documentation lifecycle with both orchestrators and the nine stages (`devkit.md:231`), the repository wiki pipeline (`devkit.md:268`), the extended cross-skill graph (`devkit.md:319`), delegation semantics, and HARD-GATEs kept byte-identical to README's copy (`devkit.md:451`).
- **Drift tooling added**: `scripts/check-kit-docs.mjs` with 13 rules — catalog completeness (including the `name` column), count, duplicate headings, folder-tree accuracy for directories and files, internal links (including `wiki/`, anchored links, reference-style definitions, code-fence awareness), frontmatter convention, `argument-hint` presence on every skill, documented flags existing in their skill, Commands-table coverage, HARD-GATE parity, manifest sync, wiki freshness, and wiki coverage (`scripts/check-kit-docs.mjs:110`). Wired as `make check-docs` and into `make doctor`, which now fails on drift (`Makefile:76`, `Makefile:85`).
- **Manifests consolidated**: `AGENTS.md` is the single source of truth and `scripts/sync-manifests.mjs` regenerates `CLAUDE.md` and `.cursorrules` from it, so the third copy can no longer drift from the two the installer ships (`Makefile:88`).
- **Frontmatter standardized across 36 `SKILL.md` files**: `name`/`description`/`argument-hint`/`license` top-level; `version`/`last_updated`/`author` under `metadata`; the five top-level `version`/`last_updated` blocks migrated; `argument-hint` added to the 25 skills that lacked one; the convention documented and marked checked/unchecked per field (`README.md:426`).
- **Wiki coverage closed**: `scripts/gen-wiki-pages.mjs` generates the 36 compact guides for the 18 undocumented skills from each `SKILL.md`, marked so the 34 hand-written deep dives are never overwritten (only `--adopt` takes one over) (`Makefile:91`).
- **Fixes found by the new rules**: a broken relative link and a stale section reference in `dev-shared/jev/usecase-intent-routing.md`, and two broken `references/install.md` links in `wiki/{en,vi}/hi-cortex-skill.md`.

## Impact

Risk level: **low**. No runtime behaviour changed; the repository is documentation, metadata, and three dependency-free Node scripts that read and write only inside the repo root. Two review rounds found and closed fifteen defects: rules that could pass vacuously (renamed section, a skill dropped from the Commands table but mentioned in prose, valueless frontmatter keys, `support: true` self-exemption, empty `argument-hint`, an emptied wiki page), unsupported caller/escalation claims in the workflow graph, and `--force` being able to destroy hand-written wiki pages. Verification is now mechanical: 34 drift injections against byte-identical copies, each caught by its intended rule, plus all 10 Mermaid blocks rendering under mermaid v12.

## Decision

A drift checker was chosen over periodic manual review, because the original defect was not a single mistake but the absence of any mechanism tying documentation to the tree. Rules were made to fail loudly rather than warn: `make doctor` reports `[FAIL] docs drift detected`, so drift surfaces during normal setup instead of after a release.

The fix round deliberately rejected two tempting shortcuts. First, "generate all wiki pages" would have destroyed 34 hand-written deep dives, so the generator skips anything without its marker and the checker treats the two page classes differently. Second, "add a rule that warns" for unsupported graph edges was avoided: claims in `devkit.md` were corrected against the skill files instead of being documented as aspirational, since the kit's own `AGENTS.md` forbids fabricating context.

Scope grew by one script (`gen-wiki-pages.mjs`) beyond the original phase plan so the 36 new pages are regenerable rather than hand-written; this is recorded in the plan's execution notes (`docs/plans/devkit-doc-realignment/phase-05-drift-check-manifests-wiki.md`). `metadata.support` remains reserved for `dev-shared` and is now enforced.

## References

- Plan: `docs/plans/devkit-doc-realignment/plan.md`
- Checker: `scripts/check-kit-docs.mjs`, `scripts/sync-manifests.mjs`, `scripts/gen-wiki-pages.mjs`
- Entry points: `Makefile` (`check-docs`, `sync-manifests`, `wiki`, `doctor`)
- Docs: `README.md`, `devkit.md`, `wiki/{en,vi}/`, `AGENTS.md`
