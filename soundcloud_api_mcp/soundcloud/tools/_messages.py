"""Conversations (classic app module 335): `/users/{me}/conversations[/{other}[/messages]]`. A thread's id is the
other person's user id; a message has `content`, `sent_at` and `sender_urn` (web bundle, 30.10.2026)."""

from __future__ import annotations

from typing import Any

from soundcloud_api_mcp.soundcloud.tools._api import str_id, urn_id, user_row


def message_row(message: dict[str, Any], me_id: str) -> dict[str, Any]:
    sender = urn_id(message.get("sender_urn")) or str_id((message.get("sender") or {}).get("id"))
    return {
        "message_id": str_id(message.get("id")),
        "sent_at": message.get("sent_at"),
        "from_me": sender == me_id,
        "text": message.get("content"),
    }


def conversation_row(conversation: dict[str, Any], me_id: str) -> dict[str, Any]:
    users = [u for u in conversation.get("users") or [] if str(u.get("id")) != me_id]
    last = conversation.get("last_message")
    return {
        "user_id": str_id(conversation.get("id")),
        "with": user_row(users[0]) if users else None,
        "read": conversation.get("read"),
        "last_message": message_row(last, me_id) if isinstance(last, dict) else None,
    }
