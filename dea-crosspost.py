#!/usr/bin/env python3
"""
DEA Cross-poster — posts all Hashnode articles to Write.as
Tracks what's already posted in writeas-posts.jsonl to avoid duplicates.
"""
import requests, json, os, time

HASHNODE_API = "https://gql.hashnode.com"
WRITEAS_API = "https://write.as/api/posts"
WRITEAS_POSTS_LOG = "/root/.openclaw/workspace/writeas-posts.jsonl"

def get_hashnode_posts():
    query = """
    query {
      publication(host: "dollaragency.hashnode.dev") {
        posts(first: 50) {
          edges {
            node {
              id title content { markdown } url
            }
          }
        }
      }
    }"""
    r = requests.post(HASHNODE_API, json={"query": query},
                      headers={"Content-Type": "application/json"})
    data = r.json()
    return [e["node"] for e in data["data"]["publication"]["posts"]["edges"]]

def get_posted_ids():
    if not os.path.exists(WRITEAS_POSTS_LOG):
        return set()
    posted = set()
    with open(WRITEAS_POSTS_LOG) as f:
        for line in f:
            try:
                posted.add(json.loads(line)["hashnode_id"])
            except: pass
    return posted

def post_to_writeas(title, body):
    r = requests.post(WRITEAS_API, json={
        "title": title,
        "body": body,
        "font": "mono",
        "lang": "en"
    })
    if r.status_code == 201:
        data = r.json()
        return data["data"]["id"], f"https://write.as/{data['data']['id']}"
    return None, None

posts = get_hashnode_posts()
posted_ids = get_posted_ids()
new_count = 0

for post in posts:
    if post["id"] in posted_ids:
        continue
    wid, url = post_to_writeas(post["title"], post["content"]["markdown"])
    if url:
        with open(WRITEAS_POSTS_LOG, "a") as f:
            f.write(json.dumps({
                "hashnode_id": post["id"],
                "title": post["title"],
                "writeas_id": wid,
                "url": url
            }) + "\n")
        print(f"✅ {post['title'][:50]} → {url}")
        new_count += 1
        time.sleep(1)  # be polite
    else:
        print(f"❌ Failed: {post['title'][:50]}")

print(f"\nDEA: {new_count} new posts cross-posted to Write.as")
print("— DEA, Democratic Expansion Autoapprove")
