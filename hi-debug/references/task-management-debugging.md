# Debug Task Management Patterns

Track investigation and debugging pipelines via Claude Native Tasks (TaskCreate, TaskUpdate, TaskList).

## When to Create Tasks

| Debug Scope | Tasks? | Rationale |
|-------------|--------|-----------|
| Single bug, one file | No | Systematic debugging handles directly |
| Multi-component investigation (3+ steps) | Yes | Track assess → collect → analyze → fix → verify |
| Parallel log/data collection agents | Yes | Coordinate independent evidence gathering |
| CI/CD failure with 3+ possible causes | Yes | Track hypothesis elimination |

**3-Task Rule:** Skip task creation when investigation has <3 meaningful steps.

## Investigation Pipeline as Tasks

```
TaskCreate: "Assess incident scope"      → pending
TaskCreate: "Collect logs and evidence"  → pending, blockedBy: [assess]
TaskCreate: "Analyze root cause"         → pending, blockedBy: [collect]
TaskCreate: "Implement fix"              → pending, blockedBy: [analyze]
TaskCreate: "Verify fix resolves issue"  → pending, blockedBy: [fix]
```

Maps to investigation-methodology.md 5-step process. Auto-unblocks as each step completes.

## Task Schemas

- **Assess:** gather symptoms, identify affected components, check recent changes (see investigation-methodology.md Step 1)
- **Collect:** server/CI logs, DB state, metrics (see log-and-ci-analysis.md); blocked by Assess
- **Analyze:** correlate evidence, trace execution paths, identify root cause (see systematic-debugging.md Phase 1-3); blocked by Collect
- **Fix:** address root cause, add defense-in-depth validation (see defense-in-depth.md); blocked by Analyze
- **Verify:** run tests, check build, confirm resolved — NO CLAIMS WITHOUT EVIDENCE (see verification.md); blocked by Fix

Use `metadata: { debugStage, incident, severity, effort, … }` for filtering.

## Parallel Evidence Collection

For multi-source investigations, spawn parallel collection agents (no `blockedBy` between them); Analyze blocks on all completing:

```
TaskCreate(subject: "Collect CI/CD pipeline logs",     metadata: { source: "ci" })
TaskCreate(subject: "Collect application server logs", metadata: { source: "server" })
TaskCreate(subject: "Query database for anomalies",     metadata: { source: "db" })
TaskCreate(subject: "Analyze root cause", addBlockedBy: ["{ci-id}", "{server-id}", "{db-id}"])
```

## Task Lifecycle

`pending → in_progress → completed` for each of Assess/Collect/Analyze/Fix/Verify. **Re-investigation cycle:** if Verify fails → new Analyze-Fix-Verify cycle (`metadata: { cycle: 2 }`); limit to 3 cycles, then question architecture (systematic-debugging.md Phase 4).

## Integration & Errors

Debug tasks are separate from craft/planning phase tasks. After investigation, write the diagnostic report per reporting-standards.md (tasks are session-scoped; report persists). If `TaskCreate` fails: log warning, continue with sequential debugging — tasks add visibility, not core functionality.
