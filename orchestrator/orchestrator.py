"""Orchestrator for one or many nodes.

Dispatches bounded headless tasks over an authenticated control channel.
No GUI/RFB dependency for task execution.
Accepts either a single NodeContract or a NodeRegistry.
"""
from __future__ import annotations

import time
from typing import Dict, Optional, Union

from .node_contract import NodeContract, NodeState, Task, TaskStatus
from .registry import NodeRegistry


class Orchestrator:
    def __init__(self, target: Union[NodeContract, NodeRegistry]) -> None:
        if isinstance(target, NodeRegistry):
            self.registry: Optional[NodeRegistry] = target
            self.node: Optional[NodeContract] = None
        else:
            self.registry = None
            self.node = target
        self._tasks: Dict[str, Task] = {}

    def _pick_node(self) -> Optional[NodeContract]:
        if self.registry is not None:
            return self.registry.select()
        return self.node

    def submit(self, command: str, timeout_s: float = 60.0) -> Task:
        task = Task.create(command, timeout_s=timeout_s)
        self._tasks[task.task_id] = task
        node = self._pick_node()
        if node is None or not node.acquire():
            task.mark_failed("no READY node available")
            return task
        task.mark_running()
        try:
            result = self._execute_bounded(task, node)
            task.mark_succeeded(result)
        except TimeoutError:
            task.mark_timed_out()
        except Exception as exc:  # noqa: BLE001 - surface to telemetry
            task.mark_failed(str(exc))
        finally:
            node.release(degraded=(task.status != TaskStatus.SUCCEEDED))
        return task

    def _execute_bounded(self, task: Task, node: NodeContract) -> str:
        deadline = time.time() + task.timeout_s
        # Placeholder for the real authenticated control-channel call.
        if time.time() > deadline:
            raise TimeoutError("task exceeded bound")
        return f"ok: executed '{task.command}' on {node.node.node_id}"

    def get(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def node_state(self) -> Optional[NodeState]:
        node = self._pick_node()
        if node is None:
            return None
        return node.node.state

    def ready_count(self) -> int:
        if self.registry is not None:
            return self.registry.ready_count()
        if self.node and self.node.node.state == NodeState.READY and self.node.node.healthy:
            return 1
        return 0
