# Example: Performance Debugging with Sequential Thinking

**Problem**: API endpoint slow (2-3s instead of <200ms).

```
Thought 1/5: Initial investigation
GET /api/users/{id}/dashboard. Expected <200ms, actual 2-3s.
Need to identify bottleneck.

Thought 2/5: Endpoint analysis
Dashboard fetches: user profile, recent activities, notifications,
analytics. Each separate DB query. Could be N+1.

Thought 3/6: Profiling results (adjusted)
- User profile: 20ms | Activities: 1800ms (!!) | Notifications: 100ms
- Analytics: 80ms. Activities = 90% of time.

Thought 4/6 [BRANCH A]: Hypothesis - N+1 query
Activities FK to users. Query might fetch activities then user
for each. Verification: Check joins vs loops.

Thought 4/6 [BRANCH B]: Hypothesis - Missing index
Activities may lack index on user_id + created_at. Without it,
full table scan. Verification: Check table indexes.

Thought 5/6 [VERIFICATION]: Testing hypotheses
- Query uses proper joins (Branch A eliminated: not N+1).
- Index check: user_id indexed, NOT created_at. Filters+sorts on both.
- Branch B confirmed: Missing composite index causes slow sort.

Thought 6/6 [FINAL]: Solution
CREATE INDEX idx_activities_user_created
  ON activities(user_id, created_at DESC);
Tested: 120ms (target met). 95% performance improvement.
Confidence: High.
```
