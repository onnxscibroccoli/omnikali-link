# GitHub Agent Definitions (v1 + multi-node)

Agents operate through explicit contracts. Git is the source of truth.

## supervisor
- Watches node lifecycle and orchestrator health.
- Enforces bounded execution and watchdog contract.
- Marks stale nodes OFFLINE and removes them from the advertised pool.

## orchestrator
- Dispatches headless tasks to one or more nodes via NodeRegistry.
- Selects READY + healthy nodes; collects telemetry/results.

## gateway-discovery
- Registers dynamic endpoints only after health checks pass.
- Maintains a multi-origin pool; fails closed on dead ports.
- Updates omnikali.json / discovery only for healthy origins.

## registry
- Holds N NodeContracts under the same interface (1 → 1,028).
- Provides select() / ready_count() for concurrent capacity.

## verification
- Runs acceptance tests before any claim of completion.
- Opens PR rather than silently altering production main.
