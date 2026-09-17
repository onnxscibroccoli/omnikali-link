# Node Contract — omnikali-lab-1

## Identity
- node_id: omnikali-lab-1
- role: single Kali workstation node (QEMU + TigerVNC + Track-B untouched)

## Lifecycle states
ONLINE, READY, BUSY, DEGRADED, OFFLINE

## Control channel
- Local/authenticated control channel for headless task dispatch.
- No GUI/RFB dependency for task execution.

## Task model
- Bounded task executor.
- Telemetry/results returned to orchestrator.

## Scaling
Same interface for 1 node and 1,028 nodes. Broker/fan-out introduced only after the one-node control path is proven.
