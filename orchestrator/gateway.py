"""Health-aware gateway registration.

Only advertise a dynamic preview endpoint after a health/readiness check passes.
Fail closed on dead HDS ports.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, List, Optional
from urllib.parse import urlparse


ALLOWED_SUFFIXES = (
    ".trycloudflare.com",
    ".serveousercontent.com",
    ".serveo.net",
    ".localhost.run",
    ".lhr.life",
    ".pinggy.io",
    ".loca.lt",
)


@dataclass
class OriginCandidate:
    url: str
    healthy: bool = False
    checked_at: float = 0.0


class Gateway:
    """Registers dynamic origins only when healthy."""

    def __init__(
        self,
        health_check: Optional[Callable[[str], bool]] = None,
        stable_fallback: Optional[str] = None,
    ) -> None:
        self._health_check = health_check or self._default_health_check
        self._stable_fallback = stable_fallback
        self._registered: Optional[OriginCandidate] = None

    @staticmethod
    def _default_health_check(url: str) -> bool:
        # Real check hits /api/desktop HEAD; v1 provides a pure validator.
        try:
            u = urlparse(url)
        except Exception:  # noqa: BLE001
            return False
        if u.scheme != "https":
            return False
        host = u.hostname or ""
        if host.startswith("api.") or host.startswith("www."):
            return False
        return any(host.endswith(s) for s in ALLOWED_SUFFIXES)

    def validate(self, url: str) -> bool:
        return self._health_check(url)

    def register(self, url: str) -> Optional[OriginCandidate]:
        if not self.validate(url):
            # Fail closed: do not advertise dead or invalid endpoints.
            self._registered = None
            return None
        cand = OriginCandidate(url=url, healthy=True, checked_at=time.time())
        self._registered = cand
        return cand

    def advertise(self) -> Optional[str]:
        if self._registered and self._registered.healthy:
            return self._registered.url
        if self._stable_fallback and self.validate(self._stable_fallback):
            return self._stable_fallback
        return None

    @property
    def current(self) -> Optional[OriginCandidate]:
        return self._registered
