"""Multi-node registry.

Holds N NodeContracts under the same interface used by the one-node path.
Selection prefers READY + healthy nodes; scales from 1 to 1,028 without
changing the orchestrator call sites.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from .node_contract import NodeContract, NodeState


class NodeRegistry:
    """Explicit pool of nodes. Same contract for 1 node or many."""

    def __init__(self) -> None:
        self._nodes: Dict[str, NodeContract] = {}

    def register(self, node: NodeContract) -> None:
        self._nodes[node.node.node_id] = node

    def unregister(self, node_id: str) -> None:
        self._nodes.pop(node_id, None)

    def get(self, node_id: str) -> Optional[NodeContract]:
        return self._nodes.get(node_id)

    def list_nodes(self) -> List[NodeContract]:
        return list(self._nodes.values())

    def ready_nodes(self) -> List[NodeContract]:
        return [
            n
            for n in self._nodes.values()
            if n.node.state == NodeState.READY and n.node.healthy and not n.node.is_stale()
        ]

    def select(self) -> Optional[NodeContract]:
        """Pick one READY healthy node (simple round-robin by insertion order)."""
        ready = self.ready_nodes()
        if not ready:
            return None
        # Prefer the least-recently-used by last_heartbeat ascending.
        ready.sort(key=lambda n: n.node.last_heartbeat)
        return ready[0]

    def count(self) -> int:
        return len(self._nodes)

    def ready_count(self) -> int:
        return len(self.ready_nodes())
