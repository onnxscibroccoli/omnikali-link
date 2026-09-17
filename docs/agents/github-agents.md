# GitHub Agent Definitions (v1)

Agents operate through explicit contracts. Git is the source of truth.

## supervisor
- Watches node lifecycle and orchestrator health.
- Enforces bounded execution and watchdog contract.

## orchestrator
- Dispatches headless tasks to omnikali-lab-1.
- Collects telemetry/results.

## gateway-discovery
- Registers dynamic endpoints only after health checks pass.
- Fails closed on dead ports.

## verification
- Runs acceptance tests before any claim of completion.
- Opens PR rather than silently altering production main.
