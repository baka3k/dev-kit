# Example: Architecture Decision with Sequential Thinking

**Problem**: Choose state management for growing React app.

```
Thought 1/4: Initial assessment
React app growing complex. useState scattered. Need centralized state.
Options: Redux, MobX, Zustand, Context, Jotai. Next: Define requirements.

Thought 2/5: Requirements (adjusted up)
Real-time (WebSocket), offline support, complex nested state,
TypeScript, multi-dev maintainability. Eliminates simpler solutions.

Thought 3/5 [REVISION of Thought 1]: Scope refinement
- Original: Need global state management
- Realization: Not all state needs centralization
- Better breakdown: Server→React Query, UI→local useState,
  Auth→Context, App settings→simple global store
- Impact: Reduces problem scope, changes evaluation criteria

Thought 4/6: Re-evaluation
Only need lightweight store for app settings. Zustand fits
(minimal boilerplate, TS support, no provider, ~1KB).
React Query handles server state (cache, refetch, offline).

Thought 5/6 [HYPOTHESIS]: Hybrid approach
Zustand (theme/prefs/UI flags) + React Query (server data) +
useState (component-local). Uncertainty: Real-time updates?

Thought 6/6 [FINAL]: Verified solution
React Query supports WebSocket via custom hooks. Zustand for
global UI, React Query for server, local for components.
Confidence: High. Trade-off: React Query learning curve.
```
