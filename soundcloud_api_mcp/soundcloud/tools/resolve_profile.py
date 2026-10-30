"""Resolve profile: a SoundCloud profile link to its user id, name, counts and bio (`GET /resolve`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import PROFILE_URL_SCHEMA, profile_row, resolve

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"url": PROFILE_URL_SCHEMA},
    "required": ["url"],
    "additionalProperties": False,
}


@tool(
    name="resolve_profile",
    title="Resolve profile",
    access="read",
    description="Look up a SoundCloud profile by its link: user id, name, city, bio and follower counts.",
    details=(
        "Turns a profile link (or the name after soundcloud.com/) into the profile: user_id, username, full name, "
        "city, country, bio, followers, followings, tracks, playlists and likes. Use it to write a personal "
        "message, then find_conversation to check you have not written to this person before."
    ),
    input_schema=INPUT_SCHEMA,
    route="GET /profiles/resolve",
    example_response={
        "user_id": "1094512",
        "permalink": "harbor-lights",
        "username": "Harbor Lights",
        "full_name": "Dana Ruiz",
        "url": "https://soundcloud.com/harbor-lights",
        "city": "Austin",
        "country_code": "US",
        "followers_count": 2310,
        "verified": False,
        "description": "Synth pop from Texas. Bookings: see link.",
        "followings_count": 180,
        "track_count": 42,
        "playlist_count": 6,
        "likes_count": 512,
        "created_at": "2014-03-02T17:40:11Z",
    },
)
async def resolve_profile(ctx: ToolContext, args: dict[str, Any]) -> Any:
    return profile_row(await resolve(ctx, args["url"]))
