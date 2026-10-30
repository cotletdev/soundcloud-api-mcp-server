# AGENTS.md

You are an AI agent in a clone of this repo. It is a self-hosted SoundCloud API and MCP server: 10 tools that work in the user's own SoundCloud account, through the session of their own Google Chrome. Your usual job is one of three: set it up for the user, use its tools for them, or change its code. Human docs: `README.md`.

## Before you start

- The license allows noncommercial use only (PolyForm Noncommercial 1.0.0, `LICENSE`). If the user is setting this up for a company, a team or clients, say so and point to the hosted version at https://cotlet.dev/integrations/soundcloud-api-mcp-server. Do not continue the setup for that use.
- Every tool acts as the user on SoundCloud. The one tool with access `write`, `update_track`, changes a track's title, description, genre, tags or comment setting, and listeners see the result.

## Set it up for the user

Do the steps yourself. Ask the user only for what needs their hands in Chrome.

1. Check Python: `python3 --version` must be 3.11 or newer.
2. Install in the repo root:

   ```bash
   python3 -m venv .venv && .venv/bin/pip install -e .
   .venv/bin/soundcloud-mcp --version
   ```

   On Windows the path is `.venv\Scripts\soundcloud-mcp`. With uv: `uv venv && uv pip install -e .`.
3. Ask the user to do two things in Chrome. You cannot open `chrome://` pages for them.
   - Open `chrome://inspect/#remote-debugging` and switch remote debugging on.
   - Be signed in at https://soundcloud.com.
4. Run `.venv/bin/soundcloud-mcp connect`. Tell the user to click **Allow** when Chrome asks about the connection. Success prints `Signed in to SoundCloud as <name> (soundcloud.com/<profile>)`.
5. Check: `.venv/bin/soundcloud-mcp status`, then `.venv/bin/soundcloud-mcp call get_profile`.
6. Add the MCP server to the user's client. Use the absolute path of `.venv/bin/soundcloud-mcp`:
   - Claude Code: `claude mcp add soundcloud -- <abs path>/.venv/bin/soundcloud-mcp mcp`
   - Claude Desktop, Cursor, Codex: the config blocks in `README.md`, section "MCP server".
   - Add `--read-only` after `mcp` if the user only wants to read.
   The client loads new MCP servers on its next start. Tell the user.

If step 4 fails:

| Message | What to do |
|---|---|
| `Chrome remote debugging is off` | Step 3 is not done, or Chrome is Beta, Canary or a custom profile: pass `--profile-dir "<profile folder>"`. |
| `Could not connect to Chrome` | The user did not click Allow, or Chrome is closed. Run `connect` again. |
| `This Chrome is not signed in to SoundCloud` | The user signs in at soundcloud.com in that Chrome, then run `connect` again. |
| No Chrome on this machine (a server) | The user copies the `oauth_token` cookie from Chrome DevTools (Application, Cookies, https://soundcloud.com) and runs `soundcloud-mcp connect --token` themselves. Never ask them to paste the token into the chat. |

## Use the tools

- With the MCP server added, call its tools. Without it: `.venv/bin/soundcloud-mcp call <tool> key=value ...`, or one JSON object as the argument.
- `.venv/bin/soundcloud-mcp tools` lists every tool with access and route. `tools --json` adds the input schemas.
- Start with `get_profile` or `list_tracks`. `track_id` comes from `list_tracks`, a person's `user_id` from `list_conversations` or `resolve_profile`.
- Lists return `next_cursor`. Pass it back as `cursor` for the next page.
- Before `update_track`, show the user the new values and get their OK. A field you leave out stays as it is; an empty `description` or `genre` clears it, and `tags` replaces every tag.
- For a script or a cron job, use `soundcloud_api_mcp.scripting` (`call`, `paginate`, `write_rows`) and the scripts in `examples/` as models.
- For a REST API (n8n, other languages): `.venv/bin/soundcloud-mcp serve`, routes under `http://127.0.0.1:8787/api/v1/soundcloud`, docs at `/docs`.

Errors come as `<code>: <message>`. `auth_expired` means SoundCloud signed the session out: the user signs in again in Chrome and you run `connect`. `target_blocked` means SoundCloud's bot check stopped a request: the user opens soundcloud.com in Chrome, does the same thing once by hand, and you run `connect` again. More codes: `README.md`, section "Errors".

## Keep secrets out

- `~/.config/soundcloud-api-mcp/session.json` and `SOUNDCLOUD_AUTH_TOKEN` give full access to the user's SoundCloud account. Never print, log, commit or copy their content.
- `serve` listens on 127.0.0.1. Never start it on another address without `SOUNDCLOUD_MCP_TOKEN`.

## Change the code

| Path | What | Edit? |
|---|---|---|
| `soundcloud_api_mcp/soundcloud/` | the SoundCloud tools, one file per tool in `tools/`, shared request code in `client.py` (client_id, OAuth header) and `tools/_api.py` | Yes for a local fix, but the next `git pull` brings our version of these files. Report the bug at https://github.com/cotletdev/soundcloud-api-mcp-server/issues |
| `soundcloud_api_mcp/app.py` | app name, domains, session cookie, REST prefix | Rarely |
| `soundcloud_api_mcp/core/` | `@tool` declaration, errors, the HTTP client with the session (`context.py`) | Yes |
| `soundcloud_api_mcp/session.py` | reading cookies from Chrome over CDP, the session file | Yes |
| `soundcloud_api_mcp/runner.py`, `api.py`, `mcp_server.py`, `mcp_context.py`, `cli.py` | tool registry, REST API, MCP server, its prompts and resources, command line | Yes |
| `examples/` | scripts for common jobs | Yes |

A new tool is a new file in `soundcloud_api_mcp/soundcloud/tools/` with a `@tool(...)` declaration (name, access, input schema, `route`). The registry finds it, and the REST API, the MCP server and the CLI show it without other changes.

There is no test suite. After a change, run `.venv/bin/soundcloud-mcp tools` and one read tool against the user's account.
