---
name: hi-tech-build-audit
description: "Audit a repository's technology stack, build system, dependency management, CI/CD pipelines, deployment targets, and platform assumptions. Use for build onboarding, migration readiness, deployment review, or CI/CD documentation."
---

# Technology and Build Audit

Read [dev-shared/leaf-contract.md](../dev-shared/leaf-contract.md). Produce verified build and deployment evidence. Do not own module reconnaissance or cross-artifact synthesis.

## Inputs

Require a readable absolute `repo_root`. Accept `target_env`: `local`, `container`, `cloud`, `hybrid`, or `auto` (default). Accept `depth`: `quick`, `standard` (default), or `deep`. Default output to `discovery-output/audit-data`.

## Workflow

1. Validate input and output boundaries.
2. Use retrieval rules in [audit-checklist.md](references/audit-checklist.md) and [dev-shared/retrieval-protocol.md](../dev-shared/retrieval-protocol.md). Discover callable metadata; fast-fail unavailable layers once.
3. Inventory languages, runtimes, frameworks, package managers, build systems, dependency locks, generated code, and version constraints.
4. Verify build, test, lint, packaging, and local-run commands from files. Label convention-inferred commands; never present them as verified.
5. Inspect CI/CD triggers, jobs, gates, artifacts, secrets references, environments, and deployment targets.
6. For `deep`, trace API-layer and runtime dependencies only where graph/source evidence establishes them.
7. Redact values of secrets and `.env` entries while preserving key names and evidence locations.
8. Write artifacts per [output-contract.md](references/output-contract.md) and validate required outputs.

## Outputs

- `build-report.md`, `tech-stack.json`, `ci-cd-pipelines.md`, and `artifact-manifest.json` — required.
- `platform-targets.md` — when deployment targets detected.
- `api-dependencies.md` — when `depth=deep`.

Complete only when each claimed command or technology cites repository evidence, required artifacts validate, detected/absent/unknown are distinct, and the manifest reflects partial or blocked evidence honestly.

Return a prerequisite or evidence-gap result to the root when another capability is needed.
