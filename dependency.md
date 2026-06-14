# Skill Dependency Graph

> This file details the relationships between skills: which skills call others, which are standalone, and any external references pointing to non-existent skills.

---

## 1. Dependency Graph Overview

```mermaid
graph TD
    knows[knows] --> standalone
    cook[hi:cook] --> |Step 1| explore[hi:explore]
    cook --> |Step 2| plan[hi:plan]
    cook --> |Step 6| log[hi:log]
    plan --> |research-phase| seqthink[sequential-thinking]
    plan --> |research-phase| docs[docs-seeker]
    plan -.-> |optional| log
    fix[hi:fix] --> explore
    fix --> |diagnosis-protocol| debug[hi:debug]
    fix --> |diagnosis-protocol| probsolve[hi:problem-solving]
    debug --> |Tools section| docs
    debug --> |Tools section| explore
    debug --> |Tools section| probsolve

```

---

## 2. Skill Details

### 2.1 `knows` — Knowledge Retrieval

| Property | Value |
| --- | --- |
| **Status** | 🟢 Primary — called directly |
| **Calls** | *None. Fully standalone.* |
| **Called by** | *None.* |
| **Description** | Fetches evidence from Git history, MCP (mind/graph), and memory files. |

---

### 2.2 `hi:cook` — Feature Implementation

| Property | Value |
| --- | --- |
| **Status** | 🟢 Primary — called directly |
| **Calls** | `hi:explore`, `hi:plan`, `hi:log` |
| **Called by** | *None.* |
| **Description** | Main orchestrator for implementation: research → plan → code → test → review → finalize. |

**Call Details:**

| Step | Call | File:Line | Purpose |
| --- | --- | --- | --- |
| Step 1: Research | `hi:explore` | `hi-cook/SKILL.md:41` | "Spawn researcher + hi:explore. Reports <=150 lines." |
| Step 2: Plan | `hi:plan` | `hi-cook/SKILL.md:44` | "Spawn planner. Fast: /hi:plan --fast." |
| Step 6: Finalize | `hi:log` | `hi-cook/SKILL.md:62` | "/hi:log" — log after completion |

---

### 2.3 `hi:plan` — Implementation Planning

| Property | Value |
| --- | --- |
| **Status** | 🟢 Primary — called directly |
| **Calls** | `sequential-thinking`, `docs-seeker`, `hi:log` (optional) |
| **Called by** | `hi:cook` (Step 2) |
| **Description** | Designs architecture, implementation plans, scope challenges, and red-team reviews. |

---

### 2.4 `hi:explore` — Parallel Codebase Explorer

| Property | Value |
| --- | --- |
| **Status** | 🔵 Linked — called by `hi:cook` and `hi:fix` |
| **Calls** | *None. Standalone.* |
| **Called by** | `hi:cook` (Step 1), `hi:fix` (Step 1) |
| **Description** | Uses parallel agents to scan codebase, find files, and collect context. |

---

### 2.5 `hi:log` — Session Logging

| Property | Value |
| --- | --- |
| **Status** | 🔵 Linked — called by `hi:cook` and `hi:plan` |
| **Calls** | *None. Standalone.* |
| **Called by** | `hi:cook` (Step 6), `hi:plan` (optional, archive-workflow) |
| **Description** | Logs analysis of changes and decisions. |

---

### 2.6 `sequential-thinking` — Sequential Thinking

| Property | Value |
| --- | --- |
| **Status** | 🔵 Linked — called by `hi:plan` |
| **Calls** | *None. Standalone.* |
| **Called by** | `hi:plan` (research-phase) |
| **Description** | Step-by-step analysis for complex problems using revision, branching, and hypothesis testing. |

---

### 2.7 `docs-seeker` — Documentation Discovery

| Property | Value |
| --- | --- |
| **Status** | 🔵 Linked — called by `hi:plan` |
| **Calls** | *None. Standalone.* |
| **Called by** | `hi:plan` (research-phase) |
| **Description** | Script-first documentation discovery via llms.txt standard. |

---

### 2.8 `hi:debug` — Debugging & System Investigation

| Property | Value |
| --- | --- |
| **Status** | 🔵 Linked — called by `hi:fix` |
| **Calls** | `docs-seeker`, `hi:explore`, `hi:problem-solving` |
| **Called by** | `hi:fix` (diagnosis-protocol.md) |
| **Description** | Debug framework: systematic debugging, root cause tracing, defense-in-depth, log/CI analysis, performance diagnostics. |
| **Other refs** | Also references `ck:chrome-devtools` ✗ and `ck:repomix` ✗ — no corresponding skills. |

---

### 2.9 `hi:problem-solving` — Problem-Solving Techniques

| Property | Value |
| --- | --- |
| **Status** | 🔵 Linked — called by `hi:fix` and `hi:debug` |
| **Calls** | *None. Standalone.* |
| **Called by** | `hi:fix` (diagnosis-protocol.md), `hi:debug` (Tools Integration) |
| **Description** | Systematic stuck-unsticking: simplification, collision-zone thinking, pattern recognition, inversion, scale games. |

---

### 2.10 `hi:fix` — Bug Fixing (Orchestrator Layer)

| Property | Value |
| --- | --- |
| **Status** | ⚪ Unused — **NOT called by any primary skill** |
| **Calls** | `hi:explore`, `hi:debug`, `hi:problem-solving` |
| **Called by** | *None.* |
| **Description** | Orchestrator for bug fixing: locate → diagnose → fix → verify → finalize. |

---

## 3. External References — Missing Skills

| Skill name | Referenced from | File:Line | Suggestion |
| --- | --- | --- | --- |
| `hi:git` | `hi-plan/references/archive-workflow.md:17` | "stage+commit+push via /hi:git" | Delete or create skill |
| `ck:chrome-devtools` | `hi-debug/SKILL.md:111` | "ck:chrome-devtools skill" | Delete or create skill |
| `ck:repomix` | `hi-debug/SKILL.md:109` | "ck:repomix skill" | Delete or create skill |

---

## 4. Summary Table

| Skill | Primary | Calls others? | Called by? | Missing Ref? | Note |
| --- | --- | --- | --- | --- | --- |
| `knows` | ✅ | ❌ | ❌ | ❌ | Fully standalone |
| `hi:cook` | ✅ | `explore`, `plan`, `log` | ❌ | ❌ | Main orchestrator |
| `hi:plan` | ✅ | `sequential`, `docs`, `log` | `cook` | ❌ | Refs fixed |
| `hi:explore` | 🔵 | ❌ | `cook`, `fix` | ❌ | Service skill |
| `hi:log` | 🔵 | ❌ | `cook`, `plan` | ❌ | Service skill |
| `sequential-thinking` | 🔵 | ❌ | `plan` | ❌ | Added |
| `docs-seeker` | 🔵 | ❌ | `plan` | ❌ | Added |
| `hi:debug` | 🔵 | `docs`, `explore`, `probsolve` | `fix` | ❌ | Added |
| `hi:problem-solving` | 🔵 | ❌ | `fix`, `debug` | ❌ | Added |
| `hi:fix` | ⚪ | `explore`, `debug`, `probsolve` | ❌ | ❌ | Safe to delete |

---
