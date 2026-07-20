---
name: hi-craft
description: "ALWAYS activate before implementing ANY feature, plan, or fix."
argument-hint: "[task] [--full|--review|--auto|--no-test]  — default: fast mode"
metadata:
  author: baka3k
  version: "3.0.0"
---
# Craft - Feature Implementation

<HARD-GATE>
Do NOT write code until a plan exists and has been reviewed.
User override: "just code it" or "skip planning" - then respect.
</HARD-GATE>

## Intent Detection
| Input | Mode | Behavior |
|-------|------|----------|
| --full, "full" | full | Full workflow with research + review |
| --review | review |There are gate reviews at the end. |
| --auto, "trust me", "yolo" | auto | Auto-approve all |
| --no-test | no-test | Skip testing |
| Path to plan.md/phase-*.md | code | Execute existing plan |
| Default | fast | Skip research, skip review, fast test |

## Process Flow
`[Plan] -> [Implement] -> [Test] -> [Finalize]`

## Mode Matrix
| Mode | Research | Review | Testing |
|------|----------|--------|---------|
| fast (default) | Skip | Skip | Run command |
| full | Yes | MUST | Run command |
| review | Skip | MUST | Run command |
| auto | Skip | Auto-pass | Run command |
| no-test | Skip | Skip | Skip |

## Steps

### Step 1: Plan (skip if plan.md provided)

* Use `sequential-thinking` to analyze the task briefly.
* Use `hi-docs-seeker` if documentation lookup is required.
* Do not spawn a separate planner. Call `hi-plan --fast` inline if needed.

### Step 2: Implement

Execute tasks directly. Set TaskUpdate to `in_progress` on each task.
Parallel mode: launch `fullstack-developer` per phase.

### Step 3: Test (skip no-test)

Run the test command. Check the output. If it fails:

* 1st-2nd time: analyze and fix it yourself.
* 3rd+ time: spawn `hi-fix` for in-depth debugging.
Do not spawn a separate tester.

### Step 4: Finalize
1. TaskUpdate all tasks complete
2. git commit
3. /hi-log

## Review (optional, flag --review hoặc full mode)
Run code-reviewer. Score>=9.5 + 0 critical = auto-approve (auto mode only).
Max 3 fix cycles. Critical issues always block: Security, Performance, Architecture violations.
