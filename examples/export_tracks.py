#!/usr/bin/env python3
"""Export your SoundCloud tracks, private ones too, to CSV or JSON with plays, likes, reposts and comments.

    python export_tracks.py --out tracks.csv
    python export_tracks.py --sharing private      # only private tracks, with their secret links

Pages are followed automatically.
"""

import argparse

from soundcloud_api_mcp.scripting import paginate, run, write_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sharing", choices=["all", "public", "private"], default="all")
    parser.add_argument("--max", type=int, help="Stop after this many tracks")
    parser.add_argument("--out", help="Save to .csv or .json instead of printing")
    args = parser.parse_args()

    rows = list(paginate("list_tracks", {"limit": 50}, "tracks", args.max))
    if args.sharing != "all":
        rows = [t for t in rows if t.get("sharing") == args.sharing]
    write_rows(rows, args.out)


if __name__ == "__main__":
    run(main)
