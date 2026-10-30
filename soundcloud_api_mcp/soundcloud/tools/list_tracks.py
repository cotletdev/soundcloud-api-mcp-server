"""List tracks: the own tracks, private ones too (GraphQL `MyTracks`), with counts (`GET /tracks?ids=`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.helpers import limit
from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import CURSOR_SCHEMA, LIMIT_SCHEMA, own_tracks, track_row
from soundcloud_api_mcp.soundcloud.tools._examples import TRACK

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"limit": LIMIT_SCHEMA, "cursor": CURSOR_SCHEMA},
    "required": [],
    "additionalProperties": False,
}


@tool(
    name="list_tracks",
    title="List tracks",
    access="read",
    description="Your tracks, public and private, newest first, with plays, likes, reposts and comments.",
    details=(
        "Lists the tracks of the signed-in account as Artist Studio does, private ones included, each with its "
        "link (secret_url for a private track), sharing, genre, tags, whether comments are on, and its play, like, "
        "repost, comment and download counts. Pass next_cursor back as cursor for the next page."
    ),
    input_schema=INPUT_SCHEMA,
    route="GET /tracks",
    example_response={"tracks": [TRACK], "next_cursor": None},
)
async def list_tracks(ctx: ToolContext, args: dict[str, Any]) -> Any:
    rows, cursor = await own_tracks(ctx, limit(args, 20, 50), args.get("cursor"))
    return {"tracks": [track_row(t) for t in rows], "next_cursor": cursor}
