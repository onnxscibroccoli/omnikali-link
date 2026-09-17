"""Node contract for omnikali-lab-1.

Lifecycle: ONLINE -> READY -> BUSY -> DEGRADED -> OFFLINE
Same interface scales from 1 to 1,028 nodes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional
import time
import uuid


class NodeState(str, Enum):
    ONLINE = "ONLINE"
    READY = "READY"
    BUSY = "BUSY"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"


@dataclass
class NodeInfo:
    node_id: str
    state: NodeState = NodeState.OFFLINE
    last_heartbeat: float = 0.0
    capabilities: Dict[str, Any] = field(default_factory=dict)
    endpoint: Optional[str] = None
    healthy: bool = False

    def heartbeat(self, state: NodeState, healthy: bool = True) -> None:
        self.state = state
        self.healthy = healthy
        self.last_heartbeat = time.time()

    def is_stale(self, ttl: float = 30.0) -> bool:
        return (time.time() - self.last_heartbeat) > ttl


@dataclass
class Task:
    task_id: str
    command: str
    timeout_s: float = 60.0
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[float] = None
    finished_at: Optional[float] = None

    @classmethod
    def create(cls, command: str, timeout_s: float = 60.0) -> "Task":
        return cls(task_id=str(uuid.uuid4()), command=command, timeout_s=timeout_s)

    def mark_running(self) -> None:
        self.status = TaskStatus.RUNNING
        self.started_at = time.time()

    def mark_succeeded(self, result: str) -> None:
        self.status = TaskStatus.SUCCEEDED
        self.result = result
        self.finished_at = time.time()

    def mark_failed(self, error: str) -> None:
        self.status = TaskStatus.FAILED
        self.error = error
        self.finished_at = time.time()

    def mark_timed_out(self) -> None:
        self.status = TaskStatus.TIMED_OUT
        self.finished_at = time.time()


class NodeContract:
    """Explicit contract between orchestrator and a single node."""

    def __init__(self, node_id: str = "omnikali-lab-1") -> None:
        self.node = NodeInfo(node_id=node_id)

    def register(self, endpoint: str, capabilities: Optional[Dict[str, Any]] = None) -> None:
        self.node.endpoint = endpoint
        self.node.capabilities = capabilities or {"headless": True, "rfb": True}
        self.node.heartbeat(NodeState.ONLINE, healthy=True)

    def ready(self) -> None:
        if self.node.state == NodeState.ONLINE:
            self.node.heartbeat(NodeState.READY, healthy=True)

    def acquire(self) -> bool:
        if self.node.state == NodeState.READY and self.node.healthy:
            self.node.heartbeat(NodeState.BUSY, healthy=True)
            return True
        return False

    def release(self, degraded: bool = False) -> None:
        state = NodeState.DEGRADED if degraded else NodeState.READY
        self.node.heartbeat(state, healthy=not degraded)

    def offline(self) -> None:
        self.node.heartbeat(NodeState.OFFLINE, healthy=False)
