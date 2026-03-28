#!/usr/bin/env python3
"""
Script to check for new comments on Hashnode
"""

import requests
import json
import sys

def check_hashnode_comments():
    """Check for comments on Hashnode publication"""
    
    # GraphQL query
    query = """
    query GetComments {
      publication(id: "dollaragency") {
        posts(first: 10) {
          edges {
            node {
              id
              title
              url
              commentCount
              comments(first: 20) {
                edges {
                  node {
                    id
                    content
                    createdAt
                    author {
                      name
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    
    # GraphQL endpoint
    url = 'https://api.hashnode.com/graphql'
    
    try:
        response = requests.post(url, json={'query': query})
        print(f"Response Status: {response.status_code}")
        print(f"Response Length: {len(response.text)}")
        
        if response.status_code == 200:
            data = response.json()
            print("GraphQL query successful!")
            
            # Extract comments
            comments = []
            posts = data.get('data', {}).get('publication', {}).get('posts', {}).get('edges', [])
            
            for post_edge in posts:
                post = post_edge.get('node', {})
                post_title = post.get('title', 'No Title')
                post_url = post.get('url', 'No URL')
                comment_edges = post.get('comments', {}).get('edges', [])
                
                for comment_edge in comment_edges:
                    comment = comment_edge.get('node', {})
                    comment_content = comment.get('content', 'No Content')
                    comment_author = comment.get('author', {}).get('name', 'Anonymous')
                    comment_created = comment.get('createdAt', 'No Date')
                    
                    comments.append({
                        'post_title': post_title,
                        'post_url': post_url,
                        'content': comment_content,
                        'author': comment_author,
                        'created_at': comment_created
                    })
            
            print(f"Found {len(comments)} comments")
            return comments
        else:
            print(f"GraphQL error: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    comments = check_hashnode_comments()
    
    if comments:
        print("\n=== COMMENTS FOUND ===")
        for i, comment in enumerate(comments, 1):
            print(f"\n{i}. Post: {comment['post_title']}")
            print(f"   Author: {comment['author']}")
            print(f"   Content: {comment['content'][:100]}...")
            print(f"   Created: {comment['created_at']}")
    else:
        print("No comments found")