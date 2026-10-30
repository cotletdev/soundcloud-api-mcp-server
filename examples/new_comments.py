#!/usr/bin/env python3
"""The newest comments on your SoundCloud tracks, with the track title, so you can answer the real fans.

python new_comments.py                         # newest comments on all your tracks
python new_comments.py --track-id 2400000001   # one track, every page
python new_comments.py --since 2026-10-01 --out comments.csv
"""

import argparse

from soundcloud_api_mcp.scripting import call, paginate, run, write_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--track-id", help="Only this track, from list_tracks")
    parser.add_argument("--since", help="Only comments on or after this date (YYYY-MM-DD)")
    parser.add_argument("--max", type=int, help="Stop after this many comments")
    parser.add_argument("--out", help="Save to .csv or .json instead of printing")
    args = parser.parse_args()

    if args.track_id:
        comments = list(paginate("list_comments", {"track_id": args.track_id, "limit": 50}, "comments", args.max))
    else:
        comments = call("list_comments")["comments"][: args.max]
    if args.since:
        comments = [c for c in comments if (c.get("created_at") or "") >= args.since]
    titles: dict[str, str] = {}
    rows = []
    for comment in comments:
        track_id = comment.get("track_id")
        if track_id and track_id not in titles:
            titles[track_id] = call("get_track", {"track_id": track_id}).get("title") or ""
        user = comment.get("user") or {}
        rows.append(
            {
                "created_at": comment.get("created_at"),
                "track": titles.get(track_id or "", ""),
                "from": user.get("username"),
                "profile": user.get("url"),
                "body": comment.get("body"),
                "at_seconds": (comment.get("at_ms") or 0) // 1000,
                "comment_id": comment.get("comment_id"),
            }
        )
    write_rows(rows, args.out)


if __name__ == "__main__":
    run(main)
