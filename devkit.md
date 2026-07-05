# DevKit — Workflow Diagrams

> Visual workflows for the 3 core skills: `hi-cook`, `hi-fix`, `hi-plan`. Mapped to current `SKILL.md` versions (cook v3.0.0, fix v2.0.0, plan v2.0.0).

---

## 0. Leaf Skills (Called automatically by main skills)

| Skill | Called by | Purpose |
| --- | --- | --- |
| `hi-explorer` | cook, fix, debug | Codebase scanning & file discovery |
| `hi-log` | cook, plan | Session logging |
| `sequential-thinking` | plan | Step-by-step analysis |
| `docs-seeker` | plan, debug | Documentation lookup |
| `hi-debug` | fix | Advanced debugging |
| `hi-problem-solving` | fix, debug | Stuck-unsticking framework |

## 1. `hi-cook` — Feature Implementation

### 1.1 Mode Matrix

| Mode | Research | Plan | Review | Test | Finalize |
| --- | --- | --- | --- | --- | --- |
| `fast` (default) | skip | inline `hi-plan --fast` | skip | run | commit + log |
| `full` | yes (`explorer` + researcher) | yes | MUST | run | commit + log + review |
| `review` | skip | inline | MUST | run | commit + log + review |
| `auto` | skip | inline | auto-pass | run | commit + log |
| `no-test` | skip | inline | skip | skip | commit + log |
| `code` (path to plan) | skip | — | optional | run | commit + log |

### 1.2 Quick (default) — Linear Flow

```mermaid
graph LR
    A[1. Plan<br/>sequential-thinking<br/>+ docs-seeker] --> B[2. Implement<br/>direct execution]
    B --> C[3. Test<br/>run command]
    C -->|pass| D[4. Finalize<br/>commit + /hi-log]
    C -->|fail ≤2| C
    C -->|fail ≥3| E[spawn hi-fix]

    classDef step fill:#bbdefb,stroke:#0d47a1,color:#000
    classDef fail fill:#ffcdd2,stroke:#b71c1c,color:#000
    class A,B,C,D step
    class E fail

```

---

## 2. `hi-fix` — Issue Resolution

### 2.1 Quick (default) — Linear Flow

```mermaid
graph LR
    A[1. Explorer<br/>locate-only, 1 agent] --> B[2. Diagnose<br/>read error,<br/>find root cause]
    B --> C[3. Fix<br/>root cause,<br/>minimal change]
    C --> D[4. Verify<br/>typecheck + lint]
    D --> E[5. Finalize<br/>report → commit]

    classDef step fill:#bbdefb,stroke:#0d47a1,color:#000
    class A,B,C,D,E step

```

### 2.2 Standard / Deep — Escalation Path

```mermaid
graph TD
    A["Explorer: hi-explorer<br/>2-3 parallel"] --> B["Diagnose"]

    B --> B1{"Diagnosis stuck?"}

    B1 -->|Yes| B2["activate hi-debug"]
    B1 -->|"2+ hypo fail"| B3["activate hi-problem-solving"]
    B1 -->|No| C

    B2 --> B
    B3 --> B

    C["Fix: root cause"] --> D{"Verify level"}

    D -->|Standard| D1["typecheck+lint<br/>+ build + test"]
    D -->|Deep| D2["comprehensive:<br/>edge cases,<br/>security, perf"]

    D1 --> E["Finalize: report →<br/>review (if --review)<br/>→ docs → commit"]
    D2 --> E

    classDef step fill:#bbdefb,stroke:#0d47a1,color:#000
    classDef skill fill:#c8e6c9,stroke:#1b5e20,color:#000
    classDef gate fill:#ffe0b2,stroke:#e65100,color:#000

    class A,C,E step
    class B2,B3 skill
    class B,B1,D gate

```

---

## 3. `hi-plan` — Implementation Planning

### 3.1 Fast (default) — Linear Flow

```mermaid
graph LR
    A[1. Cross-Plan Scan<br/>scan if<br/>plan active] --> B[2. Scope Challenge<br/>SKIP - fast]
    B --> C[3. Codebase Analysis<br/>Read docs, scan<br/>no subagent]
    C --> D[4. Plan Documentation<br/>plan.md + phase-XX.md]
    D --> E{Phases ≥ 3?}
    E -->|Yes| F[5. Hydrate Tasks<br/>TaskCreate/phase]
    E -->|No| G[Skip: overhead > benefit]
    F --> H[6. Output<br/>absolute path]
    G --> H

    classDef step fill:#bbdefb,stroke:#0d47a1,color:#000
    classDef skip fill:#e0e0e0,stroke:#616161,color:#000
    classDef gate fill:#ffe0b2,stroke:#e65100,color:#000
    class A,C,D,F,H step
    class B,G skip
    class E gate

```

### 3.2 Full (--full) — 10 Steps

```mermaid
graph TD
    A[1. Pre-Creation Check<br/>Check Plan Context] --> B[2. Cross-Plan Scan<br/>Detect blockedBy/blocks,<br/>update both plans]
    B --> C[3. Scope Challenge<br/>3 questions,<br/>select mode]
    C --> D[4. Research<br/>Spawn 1 researcher]
    D --> E[5. Codebase Analysis<br/>Read docs, scan if needed]
    E --> F[6. Plan Documentation<br/>plan.md + phase-XX.md]
    F --> G[7. Red Team<br/>/hi-plan red-team path]
    G --> H[8. Validate<br/>/hi-plan validate path]
    H --> I{Phases ≥ 3?}
    I -->|Yes| J[9. Hydrate Tasks<br/>TaskCreate/phase]
    I -->|No| K[Skip tasks]
    J --> L[10. Output<br/>absolute path<br/>+ cook command]
    K --> L

    classDef step fill:#bbdefb,stroke:#0d47a1,color:#000
    classDef skip fill:#e0e0e0,stroke:#616161,color:#000
    classDef gate fill:#ffe0b2,stroke:#e65100,color:#000
    class A,B,C,D,E,F,G,H,J,L step
    class K skip
    class I gate

```

### 3.3 Subcommands

```mermaid
graph LR
    Main[hi-plan] --> Default[default<br/>fast mode]
    Main --> Full[--full<br/>full flow]
    Main --> Hard[--hard<br/>2 researchers + red team]
    Main --> Parallel[--parallel<br/>2 researchers + red team]
    Main --> Two[--two<br/>2+ researchers,<br/>select after]
    Main --> NoTasks[--no-tasks<br/>skip task hydration]
    Main --> Archive[/hi-plan archive<br/>Archive plans + log/]
    Main --> RedTeam[/hi-plan red-team path<br/>Adversarial review/]
    Main --> Validate[/hi-plan validate path<br/>Critical questions interview/]

    classDef mode fill:#e3f2fd,stroke:#0d47a1,color:#000
    classDef sub fill:#c8e6c9,stroke:#1b5e20,color:#000
    class Default,Full,Hard,Parallel,Two,NoTasks mode
    class Archive,RedTeam,Validate sub

```

---

## 4. Cross-skill Integration

```mermaid
graph TD
    User([User request]) --> Detect{Detect intent}

    Detect -->|Implement feature| Cook[hi-cook]
    Detect -->|Fix bug| Fix[hi-fix]
    Detect -->|Plan / architecture| Plan[hi-plan]

    Cook -->|Step 1: Plan| Plan
    Cook -->|Step 3: Test fail ≥3| Fix
    Cook -->|Step 4: Finalize| Log[hi-log]

    Fix -->|Step 1: Explorer| explorer[hi-explorer]
    Fix -->|Step 2: Diagnose stuck| Debug[hi-debug]
    Fix -->|Step 2: 2+ hypotheses fail| PS[hi-problem-solving]
    Fix -->|Step 4: Verify| Log

    Plan -->|research-phase| ST[sequential-thinking]
    Plan -->|research-phase| Docs[docs-seeker]
    Plan -->|archive-workflow.md| Log

    Debug -->|Tools section| explorer
    Debug -->|Tools section| Docs
    Debug -->|Tools section| PS

    explorer --> Output[Report: files + descriptions]
    Debug --> Output2[Root cause + fix recommendation]
    PS --> Output3[Stuck-unsticking framework]
    Log --> Output4[Session log entries]

    classDef primary fill:#c8e6c9,stroke:#1b5e20,color:#000
    classDef linked fill:#bbdefb,stroke:#0d47a1,color:#000
    classDef leaf fill:#fff9c4,stroke:#f57f17,color:#000
    classDef endnode fill:#f5f5f5,stroke:#333,color:#000

    class Cook,Fix,Plan primary
    class explorer,Debug,Log,ST,Docs,PS linked
    class Output,Output2,Output3,Output4 leaf
    class User,Detect endnode

```

---

## 5. HARD-GATEs

| Skill | HARD-GATE | Violation Behavior |
| --- | --- | --- |
| `hi-cook` | No code without plan + review | Stop, request `hi-plan` first (unless user says "just code it") |
| `hi-fix` | No fix before Explorer + Diagnose | Force Steps 1-2; if fail 3+ times → STOP, ask user for architecture |
| `hi-plan` | Cross-Plan Scan update **both plan.md** | Ensure bidirectional update, no plan left behind |

---

## 6. General Rules (Cross-cutting)

1. **Hard-gate first, fast-path later** — default to lightweight mode, use flags for expansion.
2. **Inline > Spawn** — only spawn sub-skills when necessary (3+ fails, 2+ hypothesis fails, large scope).
3. **Token budget** — each subagent spawn = 10-15K tokens. Prioritize inline methodology.
4. **Test/Verify just enough** — `typecheck+lint` for quick, `+build+test` for standard, `comprehensive` for deep.
5. **Review optional** — run only via `--review` or `full` mode. Auto-approve requires score ≥ 9.5 + 0 critical.
6. **Finalize = commit + log** — always conclude with git commit + `/hi-log` (recording decisions, root causes, impacts).
