#!/usr/bin/env python3
import json, os, base64, urllib.request, urllib.parse, time

SA_FILE = "/root/.openclaw/workspace/secrets/gcp-service-account.json"
PROJECT_ID = "sovereign-see"
REGION = "us-central1"
SERVICE_NAME = "dollar-dashboard"

def load_sa():
    with open(SA_FILE) as f:
        return json.load(f)

def get_access_token(sa):
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        header_b64 = base64.urlsafe_b64encode(json.dumps({"alg":"RS256","typ":"JWT"}).encode()).rstrip(b'=')
        now = int(time.time())
        payload = {"iss": sa["client_email"],
                   "scope": "https://www.googleapis.com/auth/cloud-platform",
                   "aud": sa["token_uri"], "exp": now+3600, "iat": now}
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=')
        signing_input = header_b64 + b'.' + payload_b64
        pk = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
        sig = pk.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
        jwt = (signing_input + b'.' + base64.urlsafe_b64encode(sig).rstrip(b'=')).decode()
        data = urllib.parse.urlencode({"grant_type":"urn:ietf:params:oauth:grant-type:jwt-bearer","assertion":jwt}).encode()
        req = urllib.request.Request(sa["token_uri"], data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read()).get("access_token")
    except Exception as e:
        print(f"Auth error: {e}")
        return None

def api(token, method, url, body=None):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}

def main():
    sa = load_sa()
    token = get_access_token(sa)
    if not token:
        print("Failed to get token")
        return
    url = f"https://run.googleapis.com/v2/projects/{PROJECT_ID}/locations/{REGION}/services/{SERVICE_NAME}"
    result = api(token, "GET", url)
    if "error" in result:
        print("Service fetch error:", result["error"])
    else:
        print(json.dumps(result, indent=2))
        # Check container image
        template = result.get("template", {})
        containers = template.get("containers", [])
        if containers:
            image = containers[0].get("image", "")
            print(f"Current image: {image}")
        # Check service status
        print(f"Service URI: {result.get('uri', 'N/A')}")
        print(f"Ready: {result.get('conditions', [])}")

if __name__ == "__main__":
    main()