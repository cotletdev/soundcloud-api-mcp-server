"""Shared calls and answer shapes of the SoundCloud tools: the own user, GraphQL, REST paging, rows."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import parse_qs, urlsplit

from soundcloud_api_mcp.core.errors import ErrorCode, TargetBlockedError, ToolError
from soundcloud_api_mcp.core.helpers import limit
from soundcloud_api_mcp.soundcloud.client import WEB, api, client_id, headers

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext

GRAPH = "https://graph.soundcloud.com/graphql"
ID_SCHEMA: dict[str, Any] = {"type": "string", "pattern": "^[0-9]{1,20}$"}
LIMIT_SCHEMA: dict[str, Any] = {"type": "integer", "minimum": 1, "maximum": 50, "description": "Default 20."}
CURSOR_SCHEMA: dict[str, Any] = {"type": "string", "maxLength": 200, "description": "next_cursor from the last call."}
PROFILE_URL_SCHEMA: dict[str, Any] = {
    "type": "string",
    "minLength": 1,
    "maxLength": 300,
    "description": "Profile link (https://soundcloud.com/<name>) or the bare name after soundcloud.com/.",
}
# DataDome answers creating writes (messages, comments, playlists) with a slider challenge.
_BLOCKED = (
    "SoundCloud's bot check stopped this action. Open SoundCloud in Chrome, do the same "
    "action once by hand (and the slider if it shows), then try again."
)


def str_id(value: Any) -> str | None:
    return None if value is None else str(value)


def urn_id(urn: Any) -> str | None:
    """`soundcloud:comments:123` → `123`."""
    return str(urn).rsplit(":", 1)[-1] if urn else None


async def me(ctx: ToolContext) -> dict[str, Any]:
    """The signed-in user (`GET /me`)."""
    return (await api(ctx, "GET", "/me")).json() or {}


async def get(ctx: ToolContext, path: str, params: dict[str, Any] | None = None) -> Any:
    return (await api(ctx, "GET", path, params)).json()


async def write(ctx: ToolContext, method: str, path: str, body: Any = None) -> Any:
    """A write on api-v2; DataDome's challenge becomes a message a person can act on."""
    try:
        response = await api(ctx, method, path, body=body)
    except ToolError as exc:
        if exc.code == ErrorCode.TARGET_BLOCKED:
            raise TargetBlockedError(_BLOCKED) from exc
        raise
    if response.status == 404:
        raise ToolError("SoundCloud did not find it, or it is not yours.", ErrorCode.INVALID_INPUT)
    if response.status >= 400:
        raise ToolError("SoundCloud refused the change.", ErrorCode.TARGET_ERROR)
    return response.json() if response.text.strip() else None


async def graphql(ctx: ToolContext, name: str, query: str, variables: dict[str, Any]) -> dict[str, Any]:
    """One GraphQL operation as the Next.js app sends it (full text, no persisted hash)."""
    params = {"client_id": await client_id(ctx)}
    payload = {"operationName": name, "query": query, "variables": variables}
    extra = {**headers(ctx), "content-type": "application/json", "apollographql-client-name": "v2"}
    try:
        response = await ctx.call("POST", GRAPH, params=params, json=payload, headers=extra)
    except ToolError as exc:
        if exc.code == ErrorCode.TARGET_BLOCKED:
            raise TargetBlockedError(_BLOCKED) from exc
        raise
    body = response.json() or {}
    if body.get("errors") or not isinstance(body.get("data"), dict):
        raise ToolError("SoundCloud refused the request.", ErrorCode.TARGET_ERROR)
    return body["data"]


async def page(ctx: ToolContext, path: str, args: dict[str, Any], **params: Any) -> tuple[list[Any], str | None]:
    """One REST list page: `limit` + `offset` in, `collection` and the next offset (from `next_href`) out."""
    cursor = args.get("cursor") or "0"
    if not cursor.isdigit():
        raise ToolError("cursor must be the next_cursor value from the previous call.", ErrorCode.INVALID_INPUT)
    query = {**params, "limit": limit(args, 20, 50), "offset": cursor, "linked_partitioning": 1}
    body = await get(ctx, path, query) or {}
    rows = body.get("collection") or []
    following = (parse_qs(urlsplit(body.get("next_href") or "").query).get("offset") or [None])[0]
    return rows, following if rows and following and following != cursor else None


async def resolve(ctx: ToolContext, url: str) -> dict[str, Any]:
    """A profile link or bare name to the user object (`GET /resolve`)."""
    name = url.strip().split("?")[0].rstrip("/")
    if not name.startswith("http"):
        name = f"{WEB}/{name.removeprefix('soundcloud.com/').lstrip('@/')}"
    response = await api(ctx, "GET", "/resolve", {"url": name})
    found = response.json() if response.status == 200 else None
    if not isinstance(found, dict) or found.get("kind") != "user":
        raise ToolError("No SoundCloud profile at this link.", ErrorCode.INVALID_INPUT)
    return found


async def fetch_track(ctx: ToolContext, track_id: str) -> dict[str, Any]:
    """One track (`GET /tracks/{id}`): any public one, or an own private one."""
    response = await api(ctx, "GET", f"/tracks/{track_id}")
    found = response.json() if response.status == 200 else None
    if not isinstance(found, dict) or found.get("kind") != "track":
        raise ToolError("No track with this id that you can see.", ErrorCode.INVALID_INPUT)
    return found


def user_row(user: dict[str, Any]) -> dict[str, Any]:
    return {
        "user_id": str_id(user.get("id")),
        "permalink": user.get("permalink"),
        "username": user.get("username"),
        "full_name": user.get("full_name") or None,
        "url": user.get("permalink_url"),
        "city": user.get("city") or None,
        "country_code": user.get("country_code"),
        "followers_count": user.get("followers_count"),
        "verified": bool(user.get("verified")),
    }


def profile_row(user: dict[str, Any]) -> dict[str, Any]:
    """A profile with its counts and bio, as `/me`, `/users/{id}` and `/resolve` give it."""
    return {
        **user_row(user),
        "description": user.get("description") or None,
        "followings_count": user.get("followings_count"),
        "track_count": user.get("track_count"),
        "playlist_count": user.get("playlist_count"),
        "likes_count": user.get("likes_count"),
        "created_at": user.get("created_at"),
    }


def track_row(track: dict[str, Any]) -> dict[str, Any]:
    secret = track.get("secret_token")
    url = track.get("permalink_url")
    return {
        "track_id": str_id(track.get("id")),
        "title": track.get("title"),
        "url": url,
        "secret_url": f"{url}/{secret}" if url and secret else None,
        "sharing": track.get("sharing"),
        "description": track.get("description") or None,
        "genre": track.get("genre") or None,
        "tags": track.get("tag_list") or None,
        "commentable": track.get("commentable"),
        "duration_ms": track.get("duration"),
        "plays": track.get("playback_count"),
        "likes": track.get("likes_count"),
        "reposts": track.get("reposts_count"),
        "comments": track.get("comment_count"),
        "downloads": track.get("download_count"),
        "created_at": track.get("created_at"),
        "state": track.get("state"),
    }


def comment_row(comment: dict[str, Any]) -> dict[str, Any]:
    user = comment.get("user") or {}
    return {
        "comment_id": str_id(comment.get("id")),
        "track_id": str_id(comment.get("track_id")),
        "body": comment.get("body"),
        "at_ms": comment.get("timestamp"),
        "created_at": comment.get("created_at"),
        "user": {
            "user_id": str_id(user.get("id")),
            "permalink": user.get("permalink"),
            "username": user.get("username"),
            "url": user.get("permalink_url"),
        },
    }


async def own_tracks(ctx: ToolContext, first: int, after: str | None) -> tuple[list[dict[str, Any]], str | None]:
    """The own tracks, private ones too (Artist Studio's `MyTracks`), with their REST details and counts."""
    query = (
        "query MyTracks($first: Int, $after: String) { myTracks(first: $first, after: $after) "
        "{ tracks { urn } metadata { endCursor } } }"
    )
    data = (await graphql(ctx, "MyTracks", query, {"first": first, "after": after}))["myTracks"] or {}
    ids = [urn_id(t.get("urn")) for t in data.get("tracks") or [] if t.get("urn")]
    if not ids:
        return [], None
    found = {str(t.get("id")): t for t in await get(ctx, "/tracks", {"ids": ",".join(i for i in ids if i)}) or []}
    rows = [found[i] for i in ids if i in found]
    cursor = (data.get("metadata") or {}).get("endCursor") or None
    return rows, cursor if len(ids) >= first else None
