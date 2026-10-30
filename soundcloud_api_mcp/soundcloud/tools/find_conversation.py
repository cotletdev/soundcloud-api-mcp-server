"""Find conversation: whether a profile has been messaged, by its link (`GET /resolve`, then the thread's newest
message). The duplicate check before a first message; no thread search exists."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import PROFILE_URL_SCHEMA, get, me, resolve, user_row
from soundcloud_api_mcp.soundcloud.tools._examples import MESSAGE, USER
from soundcloud_api_mcp.soundcloud.tools._messages import message_row

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"url": PROFILE_URL_SCHEMA},
    "required": ["url"],
    "additionalProperties": False,
}


@tool(
    name="find_conversation",
    title="Find conversation",
    access="read",
    description="Check whether you have already messaged a SoundCloud profile, by its link.",
    details=(
        "Looks up the profile and your thread with it. messaged is false when neither of you has written; else "
        "last_message is the newest message either way."
    ),
    input_schema=INPUT_SCHEMA,
    route="GET /conversations/find",
    example_response={"user_id": "1094512", "with": USER, "messaged": True, "last_message": MESSAGE},
)
async def find_conversation(ctx: ToolContext, args: dict[str, Any]) -> Any:
    user = await resolve(ctx, args["url"])
    me_id, user_id = str((await me(ctx)).get("id")), str(user.get("id"))
    body = await get(ctx, f"/users/{me_id}/conversations/{user_id}/messages", {"limit": 1}) or {}
    newest = (body.get("collection") or [None])[0]
    return {
        "user_id": user_id,
        "with": user_row(user),
        "messaged": newest is not None,
        "last_message": message_row(newest, me_id) if isinstance(newest, dict) else None,
    }
