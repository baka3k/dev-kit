# Error And Recovery Matrix

Consolidate failures and recovery behavior across the module.

## Retrieval

1. Query invalid input, timeout, cancellation, retry, abort, trouble, device/host failure, partial completion, rollback, and restart behavior.
2. Trace each failure from detection through state change, cleanup, external notification, user outcome, and terminal state.
3. Record retry count, backoff, timeout source, idempotency, rollback scope, and escalation when evidenced.
4. Use Serena to confirm exception/error codes, branches, cleanup, and logging.
5. Distinguish handled, propagated, ignored, and unresolved failures.

Write `error-recovery.md`. Every matrix row must name the triggering condition, detection point, recovery action, final outcome, and evidence.
