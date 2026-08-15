# Audit Output Contract

`tech-stack.json` records technologies with category, name, version or `unknown`, evidence refs, and confidence. `build-report.md` distinguishes verified commands, inferred commands, prerequisites, environment variables, and blockers. `ci-cd-pipelines.md` records trigger, jobs, gates, artifacts, deployment environments, and evidence.

Use artifact envelope `1.0` with producer `hi-tech-build-audit`. Required outputs fail validation when absent; optional outputs become warnings only when their condition applies.
