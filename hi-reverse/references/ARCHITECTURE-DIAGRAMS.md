# Architecture And Flow Diagrams

Generate only diagrams activated by the artifact plan.

## Activity Diagram

Use for a branch-heavy use case. Derive nodes and guards from the validated trace; include main, alternate, error, timeout, and recovery outcomes.

## Component Context

Show the target module, actors, neighboring modules, host/device services, storage, and direction of runtime relationships. Do not treat includes as runtime calls.

## IPC Topology

Show processes/components, channels, message direction, request/response pairs, callbacks, and shared-memory boundaries. Link channel labels to the interface catalog.

## Data Flow

Show business data from source through validation, transformation, persistence, external transmission, and terminal consumers. Link data labels to the data dictionary.

## Deployment Runtime

Show processes, services, devices, threads, and runtime nodes with communication channels. Do not invent infrastructure not evidenced by configuration or code.

All files must use the registered Mermaid root and retain an adjacent evidence table or package-manifest references.
