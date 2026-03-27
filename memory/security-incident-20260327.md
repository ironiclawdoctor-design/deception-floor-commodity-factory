# Security Incident — Hashnode API Key Exposure
**Incident ID:** SEC-20260327-001  
**Timestamp:** 2026-03-27T01:41 UTC  
**Severity:** HIGH  
**Status:** OPEN — rotation required  

---

## What Was Exposed

**File:** `/root/.openclaw/workspace/secrets/hashnode.json`  
**Contents exposed:**
- `api_key`: `2824c3af-2b0f-4836-9185-7e9d4547e304`
- `pub_id`: `69c07db4d9da55a9a5fa1ab6`

**How it was exposed:** The key was included verbatim in a subagent result returned to the main session context. Any session participant or log viewer with access to the main agent output at the time of exposure may have seen the key.

---

## Rotation Instructions for CFO

### Step 1 — Regenerate the API Token

1. Go to: **https://hashnode.com/settings/developer**
2. Log in to the account associated with publication `69c07db4d9da55a9a5fa1ab6`
3. Find the **Personal Access Token** section
4. Click **Regenerate** or **Revoke and Create New**
5. Copy the new token

### Step 2 — Update the Secret on Disk

Replace the contents of `/root/.openclaw/workspace/secrets/hashnode.json` with:

```json
{
  "api_key": "<NEW_TOKEN_HERE>",
  "pub_id": "69c07db4d9da55a9a5fa1ab6"
}
```

Run:
```bash
chmod 600 /root/.openclaw/workspace/secrets/hashnode.json
```

### Step 3 — Verify Revocation

The old key `2824c3af-2b0f-4836-9185-7e9d4547e304` should return 401 after rotation. Any agent using it will fail auth — that is expected and correct.

### Step 4 — Audit

- Check Hashnode article publish/edit logs for any unauthorized posts after 2026-03-27T01:00 UTC
- If unauthorized activity is found, escalate to Hashnode support

---

## Impact Assessment

- **Scope:** Hashnode account access (read/write to blog publications)
- **Financial impact:** Low (no billing credentials exposed)
- **Reputational risk:** Medium (unauthorized article publishing possible)
- **Priority:** Rotate within 24 hours

---

## Post-Rotation Checklist

- [ ] New token stored in `secrets/hashnode.json`
- [ ] `chmod 600` applied
- [ ] Old token confirmed revoked (401 on test request)
- [ ] Hashnode publish log reviewed for unauthorized activity
- [ ] MEMORY.md updated with rotation date

---

*Documented by Fiesta subagent — suba-incident-recovery*
