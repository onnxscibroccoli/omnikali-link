# omnikali-link

Public dynamic-DNS pointer for [omnikali.vercel.app](https://omnikali.vercel.app).

`omnikali.json` is the live origin. The Vercel name reverse-proxies that URL.

## Orchestrator

Control plane for one or many Kali nodes:

| Module | Role |
|--------|------|
| `orchestrator/node_contract.py` | Node lifecycle + task model |
| `orchestrator/registry.py` | Multi-node pool (same interface for 1…N) |
| `orchestrator/orchestrator.py` | Headless task dispatch (single or registry) |
| `orchestrator/gateway.py` | Health-aware multi-origin registration (fail closed) |
| `orchestrator/watchdog.py` | Supervisor / stale-node contract |
| `tests/test_orchestrator.py` | Acceptance tests |

```bash
python -m tests.test_orchestrator
```

### Dynamic DNS path
1. Stand up a tunnel (Cloudflare quick tunnel, etc.).
2. Confirm health (e.g. `HEAD /api/desktop`).
3. Register the URL via Gateway + NodeContract → NodeRegistry.
4. Only healthy origins are advertised.

Design docs live under `docs/`. Git remains the source of truth; agents operate through explicit contracts.

**Current live origin status is external** — when the tunnel is down, discovery correctly fails closed or falls back only if a healthy candidate exists.
