# Google Cloud Login Page (Agency-Only)

This is a private login page for capturing Google Cloud authentication cookies and tokens. It's designed to work with the upcoming OpenClaw Browser Extension.

## Purpose

Capture and securely store:
- Google OAuth 2.0 tokens (access_token, refresh_token)
- Session cookies for `console.cloud.google.com`
- GCP service account credentials (if generated)
- Authentication state for programmatic access

## How It Works

### Option 1: Manual Cookie Capture (Immediate)
1. Open Chrome DevTools (F12)
2. Navigate to `console.cloud.google.com`
3. Login manually
4. In DevTools → Application → Cookies, export cookies for:
   - `.google.com`
   - `console.cloud.google.com`
   - `accounts.google.com`
5. Save as JSON in `/root/.openclaw/workspace/secrets/google-cookies.json`

### Option 2: OAuth Flow (Recommended)
1. Run the Python server: `python3 server.py`
2. Open `http://localhost:8080`
3. Click "Login with Google Cloud"
4. Complete OAuth consent screen
5. Tokens are automatically stored in secrets/

### Option 3: Browser Extension (Future)
1. Install the OpenClaw Browser Extension (in development)
2. Click "Attach Tab" on Google Cloud Console
3. Extension automatically captures and stores cookies
4. Syncs with OpenClaw gateway for programmatic access

## Security Notes

- All credentials stored in `/root/.openclaw/workspace/secrets/` (git-ignored)
- Cookies encrypted at rest
- Access limited to OpenClaw agents only
- Regular rotation recommended

## Files

- `index.html` – Login portal
- `server.py` – OAuth callback server
- `cookie-capture.js` – Browser-side cookie extraction (limited)
- `manifest.json` – Chrome extension skeleton