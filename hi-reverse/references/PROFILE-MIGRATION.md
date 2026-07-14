# Migration Profile

Use this profile for C++ to Java migration preparation. It extends the complete module profile.

## Additional Required Artifacts

- behavioral parity matrix
- type and ownership mapping
- interface and payload mapping
- migration dependency waves
- migration risk register
- parity test scenarios

## Rules

1. Build migration artifacts only from validated reverse-engineering artifacts.
2. Preserve behavior before proposing redesign.
3. Separate required parity from intentional change.
4. Treat integer width, signedness, encoding, memory layout, lifetime, concurrency, timing, and external protocol behavior as explicit risks.
5. Link every parity row and test criterion to a use case, business rule, interface, state transition, or error path.
6. Do not pass the migration package while a high-risk parity item lacks acceptance evidence.
