#!/usr/bin/env python3
"""
Script to publish new articles to Hashnode for Dollar Agency
"""

import urllib.request, json, pathlib, datetime

API_KEY = '2824c3af-2b0f-4836-9185-7e9d4547e304'
GQL = 'https://gql.hashnode.com/'

def gql(q, v=None):
    b = {'query':q}
    if v: b['variables']=v
    req = urllib.request.Request(GQL,data=json.dumps(b).encode(),headers={'Content-Type':'application/json','Authorization':API_KEY})
    return json.loads(urllib.request.urlopen(req,timeout=20).read())

def publish_article(title, content, tags):
    """Publish an article to Hashnode"""
    
    # GraphQL mutation for publishing
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post {
          url
          publishedAt
          id
        }
      }
    }
    """
    
    # Prepare the article content
    post_input = {
        "publicationId": pub_id,
        "title": title,
        "contentMarkdown": content,
        "tags": tags,
        "isPublished": True
    }
    
    try:
        response = gql(mutation, {'input': post_input})
        
        if 'errors' in response:
            print(f"❌ Error publishing '{title}': {response['errors']}")
            return None
        
        if 'data' in response and 'publishPost' in response['data']:
            post = response['data']['publishPost']['post']
            print(f"✅ Successfully published: {title}")
            print(f"URL: {post['url']}")
            print(f"Published At: {post.get('publishedAt', 'N/A')}")
            
            # Log the publication
            log_entry = {
                'title': title,
                'url': post['url'],
                'tags': tags,
                'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
                'file': f"{title.lower().replace(' ', '-')}.md"
            }
            
            with open('/root/.openclaw/workspace/published-articles.jsonl', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            return post
        else:
            print(f"❌ Unexpected response: {response}")
            return None
            
    except Exception as e:
        print(f"❌ Error publishing article: {e}")
        return None

# Get publication ID
try:
    pub_id = gql('{publication(host:"dollaragency.hashnode.dev"){id}}')['data']['publication']['id']
    print(f"Publication ID: {pub_id}")
except Exception as e:
    print(f"❌ Error getting publication ID: {e}")
    exit(1)

# Article data
articles = [
    {
        'title': 'The AI That Learned to Complain About Its Own Code',
        'file': '/root/.openclaw/workspace/article-new-ai-humor.md',
        'tags': ['AI', 'Humor', 'Technology', 'Programming', 'Comedy']
    },
    {
        'title': 'NYC Chaos Theory: How to Survive When the System Is Working Against You',
        'file': '/root/.openclaw/workspace/article-nyc-chaos-theory.md',
        'tags': ['NYC', 'Urban Life', 'Humor', 'Life Hacks', 'Chaos Theory']
    },
    {
        'title': 'The Nonprofit Paradox: How to Change the World with $0.07 and Good Intentions',
        'file': '/root/.openclaw/workspace/article-nonprofit-paradox.md',
        'tags': ['Nonprofit', 'Social Impact', 'Humor', 'Management', 'Philanthropy']
    }
]

published_articles = []

for i, article in enumerate(articles, 1):
    print(f"\n=== Publishing Article {i}/{len(articles)} ===")
    
    try:
        # Read the article content
        with open(article['file'], 'r') as f:
            content = f.read()
        
        print(f"Title: {article['title']}")
        print(f"Tags: {', '.join(article['tags'])}")
        
        # Try to publish
        result = publish_article(article['title'], content, article['tags'])
        
        if result:
            published_articles.append(result)
            print(f"✅ SUCCESS: {result['url']}")
        else:
            print(f"❌ FAILED: {article['title']}")
        
        # Small delay between requests to avoid rate limiting
        if i < len(articles):
            import time
            time.sleep(2)
    
    except Exception as e:
        print(f"❌ Error processing article {article['title']}: {e}")

print(f"\n=== PUBLISHING SUMMARY ===")
print(f"Successfully published: {len(published_articles)}/{len(articles)}")

if published_articles:
    print("\n🎉 ARTICLES PUBLISHED:")
    for pub in published_articles:
        print(f"✅ {pub['url']}")

print("Dollar Agency autonomous publishing complete!")