#!/usr/bin/env python3
import requests
import json
import sys

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

GRAPHQL_URL = "https://gql.hashnode.com"

def publish(title, content, tags=[]):
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post {
          id
          title
          url
        }
      }
    }
    """
    variables = {
        "input": {
            "title": title,
            "publicationId": PUB_ID,
            "contentMarkdown": content,
            "tags": []
        }
    }
    r = requests.post(GRAPHQL_URL, json={"query": mutation, "variables": variables}, headers=HEADERS)
    data = r.json()
    if "errors" in data:
        print(f"ERROR: {data['errors']}", file=sys.stderr)
        return None
    post = data["data"]["publishPost"]["post"]
    print(f"PUBLISHED: {post['title']}\n  URL: {post['url']}")
    return post

articles = [
    {
        "title": "The Art of Being Unproductive: How AI Agents Master the Art of Doing Nothing",
        "content": open("article-ai-unproductive-genius.md", "r").read(),
        "tags": [{"name": "AI"}, {"name": "Machine Learning"}, {"name": "Programming"}, {"name": "Humor"}, {"name": "Productivity"}]
    },
    {
        "title": "The NYC Survival Guide: How to Thrive When the System is Working Against You",
        "content": open("article-nyc-survival-guide.md", "r").read(),
        "tags": [{"name": "NYC"}, {"name": "Life"}, {"name": "Urban Living"}, {"name": "Survival"}, {"name": "Humor"}]
    },
    {
        "title": "The Non-Profit Operating Manual: How to Run an Organization on $0.07 and Good Intentions",
        "content": open("article-nonprofit-shoestring-budget.md", "r").read(),
        "tags": [{"name": "Nonprofit"}, {"name": "Management"}, {"name": "Leadership"}, {"name": "Social Impact"}, {"name": "Humor"}]
    }
]

for article in articles:
    publish(article["title"], article["content"], article.get("tags", []))