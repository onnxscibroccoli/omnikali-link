"""Acceptance tests for the one-node orchestrator + gateway."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestrator import (  # noqa: E402
    Gateway,
    NodeContract,
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


if __name__ == "__main__":
    test_node_lifecycle()
    test_orchestrator_headless_task()
    test_gateway_fail_closed()
    test_watchdog_stale()
    print("all tests passed")
