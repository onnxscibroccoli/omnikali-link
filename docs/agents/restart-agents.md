# Restart agents

Added to the one-node contract. Same interface at 1 and at 1,028.

| Agent | Role |
| --- | --- |
| power | Owns the restart protocol. Local session never waits. |
| wake | Issues a wake ticket when the origin is off, then awaits pointer health. |
| pointer-sync | Reads GitHub `omnikali.json` during restart. Never writes `main`. |

Existing agents (supervisor, orchestrator, gateway-discovery, registry,
verification, reservation, recovery, telemetry, desktop-session, shell,
filesystem, github-link, lab-network, remote-desktop) are unchanged.
