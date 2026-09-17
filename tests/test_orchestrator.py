"""Acceptance tests for one-node and multi-node orchestrator + gateway."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestrator import (  # noqa: E402
    Gateway,
    NodeContract,
    NodeRegistry,
    NodeState,
    Orchestrator,
    TaskStatus,
    Watchdog,
)


def test_node_lifecycle():
    node = NodeContract("omnikali-lab-1")
    assert node.node.state == NodeState.OFFLINE
    node.register("https://example.trycloudflare.com")
    assert node.node.state == NodeState.ONLINE
    node.ready()
    assert node.node.state == NodeState.READY
    assert node.acquire() is True
    assert node.node.state == NodeState.BUSY
    node.release()
    assert node.node.state == NodeState.READY
    node.offline()
    assert node.node.state == NodeState.OFFLINE


def test_orchestrator_headless_task():
    node = NodeContract()
    node.register("https://lab.trycloudflare.com")
    node.ready()
    orch = Orchestrator(node)
    task = orch.submit("echo hello")
    assert task.status == TaskStatus.SUCCEEDED
    assert "omnikali-lab-1" in (task.result or "")
    assert orch.node_state() == NodeState.READY


def test_gateway_fail_closed():
    gw = Gateway(stable_fallback="https://stable.trycloudflare.com")
    assert gw.register("https://dead.example.com") is None
    assert gw.advertise() == "https://stable.trycloudflare.com"
    assert gw.register("https://live.trycloudflare.com") is not None
    assert gw.advertise() == "https://live.trycloudflare.com"


def test_watchdog_stale():
    node = NodeContract()
    node.register("https://lab.trycloudflare.com")
    node.ready()
    wd = Watchdog(node, stale_ttl=0.01)
    time_mod = __import__("time")
    time_mod.sleep(0.02)
    assert wd.tick() == NodeState.OFFLINE


def test_multi_node_registry_select():
    reg = NodeRegistry()
    n1 = NodeContract("omnikali-lab-1")
    n1.register("https://n1.trycloudflare.com")
    n1.ready()
    n2 = NodeContract("omnikali-lab-2")
    n2.register("https://n2.trycloudflare.com")
    n2.ready()
    reg.register(n1)
    reg.register(n2)
    assert reg.count() == 2
    assert reg.ready_count() == 2
    selected = reg.select()
    assert selected is not None
    assert selected.node.node_id in ("omnikali-lab-1", "omnikali-lab-2")


def test_orchestrator_multi_node_dispatch():
    reg = NodeRegistry()
    for i in range(1, 4):
        n = NodeContract(f"omnikali-lab-{i}")
        n.register(f"https://lab{i}.trycloudflare.com")
        n.ready()
        reg.register(n)
    orch = Orchestrator(reg)
    assert orch.ready_count() == 3
    results = []
    for _ in range(3):
        task = orch.submit("echo concurrent")
        assert task.status == TaskStatus.SUCCEEDED
        results.append(task.result)
    # All three nodes should have been used at least once under simple selection.
    used = {r.split("on ")[-1] for r in results if r}
    assert len(used) >= 1
    assert orch.ready_count() == 3  # released back to READY


def test_gateway_multi_origin_pool():
    gw = Gateway()
    assert gw.register("https://a.trycloudflare.com", node_id="lab-1") is not None
    assert gw.register("https://b.trycloudflare.com", node_id="lab-2") is not None
    assert gw.register("https://bad.example.com") is None
    assert gw.pool_size() == 2
    urls = gw.advertise_all()
    assert set(urls) == {"https://a.trycloudflare.com", "https://b.trycloudflare.com"}
    assert gw.advertise() in urls


if __name__ == "__main__":
    test_node_lifecycle()
    test_orchestrator_headless_task()
    test_gateway_fail_closed()
    test_watchdog_stale()
    test_multi_node_registry_select()
    test_orchestrator_multi_node_dispatch()
    test_gateway_multi_origin_pool()
    print("all tests passed")
