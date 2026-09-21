"""Regression tests for the real OmniKali node execution boundary."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestrator.executor import AllowlistedExecutor, CommandRejected  # noqa: E402
from orchestrator.node_contract import NodeContract, NodeState, TaskStatus  # noqa: E402
from orchestrator.orchestrator import Orchestrator  # noqa: E402


class NodeRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.executor = AllowlistedExecutor(
            commands={"say": (sys.executable, "-c", "print('hello from node')")}
        )
        self.node = NodeContract("omnikali-node", executor=self.executor)
        self.node.register("https://node.trycloudflare.com")
        self.node.ready()

    def test_orchestrator_returns_real_process_output(self) -> None:
        task = Orchestrator(self.node).submit("say", timeout_s=2)
        self.assertEqual(TaskStatus.SUCCEEDED, task.status)
        self.assertEqual("hello from node", task.result)
        self.assertEqual(NodeState.READY, self.node.node.state)

    def test_unlisted_command_is_rejected_without_shell_execution(self) -> None:
        with self.assertRaises(CommandRejected):
            self.executor.run("rm -rf /", timeout_s=1)

    def test_nonpositive_timeout_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.executor.run("say", timeout_s=0)

    def test_double_acquire_is_rejected(self) -> None:
        self.assertTrue(self.node.acquire())
        self.assertFalse(self.node.acquire())
        self.node.release()
        self.assertTrue(self.node.acquire())
        self.node.release()

    def test_missing_executor_degrades_then_recovers(self) -> None:
        bare = NodeContract("omnikali-bare")
        bare.register("https://bare.trycloudflare.com")
        bare.ready()
        task = Orchestrator(bare).submit("say", timeout_s=1)
        self.assertEqual(TaskStatus.FAILED, task.status)
        self.assertEqual(NodeState.DEGRADED, bare.node.state)
        self.assertTrue(bare.recover())
        self.assertEqual(NodeState.READY, bare.node.state)


if __name__ == "__main__":
    unittest.main()
