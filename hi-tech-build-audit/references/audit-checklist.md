# Build Audit Checklist

Inspect only relevant evidence:

- Languages/runtimes: manifests, toolchain files, lockfiles, compiler settings.
- Build: targets, profiles, plugins, generated sources, native extensions, environment inputs.
- Quality: test runners, lint/static analysis, coverage, security gates.
- CI/CD: events, reusable workflows, matrices, caches, artifacts, approvals, deployments.
- Containers/cloud: Dockerfiles, compose, Helm/Kubernetes, serverless, PaaS/IaC configuration.
- Runtime: ports, health checks, migrations, queues, storage, external services.

Depth rules:

- `quick`: verified primary build/run commands and platform detection.
- `standard`: quick plus CI/CD, testing, packaging, and deployment configuration.
- `deep`: standard plus verified API/runtime dependency evidence and risk analysis.

Fast-fail `mind_mcp → graph_mcp → Serena → rg`. Do not repeat failed capability calls or expose infrastructure endpoints in output.
