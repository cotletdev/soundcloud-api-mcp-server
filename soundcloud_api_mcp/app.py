"""Everything the server knows about SoundCloud outside `soundcloud/`: names, domains and the session cookie.

The rest of the package reads these values and never names the app itself.
"""

from __future__ import annotations

NAME = "SoundCloud"
SLUG = "soundcloud"
# The command and the prefix of every environment variable (SOUNDCLOUD_AUTH_TOKEN, SOUNDCLOUD_MCP_TOKEN ...).
CLI = "soundcloud-mcp"
ENV = "SOUNDCLOUD"
# Requests may reach only these hosts and their subdomains. Their cookies are read from Chrome.
# api-v2 and graph are subdomains of soundcloud.com; sndcdn.com serves the web bundle that holds the client_id.
DOMAINS = ("soundcloud.com", "sndcdn.com")
# Present only while signed in. The first is the cookie a pasted token sets. Tools send its value as the
# `Authorization: OAuth <token>` header too: api-v2 answers 401 to the cookie alone.
SESSION_COOKIES = ("oauth_token",)
COOKIE_DOMAIN = ".soundcloud.com"
LOGIN_URL = "https://soundcloud.com/signin"
# A final URL with one of these means the app signed the session out.
LOGGED_OUT_MARKERS = ("/signin",)
# An answer with one of these asks you to sign in again before a sensitive action. SoundCloud has none.
RELOGIN_MARKERS: tuple[str, ...] = ()
# Paths of your SoundCloud account that tools may read but never write. Common password, email and sign-in
# paths are refused for every app (core/account_guard.py); SoundCloud adds none.
ACCOUNT_PATHS: tuple[str, ...] = ()
# REST routes live under this path, the same as on cotlet.dev.
API_PREFIX = "/api/v1/soundcloud"
# Prepended to the MCP server's instructions: where an agent starts.
AGENT_START = "Start with get_profile or list_tracks: their ids are what the other tools take."
