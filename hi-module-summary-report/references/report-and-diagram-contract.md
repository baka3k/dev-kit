# Report and Diagram Contract

## Module summary

Include `Architecture Overview`, `Module Dependency Graph`, and `Module Details`. Each module contains responsibility, key technologies, internal structure, internal/external dependencies, risks, and evidence refs.

## Risk assessment

For every risk record severity, likelihood, affected modules, evidence, impact, mitigation, owner when known, and validation action.

## Mermaid

- Architecture uses `graph TD` and layer subgraphs: frontend, backend, data, infrastructure, other.
- Dependency view uses `graph LR`, groups by domain, and uses `import`, `call`, `event`, or `db` edge labels only when evidenced.
- Sanitize node IDs and quote labels. Cap the dependency diagram at 80 highest-evidence edges; record omissions.
- Produce `.mmd` source even when no renderer is available. Rendering is optional and never required for semantic completion.
