# DevKit

A token-efficient agent skills kit for software engineering workflows. **34 composable skills** plus the `dev-shared` support package, built for Claude Code / Cursor / Continue / Copilot / OpenCode / Qwen Code / Antigravity / Hermes and any agent that reads `SKILL.md`.

## Advanced Capabilities

Integrated with Cortex Harness, DevKit delivers an end-to-end Software Development Life Cycle (SDLC) framework: a unified execution model for planning, implementation, debugging, repository evidence search, security review, scenario generation, discovery-to-documentation pipelines, browser automation, session logging, and other extensible engineering workflows.

For enterprise-scale projects with codebases containing millions of lines of code (LOC) and documentation repositories spanning tens of gigabytes, integration with Cortex Harness is recommended: https://github.com/baka3k/cortex-harness

The pre-configured skills provide native support for hybrid retrieval across both Graph Databases (GraphDB) and Vector Databases (VectorDB). By combining graph-based code relationship queries with semantic vector search, the system delivers high-quality contextual retrieval, significantly accelerating project onboarding, codebase comprehension, and AI-assisted software development.

## Installation

```bash
npx skill-dev                       # default: baka3/dev-kit on GitHub
npx skill-dev <url>                 # any supported source
npx skill-dev owner/repo            # GitHub shorthand
npx skill-dev ./local-skills        # local directory
npx skill-dev https://example.com   # well-known endpoint
npx skill-dev --no-manifest         # skip AGENTS.md / CLAUDE.md auto-install
npx skill-dev -h                    # help
npx skill-dev -v                    # version
```

```bash
$ npx skill-dev
┌   devkit   Dev Kit Installer
│
◆  Select skills
│  ◼ hi-craft
│  ◼ hi-debug
│  ◼ hi-scout
│  ◼ hi-fix
│  ◼ hi-knows
│  ◼ hi-log
│  ◼ hi-plan (Should ALWAYS activate before implementing ANY implement, or fix.)
│  ◼ hi-predict
│  ◼ hi-problem-solving
│  ◼ hi-scenario
│  ◼ hi-security
│  ◼ hi-sequential-thinking
│  ◼ typesafe-ai
└ ....

◇ Select target agent
❯ Claude Code
  OpenCode
  Qwen Code
  GitHub Copilot
  Cursor
  Continue
  Antigravity
  Hermes
  Generic

◇ Install location
❯ Global (~/.claude/skills)
  Current project

◇ Summary
Agent: Claude Code
Skills: 12 selected
Location: Global
Install? (Y/n)
```

During installation, select the skills, the target agent, and the install location. DevKit supports global and project-local installation.

The `dev-shared/` support package holds the cross-skill contracts (`leaf-contract.md`, `delegation-contract.md`, `orchestrator-contract.md`, `retrieval-protocol.md`, `test-budget.md`, `graph-function-selection.md`, `jev-contract.md`, `roles/…`) that `hi-*` skills reference via `../dev-shared/…` paths. It carries its own marker `SKILL.md` (`metadata.support: true`), so `skill-dev` ships it in every install that includes skills referencing it — the packages land as siblings in the target skills dir and the relative links stay resolvable.

## Custom Sources

`skill-dev` uses source providers instead of requiring a local `git clone`.

| Provider | Example | Notes |
| --- | --- | --- |
| GitHub | `https://github.com/owner/repo` | Uses GitHub tree and raw file APIs. |
| GitLab | `https://gitlab.com/owner/repo` | Uses GitLab repository tree APIs. |
| Well-known | `https://example.com` | Reads `/.well-known/agent-skills/index.json`. |
| Local | `./my-skills` | Reads `SKILL.md` files from a directory tree. |

A skill is any directory containing a `SKILL.md` with YAML frontmatter:

```markdown
---
name: Code Review
description: Carefully review code for correctness, performance, and style.
---

# Code Review
```

Skill repositories may lay out skills under `skills/`, `skills/.curated/`, `.agents/skills/`, or at the repo root.

## How Installation Works

For each selected skill and target agent, the installer:

1. Writes the skill to the canonical `.agents/skills/<name>` location.
2. Links the target agent skills directory to that canonical copy when possible.
3. Falls back to recursive copy on Windows or when links are unavailable.

The result is one canonical skill copy that multiple agents can consume.

## Manifest Files

Whenever the source repo (or local directory / well-known endpoint) carries `AGENTS.md` or `CLAUDE.md` at its root, `skill-dev` automatically copies them. Each file routes to its own "natural home" so the install mirrors how the skills directory is laid out:

| File | Global scope target | Why |
| --- | --- | --- |
| `AGENTS.md` | `~/.agents/AGENTS.md` | Universal, agent-neutral. Sibling of the canonical `~/.agents/skills/` so the same content is shared by every agent. |
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Claude-Code-specific. Sits alongside the `skills/` symlink that points into `~/.agents/skills/`. Respects `$CLAUDE_CONFIG_DIR` if set. |
| Other (e.g. `GEMINI.md`) | `~/.agents/` (fallback) | Unknown filenames default to the canonical `~/.agents/` — add a new switch case in `src/install/manifest.ts` to route a new manifest elsewhere. |

For **project scope** every file lands at the project root (`<cwd>/AGENTS.md`, `<cwd>/CLAUDE.md`) — same convention as the rest of the ecosystem.

`AGENTS.md` is the single source of truth for the operating directives. `CLAUDE.md` and `.cursorrules` are **generated from it** with `node scripts/sync-manifests.mjs`, because the installer only ships `AGENTS.md` and `CLAUDE.md` — generating the third keeps the Cursor copy from drifting. Language policy is stated once, in `AGENTS.md`: skill documentation and code comments are English; chat replies follow the operator's language.

The directives themselves:

```
# Root Agent: Context Search Directive

**Objective:** Gather project context before executing tasks.
**Fast-Fail Rule:** If a tool is missing or disconnected -> SKIP IMMEDIATELY to the next level (Do NOT retry).

## Strict Priority Flow
*Proceed to the next step ONLY if the current step yields no results or the tool is unavailable.*

1. **`mind_mcp`**: Retrieve project docs, concepts, and foundational knowledge.
2. **`graph_mcp` (`semantic_search`,`explore_graph`)**: Find codebase relationships and logic (rely on semantics, not exact string matching).
3. **`serena` (search)**: Broad codebase search.
4. **`grep`/`rg` (Native tools)**: File system sweep for exact strings (Absolute last resort).

## Mandatory Rules
- **No Hallucination:** If the entire search chain fails, stop and ask the user for details. Never fabricate context.
- **Merge Context:** Prioritize structured data from `graph_mcp` if tools return overlapping information.
- **No Assumptions:** Ask, don't guess. Highlight tradeoffs and admit confusion.
- **Minimal Code:** Solve only the target problem. No over-engineering.
- **Strict Scope:** Touch only what's necessary. Clean up your own mess.
- **Success Criteria:** Iterate until explicitly verified.
```

**NOTICE**: For complex codebases exceeding millions of Lines of Code and massive documentation scale (tens of gigabytes), you need mind_mcp & graph_mcp - please integrate with **cortex-harness** (https://github.com/baka3k/cortex-harness).

- mind_mcp: **GraphRAG** – Handles project document processing and retrieval.
- graph_mcp: **GraphCode** – Maps the source code call graph, visualizing function-level node interactions.

About Serena - refer https://github.com/oraios/serena

## Supported Agents

| Agent | Global install | Project install |
| --- | --- | --- |
| Claude Code | `~/.claude/skills` | `.claude/skills` |
| OpenCode | `~/.config/opencode/skills` | `.opencode/skills` |
| Qwen Code | `~/.qwen/skills` | `.qwen/skills` |
| GitHub Copilot | `~/.copilot/skills` | `.github/skills` |
| Cursor | `~/.cursor/skills` | `.cursor/skills` |
| Continue | `~/.continue/skills` | `.continue/skills` |
| Antigravity | `~/.gemini/skills` | `.gemini/skills` |
| Hermes | `~/.hermes/profiles/default/skills` | `.hermes/skills` |
| Generic | `~/.devkit/skills` | `.devkit/skills` |

Set `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, or `XDG_CONFIG_HOME` to override the base config directory.

## What Is Included

34 skills in six groups, plus the `dev-shared` support package. Every row is one directory under the repo root.

### Core Workflow (4)

| Directory | Skill name | Purpose |
| --- | --- | --- |
| `hi-plan/` | `hi-plan` | Implementation plans, architecture plans, phased roadmaps, and plan validation. |
| `hi-craft/` | `hi-craft` | Feature implementation workflow: plan, implement, test, and finalize. |
| `hi-fix/` | `hi-fix` | Bug, test, CI, type, lint, UI, and runtime issue resolution. |
| `hi-debug/` | `hi-debug` | Root-cause debugging for failures, logs, CI, databases, performance, and system behavior. |

### Evidence And Exploration (4)

| Directory | Skill name | Purpose |
| --- | --- | --- |
| `hi-scout/` | `hi-scout` | Traceable evidence from project docs, semantic code search, symbols, call paths, dependency analysis, external web/GitHub/image research, and parallel exploration. |
| `hi-knows/` | `hi-knows` | Unified knowledge retrieval from Git, MCP, and memory files. |
| `hi-docs-seeker/` | `hi-docs-seeker` | Current, authoritative technical documentation for libraries, frameworks, APIs, versions, migrations, and compatibility. |
| `hi-repo-recon/` | `hi-repo-recon` | Map an unfamiliar repository into a module inventory, entry-point map, and key-function catalog. |

### Discovery And Artifact (7)

The five leaf skills in this group are **draft-only**: they produce evidence-backed artifacts and never publish, deploy, or modify implementations. Publication is owned by an orchestrator with explicit human approval.

| Directory | Skill name | Purpose |
| --- | --- | --- |
| `hi-usecase-discovery/` | `hi-usecase-discovery` | Business use cases per source module: actors, permissions, rules, flows, outcomes, IDs, tests, coverage. |
| `hi-behavior-modeling/` | `hi-behavior-modeling` | Technical behavior as sequence, activity, state-machine, and event-flow documentation. |
| `hi-api-contract-discovery/` | `hi-api-contract-discovery` | HTTP and asynchronous API contracts: OpenAPI/AsyncAPI drafts, endpoints, messages, schemas, auth, errors. |
| `hi-data-model-discovery/` | `hi-data-model-discovery` | Logical and physical data models, ERDs, entity and field inventories, data dictionaries, ownership, lifecycle, migration gaps. |
| `hi-command-spec-discovery/` | `hi-command-spec-discovery` | Special command and protocol wire-format specs: APDU/TLV fields, CLA/INS/P1/P2/Lc/Le framing, opcodes, status words, command-specific models. |
| `hi-reverse/` | `hi-reverse` | Reverse-engineer C and C++ modules into validated use-case, module, and C++-to-Java migration artifact packages. |
| `hi-cross-artifact-validation/` | `hi-cross-artifact-validation` | Read-only validation across discovery outputs: stable-ID resolution, actor/auth alignment, state-lifecycle matches, schema compatibility. |

### Documentation Lifecycle (6)

| Directory | Skill name | Purpose |
| --- | --- | --- |
| `hi-maintenance-docs/` | `hi-maintenance-docs` | Orchestrate a complete, navigable, evidence-backed maintenance documentation pack across nine stages. |
| `hi-document-lifecycle/` | `hi-document-lifecycle` | Single-domain lifecycle: generate, clarify/refine, review/update, with pause/resume. |
| `hi-document-refinement/` | `hi-document-refinement` | Find ambiguity, terminology gaps, missing semantics, and under-specified diagrams; apply validated clarifications to an isolated candidate revision. |
| `hi-document-review-resolution/` | `hi-document-review-resolution` | Assign a disposition to every review comment and apply accepted changes idempotently. |
| `hi-repowiki/` | `hi-repowiki` | Generate or update the repository wiki: architecture, installation, configuration, CLI/build automation, APIs, testing, deployment, modules. |
| `hi-module-summary-report/` | `hi-module-summary-report` | Synthesize existing module-inventory and tech-audit artifacts into an architecture summary, per-module breakdown, and risk assessment. |

### Analysis And Review (6)

| Directory | Skill name | Purpose |
| --- | --- | --- |
| `hi-scenario/` | `hi-scenario` | Edge-case and test-scenario generation across 12 dimensions. |
| `hi-brainstorm/` | `hi-brainstorm` | Independent expert ideation, rebuttal, weighted scoring, and solution selection before implementation. |
| `hi-predict/` | `hi-predict` | Five-persona pre-analysis before risky features, refactors, or releases. |
| `hi-security/` | `hi-security` | STRIDE + OWASP security audit with MCP-assisted code analysis and optional iterative auto-fix. |
| `hi-sequential-thinking/` | `hi-sequential-thinking` | Step-by-step reasoning with revision, branching, and hypothesis testing. |
| `hi-problem-solving/` | `hi-problem-solving` | Structured techniques for stuck points, recurring patterns, constraints, and scale uncertainty. |

### Utilities And Integrations (7)

| Directory | Skill name | Purpose |
| --- | --- | --- |
| `hi-log/` | `hi-log` | Session log entries for recent changes, decisions, impacts, and reflections. |
| `hi-project-organization/` | `hi-project-organization` | File placement, output naming, directory organization, and Markdown structure. |
| `hi-tech-build-audit/` | `hi-tech-build-audit` | Technology stack, build system, dependency management, CI/CD pipelines, deployment targets, platform assumptions. |
| `hi-chrome-devtools/` | `hi-chrome-devtools` | Browser automation through Puppeteer CLI scripts with persistent sessions, screenshots, performance, network, scraping, forms, auth, and debugging. |
| `hi-cortex/` | `hi-cortex` | Cortex Harness setup, project config, code/doc sync, and MCP lifecycle for graph/vector retrieval. |
| `slide-kit/` | `slide-kit` | Generate `.pptx` slide decks in the Modernization corporate style, strictly brand-neutral. |
| `typesafe-ai/` | `typesafe-ai` | Build AI-powered features with TypeSafe System One models (Jev): typed judgments as programming primitives. |

### Support Package

| Directory | Skill name | Purpose |
| --- | --- | --- |
| `dev-shared/` | `dev-shared` | Cross-skill contracts and role briefs. Marked `metadata.support: true` — installed alongside the skills that reference it, never activated directly. |

## Commands And Invocation

Skills are invoked by slash command or by bare name, depending on the harness. A flag is optional unless the row says otherwise. Rows without flags take a natural-language task.

| Skill | Invocation | Modes / flags | Subcommands |
| --- | --- | --- | --- |
| `hi-plan` | `/hi-plan [task]` | `--full`, `--hard`, `--parallel`, `--two`, `--no-tasks` (default: fast) | `archive`, `red-team <path>`, `validate <path>` |
| `hi-craft` | `/hi-craft [task \| plan path]` | `--full`, `--parallel`, `--review`, `--auto`, `--no-test`, `--test-budget=N` (default: fast) | — |
| `hi-fix` | `/hi-fix [issue]` | `--standard`, `--deep`, `--parallel`, `--review` (default: quick) | — |
| `hi-debug` | `/hi-debug [error or issue description]` | — | — |
| `hi-scout` | `/hi-scout [question \| symbol \| path \| SQL \| impact target \| repo URL \| docs topic \| image]` | `--code`, `--doc`, `--ask`, `--deep`, `--impact`, `--external`, `--parallel` | — |
| `hi-knows` | `/hi-knows [target]` | intent: `why-changed`, `impact-analysis`, `architecture-context`, `history-trace` | — |
| `hi-docs-seeker` | `/hi-docs-seeker [question]` | mode: `topic`, `version`, `migration`, `compatibility`, `overview` | — |
| `hi-repo-recon` | `/hi-repo-recon [repo path]` | `scope`: `backend`, `frontend`, `infra`, `data`, `all`; `depth`: `quick`, `standard`, `deep` | — |
| `hi-usecase-discovery` | `/hi-usecase-discovery [module name]` | `output_dir` (default `usecase`), `parser_type` (default `cplus`) — draft-only | — |
| `hi-behavior-modeling` | `/hi-behavior-modeling [module \| symbol \| use-case anchor]` | requested modes: `sequence`, `activity`, `state-machine`, `event-flow` — draft-only | — |
| `hi-api-contract-discovery` | `/hi-api-contract-discovery [service \| module \| endpoint scope]` | protocol mode: HTTP, asynchronous; visibility `internal` — draft-only | — |
| `hi-data-model-discovery` | `/hi-data-model-discovery [database \| module \| entity scope]` | visibility `internal` — draft-only | — |
| `hi-command-spec-discovery` | `/hi-command-spec-discovery [module or command anchor]` | command name/opcode/header, protocol hints, visibility `internal` — draft-only | — |
| `hi-reverse` | `/hi-reverse [module \| use-case \| migration]` | `--check-catalog`, `--profile`, `--module`, `--use-case`, `--condition`, `--output-root`, `--next`, `--summary` | `hi-reverse-init`, `hi-reverse-plan`, `hi-reverse-metrics`, `hi-reverse-validate-artifact`, `hi-reverse-validate-package` |
| `hi-cross-artifact-validation` | `/hi-cross-artifact-validation [output_root]` | `domains`, `strict` (default `false`), `output_dir` (default `cross-validation`) | — |
| `hi-maintenance-docs` | `/hi-maintenance-docs [repo_root]` | inputs: `scope`, `audience`, `visibility`, requested modes, `review_required` (default `true`) | — |
| `hi-log` | `/hi-log [topic]` | `--since <ref>`, `--scope <dir>` | — |
| `hi-document-lifecycle` | `/hi-document-lifecycle [domain]` | phase: `generate`, `clarify_refine`, `review_update`; resumes from checkpoint | — |
| `hi-document-refinement` | `/hi-document-refinement [draft]` | `mode`: `analyze`, `apply` | — |
| `hi-document-review-resolution` | `/hi-document-review-resolution [revision + comments]` | dispositions: `accepted`, `rejected`, `needs_information`, `duplicate`, `stale`, `out_of_scope`, `unsupported_by_evidence` | — |
| `hi-repowiki` | `/hi-repowiki [repo]` | `mode`: `generate`, `update`, `plan-only`; `language`: `en`, `zh`; `template`, `coverage_profile`, `--resume` | — |
| `hi-module-summary-report` | `/hi-module-summary-report [artifacts]` | `audience`: `engineering`, `management`, `mixed`; `depth`: `executive`, `standard`, `detailed`; `mermaid` (default `true`) | — |
| `hi-scenario` | `/hi-scenario [feature or module]` | depth: `quick` (default), `deep`; optional focus dimensions and severity filter | — |
| `hi-brainstorm` | `/hi-brainstorm [decision or topic]` | modes: `quick` (3 lenses), `standard` (default, 5 lenses), `deep` | — |
| `hi-predict` | `/hi-predict [change proposal]` | `--files <glob>`, concern areas, depth: `quick`, `deep` | — |
| `hi-security` | `/hi-security [source root + scope]` | mode: `audit`, `audit-fix`; focus: `auth`, `data`, `api`, `infra`, `all`; max fix iterations (default 10) | — |
| `hi-cortex` | `/hi-cortex [setup \| status \| add-code \| sync-code \| add-doc \| sync-doc \| start-mcp \| stop-mcp \| doctor] [project path or repo URL]` | `--project-dir`, `--name`, `--sync-mode`, `--git`, `--full-scan` | `dev init`, `dev sync code add`, `dev sync doc add`, `dev mcp`, `dev start`, `dev stop` |
| `hi-chrome-devtools` | `/hi-chrome-devtools [url or task]` | `--headless`, `--url`, `--output`, `--ref`, `--action`, `--timeout`, `--wait-until`, `--wait-for-login`, `--close` | scripts: `navigate`, `screenshot`, `click`, `fill`, `evaluate`, `snapshot`, `console`, `network`, `performance` |
| `slide-kit` | `/slide-kit [deck request]` | `--output-dir` | `scripts/gen_deck.py spec.json -o deck.pptx`, `scripts/render_preview.py` |
| `hi-sequential-thinking` | `/hi-sequential-thinking [problem]` | — | — |
| `hi-problem-solving` | `/hi-problem-solving [problem]` | — | — |
| `hi-project-organization` | `/hi-project-organization [path]` | modes: `advisory`, `organize` | — |
| `hi-tech-build-audit` | `/hi-tech-build-audit [repo path]` | `target_env`: `local`, `container`, `cloud`, `hybrid`, `auto`; `depth`: `quick`, `standard`, `deep` | — |
| `typesafe-ai` | `/typesafe-ai [feature intent]` | primitives: `choice`, `noul`, `score` | — |

## Evidence Retrieval (hi-scout)

`hi-scout` is the shared evidence layer for questions that require verified repository context. Use it before planning or changing code when the answer depends on codebase structure, architecture, cross-file behavior, impact analysis, project documentation, or an external source.

The expected context search chain is:

1. `mind_mcp` for project documents, concepts, and foundational knowledge.
2. `graph_mcp` semantic search for code relationships and logic.
3. `serena` search for broad codebase discovery.
4. `rg` or `grep` only as the final exact-string filesystem sweep.

If one level is missing or disconnected, skip immediately to the next level. If the full chain yields no evidence, stop and ask for more details instead of guessing.

`hi-scout` is intentionally evidence-only. It gathers and verifies context; orchestration always stays with the calling skill or agent, and the skill never plans or implements. Sequential search is the default; `--external` and `--parallel` are explicit escalation modes.

Recommended modes:

| Mode | Use when |
| --- | --- |
| `--code` | You need symbol, file, call path, or implementation evidence. |
| `--doc` | You need project docs, concepts, requirements, or architectural notes. |
| `--ask` | You need a short answer from the nearest sufficient evidence. |
| `--deep` | You need to reconcile code and docs. |
| `--impact` | You need dependency, blast-radius, caller, or workflow impact evidence. |
| `--external` | The target is web docs, a GitHub repo, or an image/UI, reached through MCP tools. |
| `--parallel` | The target splits into 1-5 independent scopes worth running as separate agents. |

## Typical Workflows

```text
Implement feature:    hi-craft -> hi-plan --fast -> implement -> test -> hi-log
Fix bug:              hi-fix -> hi-scout -> diagnose -> fix -> verify
Plan architecture:    hi-plan --full -> hi-scout --deep -> phases -> validate
Investigate failure:  hi-debug -> logs/traces -> root cause -> fix recommendation
Impact analysis:      hi-scout --impact -> hi-predict -> scoped plan
External research:    hi-scout --external --parallel -> docs/repo/image evidence -> next step
Security audit:       hi-security -> findings -> optional auto-fix -> re-verify
Scenario coverage:    hi-scenario -> edge cases -> tests or review checklist
Browser task:         hi-chrome-devtools -> inspect/click/screenshot/network
Command spec:         hi-command-spec-discovery -> APDU/TLV + opcode/status-word draft -> hi-cross-artifact-validation
Doc pack:             hi-maintenance-docs -> recon/audit -> use cases/API/data/command -> behavior -> validation -> refinement
Repo wiki:            hi-repowiki -> recon + tech-build-audit -> module summary -> /repowiki/
```

## Workflow Diagrams

Mode matrices, per-skill flow diagrams, the cross-skill integration graph, delegation semantics, and pipeline details live in [devkit.md](devkit.md).

## HARD-GATEs

| Skill | HARD-GATE | Violation behavior |
| --- | --- | --- |
| `hi-craft` | Do not edit until a reviewed plan exists, unless the user explicitly skips planning. | Stop, create or reuse a plan, then continue. |
| `hi-fix` | Do not fix before locating the failure and identifying root cause. | Return to explore/diagnose; after 3 failed fix attempts, question architecture with the user. |
| `hi-plan` | Scan active plans first and record relevant `blockedBy` / `blocks` relationships. | Update the related plans before producing the new plan. |
| `hi-scout` | Provide traceable evidence only; do not invent context or own implementation decisions. | Report search coverage and ask for details if evidence is missing. |
| `hi-security` | Security findings need source evidence and severity-ranked remediation. | Do not auto-fix outside the requested audit/fix scope. |
| `hi-project-organization` | Do not override established project layout without evidence. | Use existing conventions or return an advisory recommendation. |

## Folder Structure

```text
dev-kit/
├── AGENTS.md                      # Single source of truth for operating directives
├── CLAUDE.md                      # Generated from AGENTS.md
├── .cursorrules                   # Generated from AGENTS.md
├── LICENSE                        # MIT
├── Makefile                       # install / install-latest / doctor / check-docs / sync-manifests / wiki / prepare
├── README.md                      # This file: catalog, install, invocation
├── devkit.md                      # Workflow diagrams and cross-skill integration
├── scripts/
│   ├── check-kit-docs.mjs         # Documentation drift checker (make check-docs)
│   ├── sync-manifests.mjs         # Regenerate CLAUDE.md and .cursorrules from AGENTS.md
│   └── gen-wiki-pages.mjs         # Generate the compact wiki guides (make wiki)
├── docs/
│   ├── logs/                      # hi-log session entries
│   └── plans/                     # hi-plan plan directories
├── wiki/
│   ├── en/                        # English skill guides
│   └── vi/                        # Vietnamese skill guides
├── dev-shared/                    # Support package: contracts and role briefs
│   ├── delegation-contract.md
│   ├── orchestrator-contract.md
│   ├── leaf-contract.md
│   ├── retrieval-protocol.md
│   ├── test-budget.md
│   ├── graph-function-selection.md
│   ├── jev-contract.md
│   ├── jev/                       # jev_ask.py adapter and recipes
│   └── roles/                     # researcher, implementer, reviewer, log-writer
├── hi-plan/                       # Core workflow
├── hi-craft/
├── hi-fix/
├── hi-debug/
├── hi-scout/                      # Evidence and exploration
├── hi-knows/
├── hi-docs-seeker/
├── hi-repo-recon/
├── hi-usecase-discovery/          # Discovery and artifact (draft-only leaves)
├── hi-behavior-modeling/
├── hi-api-contract-discovery/
├── hi-data-model-discovery/
├── hi-command-spec-discovery/
├── hi-reverse/
├── hi-cross-artifact-validation/
├── hi-maintenance-docs/           # Documentation lifecycle
├── hi-document-lifecycle/
├── hi-document-refinement/
├── hi-document-review-resolution/
├── hi-repowiki/
├── hi-module-summary-report/
├── hi-scenario/                   # Analysis and review
├── hi-brainstorm/
├── hi-predict/
├── hi-security/
├── hi-sequential-thinking/
├── hi-problem-solving/
├── hi-log/                        # Utilities and integrations
├── hi-project-organization/
├── hi-tech-build-audit/
├── hi-chrome-devtools/
├── hi-cortex/
├── slide-kit/
└── typesafe-ai/
```

## Key Conventions

- Evidence comes before assumptions. Prefer traceable context from `mind_mcp`, `graph_mcp`, `serena`, then native search.
- Keep changes scoped. Skills should solve the target problem without unrelated refactors or cleanup.
- Use the lightest useful mode first. Escalate to deep, review, parallel, or impact modes when risk or uncertainty justifies it.
- `hi-scout` gathers evidence; implementation and final decisions stay with the orchestrating skill or agent.
- Discovery artifacts are draft-only. Only an orchestrator with explicit human approval publishes a document.
- Every workflow that mutates the repository ends with a commit plus a `hi-log` entry under `docs/logs/`.
- Known process gap: `docs/logs/` still holds a single entry while `hi-log` is a mandatory finalize step. Logging discipline, not tooling, is what is missing.
- Human-facing skill output may be localized by the calling agent. Technical artifacts, identifiers, paths, and commands stay precise.

## Adding A Skill

1. Create `your-skill/SKILL.md` with `name`, `description`, `argument-hint` when the skill takes modes or flags, and `metadata.version` / `metadata.author`.
2. Add `references/` when the skill needs supporting procedures or deeper instructions.
3. Add `scripts/` only for reusable automation that the skill should call instead of retyping.
4. Add `agents/openai.yaml` when the skill should appear in an agent picker.
5. Run `make check-docs` — it verifies the catalog entry, the folder tree, frontmatter, internal links, and HARD-GATE parity.

The frontmatter convention. `make check-docs` validates it with regex checks (the frontmatter is not parsed as YAML):

| Field | Level | Rule |
| --- | --- | --- |
| `name` | top level | Must equal the directory name. Checked. |
| `description` | top level | Must be present and non-empty; drives skill routing. Presence is checked, wording is not. |
| `argument-hint` | top level | Must be present and non-empty on every skill; use the real mode/flag spellings. Checked. |
| `license` | top level | Only where a license is actually known. Not checked. |
| `metadata.version` | under `metadata` | Required for every skill; start at `1.0.0`. Checked. |
| `metadata.last_updated` | under `metadata` | Required; `YYYY-MM-DD`. Checked. |
| `metadata.author` | under `metadata` | Required. Checked. |
| `metadata.support` | under `metadata` | `true` only in `dev-shared/`, which is exempt from the version rule; anywhere else it is a finding. Checked. |

`hooks:` is advisory metadata, not an executable contract. `hi-predict`, `hi-scenario`, and `hi-security` declare pre/post guards (`mcp-health-check`, `input-validation`, `output-redaction`, `cleanup-handler`) that document intended lifecycle guards for harnesses that support hooks; nothing in this kit consumes or executes them.

## Development

```bash
make install         # Install skills from this local checkout via skill-dev
make install-latest  # Install the newest skills from GitHub (baka3/dev-kit)
make doctor          # Health check: git/node/npx, uv, skills, Cortex 'dev', docs drift
make check-docs      # Verify README/devkit.md/manifests/wiki against the real skill tree
make sync-manifests  # Regenerate CLAUDE.md and .cursorrules from AGENTS.md
make wiki            # (Re)generate wiki guides owned by scripts/gen-wiki-pages.mjs
make prepare         # Clone cortex-harness and install 'dev' (no-op if installed)
```

`make check-docs` runs 13 drift rules: catalog completeness (including the `name` column), count, duplicate headings, folder-tree accuracy (including non-directory entries), internal links, frontmatter convention, `argument-hint` presence on every skill, documented flags existing in their skill, Commands-table coverage of every skill, HARD-GATE parity between README and `devkit.md`, manifest sync, wiki coverage, and wiki freshness against the skill sources. `make doctor` includes it, so setup and health checks fail on drift.

The `wiki/` guides come from two sources: hand-written deep dives (kept as-is — the generator only rewrites pages carrying its marker, and only `--adopt <skill>` takes one over) and pages generated from each `SKILL.md` by `scripts/gen-wiki-pages.mjs`. To document a new skill, add its Vietnamese one-liner and its relations to that script, then run `make wiki`. For a full repository wiki instead of per-skill guides, use `hi-repowiki`.

## Reference Docs

| Doc | What it contains |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Root agent context-search directive and mandatory operating rules. |
| [devkit.md](devkit.md) | Workflow diagrams, mode matrices, delegation semantics, cross-skill integration. |
| [wiki/](wiki/) | Per-skill guides in English and Vietnamese. |
| [docs/plans/](docs/plans/) | Active and archived implementation plans. |

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
