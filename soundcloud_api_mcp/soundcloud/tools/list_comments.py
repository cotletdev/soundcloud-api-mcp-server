"""List comments: on one track (`GET /tracks/{id}/comments?threaded=1`), or on all own tracks (GraphQL
`UserTrackComments`, the free plan's comment inbox)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import (
    CURSOR_SCHEMA,
    ID_SCHEMA,
    LIMIT_SCHEMA,
    comment_row,
    graphql,
    page,
    urn_id,
)
from soundcloud_api_mcp.soundcloud.tools._examples import COMMENT

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "track_id": {**ID_SCHEMA, "description": "One track. Without it: comments on all your tracks."},
        "limit": {**LIMIT_SCHEMA, "description": "With track_id only. Default 20."},
        "cursor": CURSOR_SCHEMA,
    },
    "required": [],
    "additionalProperties": False,
}

_ALL = (
    "query UserTrackComments($after: String) { userTrackCommentsWithReplies(after: $after) { comments "
    "{ urn body createdAt trackTime track { urn title } user { urn permalink username permalinkUrl } } "
    "pageInfo { endCursor } } }"
)


def _graph_row(comment: dict[str, Any]) -> dict[str, Any]:
    user, track = comment.get("user") or {}, comment.get("track") or {}
    return {
        "comment_id": urn_id(comment.get("urn")),
        "track_id": urn_id(track.get("urn")),
        "body": comment.get("body"),
        "at_ms": comment.get("trackTime"),
        "created_at": comment.get("createdAt"),
        "user": {
            "user_id": urn_id(user.get("urn")),
            "permalink": user.get("permalink"),
            "username": user.get("username"),
            "url": user.get("permalinkUrl"),
        },
    }


@tool(
    name="list_comments",
    title="List comments",
    access="read",
    description="Comments on one of your tracks, or the newest comments on all your tracks.",
    details=(
        "With track_id: the comments on that track, newest first, replies included, each with its author, text "
        "and the point in the track (at_ms). Without: the newest comments other people left on any of your "
        "tracks. Pass next_cursor back as cursor."
    ),
    input_schema=INPUT_SCHEMA,
    route="GET /comments",
    example_response={"comments": [COMMENT], "next_cursor": None},
)
async def list_comments(ctx: ToolContext, args: dict[str, Any]) -> Any:
    if track_id := args.get("track_id"):
        rows, cursor = await page(ctx, f"/tracks/{track_id}/comments", args, threaded=1, filter_replies=0)
        return {"comments": [{**comment_row(r), "track_id": track_id} for r in rows], "next_cursor": cursor}
    data = (await graphql(ctx, "UserTrackComments", _ALL, {"after": args.get("cursor")}))[
        "userTrackCommentsWithReplies"
    ] or {}
    comments = data.get("comments") or []
    cursor = (data.get("pageInfo") or {}).get("endCursor") if comments else None
    return {"comments": [_graph_row(c) for c in comments], "next_cursor": cursor}
