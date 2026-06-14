# Log & CI/CD Analysis

## GitHub Actions

```bash
gh run list --limit 10                                # recent runs (all workflows)
gh run list --workflow=ci.yml --limit 5               # specific workflow
gh run view <run-id>                                  # run details
gh run view <run-id> --log-failed                     # failed job logs only
gh run view <run-id> --log > /tmp/ci-full.txt         # full logs
gh run rerun <run-id> --failed                        # rerun failed jobs
```

### Common CI/CD Failure Patterns

| Pattern | Likely Cause | Investigation |
|---------|-------------|---------------|
| Passes locally, fails CI | Environment diff | Check Node/Python version, OS, env vars |
| Intermittent failures | Race conditions, flaky tests | Run 3x, check timing, shared state |
| Timeout failures | Resource limits, infinite loops | Check resource usage, add timeouts |
| Permission errors | Token/secret misconfiguration | Verify `GITHUB_TOKEN`, secret names |
| Dependency install fails | Registry issues, version conflicts | Check lockfile, registry status |
| Build succeeds, tests fail | Test environment setup | Check test config, DB setup, fixtures |

### Analyzing Failed Steps

- Identify failing step: `gh run view <id>` shows step-by-step status
- Get focused logs: `gh run view <id> --log-failed`; search for `Error:`, `FAIL`, `exit code`, stack traces
- Check annotations: `gh api repos/{owner}/{repo}/check-runs/{id}/annotations`

## Server & Application Log Analysis

**Collection strategy:** identify log locations, filter by incident timeframe, correlate request IDs across services, look for patterns (repeated errors, rate changes, unusual payloads).

**Structured queries** (PostgreSQL examples; use Grep tool on plain logs):

```bash
# Slow queries
psql -c "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
# Active connections
psql -c "SELECT count(*), state FROM pg_stat_activity GROUP BY state;"
```

**Cross-source correlation:** align timestamps across sources (timezone-aware), build timeline (first error → propagation → user impact), identify trigger (what changed immediately before?), map blast radius (affected services/endpoints).

**Error pattern recognition:** sudden spike → deploy/config/external dep; gradual increase → resource leak/data growth; periodic → cron/scheduled; single endpoint → code/data; all endpoints → infra/db/network.

**Key log fields to prioritize:** timestamp, level, error message, stack trace, request ID, user ID, endpoint, response code, duration.

## Evidence Preservation

Always capture for the diagnostic report: exact error messages and stack traces, timestamps and request IDs, before/after comparison (normal vs error), counts and frequencies.
