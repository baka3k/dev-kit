# Concurrency Model

Generate the concurrency model when the `concurrency` condition is active.

## Retrieval

1. Identify threads, tasks, event loops, queues, mutexes, semaphores, atomics, interrupts, callbacks, and shared mutable objects.
2. Trace creation, ownership, scheduling, blocking, wakeup, shutdown, and handoff relationships.
3. Query Graph-RAG for asynchronous boundaries and use Serena for registration, lock scope, and shared-state access.
4. Record ordering guarantees, thread affinity, reentrancy, race-sensitive state, and deadlock risks only when evidenced.
5. Keep runtime concurrency separate from ordinary call dependencies.

Write `concurrency.mmd` as a flowchart of execution contexts, queues, synchronization, and shared state. Include an adjacent evidence/risk table in the module documentation.
