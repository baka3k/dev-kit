---
name: dev-shared
description: "Shared contracts and role briefs referenced by other DevKit skills via ../dev-shared/ paths (delegation, orchestrator, leaf, retrieval, graph selection). Support package: install alongside hi-* skills; never activate directly."
metadata:
  author: baka3k
---

# DevKit Shared Contracts

This directory is not an invocable skill. It holds the cross-skill contracts that
other skills reference with relative paths (`../dev-shared/...`), so it must be
installed as a sibling of the skills that use it.

- `delegation-contract.md` — probe → role brief → spawn/inline → receipt. Every worker launch follows this.
- `orchestrator-contract.md` — ownership, worker constraints, failure/resume semantics for lifecycle orchestrators.
- `leaf-contract.md` — evidence-backed artifacts, local manifest, completion conditions for leaf skills.
- `retrieval-protocol.md` — layered search order shared by discovery skills.
- `graph-function-selection.md` — when to use which `graph_mcp` function.
- `roles/` — paste-into-prompt briefs for delegated roles (`researcher`, `implementer`, `reviewer`).

Skills upgrade these files by editing them here; the installer ships them verbatim.
