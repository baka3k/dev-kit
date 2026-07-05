# Log-Writer Subagent Contract

Defines inputs, outputs, and scope rules for the log-writer subagent spawned by `hi-log`.

## Inputs
- `topic` (optional) - focus area string
- `since` (optional) - git ref / sha / ISO date cutoff
- `scope` (optional) - directory restriction
- Recent observations from claude-mem
- git diff + git log within scope/since window

## Output
- One file per event at `./docs/logs/YYYY-MM-DD-<slug>.md`
- Filename slug: kebab-case, <= 60 chars, no date prefix collision
- Format: see `../SKILL.md` -> "Output Format" section

## Scope Rules
- Read-only on source. Never edit code or configs.
- May create new files under `./docs/logs/` only.
- May update existing log files when appending a decision correction.
- Never delete logs. Archive via /hi-project-organization.

## Quality Bar
- Every entry MUST contain: Context, Change, Impact, Decision, References.
- Impact level declared (low/med/high). No "TBD" placeholders.
- File references use `path:LINE` form. Commits use full sha.
- If a section has nothing to say, omit the file entirely (do not log empty events).
- Cross-link to plans (`./plans/<id>/`) when work traces back to a plan.

## Timeout
- 3 min per log-writer spawn. Skip non-responders.
- Max 5 events per invocation. Split into multiple /hi-log calls if more.
