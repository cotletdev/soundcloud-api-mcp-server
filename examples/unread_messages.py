#!/usr/bin/env python3
"""Your SoundCloud message threads with unread messages, each with its last few messages.

    python unread_messages.py
    python unread_messages.py --all --messages 5
    python unread_messages.py --out unread.json

Reading here does not mark anything as read on SoundCloud.
"""

import argparse

from soundcloud_api_mcp.scripting import call, paginate, run, write_rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--all", action="store_true", help="Every thread, not only unread ones")
    parser.add_argument("--messages", type=int, default=3, help="Last messages to show per thread")
    parser.add_argument("--max", type=int, default=50, help="Stop after this many threads")
    parser.add_argument("--out", help="Save to .csv or .json instead of printing")
    args = parser.parse_args()

    params = {"unread_only": None if args.all else True, "limit": 50}
    rows = []
    for thread in paginate("list_conversations", params, "conversations", args.max):
        person = thread.get("with") or {}
        messages = call("get_conversation", {"user_id": thread["user_id"], "limit": args.messages})["messages"]
        rows.append(
            {
                "with": person.get("username"),
                "profile": person.get("url"),
                "read": thread.get("read"),
                "messages": [
                    {"sent_at": m.get("sent_at"), "from_me": m.get("from_me"), "text": m.get("text")} for m in messages
                ],
            }
        )
    write_rows(rows, args.out)


if __name__ == "__main__":
    run(main)
