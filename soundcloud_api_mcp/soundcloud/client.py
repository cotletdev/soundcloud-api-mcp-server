"""SoundCloud web requests, read from the web app's bundle on 30.10.2026.

The web app (soundcloud.com) calls `https://api-v2.soundcloud.com/...` as JSON. Every call carries the query
`client_id` (the web client's public id, a 32-character string in one of the `a-v2.sndcdn.com/assets/*.js`
bundles) and, signed in, the header `Authorization: OAuth <token>`, the token being the cookie `oauth_token`
on `.soundcloud.com` (JS-readable). The cookie alone is not enough: api-v2 answers 401 without the header.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any
from urllib.parse import unquote

from soundcloud_api_mcp.core.errors import AuthExpiredError, ErrorCode, ToolError

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext
    from soundcloud_api_mcp.core.http import HttpResponse

WEB = "https://soundcloud.com"
API = "https://api-v2.soundcloud.com"
# 200 with the signed-in user (`id`, `username`, `permalink`, `full_name`); 401 without a valid token.
SESSION_URL = f"{API}/me"
TOKEN_COOKIE = "oauth_token"
# A dev run gets no cookie values, only this localStorage mirror of the token (set over CDP, BUILD.md Notes).
DEV_MIRROR_KEY = "cotlet:dev-auth"
_CLIENT_ID_KEY = "client-id"
_ASSET = re.compile(r'<script[^>]+src="(https://a-v2\.sndcdn\.com/assets/[^"]+\.js)"')
_CLIENT_ID = re.compile(r'client_id:"(\w{32})"')


def auth_token(ctx: ToolContext) -> str | None:
    """The `oauth_token` of this run or the profile, or the dev mirror; None when signed out."""
    received = getattr(ctx.http, "received_cookies", None) or []
    for cookie in [*reversed(received), *ctx.profile.cookies]:
        if cookie.name == TOKEN_COOKIE and cookie.value:
            return unquote(cookie.value)
    return (ctx.profile.local_storage.get(WEB) or {}).get(DEV_MIRROR_KEY) or None


def headers(ctx: ToolContext) -> dict[str, str]:
    """What the web app sends with every api-v2 call."""
    found = {"accept": "application/json, text/javascript, */*; q=0.01", "origin": WEB, "referer": f"{WEB}/"}
    token = auth_token(ctx)
    if token is not None:
        found["authorization"] = f"OAuth {token}"
    return found


def request_headers(ctx: ToolContext) -> dict[str, str]:
    """The tools' identity headers for `docker/prod-run … request` (integrations/CLAUDE.md). Add
    `?client_id=<id>` to the URL by hand: `client_id(ctx)` prints it in a dev run."""
    return headers(ctx)


async def client_id(ctx: ToolContext, fresh: bool = False) -> str:
    """The web client's public id from the bundles, kept a day; SoundCloud rotates it with deploys."""
    if not fresh and (cached := await ctx.cache_get(_CLIENT_ID_KEY)):
        return cached
    page = await ctx.call("GET", f"{WEB}/discover", headers={"accept": "text/html"})
    # The id sits in one of the last bundles: read them from the end.
    for src in reversed(_ASSET.findall(page.text)):
        found = _CLIENT_ID.search((await ctx.call("GET", src)).text)
        if found:
            await ctx.cache_set(_CLIENT_ID_KEY, found.group(1), ttl_s=86_400)
            return found.group(1)
    raise ToolError("SoundCloud changed its web app.", ErrorCode.TARGET_ERROR)


async def api(
    ctx: ToolContext, method: str, path: str, params: dict[str, Any] | None = None, body: Any = None
) -> HttpResponse:
    """One api-v2 call as the web app sends it. `ctx.call` reads a 401 as signed out, but a rotated
    `client_id` answers 401 too: that one call goes once more with a fresh id first."""
    if auth_token(ctx) is None:
        raise AuthExpiredError("SoundCloud has no session in this browser. Sign in again in Chrome, then run connect.")
    for fresh in (False, True):
        query = {**(params or {}), "client_id": await client_id(ctx, fresh=fresh), "app_locale": "en"}
        try:
            return await ctx.call(method, f"{API}{path}", params=query, json=body, headers=headers(ctx))
        except AuthExpiredError:
            if fresh:
                raise
    raise AssertionError("unreachable")
