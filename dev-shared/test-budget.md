# Test Budget Contract (Proportionate Testing)

How many tests a change gets is decided by mapping, not by momentum. Every skill or role that plans, writes, or reviews tests follows this contract. A fixed number cannot fit every feature; a risk-tiered budget scales naturally — a money-handling rule earns several tests, a getter earns zero.

## 1. Mapping Before Writing

Every test maps to a named behavior:

- an acceptance criterion or task in the active plan/phase file,
- a business rule or edge case from a scenario report,
- a bug being fixed (one regression test per bug).

No mapped behavior, no test. "Done" means every mapped behavior has at least one test, proven by a rule → test-name checklist in the report — never by case count.

## 2. Three Values per Input Dimension

For each input dimension, test `{typical, boundary, invalid}` — three cases, not one hundred. Multiple dimensions combine by pairwise sampling, never the full cartesian product. A specific combination that matters is hand-picked and added to the mapping (§1).

## 3. Parameterize, Don't Duplicate

Similar cases collapse into one table-driven/parameterized test with N rows. The budget counts test functions, not rows.

## 4. Tiers

| Tier | Targets | Unit tests |
|------|---------|------------|
| Always | Business rules; money, auth, permission, data-integrity paths; public API contracts; one regression test per fixed bug | Required |
| Judgment | Complex branching, state machines, parsers, concurrency guards | Required when the branch carries behavior not covered above |
| Never | Getters/setters, DTOs without logic, generated code, framework/library behavior, config constants | Zero — covered by types or integration tests elsewhere |

## 5. Soft Ceiling with Justification

Default working ceiling: ~10–15 new test functions per task or phase, ~40 per feature. Exceeding it is allowed, but every extra batch carries a one-line justification ("payment retries: 6 table rows cover the retry matrix"), or prior user approval in auto/parallel mode. The ceiling is a checkpoint that forces thinking, not a wall.

A user-supplied explicit budget (`--test-budget=N` on `hi-craft`) or an explicit "exhaustive tests" request overrides the ceiling for that run; the mapping rules (§1–§3) still apply.

## 6. Scenario Reports

`hi-scenario` output already ranks severity. Only Critical and High scenarios become unit tests now; Medium and Low go to the report's backlog table (its "test priorities" section) instead of the test suite.

## Duty Table

| Skill / Role | Duty |
|--------------|------|
| `hi-plan` | Each `phase-XX.md` states its test scope: mapped acceptance criteria and expected size (S/M/L). |
| `hi-craft`, `implementer` | Write tests within the budget; return the rule → test-name checklist. |
| `hi-scenario` | Split by severity: Critical/High → tests now; Medium/Low → backlog. |
| `reviewer` | The `scope-complexity` lens flags unmapped and duplicate tests as findings. |
| `--parallel` mode | Orchestrator puts the per-phase test scope in the phase file so every delegated implementer inherits it (constraints per `delegation-contract.md`). |
