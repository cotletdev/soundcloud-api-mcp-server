"""Get track: one track with its counts, sharing and secret link (`GET /tracks/{id}`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import ID_SCHEMA, fetch_track, track_row
from soundcloud_api_mcp.soundcloud.tools._examples import TRACK

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"track_id": {**ID_SCHEMA, "description": "From list_tracks."}},
    "required": ["track_id"],
    "additionalProperties": False,
}


@tool(
    name="get_track",
    title="Get track",
    access="read",
    description="One track: title, description, genre, tags, sharing, secret link, plays, likes and comments.",
    details=(
        "Returns one track by track_id: title, link, secret_url when it is private and yours, sharing, "
        "description, genre, tags, whether comments are on, length, and plays, likes, reposts, comments and "
        "downloads. Works for any public track and for your own private ones."
    ),
    input_schema=INPUT_SCHEMA,
    route="GET /tracks/{track_id}",
    example_response=TRACK,
)
async def get_track(ctx: ToolContext, args: dict[str, Any]) -> Any:
    return track_row(await fetch_track(ctx, args["track_id"]))
