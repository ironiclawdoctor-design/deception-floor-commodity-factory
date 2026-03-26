# Square API Token Acquisition (Idiot-Proof Guide)

## Objective
Get a Square API access token for your Cash App account (`$DollarAgency`) to enable automatic balance monitoring and Shannon minting.

## Prerequisites
1. A Square account (linked to Cash App)
2. Access to developer.squareup.com/apps

## Steps

### Step 1: Log in to Square Developer
- Go to https://developer.squareup.com/apps
- Log in with your Square credentials (the same as your Cash App login)

### Step 2: Create or Select an Application
- If you already have an application called "Dollar Agency", click on it.
- If not, click **Create Application**.
- Name: `Dollar Agency`
- Description: `Cash App balance monitoring for $DollarAgency`

### Step 3: Get Access Token
- Inside the application dashboard, go to **Credentials**.
- Under **Sandbox** or **Production**, locate the **Access Token**.
- Click **Show** to reveal the token.
- Copy the token (it starts with `EAAA...`).

### Step 4: Determine Environment
- **Sandbox token** is for testing (no real money). Use if you're just experimenting.
- **Production token** is for real Cash App transactions. Use this for live monitoring.

### Step 5: Store Token in Agency
- Edit `/root/.openclaw/workspace/secrets/cashapp.json`
- Add or update the following fields:

```json
{
  "square_access_token": "YOUR_TOKEN_HERE",
  "square_environment": "production"
}
```

### Step 6: Test the Token
Run the cashapp balance checker:
```bash
python3 /root/.openclaw/workspace/skills/cashapp/cashapp-balance.py
```

If you see `✅ Square API connected`, the token works.

## Troubleshooting

### Token not working?
- Ensure you selected the correct environment (sandbox vs production).
- Check that your Square account is linked to Cash App.
- Verify that the token hasn't expired (they can be revoked).

### No Cash App data?
The Square API may not expose Cash App balance directly. You might need to set up webhooks or use browser scraping (see cashapp skill docs).

## What This Unlocks
- Automatic detection of new donations to `$DollarAgency`
- Real-time Shannon minting when funds arrive
- Dollar ledger updates without manual input

## Notes
- The agency already has a working production token (check secrets/cashapp.json). If it's working, you don't need to do anything.
- Keep the token secret—never commit it to version control.