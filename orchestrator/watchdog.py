"""Supervisor / watchdog contract.

Watches node lifecycle and orchestrator health. Enforces bounded execution.
"""
from __future__ import annotations

import time
from typing import Callable, Optional

from .node_contract import NodeContract, NodeState


class Watchdog:
    def __init__(
        self,
        node: NodeContract,
        on_degraded: Optional[Callable[[], None]] = None,
        on_offline: Optional[Callable[[], None]] = None,
        stale_ttl: float = 30.0,
    ) -> None:
        self.node = node
        self.on_degraded = on_degraded or (lambda: None)
        self.on_offline = on_offline or (lambda: None)
        self.stale_ttl = stale_ttl

    def tick(self) -> NodeState:
        state = self.node.node.state
        if self.node.node.is_stale(self.stale_ttl):
            if state not in (NodeState.OFFLINE,):
                self.node.offline()
                self.on_offline()
                return NodeState.OFFLINE
        if state == NodeState.DEGRADED:
            self.on_degraded()
        return state

    def enforce_bound(self, started: float, limit: float) -> bool:
        return (time.time() - started) <= limit
