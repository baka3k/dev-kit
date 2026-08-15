# Knowledge Card Contract

## Directory Structure

Each module produces a directory at `knowledge/<lang>/<Module Name>/` containing:

```
<Module Name>/
├── _module.yaml
├── overview.md
├── architecture_design.md
├── coding_conventions.md
├── tech_stack.md
└── unique_setup_and_commands.md
```

Sub-modules are nested: `<Module Name>/<SubModule Name>/`.

## _module.yaml

```yaml
name: "<Module Name>"
scope: "<one-line purpose>"
files:
  - "path/to/file1.ts"
  - "path/to/file2.ts"
dependencies:
  - "<dependency module name>"
relationships:
  - type: parent | child | peer | depends_on | depended_by
    target: "<module name>"
sub_modules:
  - "<SubModule Name>"
```

File paths are repository-relative. Dependencies list only direct, evidence-verified relationships.

## Card Content Standards

### overview.md
- Purpose and responsibilities (2-5 sentences).
- Module boundaries (what it owns vs what it delegates).
- Key entry points and interfaces.
- Relationship to parent/peer modules.

### architecture_design.md
- Internal structure and key abstractions.
- Design patterns observed (factory, observer, strategy, etc.).
- Data flow within the module.
- Extension points and customization mechanisms.
- Mermaid diagram of internal structure when complexity warrants.

### coding_conventions.md
- Naming conventions observed (files, classes, functions, variables).
- Error handling patterns.
- Testing patterns and test organization.
- Documentation conventions.
- Import/dependency organization.

### tech_stack.md
- Languages and language features used.
- Frameworks and libraries.
- Build tools and configuration.
- External service dependencies.
- Platform/runtime requirements.

### unique_setup_and_commands.md
- Module-specific build commands (when different from project root).
- Test commands for this module.
- Development setup requirements.
- Configuration files specific to this module.
- Omit this file when the module has no unique setup (record in `_module.yaml` as `setup: inherited`).

## Evidence Rules

- Every claim derives from source files listed in `_module.yaml`.
- Patterns are observed from code, not assumed from framework defaults.
- Conventions are reported as observed, not prescribed (unless a linter/formatter config exists).
- Contradictions within the module are noted.

## Quality Gates

1. `_module.yaml` parses and all listed files exist.
2. All card files present (except `unique_setup_and_commands.md` when explicitly inherited).
3. No content references files outside the module's scope without explanation.
4. Mermaid diagrams parse when present.
5. No secrets or sensitive values in any card content.
