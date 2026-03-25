#!/usr/bin/env python3
"""
Dollar Agency External Email Stub
Sends real email via SMTP if configured, otherwise queues to outbox-pending.jsonl.

Configure via environment variables:
  SMTP_HOST  - e.g. smtp.gmail.com
  SMTP_PORT  - default 587
  SMTP_USER  - your email address
  SMTP_PASS  - app password or SMTP password
  SMTP_FROM  - sender display address (defaults to SMTP_USER)
"""

import argparse
import os
import json
import smtplib
import ssl
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

OUTBOX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outbox-pending.jsonl")


def queue_email(to, subject, body):
    """Log email to outbox-pending.jsonl when SMTP is not configured."""
    entry = {
        "to": to,
        "subject": subject,
        "body": body,
        "queued_at": datetime.now(timezone.utc).isoformat()
    }
    with open(OUTBOX_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"QUEUED: email to {to} pending SMTP config")


def send_smtp(to, subject, body):
    """Send email via SMTP."""
    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", 587))
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASS"]
    from_addr = os.environ.get("SMTP_FROM", user)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(user, password)
        server.sendmail(from_addr, to, msg.as_string())

    print(f"SENT: email to {to} via {host}")


def main():
    parser = argparse.ArgumentParser(description="Dollar Agency External Email")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body")
    args = parser.parse_args()

    smtp_configured = all(
        os.environ.get(v) for v in ("SMTP_HOST", "SMTP_USER", "SMTP_PASS")
    )

    if smtp_configured:
        try:
            send_smtp(args.to, args.subject, args.body)
        except Exception as e:
            print(f"SMTP ERROR: {e}")
            print("Falling back to queue...")
            queue_email(args.to, args.subject, args.body)
    else:
        queue_email(args.to, args.subject, args.body)


if __name__ == "__main__":
    main()
