"""Health-aware gateway registration (multi-origin).

Only advertise dynamic preview endpoints after a health/readiness check passes.
Fail closed on dead HDS ports. Supports a pool of candidates for concurrent users.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
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
    node_id: Optional[str] = None


class Gateway:
    """Registers dynamic origins only when healthy. Multi-candidate pool."""

    def __init__(
        self,
        health_check: Optional[Callable[[str], bool]] = None,
        stable_fallback: Optional[str] = None,
    ) -> None:
        self._health_check = health_check or self._default_health_check
        self._stable_fallback = stable_fallback
        self._pool: Dict[str, OriginCandidate] = {}

    @staticmethod
    def _default_health_check(url: str) -> bool:
        # Real check hits /api/desktop HEAD; v1 provides a pure validator.
        # Callers that have network can inject a live probe.
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

    def register(self, url: str, node_id: Optional[str] = None) -> Optional[OriginCandidate]:
        if not self.validate(url):
            # Fail closed: do not advertise dead or invalid endpoints.
            self._pool.pop(url, None)
            return None
        cand = OriginCandidate(
            url=url, healthy=True, checked_at=time.time(), node_id=node_id
        )
        self._pool[url] = cand
        return cand

    def unregister(self, url: str) -> None:
        self._pool.pop(url, None)

    def advertise(self) -> Optional[str]:
        healthy = [c for c in self._pool.values() if c.healthy]
        if healthy:
            # Prefer most recently checked.
            healthy.sort(key=lambda c: c.checked_at, reverse=True)
            return healthy[0].url
        if self._stable_fallback and self.validate(self._stable_fallback):
            return self._stable_fallback
        return None

    def advertise_all(self) -> List[str]:
        return [c.url for c in self._pool.values() if c.healthy]

    @property
    def current(self) -> Optional[OriginCandidate]:
        url = self.advertise()
        if url is None:
            return None
        return self._pool.get(url)

    def pool_size(self) -> int:
        return len([c for c in self._pool.values() if c.healthy])
