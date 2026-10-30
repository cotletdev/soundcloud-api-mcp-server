"""Example answers shared by several tools (anonymised from the dev account, 30.10.2026)."""

from __future__ import annotations

from typing import Any

TRACK: dict[str, Any] = {
    "track_id": "2400000001",
    "title": "Low Tide",
    "url": "https://soundcloud.com/jordan-ellis-music/low-tide",
    "secret_url": None,
    "sharing": "public",
    "description": "A slow synth loop over a field recording of the harbor.",
    "genre": "Ambient",
    "tags": 'ambient "field recording"',
    "commentable": True,
    "duration_ms": 30046,
    "plays": 12,
    "likes": 2,
    "reposts": 0,
    "comments": 1,
    "downloads": 0,
    "created_at": "2026-10-30T21:32:14Z",
    "state": "finished",
}

USER: dict[str, Any] = {
    "user_id": "1094512",
    "permalink": "harbor-lights",
    "username": "Harbor Lights",
    "full_name": "Dana Ruiz",
    "url": "https://soundcloud.com/harbor-lights",
    "city": "Austin",
    "country_code": "US",
    "followers_count": 2310,
    "verified": False,
}

MESSAGE: dict[str, Any] = {
    "message_id": "1700000001:1094512:1793395976000",
    "sent_at": "2026-10-30T21:40:12Z",
    "from_me": True,
    "text": "Hi Dana, loved the chorus on Night Drive. Open to a remix swap?",
}

COMMENT: dict[str, Any] = {
    "comment_id": "2190000001",
    "track_id": "2400000001",
    "body": "The second voice comes in nicely here.",
    "at_ms": 12000,
    "created_at": "2026-10-30T21:45:03Z",
    "user": {
        "user_id": "1094512",
        "permalink": "harbor-lights",
        "username": "Harbor Lights",
        "url": "https://soundcloud.com/harbor-lights",
    },
}
