# OmniKali Operator Console v1

## Goal
Give the one-node / multi-node control plane a real frontend: launch
omnikali-lab-1, dispatch allowlisted headless tasks, watch agents, and
fail-closed origin discovery without touching Kali / QEMU / TigerVNC / Track-B.

## Boundary
- Headless execution does not depend on RFB.
- Gateway advertises a desktop origin only after a live HEAD /api/desktop.
- Dead Cloudflare / HDS ports fail closed.
- Commands are named argv tuples. No shell. Unknown commands are rejected.
- Missing executor fails the task and marks the node DEGRADED.

## Agents
supervisor, orchestrator, gateway-discovery, registry, verification,
reservation, recovery, telemetry. See docs/agents/github-agents.md.

## Acceptance (console)
1. Launch lab-1 to ONLINE then READY even when the tunnel is down (headless path).
2. Gateway remains fail-closed until a live origin probe succeeds.
3. Dispatch of an allowlisted command returns real executor output.
4. Concurrent x3 across a 3-node pool uses three distinct nodes.
5. Verification suite 8/8 before any claim of completion.

## Git
This branch does not mutate main. The live Kali workstation origin remains
omnikali.json plus middleware.js on main.
