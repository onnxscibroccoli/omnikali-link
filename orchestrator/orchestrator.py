"""One-node orchestrator for omnikali-lab-1.

Dispatches bounded headless tasks over an authenticated control channel.
No GUI/RFB dependency for task execution.
"""
from __future__ import annotations

import time
from typing import Dict, Optional

from .node_contract import NodeContract, NodeState, Task, TaskStatus


class Orchestrator:
    def __init__(self, node: NodeContract) -> None:
        self.node = node
        self._tasks: Dict[str, Task] = {}

    def submit(self, command: str, timeout_s: float = 60.0) -> Task:
        task = Task.create(command, timeout_s=timeout_s)
        self._tasks[task.task_id] = task
        if not self.node.acquire():
            task.mark_failed("node not READY")
            return task
        task.mark_running()
        try:
            # Bounded execution against the node control channel.
            # Real transport plugs in here; v1 returns a deterministic stub result
            # so the contract and lifecycle can be verified without the guest.
            result = self._execute_bounded(task)
            task.mark_succeeded(result)
        except TimeoutError:
            task.mark_timed_out()
        except Exception as exc:  # noqa: BLE001 - surface to telemetry
            task.mark_failed(str(exc))
        finally:
            self.node.release(degraded=(task.status != TaskStatus.SUCCEEDED))
        return task

    def _execute_bounded(self, task: Task) -> str:
        deadline = time.time() + task.timeout_s
        # Placeholder for the real authenticated control-channel call.
        if time.time() > deadline:
            raise TimeoutError("task exceeded bound")
        return f"ok: executed '{task.command}' on {self.node.node.node_id}"

    def get(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def node_state(self) -> NodeState:
        return self.node.node.state
