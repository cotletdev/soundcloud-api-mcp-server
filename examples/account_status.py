#!/usr/bin/env python3
"""Your SoundCloud account at a glance: followers, tracks, plan and the upload time left on it.

python account_status.py
"""

import argparse
import json

from soundcloud_api_mcp.scripting import call, run


def main() -> None:
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
    me = call("get_profile")
    left, limit = me.get("upload_seconds_left"), me.get("upload_seconds_limit")
    print(
        json.dumps(
            {
                "username": me.get("username"),
                "url": me.get("url"),
                "plan": me.get("plan"),
                "followers": me.get("followers_count"),
                "following": me.get("followings_count"),
                "tracks": me.get("track_count"),
                "private_tracks": me.get("private_tracks_count"),
                "upload_minutes_left": None if left is None else round(left / 60),
                "upload_minutes_limit": None if limit is None else round(limit / 60),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    run(main)
