# Wiki Page Contract

## File Location

Each page is written to `content/<Section Name>/<Page Title>.md`. Section overview pages share the section folder name.

## Page Structure

Every wiki page follows this structure:

```markdown
<cite>
- path/to/source/file1.ts
- path/to/source/file2.ts
</cite>

# <Page Title>

## Table of Contents
- [Introduction](#introduction)
- ... (auto-generated from headings)

## Introduction
Brief purpose and scope of this page. What the reader will learn.

## <Core Sections>
Content sections vary by page type:

### Architecture Pages
- Overall architecture and design philosophy
- Core components and their responsibilities
- Component interaction model (with Mermaid)
- Data flow architecture
- Extension points and plugin system

### Module Pages
- Module responsibilities and boundaries
- Key abstractions and interfaces
- Internal structure and patterns
- Dependencies and integration points
- Configuration and extension points

### Feature Pages
- Feature overview and user-facing behavior
- Implementation architecture
- Data models and state management
- Error handling and edge cases

### Reference Pages
- Evidence-backed inventory table with stable names and source mappings
- Inputs, outputs, defaults, constraints, errors, and side effects where applicable
- Registration/declaration to handler/consumer trace
- Safe usage examples using placeholders rather than real credentials or endpoints

### Setup and Operations Pages
- Prerequisites and supported platforms
- Ordered, verified commands with working-directory context
- Configuration key names, precedence, validation, and consumers
- Verification, health checks, rollback/recovery, and evidenced failure diagnostics

## Architecture Diagrams
Mermaid diagrams where evidence supports them:
- Architecture overview: `graph TD`
- Dependencies: `graph LR`
- State machines: `stateDiagram-v2`
- Sequences: `sequenceDiagram`

Constraints:
- Max 30 nodes per diagram.
- Max 80 edges per diagram.
- Sanitize labels (no secrets, no real credentials).
- Every diagram has a title and text summary.
- Meaning cannot rely on color.

## Dependency Analysis
What this component/module depends on and what depends on it. Evidence-backed only.

## Troubleshooting Guide
Common issues, error patterns, and resolution guidance derived from code evidence.

## Topic-Specific Requirements

Apply the matching facet requirements in [topic-coverage-contract.md](topic-coverage-contract.md). In particular:

- CLI pages map executables, commands, flags, and build targets to registrations and handlers.
- API and protocol pages map operations/tools/resources/prompts to schemas, handlers, auth, errors, and terminal effects.
- Data/graph pages distinguish declared constraints from inferred relationships and show writers/readers.
- Query/search pages explain syntax, filters, indexes/ranking, result shapes, limits, and fallbacks.
- Incremental/sync pages explain change detection, invalidation, checkpoints, idempotency, retries, conflicts, deletion, and rename behavior when evidenced.
- Testing/deployment pages use verified commands and connect them to CI jobs, artifacts, environments, and diagnostics.

## Evidence Status
Every factual claim is marked: `verified`, `corroborated`, `inferred`, or `unknown`.
```

## Evidence Rules

- Every claim cites at least one source file in the `<cite>` block.
- `<cite>` paths are repository-relative and must reference real files.
- Inferred claims require explicit rationale.
- Contradictions between sources are documented, not silently resolved.
- No fabricated APIs, classes, or behaviors.

## Quality Gates

1. Page has a non-empty `<cite>` block with valid paths.
2. Table of Contents matches actual headings.
3. All Mermaid blocks parse without errors.
4. No secrets, tokens, credentials, or connection strings in content.
5. Evidence status is explicit for every architectural claim.
6. Page is self-contained and navigable without external context.
