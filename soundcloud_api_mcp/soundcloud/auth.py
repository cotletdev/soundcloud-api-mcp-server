"""Who is signed in: SoundCloud's own answer for the account (api-v2.soundcloud.com/me), for "Signed in as ..."."""

from __future__ import annotations

from typing import TYPE_CHECKING

from soundcloud_api_mcp.core.errors import AuthExpiredError
from soundcloud_api_mcp.soundcloud.client import api

if TYPE_CHECKING:
    from soundcloud_api_mcp.core.context import ToolContext


async def whoami(ctx: ToolContext) -> str | None:
    """None only when SoundCloud says signed out; any other failure raises (detection tries again later)."""
    try:
        response = await api(ctx, "GET", "/me")
    except AuthExpiredError:
        return None
    me = response.json() or {}
    name = me.get("full_name") or me.get("username") or ""
    permalink = me.get("permalink")
    return f"{name} (soundcloud.com/{permalink})" if name and permalink else name or None
