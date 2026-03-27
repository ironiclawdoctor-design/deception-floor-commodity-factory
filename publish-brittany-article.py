#!/usr/bin/env python3
"""
Publish specific article to Hashnode - Brittany Kritis-Garip missing persons post
"""

import urllib.request, json, pathlib, datetime

API_KEY = '2824c3af-2b0f-4836-9185-7e9d4547e304'
GQL = 'https://gql.hashnode.com/'

def gql(query, variables=None):
    body = {'query': query}
    if variables:
        body['variables'] = variables
    req = urllib.request.Request(GQL, data=json.dumps(body).encode(),
        headers={'Content-Type':'application/json','Authorization':API_KEY})
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

def main():
    # Get publication ID
    pub = gql('{publication(host:"dollaragency.hashnode.dev"){id}}')
    pub_id = pub['data']['publication']['id']
    print(f"Publication ID: {pub_id}")
    
    # Read the specific article
    path = pathlib.Path('/root/.openclaw/workspace/article-missing-brittany-kritis-garip.md')
    txt = path.read_text()
    lines = [l for l in txt.split('\n') if l.strip()]
    title = lines[0].lstrip('#').strip()
    body = '\n'.join(lines[1:]).strip()
    
    print(f"Title: {title}")
    print(f"Body length: {len(body)} characters")
    
    # Publish the article
    mutation = '''
    mutation PublishPost($input: PublishPostInput!) {
        publishPost(input: $input) { post { id url title } }
    }'''
    
    r = gql(mutation, {'input': {
        'publicationId': pub_id, 
        'title': title, 
        'contentMarkdown': body, 
        'tags': []
    }})
    
    if 'errors' in r:
        print('ERROR:', r['errors'])
        return False
    else:
        url = r['data']['publishPost']['post']['url']
        print('PUBLISHED:', url)
        
        # Log the publication
        with open('/root/.openclaw/workspace/published-articles.jsonl','a') as f:
            f.write(json.dumps({
                'title':title, 
                'url':url, 
                'file':path.name,
                'timestamp':datetime.datetime.utcnow().isoformat()+'Z'
            })+'\n')
        return True

if __name__ == "__main__":
    main()