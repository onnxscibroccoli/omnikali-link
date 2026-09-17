# omnikali-link

Public dynamic-DNS pointer for [omnikali.vercel.app](https://omnikali.vercel.app).

`omnikali.json` is the live origin. The Vercel name reverse-proxies that URL.

## Orchestrator (v1)

One-node control plane for `omnikali-lab-1`:

- `orchestrator/node_contract.py` — node lifecycle + task model
- `orchestrator/orchestrator.py` — headless task dispatch
- `orchestrator/gateway.py` — health-aware origin registration (fail closed)
- `orchestrator/watchdog.py` — supervisor / watchdog contract
- `tests/test_orchestrator.py` — acceptance tests

```bash
python -m tests.test_orchestrator
```

Design docs live under `docs/`. Git remains the source of truth; agents operate through explicit contracts.
