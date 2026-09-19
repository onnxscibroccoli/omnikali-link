# OmniKali Orchestrator v1 — Design

## Goal
Add a real orchestration/control-plane layer while preserving the existing Kali workstation (QEMU, TigerVNC, Track-B RFB state machine).

## Boundary (approved first slice)
- Build and verify the one-node orchestrator + node contract + health-aware gateway registration.
- Leave Kali, QEMU, TigerVNC, and the existing Track-B state machine untouched.
- Do not fan out to 1,028 nodes; design the protocol so 1 and 1,028 nodes share the same interface.

## Architecture

```
stable entrypoint
      ↓
health-aware discovery
      ↓
authenticated gateway
      ├── optional RFB/VNC
      └── headless control
               ↓
        omnikali-lab-1
               ↓
        bounded task executor
               ↓
        telemetry/results
```

## Node lifecycle
ONLINE → READY → BUSY → DEGRADED → OFFLINE

## Gateway rules
- Stable public entrypoint.
- Dynamic preview endpoint registration.
- Health/readiness validation before advertising an endpoint.
- Fail closed if the HDS port is dead (no redirect into Cloudflare "Port … is not found").

## Security
- Normal authenticated control-plane credentials first.
- OAuth/ZK/blind-PGP anonymity system is a separate threat-model review; not represented as implemented.

## Acceptance tests
1. browser → stable OmniKali entrypoint → endpoint discovery → health-checked gateway → authenticated session → persistent Kali node → optional RFB attachment
2. headless task → orchestrator → omnikali-lab-1 → execution result

## Git
Git remains the source of truth. Agents operate through explicit contracts.
