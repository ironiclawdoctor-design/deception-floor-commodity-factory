import urllib.request, json, pathlib, datetime

# Configuration from working script
API_KEY = '2824c3af-2b0f-4836-9185-7e9d4547e304'
GQL = 'https://gql.hashnode.com/'

def gql(query, variables=None):
    """Execute GraphQL query"""
    body = {'query': query}
    if variables:
        body['variables'] = variables
    
    req = urllib.request.Request(
        GQL, 
        data=json.dumps(body).encode(), 
        headers={
            'Content-Type': 'application/json',
            'Authorization': API_KEY
        }
    )
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

def publish_article(file_path):
    """Publish a single article from markdown file"""
    try:
        # Read and parse article
        path = pathlib.Path(file_path)
        lines = [l for l in path.read_text().split('\n') if l.strip()]
        
        # Extract title (first line, remove # prefix)
        title = lines[0].lstrip('#').strip()
        body = '\n'.join(lines[1:]).strip()
        
        print(f"Publishing: {title}")
        print(f"From file: {file_path}")
        
        # Get publication ID
        pub_id = gql('{publication(host:"dollaragency.hashnode.dev"){id}}')['data']['publication']['id']
        print(f"Publication ID: {pub_id}")
        
        # Define tags based on article content
        if 'ai' in title.lower() or 'digital' in title.lower():
            tags = [{'slug':'ai','name':'AI'}, {'slug':'technology','name':'Technology'}, {'slug':'humor','name':'Humor'}, {'slug':'psychology','name':'Psychology'}]
        elif 'allocation' in title.lower() or 'resource' in title.lower():
            tags = [{'slug':'productivity','name':'Productivity'}, {'slug':'strategy','name':'Strategy'}, {'slug':'management','name':'Management'}, {'slug':'humor','name':'Humor'}]
        elif 'nyc' in title.lower() or 'subway' in title.lower():
            tags = [{'slug':'nyc','name':'NYC'}, {'slug':'urban','name':'Urban Life'}, {'slug':'commuting','name':'Commuting'}, {'slug':'humor','name':'Humor'}]
        else:
            tags = [{'slug':'general','name':'General'}]
        
        # Publish article
        mutation = 'mutation P($i:PublishPostInput!){publishPost(input:$i){post{url}}}'
        variables = {
            'i': {
                'publicationId': pub_id,
                'title': title,
                'contentMarkdown': body,
                'tags': tags
            }
        }
        
        result = gql(mutation, variables)
        
        if 'errors' in result:
            print(f"❌ ERROR: {result['errors']}")
            return None
        else:
            url = result['data']['publishPost']['post']['url']
            print(f"✅ PUBLISHED: {url}")
            
            # Log to published articles
            published_entry = {
                'title': title,
                'url': url,
                'file': path.name,
                'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
            }
            open('/root/.openclaw/workspace/published-articles.jsonl', 'a').write(
                json.dumps(published_entry) + '\n'
            )
            print(f"📝 Logged to published-articles.jsonl")
            return published_entry
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return None

def main():
    """Publish the three new articles"""
    
    articles_to_publish = [
        'article-ai-digital-delusions.md',
        'article-allocation-paradox.md',
        'article-nyc-survival-algorithm.md'
    ]
    
    published_count = 0
    results = []
    
    print("=== DOLLAR AGENCY AUTONOMOUS PUBLISHING ===")
    print(f"API Key: {API_KEY[:8]}...")
    print(f"GraphQL Endpoint: {GQL}")
    print()
    
    for i, article_file in enumerate(articles_to_publish, 1):
        print(f"=== ARTICLE {i}/{len(articles_to_publish)} ===")
        
        result = publish_article(article_file)
        
        if result:
            published_count += 1
            results.append(result)
            print(f"✅ SUCCESS: {result['title']}")
        else:
            print(f"❌ FAILED: {article_file}")
        
        print()
        
        # Small delay between requests
        if i < len(articles_to_publish):
            print("⏳ Waiting 3 seconds before next article...")
            time.sleep(3)
    
    print("=== PUBLISHING SUMMARY ===")
    print(f"Successfully published: {published_count}/{len(articles_to_publish)}")
    
    if results:
        print("\n🎉 ARTICLES PUBLISHED:")
        for result in results:
            print(f"✅ {result['title']}")
            print(f"   URL: {result['url']}")
            print()
    
    print("Dollar Agency autonomous publishing complete!")

if __name__ == "__main__":
    import time
    main()