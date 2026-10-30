"""Get profile: the signed-in artist's own profile, counts and upload quota (`GET /me`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import me, profile_row

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

INPUT_SCHEMA: dict[str, Any] = {"type": "object", "properties": {}, "required": [], "additionalProperties": False}


@tool(
    name="get_profile",
    title="Get profile",
    access="read",
    description="Your own SoundCloud profile: name, city, bio, followers, tracks, plan and upload time left.",
    details=(
        "Returns the signed-in account's profile with follower, following, track, playlist and like counts, the "
        "private track count, the plan (free or Artist), and the upload quota in seconds. user_id is the id the "
        "conversation tools use for you."
    ),
    input_schema=INPUT_SCHEMA,
    route="GET /profile",
    example_response={
        "user_id": "1700000001",
        "permalink": "jordan-ellis-music",
        "username": "Jordan Ellis",
        "full_name": "Jordan Ellis",
        "url": "https://soundcloud.com/jordan-ellis-music",
        "city": "Portland",
        "country_code": "US",
        "followers_count": 0,
        "verified": False,
        "description": None,
        "followings_count": 0,
        "track_count": 1,
        "playlist_count": 0,
        "likes_count": 0,
        "created_at": "2026-10-30T18:05:41Z",
        "private_tracks_count": 0,
        "plan": "free",
        "email_confirmed": True,
        "upload_seconds_left": 7170,
        "upload_seconds_limit": 7200,
    },
)
async def get_profile(ctx: ToolContext, args: dict[str, Any]) -> Any:
    user = await me(ctx)
    quota = user.get("quota") or {}
    plan = ((user.get("creator_subscription") or {}).get("product") or {}).get("id")
    return {
        **profile_row(user),
        "private_tracks_count": user.get("private_tracks_count"),
        "plan": plan,
        "email_confirmed": user.get("primary_email_confirmed"),
        "upload_seconds_left": None if quota.get("unlimited_upload_quota") else quota.get("upload_seconds_left"),
        "upload_seconds_limit": None if quota.get("unlimited_upload_quota") else quota.get("upload_seconds_limit"),
    }
