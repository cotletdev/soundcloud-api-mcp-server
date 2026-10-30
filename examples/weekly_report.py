#!/usr/bin/env python3
"""Plays, likes, comments, reposts and downloads of your SoundCloud profile, with your top tracks by plays.

    python weekly_report.py                       # last 7 days
    python weekly_report.py --window DAYS_30 --top 10
    python weekly_report.py --out week.csv        # the per-track rows

Counts come from SoundCloud's own insights. Listener countries and cities need Artist Pro and are not here.
"""

import argparse
import json

from soundcloud_api_mcp.scripting import call, run, write_rows

WINDOWS = ["TODAY", "HOURS_24", "DAYS_7", "DAYS_30", "DAYS_90", "MONTHS_6", "MONTHS_12", "ALL_TIME"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--window", choices=WINDOWS, default="DAYS_7")
    parser.add_argument("--top", type=int, default=5, help="How many tracks to show, most plays first")
    parser.add_argument("--out", help="Save the per-track rows to .csv or .json")
    args = parser.parse_args()

    insights = call("get_insights", {"window": args.window})
    tracks = sorted(insights.get("tracks", []), key=lambda t: t.get("plays") or 0, reverse=True)[: args.top]
    if args.out:
        write_rows(tracks, args.out)
    print(json.dumps({"window": insights.get("window"), "totals": insights.get("totals"), "top": tracks}, indent=2))


if __name__ == "__main__":
    run(main)
