#!/usr/bin/env python3
import requests
import json

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

GRAPHQL_URL = "https://gql.hashnode.com"

# Query series list
query_series = """
query {
  publication(host: "dollaragency.hashnode.dev") {
    seriesList(first: 10) {
      edges {
        node {
          id
          name
          slug
          posts(first: 20) {
            edges {
              node {
                id
                title
                url
                publishedAt
              }
            }
          }
        }
      }
    }
  }
}
"""

r = requests.post(GRAPHQL_URL, json={"query": query_series}, headers=HEADERS)
data = r.json()
print(json.dumps(data, indent=2))
