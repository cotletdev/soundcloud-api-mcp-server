"""Update track: title, description, genre, tags and comments switch of an own track (`PUT /tracks/{urn}`).

The classic edit form sends every saved attribute that has a value: a field left out is cleared (a PUT with only
the title wiped the description, 30.10.2026). So the track is read first and sent back whole with the changes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.errors import ErrorCode, ToolError
from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import ID_SCHEMA, fetch_track, me, track_row, write
from soundcloud_api_mcp.soundcloud.tools._examples import TRACK

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

# The classic app's `getAttributesToBeSaved` (web bundle, 30.10.2026) that a GET /tracks/{id} also returns.
_SAVED = (
    "caption",
    "commentable",
    "description",
    "downloadable",
    "genre",
    "label_name",
    "license",
    "permalink",
    "purchase_title",
    "purchase_url",
    "release_date",
    "sharing",
    "tag_list",
    "title",
)

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "track_id": {**ID_SCHEMA, "description": "One of your tracks, from list_tracks."},
        "title": {"type": "string", "minLength": 1, "maxLength": 100},
        "description": {"type": "string", "maxLength": 4000, "description": "Empty string clears it."},
        "genre": {"type": "string", "maxLength": 100, "description": "Free text, e.g. Ambient. Empty clears it."},
        "tags": {
            "type": "array",
            "items": {"type": "string", "minLength": 1, "maxLength": 60},
            "maxItems": 30,
            "description": "Replaces every tag. Multi-word tags are fine.",
        },
        "commentable": {"type": "boolean", "description": "Whether listeners can comment."},
    },
    "required": ["track_id"],
    "additionalProperties": False,
}


def _tag_list(tags: list[str]) -> str:
    return " ".join(f'"{t}"' if " " in t else t for t in (tag.strip().replace('"', "") for tag in tags) if t)


@tool(
    name="update_track",
    title="Update track",
    access="write",
    description="Change the title, description, genre, tags or comment setting of one of your tracks.",
    details=(
        "Edits one of your own tracks as its Edit form does. Give only the fields to change; the rest stay. tags "
        "replaces all tags. Sharing, audio and artwork are not changed here. Returns the track as saved."
    ),
    input_schema=INPUT_SCHEMA,
    route="PATCH /tracks/{track_id}",
    example_response=TRACK,
)
async def update_track(ctx: ToolContext, args: dict[str, Any]) -> Any:
    changes = {k: args[k] for k in ("title", "description", "genre", "commentable") if k in args}
    if "tags" in args:
        changes["tag_list"] = _tag_list(args["tags"])
    if not changes:
        raise ToolError("Give at least one field to change.", ErrorCode.INVALID_INPUT)
    track = await fetch_track(ctx, args["track_id"])
    if str(track.get("user_id")) != str((await me(ctx)).get("id")):
        raise ToolError("This track is not yours.", ErrorCode.INVALID_INPUT)
    body = {key: track[key] for key in _SAVED if track.get(key) is not None}
    saved = await write(ctx, "PUT", f"/tracks/{track.get('urn')}", {"track": {**body, **changes}})
    return track_row(saved if isinstance(saved, dict) and saved.get("id") else await fetch_track(ctx, args["track_id"]))
