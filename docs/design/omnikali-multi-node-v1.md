# OmniKali Multi-Node v1 — Design

## Goal
Extend the one-node orchestrator so the same interface supports concurrent users
across multiple registered nodes, while keeping dynamic-DNS registration as the
entrypoint for new tunnels.

## Boundary
- Build NodeRegistry + multi-origin Gateway on top of the existing NodeContract.
- Leave Kali / QEMU / TigerVNC / Track-B untouched.
- Do not claim live capacity until real origins are registered and healthy.

## Architecture

```
stable entrypoint (omnikali.vercel.app)
      ↓
health-aware discovery (middleware + Gateway pool)
      ↓
authenticated gateway
      ├── optional RFB/VNC per node
      └── headless control
               ↓
        NodeRegistry
          ├── omnikali-lab-1
          ├── omnikali-lab-2
          └── …
               ↓
        bounded task executor
               ↓
        telemetry/results
```

## Dynamic DNS registration path
1. Operator (or agent) stands up a tunnel → receives a *.trycloudflare.com (or allowed) URL.
2. Health check must pass (HEAD /api/desktop or injected probe).
3. Gateway.register(url, node_id=…) adds it to the pool only if healthy.
4. NodeContract is registered into NodeRegistry and moved ONLINE → READY.
5. Orchestrator.select() / submit() picks a READY node for the next task.
6. Dead or stale nodes are removed by Watchdog (fail closed).

## Concurrent users
- Multiple READY nodes in the registry → parallel headless tasks.
- advertise_all() exposes the current healthy origin set for UI/discovery.
- Still one process of record; no silent fan-out to 1,028 machines until proven.

## Acceptance
- Registry holds N nodes under the same NodeContract interface.
- Orchestrator dispatches across the pool and returns nodes to READY.
- Gateway never advertises a dead origin.
- Tests cover selection, concurrent acquire/release, and multi-origin pool.
