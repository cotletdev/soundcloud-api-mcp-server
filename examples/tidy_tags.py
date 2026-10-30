#!/usr/bin/env python3
"""Find your SoundCloud tracks with no genre or no tags, and set them.

    python tidy_tags.py                                    # list the tracks that miss either
    python tidy_tags.py --genre Ambient --tags ambient "field recording"           # shows what it would change
    python tidy_tags.py --genre Ambient --tags ambient "field recording" --apply   # changes them

Only empty fields are filled: a genre or tags you set before stay. `--track-id` limits it to one track.
"""

import argparse
import json

from soundcloud_api_mcp.scripting import call, paginate, run, write_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--genre", help="Genre for tracks that have none")
    parser.add_argument("--tags", nargs="+", help="Tags for tracks that have none; multi-word tags in quotes")
    parser.add_argument("--track-id", help="Only this track")
    parser.add_argument("--apply", action="store_true", help="Make the changes; without it the script only shows them")
    args = parser.parse_args()

    tracks = list(paginate("list_tracks", {"limit": 50}, "tracks"))
    if args.track_id:
        tracks = [t for t in tracks if t["track_id"] == args.track_id]
    missing = [t for t in tracks if not t.get("genre") or not t.get("tags")]
    if not args.genre and not args.tags:
        write_rows([{k: t.get(k) for k in ("track_id", "title", "genre", "tags", "url")} for t in missing], None)
        return
    for track in missing:
        change = {"track_id": track["track_id"]}
        if args.genre and not track.get("genre"):
            change["genre"] = args.genre
        if args.tags and not track.get("tags"):
            change["tags"] = args.tags
        if len(change) == 1:
            continue
        if not args.apply:
            print(json.dumps({"would_change": track.get("title"), **change}))
            continue
        updated = call("update_track", change)
        print(json.dumps({"changed": updated.get("title"), "genre": updated.get("genre"), "tags": updated.get("tags")}))


if __name__ == "__main__":
    run(main)
