# GOG OAuth Recovery Plan (HE-007 Response)
## Steps to recreate (5 minutes):
1. Go to: https://console.cloud.google.com/apis/credentials
2. Create Project → "fiesta-agency"
3. OAuth consent screen → External → App name: "Fiesta Agency"
4. Credentials → Create OAuth client ID → Desktop app → Download JSON
5. Save as: ~/.openclaw/secrets/client_secret.json (chmod 600)
6. Run: gog auth credentials ~/.openclaw/secrets/client_secret.json
7. Run: gog auth add ironiclawdoctor@gmail.com --services gmail,calendar,drive,contacts,docs,sheets
## APIs to enable:
Gmail API, Google Calendar API, Drive API, Contacts API, Docs API, Sheets API
