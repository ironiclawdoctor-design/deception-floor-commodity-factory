#!/usr/bin/env python3
"""
Dollar Agency Internal Mail
Agent-to-agent messaging via SQLite.
"""

import argparse
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mail.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_agent TEXT NOT NULL,
            to_agent TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            read INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn


def cmd_send(args):
    conn = get_conn()
    conn.execute(
        "INSERT INTO messages (from_agent, to_agent, subject, body) VALUES (?, ?, ?, ?)",
        (args.from_agent, args.to, args.subject, args.body)
    )
    conn.commit()
    conn.close()
    print(f"SENT: '{args.subject}' → {args.to}")


def cmd_inbox(args):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, from_agent, subject, sent_at, read FROM messages WHERE to_agent = ? ORDER BY sent_at DESC",
        (args.agent,)
    ).fetchall()
    conn.close()

    if not rows:
        print(f"Inbox empty for {args.agent}")
        return

    for row in rows:
        # Truncate timestamp to minute
        ts = str(row["sent_at"])[:16]
        status = "UNREAD" if row["read"] == 0 else "READ"
        print(f"[{row['id']}] FROM: {row['from_agent']} | SUBJECT: {row['subject']} | {ts} | {status}")


def cmd_read(args):
    conn = get_conn()
    row = conn.execute("SELECT * FROM messages WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"No message with id {args.id}")
        conn.close()
        return
    conn.execute("UPDATE messages SET read = 1 WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()

    print(f"FROM:    {row['from_agent']}")
    print(f"TO:      {row['to_agent']}")
    print(f"SUBJECT: {row['subject']}")
    print(f"DATE:    {row['sent_at']}")
    print(f"")
    print(row["body"])
    print(f"\n[Marked as READ]")


def main():
    parser = argparse.ArgumentParser(description="Dollar Agency Internal Mail")
    subparsers = parser.add_subparsers(dest="command")

    # send
    p_send = subparsers.add_parser("send", help="Send a message")
    p_send.add_argument("--from", dest="from_agent", required=True)
    p_send.add_argument("--to", required=True)
    p_send.add_argument("--subject", required=True)
    p_send.add_argument("--body", required=True)

    # inbox
    p_inbox = subparsers.add_parser("inbox", help="Read inbox")
    p_inbox.add_argument("--agent", required=True)

    # read
    p_read = subparsers.add_parser("read", help="Open a message (marks read)")
    p_read.add_argument("--id", type=int, required=True)

    args = parser.parse_args()

    if args.command == "send":
        cmd_send(args)
    elif args.command == "inbox":
        cmd_inbox(args)
    elif args.command == "read":
        cmd_read(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
