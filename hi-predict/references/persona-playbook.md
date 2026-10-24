# Persona Analysis Playbook

Use this reference to run the per-persona analysis and (in `deep`) the challenge round for hi-predict.

Packet assembly (including the impact-evidence sections below), the evidence ledger, brief rules, independence (isolated subagents vs disclosed sequential fallback), and debate discipline are defined once in [dev-shared/expert-council.md](../../dev-shared/expert-council.md); this playbook adds the predict-specific packet sections, persona framework, and challenge round.

## Shared Context Packet

Give every persona the same neutral packet. Evidence IDs are stable so findings can cite them.

```yaml
proposal:
  summary: "What changes and why"
  scope_files: []                 # from --files or parsed from the proposal
  concern_areas: []               # optional focus: architecture|security|performance|ux|assumptions
  depth: "quick|standard|deep"
impact_evidence:                  # from hi-scout --impact or the retrieval protocol; empty when unavailable
  symbols: [{id: "sym-1", name: "...", file: "...", layer: "mind_mcp|graph_mcp|serena|rg"}]
  callers_callees: [{id: "rel-1", from: "...", to: "...", verified: true}]
  affected_workflows: [{id: "wf-1", name: "...", severity: "critical|high|medium|low"}]
  dependency_order_risks: []
evidence:                         # ledger schema: dev-shared/expert-council.md
  verified_facts: [{id: "fact-1", statement: "..."}]
  user_statements: [{id: "user-1", statement: "..."}]
  assumptions: [{id: "assumption-1", statement: "..."}]
  unknowns: [{id: "unknown-1", question: "..."}]
coverage:
  tools: {hi-scout: "used|unavailable|no results", mind_mcp: "...", graph_mcp: "...", serena: "...", rg: "..."}
```

A semantic match is a candidate, not proof — only verified relationships enter `impact_evidence`.

## Isolated Persona Brief

Issue the brief to each persona in an isolated context: one subagent per persona, same packet, run concurrently. When isolated contexts are unavailable, run clearly separated sequential passes, disclose this in the report as the isolation mode, and lower confidence.

```text
You are the <PERSONA> on a pre-implementation review panel.

Using only the shared context packet and the code it references:
1. Restate what the proposal changes from your lens; do not judge the verdict yet.
2. List your findings (concerns, threats, bottlenecks, issues, or challenged
   assumptions) with severity, each citing packet evidence IDs or marked as
   an assumption.
3. For every finding give a concrete mitigation, alternative, or the test that
   would confirm or dismiss it.
4. State your confidence and the missing evidence that would raise it.
5. Do not infer or discuss other personas' likely views. Do not implement anything.

Return the persona_output_format block for your persona only.
```

---

## Architect Persona

### Analysis Focus
- System design and component boundaries
- Scalability limitations and bottlenecks
- Coupling and cohesion impacts
- Pattern consistency with existing architecture

### Key Questions
1. Does this change introduce new coupling between modules?
2. Will this scale to 10x current load without architectural changes?
3. Does this follow existing architectural patterns or introduce a new style?
4. What existing abstractions can be reused instead of creating new ones?
5. How does this affect the dependency graph between modules?

### Red Flags
- New circular dependency introduced
- Bypasses existing service/repository layers
- Creates a god component that does too much
- Violates established module boundary conventions

### Example Prompt
Map the proposal onto the module boundaries in the packet; name every new edge in the dependency graph (`callers_callees`) and whether it crosses a layer that has no such edge today.

---

## Security Persona

### Analysis Focus
- Attack surface expansion
- Data exposure and protection
- Authentication and authorization boundaries
- Input validation and injection risks

### Key Questions
1. What new attack surface does this expose?
2. Where is user data stored, transmitted, or logged?
3. Are auth checks happening at every entry point?
4. What input is accepted and how is it validated?
5. Are secrets or tokens introduced in new code paths?

### Red Flags
- Auth check missing on new endpoint
- User data logged in plaintext
- SQL/NoSQL string concatenation
- New secret introduced without rotation plan

### Example Prompt
Enumerate every entry point, data store, log line, and secret the change introduces or touches; for each, state where authentication and validation happen, citing the symbol, or mark the gap as an assumption.

---

## Performance Persona

### Analysis Focus
- Latency impact on critical paths
- Query patterns and N+1 risks
- Memory usage and leak potential
- Resource contention and bottlenecks

### Key Questions
1. What is the added latency on the critical user path?
2. Are there N+1 query patterns in new code?
3. Does this load large datasets into memory?
4. Is there caching opportunity being missed?
5. How does this perform under peak load?

### Red Flags
- Synchronous external API call on hot path
- Unbounded collection loaded into memory
- Missing pagination on new list endpoint
- New database query without index plan

### Example Prompt
Walk the hot path through the verified callers in the packet; estimate added latency, query count, and memory for the peak case the proposal names, or mark the peak case as unknown.

---

## UX Persona

### Analysis Focus
- User flow and intuitiveness
- Error state handling and messaging
- Accessibility across devices and assistive tech
- Loading, empty, and edge case states

### Key Questions
1. What does the error state look like to the user?
2. Is this accessible via keyboard and screen reader?
3. How does this behave on mobile and slow connections?
4. What happens when the user aborts mid-flow?
5. Is the user given clear feedback for every action?

### Red Flags
- Silent failure with no user feedback
- Error reveals internal system details
- Non-responsive on mobile viewport
- Missing loading indicator for async operations

### Example Prompt
Trace the user-visible flow through loading, empty, error, abort, and assistive-technology states; name every state the proposal leaves undefined and what the user would see there today.

---

## Devil's Advocate Persona

### Analysis Focus
- Hidden assumptions in the proposal
- Simpler alternatives not considered
- Worst-case failure scenarios
- Organizational and process risks

### Key Questions
1. Why not do nothing? What is the cost of inaction?
2. What is the absolute simplest version that solves the problem?
3. Which assumption in this proposal is most likely wrong?
4. What if we removed half the scope — what would break?
5. What existing solution could we buy instead of build?

### Red Flags
- Proposal assumes a technology the team has never used
- No simpler alternative was seriously considered
- Success depends on a single person's knowledge
- Timeline assumes no interruptions or scope changes

### Example Prompt
List the proposal's load-bearing assumptions from the packet's `assumptions` and `unknowns`; for each, state what breaks if it is false, then describe the smallest alternative — including doing nothing — that still meets the stated goal.

---

## Deep Challenge Round

In `deep`, after the draft consensus exists, give each persona the anonymized agreements, conflicts, and draft verdict — not other personas' raw outputs — and ask the shared debate questions (dev-shared/expert-council.md). Revise findings only on evidence or reasoning; record every change with its cause. Persistent disagreement stays in the report as an unresolved conflict — it is never averaged away.
