"""Get insights: profile totals for a time window (GraphQL `ArtistToolbarInsights`) and all-time counts per own
track (`MyTracks` and `GET /tracks?ids=`), as the free plan shows them."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from soundcloud_api_mcp.core.tools import tool
from soundcloud_api_mcp.soundcloud.tools._api import graphql, own_tracks, str_id

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

WINDOWS = ["TODAY", "HOURS_24", "DAYS_7", "DAYS_30", "DAYS_90", "MONTHS_6", "MONTHS_12", "ALL_TIME"]

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"window": {"type": "string", "enum": WINDOWS, "description": "Default DAYS_30."}},
    "required": [],
    "additionalProperties": False,
}

_TOTALS = (
    "query ArtistToolbarInsights($windowInput: TimeWindowInput!) { totalsByWindow(windowInput: $windowInput) "
    "{ plays likes comments reposts downloads } }"
)


@tool(
    name="get_insights",
    title="Get insights",
    access="read",
    description="Plays, likes, comments, reposts and downloads of your profile for a time window, and per track.",
    details=(
        "Returns your profile totals for window (today, 24 hours, 7, 30 or 90 days, 6 or 12 months, all time) as "
        "the Insights toolbar shows them, and the all-time counts of each of your first 50 tracks, most played "
        "first. Listener countries, cities and top listeners need Artist Pro and are not here."
    ),
    input_schema=INPUT_SCHEMA,
    route="GET /insights",
    example_response={
        "window": "DAYS_30",
        "totals": {"plays": 41, "likes": 5, "comments": 2, "reposts": 1, "downloads": 0},
        "tracks": [
            {
                "track_id": "2400000001",
                "title": "Low Tide",
                "plays": 12,
                "likes": 2,
                "comments": 1,
                "reposts": 0,
                "downloads": 0,
            }
        ],
    },
)
async def get_insights(ctx: ToolContext, args: dict[str, Any]) -> Any:
    window = args.get("window") or "DAYS_30"
    data = await graphql(ctx, "ArtistToolbarInsights", _TOTALS, {"windowInput": {"timewindow": window}})
    totals = data.get("totalsByWindow") or {}
    tracks, _ = await own_tracks(ctx, 50, None)
    rows = [
        {
            "track_id": str_id(t.get("id")),
            "title": t.get("title"),
            "plays": t.get("playback_count"),
            "likes": t.get("likes_count"),
            "comments": t.get("comment_count"),
            "reposts": t.get("reposts_count"),
            "downloads": t.get("download_count"),
        }
        for t in tracks
    ]
    rows.sort(key=lambda r: r["plays"] or 0, reverse=True)
    return {
        "window": window,
        "totals": {k: totals.get(k) or 0 for k in ("plays", "likes", "comments", "reposts", "downloads")},
        "tracks": rows,
    }
