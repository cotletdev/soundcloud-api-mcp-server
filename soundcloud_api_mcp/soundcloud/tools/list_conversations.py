"""List conversations: direct-message threads, newest first (`GET /users/{me}/conversations[/unread]`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import CURSOR_SCHEMA, LIMIT_SCHEMA, me, page
from soundcloud_api_mcp.soundcloud.tools._examples import MESSAGE, USER
from soundcloud_api_mcp.soundcloud.tools._messages import conversation_row

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "unread_only": {"type": "boolean", "description": "Only threads with messages you have not read."},
        "limit": LIMIT_SCHEMA,
        "cursor": CURSOR_SCHEMA,
    },
    "required": [],
    "additionalProperties": False,
}


@tool(
    name="list_conversations",
    title="List conversations",
    access="read",
    description="Your SoundCloud message threads, newest first: who, the last message, read or not.",
    details=(
        "Lists your direct-message threads, newest first, each with the other person's profile, the last message "
        "(text, time, whether you sent it) and whether you have read it; unread_only keeps the unread ones. "
        "user_id is the other person and goes to get_conversation. Pass next_cursor "
        "back as cursor."
    ),
    input_schema=INPUT_SCHEMA,
    route="GET /conversations",
    example_response={
        "conversations": [{"user_id": "1094512", "with": USER, "read": True, "last_message": MESSAGE}],
        "next_cursor": None,
    },
)
async def list_conversations(ctx: ToolContext, args: dict[str, Any]) -> Any:
    me_id = str((await me(ctx)).get("id"))
    path = f"/users/{me_id}/conversations" + ("/unread" if args.get("unread_only") else "")
    rows, cursor = await page(ctx, path, args, **({"force": 1} if args.get("unread_only") else {}))
    return {"conversations": [conversation_row(r, me_id) for r in rows], "next_cursor": cursor}
