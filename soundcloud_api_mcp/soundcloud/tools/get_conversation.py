"""Get conversation: the messages of one thread, newest first (`GET /users/{me}/conversations/{other}/messages`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import CURSOR_SCHEMA, ID_SCHEMA, LIMIT_SCHEMA, me, page
from soundcloud_api_mcp.soundcloud.tools._examples import MESSAGE
from soundcloud_api_mcp.soundcloud.tools._messages import message_row

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "user_id": {**ID_SCHEMA, "description": "The other person, from list_conversations or resolve_profile."},
        "limit": LIMIT_SCHEMA,
        "cursor": CURSOR_SCHEMA,
    },
    "required": ["user_id"],
    "additionalProperties": False,
}


@tool(
    name="get_conversation",
    title="Get conversation",
    access="read",
    description="The messages between you and one person, newest first.",
    details=(
        "Returns the direct messages between you and user_id, newest first, each with its text, time and whether "
        "you sent it. An empty list means you have never written to each other. Pass next_cursor back as cursor "
        "for older messages. Reading does not mark the thread read."
    ),
    input_schema=INPUT_SCHEMA,
    route="GET /conversations/{user_id}",
    example_response={"user_id": "1094512", "messages": [MESSAGE], "next_cursor": None},
)
async def get_conversation(ctx: ToolContext, args: dict[str, Any]) -> Any:
    me_id = str((await me(ctx)).get("id"))
    rows, cursor = await page(ctx, f"/users/{me_id}/conversations/{args['user_id']}/messages", args)
    return {"user_id": args["user_id"], "messages": [message_row(r, me_id) for r in rows], "next_cursor": cursor}
