# Migration Artifacts

Generate these only after the module package is structurally valid and evidence-reviewed.

## Behavioral Parity

Map each C++ use case, rule, state transition, side effect, error path, and timing contract to required Java behavior and acceptance evidence.

## Type Mapping

Map C++ types, integer widths, signedness, pointers/references, ownership, lifetime, enums, unions, layout, encoding, and serialization to Java representations.

## Interface Mapping

Map APIs, IPC messages, payloads, callbacks, timeouts, retries, and external contracts to Java ports/adapters without silently changing protocol semantics.

## Migration Waves

Order work by runtime dependencies, shared data, cycles, contract ownership, and independently testable boundaries. Include cycle-breaking strategy and entry/exit criteria.

## Migration Risks

Rank compatibility, data, concurrency, performance, operational, security, and testability risks. Link mitigations and residual risks to evidence.

## Test Scenarios

Derive main, alternate, error, timeout, recovery, state, concurrency, boundary, and parity scenarios from validated artifacts. Every scenario must identify source behavior, expected Java behavior, observable outcome, and traceability IDs.

Do not present a proposed Java redesign as required parity. Record intentional changes separately.
