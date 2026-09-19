"""Bounded, shell-free command execution for an OmniKali node."""
from __future__ import annotations

import subprocess
from typing import Mapping, Sequence


class CommandRejected(ValueError):
    """Raised when a task is not in the node's explicit command policy."""


class AllowlistedExecutor:
    """Execute named argv tuples without invoking a shell."""

    def __init__(self, commands: Mapping[str, Sequence[str]]) -> None:
        self._commands = {name: tuple(argv) for name, argv in commands.items()}
        if any(not name or not argv for name, argv in self._commands.items()):
            raise ValueError("command names and argv entries must be non-empty")

    def run(self, command: str, timeout_s: float) -> str:
        if timeout_s <= 0:
            raise ValueError("timeout_s must be greater than zero")
        argv = self._commands.get(command)
        if argv is None:
            raise CommandRejected(f"command is not allowlisted: {command}")
        completed = subprocess.run(
            argv,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            shell=False,
        )
        return completed.stdout.rstrip("\n")
