"""What tools read about the browser the session came from: its cookies.

The hosted service keeps a whole browser profile; here it is built from the saved session (`session.py`).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Cookie:
    name: str
    value: str
    domain: str
    path: str = "/"


@dataclass(frozen=True)
class BrowserProfile:
    cookies: tuple[Cookie, ...] = ()
    # Origin -> {key: value}. The hosted service fills it; this server reads cookies only, so it stays empty.
    local_storage: dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass(frozen=True)
class Received:
    """The HTTP client's cookie jar as tools read it: the saved cookies plus what the app set in this run."""

    received_cookies: tuple[Cookie, ...] = ()
