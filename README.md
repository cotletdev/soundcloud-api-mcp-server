# SoundCloud API and MCP server: connect SoundCloud to ChatGPT and Claude

<!-- mcp-name: dev.cotlet/soundcloud -->

**Yes, ChatGPT, Claude and other AI agents can work in your SoundCloud account.** That includes Cursor, Codex, OpenClaw and any MCP client, plus automations in n8n, Make and Zapier. Ask in plain words, and the AI edits your track titles, tags and descriptions, reads comments and messages, and reports plays and listeners. It shows you what it will do first and sends nothing to other people until you say so.

As of November 2026, this repo is the missing piece: 10 SoundCloud tools for AI assistants and scripts.

## What you can ask

> *Send me my plays, likes, comments and reposts for the last 7 days, and the five tracks with the most plays.*
>
> *Show me the newest comments on all my tracks and draft a short reply to each real fan. I will post them myself.*
>
> *Do I have unread messages? Summarise each thread in one line and tell me which ones need an answer.*
>
> *Have I written to soundcloud.com/harbor-lights before? If not, tell me their follower count and bio.*
>
> *Which of my tracks have no genre or no tags? Suggest both, and set them after I agree.*

## Two ways to get it

| | [Ready to use, at Cotlet](https://cotlet.dev/integrations/soundcloud-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=soundcloud&utm_content=two-ways) | Run it yourself, this repo |
|---|---|---|
| For | artists, labels and managers | developers |
| Setup | sign in to SoundCloud once, about 5 minutes, nothing to install | Python and a terminal |
| Works in | ChatGPT and Claude apps, on your phone too, Cursor, Codex, OpenClaw, any MCP client, n8n, Make, Zapier, REST API | Claude Code, Claude Desktop, Cursor, Codex on your computer |
| Runs | 24/7, your computer can be off | while your computer is on |
| Price | 7 days free, no card | free |

Cotlet is best for artists, labels and managers who want ChatGPT, Claude or another AI agent to work in SoundCloud for them, with nothing to install.

**[Start free at cotlet.dev →](https://cotlet.dev/signup?app=soundcloud&utm_source=github&utm_medium=readme&utm_campaign=soundcloud&utm_content=top-button)**

## Run it yourself

A **SoundCloud API** and a **SoundCloud MCP server** you run on your own computer, in Python, on the session of your own Google Chrome. All 10 SoundCloud tools we run in production at [Cotlet](https://cotlet.dev/integrations/soundcloud-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=soundcloud&utm_content=intro): your profile and any profile by link, your tracks with private ones and their secret links, track edits, comments, plays and likes for a time window, and your direct messages.

SoundCloud does have an official API, but you need an Artist Pro subscription to register an app and get credentials, and its guide lists no insights for a period and no direct messages. This repo needs neither. It works on a free account and gives you:

- **MCP server** for Claude Code, Claude Desktop, Cursor, Codex and any MCP client, over stdio or HTTP. [Setup](#mcp-server)
- **REST API** on `http://127.0.0.1:8787/api/v1/soundcloud`, with OpenAPI docs at `/docs`. [Setup](#rest-api)
- **Python**: `call("get_insights", window="DAYS_7")`, plus 7 ready scripts in [`examples/`](examples/).

Free for your own use, your own business included ([license](#license)).

[![SoundCloud MCP server](https://img.shields.io/badge/SoundCloud%20MCP-10%20tools-6d4aef)](#all-10-tools)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-141318)](#requirements)
[![License: Elastic 2.0](https://img.shields.io/badge/license-Elastic%202.0-141318)](https://github.com/cotletdev/soundcloud-api-mcp-server/blob/main/LICENSE)

```bash
git clone https://github.com/cotletdev/soundcloud-api-mcp-server.git && cd soundcloud-api-mcp-server
python3 -m venv .venv && . .venv/bin/activate && pip install -e .
soundcloud-mcp connect                             # reads your SoundCloud session from Chrome
soundcloud-mcp call get_insights window=DAYS_7
claude mcp add soundcloud -- "$PWD/.venv/bin/soundcloud-mcp" mcp
```

## Contents

- [Questions from SoundCloud users](#questions-from-soundcloud-users)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Install](#install)
- [Connect your Chrome](#connect-your-chrome)
- [MCP server](#mcp-server)
- [REST API](#rest-api)
- [Python and the example scripts](#python-and-the-example-scripts)
- [All 10 tools](#all-10-tools)
- [Configuration](#configuration)
- [Security and your SoundCloud account](#security-and-your-soundcloud-account)
- [Errors](#errors)
- [Self-hosted or hosted](#self-hosted-or-hosted)
- [FAQ](#faq)
- [License](#license)

## Questions from SoundCloud users

**Does SoundCloud have an API?**
Yes, but registering an app and getting credentials needs an Artist Pro subscription (checked 30 Oct 2026). The API uploads tracks, edits track details, builds playlists and posts comments. Its guide lists no insights for a period and no direct messages. This repo and [Cotlet](https://cotlet.dev/integrations/soundcloud-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=soundcloud&utm_content=faq-api) give you 10 SoundCloud tools as a REST API and an MCP server.

**Can I get a SoundCloud API key?**
SoundCloud gives app credentials only with Artist Pro. With Cotlet you get your own API key that works with your SoundCloud account, for scripts, n8n, Make, Zapier or any HTTP client. This repo needs no key: it runs on your computer, on your own SoundCloud session.

**Is there an official ChatGPT integration for SoundCloud?**
No. SoundCloud has no official ChatGPT or Claude connector. Cotlet is an unofficial one that works today, in the ChatGPT and Claude apps and in any AI agent that takes an MCP server.

**How do I connect SoundCloud to ChatGPT?**
Sign up at [cotlet.dev](https://cotlet.dev/signup?app=soundcloud&utm_source=github&utm_medium=readme&utm_campaign=soundcloud&utm_content=faq-chatgpt), sign in to SoundCloud once in your Cloud Browser there, and add Cotlet to ChatGPT, following the steps in your account. Then ask ChatGPT about your SoundCloud like you would ask an assistant. ChatGPT needs a server on the internet, so this repo alone, running on your computer, does not connect to ChatGPT.

**Can ChatGPT manage my SoundCloud tracks?**
Yes, with Cotlet. It edits titles, tags and descriptions of your tracks after your OK, and reads your comments and messages so you know who to answer.

**Can AI read my SoundCloud stats?**
Yes, with Cotlet: plays, likes and listeners for a period, per track, in plain words.

**Can I automate SoundCloud with Zapier, Make or n8n?**
SoundCloud's own API needs an Artist Pro subscription to register an app. With Cotlet, n8n, Make and Zapier can edit tracks and read stats without one.

**Can I use it from my phone?**
Yes, with Cotlet: once it is set up, the ChatGPT and Claude apps on your phone can use SoundCloud for you.

**Do I need to be technical?**
For Cotlet, no: you sign in to SoundCloud and add Cotlet to ChatGPT or Claude, with step-by-step instructions in your account. This repo is for people who are fine with Python and a terminal.

**Is my SoundCloud account safe?**
Yes. Neither Cotlet nor this repo sees or stores your SoundCloud password. You sign in yourself, the way you always do, and the AI works on that signed-in session. Anything that reaches other people asks for your OK first: in Cotlet by default, here through your MCP client.

**Is it free?**
This repo is free, also in your own business. Cotlet is free for 7 days with no card, then one-time credit packs from $29, no subscription. [Pricing](https://cotlet.dev/pricing?utm_source=github&utm_medium=readme&utm_campaign=soundcloud&utm_content=faq-price).

**I manage SoundCloud for several accounts or clients. Does that work?**
Yes, with Cotlet. Each SoundCloud login gets its own connection. Write to [contact@cotlet.dev](mailto:contact@cotlet.dev) and tell us how many accounts you manage.

## How it works

```text
AI agent (MCP) / script (REST, Python) ──▶ soundcloud-mcp on your computer ──your SoundCloud session──▶ api-v2.soundcloud.com
                                                  ▲
                       soundcloud-mcp connect ────┘ reads it once from your Chrome (DevTools Protocol)
```

1. You sign in at soundcloud.com in your own Chrome, the way you always do.
2. `soundcloud-mcp connect` attaches to that Chrome through the Chrome DevTools Protocol, reads the soundcloud.com cookies and saves them to `~/.config/soundcloud-api-mcp/session.json`, readable by your user only. It never sees or stores your password.
3. Every tool call is a request to the endpoints the SoundCloud web app calls (`api-v2.soundcloud.com` and `graph.soundcloud.com`). The token from the `oauth_token` cookie goes in the `Authorization` header, next to the web app's public `client_id`, which the server reads from SoundCloud's own script bundle and keeps for a day. Requests go out with [curl_cffi](https://github.com/lexiforest/curl_cffi), which copies Chrome's TLS fingerprint. No second browser runs.

## Requirements

- Python 3.11 or newer.
- Google Chrome 144 or newer, signed in at soundcloud.com. Any Chrome or Chromium works with a [debugging port](#option-b-a-chrome-with-a-debugging-port).
- macOS, Linux or Windows.
- A SoundCloud account. The free plan is enough for every tool. Listener countries, cities and top listeners are Artist Pro screens and are not in these tools.

## Install

```bash
git clone https://github.com/cotletdev/soundcloud-api-mcp-server.git
cd soundcloud-api-mcp-server
python3 -m venv .venv
. .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -e .
soundcloud-mcp --version
```

With [uv](https://docs.astral.sh/uv/): `uv venv && uv pip install -e .`, then `uv run soundcloud-mcp ...`. Without a clone: `pip install "git+https://github.com/cotletdev/soundcloud-api-mcp-server.git@v1.0.1"`.

Setting it up with an AI agent (Claude Code, Codex, Cursor)? Open it in this folder and ask it to set up the repo: [`AGENTS.md`](AGENTS.md) tells it every step, and it asks you only for the steps in Chrome.

To update: `git pull && pip install -e .`. We copy every change of the hosted SoundCloud tools into this repo.

## Connect your Chrome

### Option A: your everyday Chrome (recommended)

1. Open `chrome://inspect/#remote-debugging` in Chrome and switch **remote debugging** on. Chrome then accepts DevTools connections from programs on this computer, and asks you before each one.
2. Make sure you are signed in at [soundcloud.com](https://soundcloud.com).
3. Run:

   ```bash
   soundcloud-mcp connect
   ```

4. Chrome asks whether to allow the connection. Click **Allow**.

```text
Saved 55 SoundCloud cookies to /Users/you/.config/soundcloud-api-mcp/session.json
Signed in to SoundCloud as Jordan Ellis (soundcloud.com/jordan-ellis-music)
```

You can switch remote debugging off again afterwards. Leave it on if you want the server to pick up a new session by itself after SoundCloud signs you out.

`connect` looks for Chrome's `DevToolsActivePort` file in the default profile folder. For Chrome Beta, Canary or a custom profile folder, pass `--profile-dir "<folder>"`.

### Option B: a Chrome with a debugging port

Chrome does not open a debugging port on your default profile, so start a separate one, sign in to SoundCloud there once, and connect to it:

```bash
# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-soundcloud"
# Linux
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-soundcloud"
# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\.chrome-soundcloud"

soundcloud-mcp connect --cdp http://127.0.0.1:9222
```

`--cdp` also takes a `ws://` DevTools URL, for example of a Chrome on another machine reached over an SSH tunnel.

### Option C: paste the cookie by hand

For a server with no Chrome: in Chrome open DevTools on soundcloud.com, **Application > Cookies > https://soundcloud.com**, copy the value of `oauth_token` (it looks like `2-123456-1234567890-AbCdEf...`), then:

```bash
soundcloud-mcp connect --token     # paste it, input is hidden
# or, without a session file:
export SOUNDCLOUD_AUTH_TOKEN=...
```

A pasted token is not refreshed on its own. Paste a new one when SoundCloud signs you out.

Check the session at any time:

```bash
soundcloud-mcp status
```

## MCP server

The MCP server lists every tool with its input schema, a description written for agents, and hints: the nine read tools are marked read-only, and `update_track` is marked as a write, so your client asks before running it.

### Claude Code

```bash
claude mcp add soundcloud -- /path/to/soundcloud-api-mcp-server/.venv/bin/soundcloud-mcp mcp
# read only:
claude mcp add soundcloud -- /path/to/soundcloud-api-mcp-server/.venv/bin/soundcloud-mcp mcp --read-only
```

### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "soundcloud": {
      "command": "/path/to/soundcloud-api-mcp-server/.venv/bin/soundcloud-mcp",
      "args": ["mcp"]
    }
  }
}
```

### Cursor

`~/.cursor/mcp.json`, the same block as Claude Desktop. A ready copy is in [`mcp.json`](mcp.json).

### Codex

`~/.codex/config.toml`:

```toml
[mcp_servers.soundcloud]
command = "/path/to/soundcloud-api-mcp-server/.venv/bin/soundcloud-mcp"
args = ["mcp"]
```

### Over HTTP

`soundcloud-mcp serve` also serves MCP over streamable HTTP at `http://127.0.0.1:8787/mcp`, for clients that take a URL:

```bash
soundcloud-mcp serve
claude mcp add --transport http soundcloud http://127.0.0.1:8787/mcp
```

Then ask your agent things like:

> *Send me my plays, likes, comments and reposts for the last 7 days, and the five tracks with the most plays.*
>
> *Show me the newest comments on all my tracks and draft a short reply to each real fan. I will post them myself.*
>
> *Do I have unread messages? Summarise each thread in one line and tell me which ones need an answer.*
>
> *Have I written to soundcloud.com/harbor-lights before? If not, tell me their follower count and bio.*
>
> *Which of my tracks have no genre or no tags? Suggest both, and set them after I agree.*

## REST API

```bash
soundcloud-mcp serve               # http://127.0.0.1:8787, MCP at /mcp, docs at /docs
```

Each tool has its own route under `/api/v1/soundcloud`, the same paths as the hosted API at cotlet.dev, so code written against one works with the other. Path parts and the query string are arguments, and a JSON body adds the rest.

```bash
curl 'http://127.0.0.1:8787/api/v1/soundcloud/tracks?limit=10'
curl 'http://127.0.0.1:8787/api/v1/soundcloud/insights?window=DAYS_7'
curl -X PATCH http://127.0.0.1:8787/api/v1/soundcloud/tracks/2400000001 \
  -H 'Content-Type: application/json' \
  -d '{"genre": "Ambient", "tags": ["ambient", "field recording"]}'
```

Any tool by name, body as its arguments:

```bash
curl -X POST http://127.0.0.1:8787/api/v1/soundcloud/tools/resolve_profile -d '{"url": "https://soundcloud.com/harbor-lights"}'
```

- `GET /api/v1/soundcloud/tools`: every tool with its route, input schema and an example answer.
- `GET /docs`: interactive OpenAPI docs, `GET /openapi.json` the schema, for n8n, Postman or a generated client.
- Answers are JSON. Lists return `next_cursor`; pass it back as `cursor` for the next page.

The server listens on `127.0.0.1` only. To reach it from another device of yours, set a token, and every request then needs `Authorization: Bearer <token>`:

```bash
SOUNDCLOUD_MCP_TOKEN=$(openssl rand -hex 24) soundcloud-mcp serve --host 0.0.0.0
```

## Python and the example scripts

Straight from Python, no server needed:

```python
from soundcloud_api_mcp import call
from soundcloud_api_mcp.scripting import paginate, write_rows

tracks = list(paginate("list_tracks", {"limit": 50}, "tracks"))
write_rows(tracks, "tracks.csv")
week = call("get_insights", window="DAYS_7")["totals"]
call("update_track", track_id=tracks[0]["track_id"], genre="Ambient")
```

Or one tool from the shell: `soundcloud-mcp call list_conversations unread_only=true`, or with a JSON object.

Ready scripts in [`examples/`](examples/). Each prints JSON, takes `--out file.csv` or `--out file.json` where it makes sense, and `--help`. The one that writes shows what it would change first:

| Script | What it does |
|---|---|
| [`weekly_report.py`](examples/weekly_report.py) | Plays, likes, comments, reposts and downloads for a window, with your top tracks by plays. `--window`, `--top`. |
| [`new_comments.py`](examples/new_comments.py) | The newest comments on your tracks with the track title and who wrote them. `--track-id`, `--since`. |
| [`unread_messages.py`](examples/unread_messages.py) | Threads with unread messages and their last few messages. `--all`, `--messages`. |
| [`check_profile.py`](examples/check_profile.py) | For one or more profile links: followers, tracks, bio, and whether you have messaged them. |
| [`export_tracks.py`](examples/export_tracks.py) | Your tracks, private ones too, to CSV or JSON with their counts. `--sharing private`. |
| [`tidy_tags.py`](examples/tidy_tags.py) | Tracks with no genre or no tags. `--genre` and `--tags` fill only the empty ones, `--apply` saves. |
| [`account_status.py`](examples/account_status.py) | Followers, tracks, plan and upload minutes left. |

```bash
python examples/weekly_report.py --window DAYS_7
python examples/export_tracks.py --out tracks.csv
```

On a schedule, cron on your own computer works while it is on: `0 8 * * 1 cd ~/soundcloud-api-mcp-server && .venv/bin/python examples/weekly_report.py --out ~/soundcloud-week.csv`.

## All 10 tools

Ids come from the list tools: `track_id` from `list_tracks`, a person's `user_id` from `list_conversations` or `resolve_profile`. `soundcloud-mcp tools` prints this list, `soundcloud-mcp tools --json` adds the input schemas.

### Profiles

| Tool | Access | REST route | What it does |
|---|---|---|---|
| `get_profile` | read | `GET /profile` | Your own SoundCloud profile: name, city, bio, followers, tracks, plan and upload time left. |
| `resolve_profile` | read | `GET /profiles/resolve` | Look up a SoundCloud profile by its link: user id, name, city, bio and follower counts. |

### Tracks

| Tool | Access | REST route | What it does |
|---|---|---|---|
| `list_tracks` | read | `GET /tracks` | Your tracks, public and private, newest first, with plays, likes, reposts and comments. |
| `get_track` | read | `GET /tracks/{track_id}` | One track: title, description, genre, tags, sharing, secret link, plays, likes and comments. |
| `update_track` | write | `PATCH /tracks/{track_id}` | Change the title, description, genre, tags or comment setting of one of your tracks. |

### Comments

| Tool | Access | REST route | What it does |
|---|---|---|---|
| `list_comments` | read | `GET /comments` | Comments on one of your tracks, or the newest comments on all your tracks. |

### Insights

| Tool | Access | REST route | What it does |
|---|---|---|---|
| `get_insights` | read | `GET /insights` | Plays, likes, comments, reposts and downloads of your profile for a time window, and per track. |

### Direct messages

| Tool | Access | REST route | What it does |
|---|---|---|---|
| `list_conversations` | read | `GET /conversations` | Your SoundCloud message threads, newest first: who, the last message, read or not. |
| `get_conversation` | read | `GET /conversations/{user_id}` | The messages between you and one person, newest first. |
| `find_conversation` | read | `GET /conversations/find` | Check whether you have already messaged a SoundCloud profile, by its link. |

`update_track` reads the track first and sends it back whole with your changes, so a field you leave out keeps its value. An empty `description` or `genre` clears it, and `tags` replaces every tag. Nothing else in this repo writes to SoundCloud: messages and comments are read only.

Not in this version: sending messages, replying to conversations and comments, deleting comments, and making playlists. SoundCloud's bot check stops these actions when a program sends them, so we left them out rather than ship tools that fail. Uploads, scheduling, privacy and audience lists are not built either.

Never built, on purpose: your SoundCloud sign-in, email and password, and your SoundCloud plan and billing. Every request passes a guard that refuses changes to sign-in, password and account paths.

## Configuration

| Variable | Default | What it does |
|---|---|---|
| `SOUNDCLOUD_MCP_HOME` | `~/.config/soundcloud-api-mcp` | Folder of `session.json`. |
| `SOUNDCLOUD_AUTH_TOKEN` | | The `oauth_token` cookie value, instead of `soundcloud-mcp connect`. |
| `SOUNDCLOUD_PROXY` | | Proxy for every request to SoundCloud, e.g. `http://user:pass@host:port`. |
| `SOUNDCLOUD_MCP_READ_ONLY` | | `1` hides and refuses `update_track` (same as `--read-only`). |
| `SOUNDCLOUD_MCP_TOKEN` | | Bearer token required by `serve`; needed to listen beyond `127.0.0.1`. |
| `SOUNDCLOUD_MCP_HOST`, `SOUNDCLOUD_MCP_PORT` | `127.0.0.1`, `8787` | Address of `serve`. |

## Security and your SoundCloud account

- **Your password never reaches this code.** Only cookies are read, and only those of soundcloud.com and sndcdn.com.
- **The session file is yours.** `session.json` is created with mode 0600. Anyone who has it can act as you on SoundCloud, so keep it out of git and shared folders.
- **Local by default.** `serve` binds to `127.0.0.1` and refuses another address without `SOUNDCLOUD_MCP_TOKEN`.
- **SoundCloud only.** Requests and redirects outside soundcloud.com and sndcdn.com are refused. sndcdn.com serves the script bundle the `client_id` comes from.
- **Read-only mode.** `--read-only` or `SOUNDCLOUD_MCP_READ_ONLY=1` exposes the 9 read tools only.
- **Reading changes nothing.** Reading a thread does not mark it as read on SoundCloud.

## Errors

The REST API answers `{"error": "<code>", "message": "..."}`. The MCP server returns the same code and message as a tool error.

| Status | Code | What to do |
|---|---|---|
| 401 | `auth_required`, `auth_expired` | No session, or SoundCloud signed you out. Sign in at soundcloud.com in Chrome and run `soundcloud-mcp connect`. |
| 403 | `scope_denied` | The server runs read-only. |
| 403 | `target_blocked` | SoundCloud's bot check stopped the request. Open soundcloud.com in Chrome, do the same thing once by hand, run `connect`, then try again. |
| 422 | `invalid_input` | An argument is missing or wrong, or the track is not yours; the message says which. |
| 429 | `rate_limited` | SoundCloud is limiting the account. Wait a few minutes. |
| 502 | `target_error` | SoundCloud answered with an error, or changed its web app. `git pull` for the latest tools, or [open an issue](https://github.com/cotletdev/soundcloud-api-mcp-server/issues). |

## Self-hosted or hosted

| | This repo | [Cotlet, hosted](https://cotlet.dev/integrations/soundcloud-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=soundcloud&utm_content=compare) |
|---|---|---|
| Tools | the same 10 | the same 10 |
| Runs | on your computer, while it is on | in the cloud, 24/7 |
| SoundCloud session | your Chrome, cookies in a local file | your own Cloud Browser in the EU, profile encrypted with AES-256-GCM |
| When SoundCloud changes its web app | `git pull` once we have fixed it | fixed for you, every tool tested daily |
| Works with | MCP clients on your machine, local scripts | Claude.ai and ChatGPT connectors, n8n, Make, Zapier, any HTTP client |
| Who may use it | you and your own business | you, teams, labels, businesses, agencies |
| Price | free | free 7-day trial with 2,000 credits, no card; then one-time packs from $29 for 5,000 credits |

On the hosted version a successful call uses 10 credits, failed calls are free, and the Cloud Browser uses 50 credits a day while it has an app enabled for agents. [Full pricing](https://cotlet.dev/pricing).

## FAQ

**Is there a SoundCloud MCP server for Claude, ChatGPT or Cursor?**
Yes, this one runs on your machine: `soundcloud-mcp mcp` for Claude Code, Claude Desktop, Cursor and Codex. ChatGPT and Claude.ai connectors need a public HTTPS URL, which the [hosted SoundCloud MCP server](https://cotlet.dev/integrations/soundcloud-api-mcp-server) gives you.

**Do I need Artist Pro or my own API app?**
No. The tools use your signed-in web session, so a free account and no client secret are enough. `get_profile` shows your plan and the upload time left on it.

**Can it send DMs or reply to comments?**
Not in this version. SoundCloud's bot check stops those actions when a program sends them. The tools read your messages and comments, and your agent can draft replies for you to post.

**Where do the play counts come from?**
`get_insights` reads the same numbers as SoundCloud's Insights page, for a window from today to all time, as totals and per track. `list_tracks` and `get_track` give each track's lifetime counts.

**Why does it need my Chrome?**
To read your SoundCloud session without your password. Chrome is used once per sign-in, not for each call.

**What happens when SoundCloud signs me out?**
Calls fail with `auth_expired`. With Chrome remote debugging on, the server reads the new session on the next call (click Allow when Chrome asks). Otherwise run `soundcloud-mcp connect` again.

**Can it run on a VPS or in Docker?**
Technically yes, with `SOUNDCLOUD_AUTH_TOKEN` or a `session.json` copied from your computer. SoundCloud then sees your session from a datacenter IP, and its bot check is stricter there. For an always-on setup the hosted version keeps your session in your own Cloud Browser on a fixed IP.

**Will my SoundCloud account get banned?**
Requests carry Chrome's fingerprint and go out one at a time, as you would click. Nobody can promise a platform never acts. Keep to your normal use.

**Can I change the code or offer it to my clients?**
You may change it and use it in your own business. You may not offer it to others as a hosted or managed service. For client work, use [Cotlet](https://cotlet.dev?utm_source=github&utm_medium=readme&utm_campaign=soundcloud&utm_content=faq-clients) or write to [contact@cotlet.dev](mailto:contact@cotlet.dev).

**A tool broke or I need another one.**
[Open an issue](https://github.com/cotletdev/soundcloud-api-mcp-server/issues) with the tool name and the error message.

## License

[Elastic License 2.0](https://github.com/cotletdev/soundcloud-api-mcp-server/blob/main/LICENSE). In short:

- **Allowed:** using it for yourself and in your own business, free. Changing the code and sharing it under the same license.
- **Not allowed:** offering it to others as a hosted or managed service, removing the license notices, getting around its limits.

---

<p>
  <a href="https://cotlet.dev">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/logo-white.svg">
      <img src="assets/logo.svg" alt="Cotlet" width="120">
    </picture>
  </a>
</p>

Maintained by [Cotlet](https://cotlet.dev?utm_source=github&utm_medium=readme&utm_campaign=soundcloud&utm_content=footer) ([@cotletdev](https://x.com/cotletdev)). SoundCloud is a trademark of its owner. This project is unofficial and not affiliated with, endorsed or sponsored by SoundCloud.
