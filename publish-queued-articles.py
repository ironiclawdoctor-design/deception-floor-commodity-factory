#!/usr/bin/env python3
"""
Publish queued local articles to Hashnode.
Runs against dollaragency.hashnode.dev.
Called by MPD cron or overnight-ops.
SR-028: logs rule pairing before exec.
"""

import json, urllib.request, pathlib, datetime, sys

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
GQL = "https://gql.hashnode.com/"
HOST = "dollaragency.hashnode.dev"
WS = pathlib.Path("/root/.openclaw/workspace")
LOG = WS / "exec-rule-log.jsonl"
SENT_LOG = WS / "published-articles.jsonl"

def gql(query, variables=None):
    body = {"query": query}
    if variables:
        body["variables"] = variables
    req = urllib.request.Request(
        GQL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": API_KEY}
    )
    resp = urllib.request.urlopen(req, timeout=20)
    return json.loads(resp.read())

def get_pub_id():
    r = gql('{ publication(host: "dollaragency.hashnode.dev") { id postsCount } }')
    return r["data"]["publication"]["id"], r["data"]["publication"]["postsCount"]

def parse_article(path):
    txt = path.read_text()
    lines = [l for l in txt.split("\n") if l.strip()]
    title = lines[0].lstrip("#").strip() if lines else path.stem
    body = "\n".join(lines[1:]).strip()
    return title, body

def already_published(title):
    if not SENT_LOG.exists():
        return False
    for line in SENT_LOG.read_text().splitlines():
        try:
            entry = json.loads(line)
            if entry.get("title") == title:
                return True
        except:
            pass
    return False

def publish(pub_id, title, body):
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
        publishPost(input: $input) {
            post { id url title }
        }
    }
    """
    r = gql(mutation, {"input": {
        "publicationId": pub_id,
        "title": title,
        "contentMarkdown": body,
        "tags": []
    }})
    if "errors" in r:
        return None, r["errors"]
    post = r["data"]["publishPost"]["post"]
    return post["url"], None

def log_rule(rule_id, status, note=""):
    entry = {
        "rule_id": rule_id,
        "status": status,
        "note": note,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    with open(LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def main():
    # SR-028: log before exec
    log_rule("PUBLISH-RUN", "running", "publish-queued-articles.py started")

    # Get articles
    articles = sorted(WS.glob("article-*.md"))
    if not articles:
        print("NO_ARTICLES: nothing to publish")
        log_rule("PUBLISH-RUN", "done", "no articles found")
        return

    # Get pub ID
    try:
        pub_id, current_count = get_pub_id()
        print(f"PUB_ID: {pub_id} | CURRENT_COUNT: {current_count}")
    except Exception as e:
        print(f"PUB_ID_FAIL: {e}")
        log_rule("PUBLISH-RUN", "error", f"pub_id fetch failed: {e}")
        sys.exit(1)

    published = 0
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    for path in articles:
        if published >= limit:
            break
        title, body = parse_article(path)
        if already_published(title):
            print(f"SKIP (already published): {title[:50]}")
            continue
        try:
            url, err = publish(pub_id, title, body)
            if err:
                print(f"FAIL: {title[:50]} — {err}")
                log_rule(f"PUBLISH-{path.stem}", "failed", str(err))
            else:
                print(f"PUBLISHED: {url}")
                with open(SENT_LOG, "a") as f:
                    f.write(json.dumps({
                        "title": title,
                        "url": url,
                        "file": path.name,
                        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
                    }) + "\n")
                log_rule(f"PUBLISH-{path.stem}", "success", url)
                published += 1
        except Exception as e:
            print(f"ERROR: {title[:50]} — {e}")
            log_rule(f"PUBLISH-{path.stem}", "error", str(e))

    print(f"\nDONE: {published} published | {len(articles) - published} remaining")
    log_rule("PUBLISH-RUN", "done", f"{published} published")

if __name__ == "__main__":
    main()
