import urllib.request, json, pathlib, datetime
API_KEY = '2824c3af-2b0f-4836-9185-7e9d4547e304'
GQL = 'https://gql.hashnode.com/'
def gql(q, v=None):
    b = {'query':q}
    if v: b['variables']=v
    req = urllib.request.Request(GQL,data=json.dumps(b).encode(),headers={'Content-Type':'application/json','Authorization':API_KEY})
    return json.loads(urllib.request.urlopen(req,timeout=20).read())
pub_id = gql('{publication(host:"dollaragency.hashnode.dev"){id}}')['data']['publication']['id']
path = pathlib.Path('/root/.openclaw/workspace/article-agency-laughter.md')
lines = [l for l in path.read_text().split('\n') if l.strip()]
title = lines[0].lstrip('#').strip()
body = '\n'.join(lines[1:]).strip()
r = gql('mutation P($i:PublishPostInput!){publishPost(input:$i){post{url}}}',{'i':{'publicationId':pub_id,'title':title,'contentMarkdown':body,'tags':[{'slug':'ai','name':'AI'},{'slug':'humor','name':'Humor'},{'slug':'productivity','name':'Productivity'},{'slug':'agency','name':'Agency'}]}})
if 'errors' in r:
    print('ERR',r['errors'])
else:
    url=r['data']['publishPost']['post']['url']
    print('PUBLISHED:',url)
    open('/root/.openclaw/workspace/published-articles.jsonl','a').write(json.dumps({'title':title,'url':url,'file':path.name,'timestamp':datetime.datetime.utcnow().isoformat()+'Z'})+'\n')