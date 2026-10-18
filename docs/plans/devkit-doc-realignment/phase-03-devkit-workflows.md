# Phase 3 — devkit.md workflow expansion

## Context Links
- [plan.md](./plan.md)
- [phase-01-readme-restructure.md](./phase-01-readme-restructure.md), [phase-02-commands-invocation.md](./phase-02-commands-invocation.md)
- Evidence: `devkit.md` (255 lines) vs `ls -d */`

## Overview
- Priority: P2
- Status: Pending
- Size: M
- Extend `devkit.md` from "3 core skills + tool table" to the real workflow surface, above all the Discovery → Validation → Documentation lifecycle pipelines that ship today but appear nowhere.

## Key Insights
- `devkit.md` names only craft/fix/plan and pins versions (craft 3.2.0, fix 2.1.0, plan 2.2.0) in prose, which will rot again; keep versions out of prose or source them in one place.
- Its cross-skill graph (section 4) already mentions `hi-repository-search`, `hi-chrome-devtools`, `cortex`, `hi-docs-seeker` but not the discovery family, document lifecycle, `hi-repowiki`, `hi-repo-recon`, `hi-tech-build-audit`, `hi-module-summary-report`, `hi-reverse`, `slide-kit`, `typesafe-ai`.
- HARD-GATEs table in section 5 lists 3 gates; `README.md` lists 6 (adds `hi-repository-search`, `hi-security`, `hi-project-organization`). Reconcile to the README set and keep one canonical copy.
- The leaf-skill table (section 0) does not reflect that the discovery skills are themselves leaves called by `hi-document-lifecycle` / `hi-maintenance-docs`.

## Requirements
- Functional
  - Section 0 leaf table: add the discovery leaves and the lifecycle orchestrators that call them.
  - New section: **Discovery Artifact Pipeline** with a Mermaid diagram —
    `hi-repo-recon` / `hi-tech-build-audit` (scope) → `hi-usecase-discovery` → `hi-behavior-modeling` + `hi-api-contract-discovery` + `hi-data-model-discovery` + `hi-command-spec-discovery` → `hi-cross-artifact-validation` → `hi-document-refinement` → `hi-document-review-resolution`, with `hi-maintenance-docs` / `hi-document-lifecycle` as orchestrators.
  - New section: **Documentation Lifecycle** — orchestrator vs leaf split, pause/resume semantics, `hi-repowiki` as whole-repo wiki generator, `hi-module-summary-report` as synthesizer over existing recon/audit artifacts.
  - Extend section 4 cross-skill graph with the new families and the analysis skills not yet drawn (`hi-brainstorm`, `hi-knows`, `hi-tech-build-audit`).
  - Section 5 HARD-GATEs: same 6 rows as README, wording identical.
  - Keep `devkit.md` and README non-overlapping: devkit.md owns diagrams/mode rationale, README owns catalog/invocation.
- Non-functional
  - Every Mermaid block must render: quote node labels containing `/`, `(`, `:`.
  - Diagram node names must match real skill names (checker rule `mermaid-node-is-skill`).

## Related Code
- Modify: `devkit.md`.
- Read-only evidence: `hi-document-lifecycle/SKILL.md`, `hi-maintenance-docs/SKILL.md`, `hi-document-refinement/SKILL.md`, `hi-document-review-resolution/SKILL.md`, `hi-cross-artifact-validation/SKILL.md`, `hi-{usecase,api-contract,data-model,behavior,command-spec}-discovery/SKILL.md`, `hi-repo-recon/SKILL.md`, `hi-tech-build-audit/SKILL.md`, `hi-repowiki/SKILL.md`, `hi-module-summary-report/SKILL.md`, `hi-reverse/SKILL.md`.

## Implementation Steps
1. Read the lifecycle and discovery `SKILL.md` files to confirm who calls whom (do not infer the chain from names alone).
2. Add the Discovery Artifact Pipeline section with the diagram; label draft-only boundaries on the discovery nodes.
3. Add the Documentation Lifecycle section; state which skill is orchestrator and which are leaves.
4. Update section 0 leaf table and section 4 graph with the new families.
5. Align section 5 HARD-GATEs with README's 6 rows.
6. Extend section 6 General Rules with one line on discovery artifacts: draft-only, evidence-backed, no publication decisions inside leaves.
7. Sanity-render the Mermaid blocks (GitHub preview or `mmdc` if available) before finishing.

## Success Criteria
- Every skill directory appears at least once in `devkit.md` (checker rule `skill-covered-in-devkit`).
- HARD-GATE rows in `devkit.md` and `README.md` are identical.
- No prose version pin remains that can silently drift.

## Test Scope
- Mapped acceptance criteria: (a) 35 skills covered, (b) HARD-GATE parity, (c) Mermaid blocks render, (d) orchestrator/leaf claims traceable to the named `SKILL.md`.
- Expected size: M. Verification: Mermaid render check + Phase 5 checker.

## Risk Assessment
- Risk: inventing the discovery chain. Mitigation: step 1 is a mandatory read of the lifecycle skills; if the chain is not evidenced, document only pairwise relations and note the gap.
- Risk: `hi-reverse` spans RE + migration (66 files) and may not belong in a single linear pipeline. Mitigation: draw it as a parallel entry point feeding Discovery & Artifact, not as a stage.
