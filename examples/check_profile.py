#!/usr/bin/env python3
"""Before you write to someone on SoundCloud: have you messaged them already, and who are they.

    python check_profile.py https://soundcloud.com/harbor-lights
    python check_profile.py harbor-lights other-artist third-artist --out checked.csv

For each profile: followers, tracks, city and bio, whether you have a thread, and its last message.
"""

import argparse

from soundcloud_api_mcp.scripting import call, run, write_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("profiles", nargs="+", help="Profile links or the names after soundcloud.com/")
    parser.add_argument("--out", help="Save to .csv or .json instead of printing")
    args = parser.parse_args()

    rows = []
    for url in args.profiles:
        profile = call("resolve_profile", {"url": url})
        found = call("find_conversation", {"url": url})
        last = found.get("last_message") or {}
        rows.append(
            {
                "username": profile.get("username"),
                "url": profile.get("url"),
                "followers": profile.get("followers_count"),
                "tracks": profile.get("track_count"),
                "city": profile.get("city"),
                "bio": profile.get("description"),
                "messaged": found.get("messaged"),
                "last_message": last.get("text"),
                "last_message_at": last.get("sent_at"),
            }
        )
    write_rows(rows, args.out)


if __name__ == "__main__":
    run(main)
