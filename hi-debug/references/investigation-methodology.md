# Investigation Methodology

Five-step structured investigation for system-level issues, incidents, and multi-component failures.

**Use when:** server 500s or unexpected responses, system behavior changed without code change, multi-component failures, need to understand "what happened" before fixing.

## Step 1: Initial Assessment

**Gather scope and impact before diving in.**

- Collect symptoms (errors, affected endpoints, user reports), identify affected components (services, DBs, queues), determine timeframe (correlate with deployments), assess severity (users affected, data at risk), check recent changes (git log, deploys, config)

```bash
gh run list --limit 10                    # recent deployments
git log --oneline -20 --since="2 days ago" # recent commits
git diff HEAD~5 -- '*.env*' '*.config*' '*.yml' '*.yaml' '*.json'  # config changes
```

## Step 2: Data Collection

**Gather evidence systematically before analysis.**

- Server/app logs (filter by timeframe/components), CI/CD pipeline logs (`gh run view <id> --log-failed`), database state (recent migrations, relevant tables), system metrics (CPU, memory, disk, network), external dependencies (third-party API status, DNS, CDN)

```bash
gh run list --workflow=<workflow> --limit 5
gh run view <run-id> --log-failed
gh run view <run-id> --log > /tmp/ci-logs.txt
```

For codebase: read `docs/codebase-summary.md` if exists and <2 days old, otherwise use `hi:repomix`; use `/hi:ciu` to find relevant files; use `hi:docs-seeker` for package docs.

## Step 3: Analysis Process

**Correlate evidence across sources.**

- Reconstruct timeline chronologically across all log sources, identify patterns (recurring errors, timing, affected segments), trace execution path through system components, analyze database (query performance, relationships, integrity), map dependencies (which components depend on failing one)

Key questions: correlate with deployments? intermittent or consistent? all users or subset? related upstream/downstream errors?

## Step 4: Root Cause Identification

**Systematic elimination with evidence.**

- List hypotheses ranked by evidence strength, test each with smallest experiment, validate with evidence (logs, metrics, reproduction), consider environmental factors (race conditions, resource limits, config drift), document the full event chain

**Avoid:** fixing first hypothesis without testing alternatives.

## Step 5: Solution Development

**Design targeted, evidence-backed fixes.**

- Immediate fix (hotfix, rollback, config change) to restore service, root cause fix to address underlying issue permanently, preventive measures (monitoring, alerting, validation), verification plan for production

Prioritize impact × urgency: restore service → fix root cause → prevent recurrence.

## Integration with Code-Level Debugging

When investigation narrows to code: switch to `systematic-debugging.md` (fix), `root-cause-tracing.md` (deep stack), `defense-in-depth.md` (after fix), then `verification.md` (always last).
