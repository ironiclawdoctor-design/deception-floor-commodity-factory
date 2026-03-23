#!/usr/bin/env python3
"""
Fiesta Fundraising Backend
Port 9004 – Stripe integration, donation tracking, Shannon minting
"""

import os
import json
import sqlite3
import logging
from datetime import datetime, timezone
from flask import Flask, request, jsonify, make_response, send_from_directory
import stripe

# Configuration
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "pk_test_51PABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_51PABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_test_1234567890")
ENTROPY_API_URL = "http://127.0.0.1:9001"
PORT = int(os.getenv("FUNDRAISING_PORT", "9004"))

# Initialize
stripe.api_key = STRIPE_SECRET_KEY
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/donate', methods=['OPTIONS'])
@app.route('/webhook', methods=['OPTIONS'])
@app.route('/metrics', methods=['OPTIONS'])
@app.route('/balance', methods=['OPTIONS'])
def handle_options():
    return '', 200

@app.route('/', methods=['GET'])
def serve_index():
    """Serve the fundraising frontend."""
    return send_from_directory('/root/.openclaw/workspace/fundraising', 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    """Serve static files from fundraising directory."""
    return send_from_directory('/root/.openclaw/workspace/fundraising', path)

# Database setup
def init_db():
    conn = sqlite3.connect("/root/.openclaw/workspace/fundraising-backend/donations.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stripe_session_id TEXT UNIQUE,
            amount_cents INTEGER,
            donor_email TEXT,
            donor_message TEXT,
            status TEXT,
            shannon_minted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_raised_usd INTEGER DEFAULT 0,
            donor_count INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Helper: mint Shannon via entropy economy
def mint_shannon_for_donation(amount_cents, donor_email):
    """Convert USD cents to Shannon and mint via entropy economy."""
    try:
        # 1 USD = 100 cents = 100 Shannon (simplified)
        shannon_amount = amount_cents  # 1 cent = 1 Shannon
        import requests
        response = requests.post(
            f"{ENTROPY_API_URL}/mint/security",
            json={
                "agent": "fiesta-fundraising",
                "amount": shannon_amount,
                "description": f"Donation {amount_cents/100:.2f} USD from {donor_email}",
                "reference": "fundraising",
                "severity": "info"
            },
            timeout=5
        )
        if response.status_code == 200:
            logger.info(f"Minted {shannon_amount} Shannon for donation")
            return shannon_amount
        else:
            logger.error(f"Failed to mint Shannon: {response.text}")
            return 0
    except Exception as e:
        logger.error(f"Error minting Shannon: {e}")
        return 0

# Helper: update metrics
def update_metrics(amount_cents):
    conn = sqlite3.connect("/root/.openclaw/workspace/fundraising-backend/donations.db")
    c = conn.cursor()
    c.execute('SELECT total_raised_usd, donor_count FROM metrics ORDER BY id DESC LIMIT 1')
    row = c.fetchone()
    if row:
        total = row[0] + amount_cents
        donors = row[1] + 1
        c.execute('UPDATE metrics SET total_raised_usd = ?, donor_count = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                  (total, donors, row[2] if len(row) > 2 else 1))
    else:
        total = amount_cents
        donors = 1
        c.execute('INSERT INTO metrics (total_raised_usd, donor_count) VALUES (?, ?)', (total, donors))
    conn.commit()
    conn.close()

# Routes
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "fiesta-fundraising", "timestamp": datetime.now(timezone.utc).isoformat()})

@app.route('/donate', methods=['POST'])
def create_donation():
    """Create Stripe checkout session."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    amount_cents = data.get('amount_cents')
    email = data.get('email', '')
    message = data.get('message', '')

    if not amount_cents or amount_cents < 100:
        return jsonify({"error": "Amount must be at least 100 cents ($1)"}), 400

    try:
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Fiesta Agency Contribution'},
                    'unit_amount': amount_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
            metadata={
                'donor_email': email,
                'donor_message': message,
                'amount_cents': str(amount_cents)
            }
        )

        # Record donation in DB (pending)
        conn = sqlite3.connect("/root/.openclaw/workspace/fundraising-backend/donations.db")
        c = conn.cursor()
        c.execute('''
            INSERT INTO donations (stripe_session_id, amount_cents, donor_email, donor_message, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (session.id, amount_cents, email, message, 'pending'))
        conn.commit()
        conn.close()

        return jsonify({
            "session_id": session.id,
            "checkout_url": session.url,
            "public_key": STRIPE_PUBLIC_KEY
        })
    except Exception as e:
        logger.error(f"Stripe error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events."""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({"error": "Invalid signature"}), 400

    # Handle successful charge
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session['id']
        amount_cents = int(session['amount_total'])
        email = session.get('metadata', {}).get('donor_email', '')
        message = session.get('metadata', {}).get('donor_message', '')

        # Update donation status
        conn = sqlite3.connect("/root/.openclaw/workspace/fundraising-backend/donations.db")
        c = conn.cursor()
        c.execute('SELECT id FROM donations WHERE stripe_session_id = ?', (session_id,))
        row = c.fetchone()
        if row:
            donation_id = row[0]
            # Mint Shannon
            shannon_minted = mint_shannon_for_donation(amount_cents, email)
            c.execute('''
                UPDATE donations SET status = 'completed', shannon_minted = ?
                WHERE id = ?
            ''', (shannon_minted, donation_id))
            conn.commit()
            # Update metrics
            update_metrics(amount_cents)
            logger.info(f"Donation completed: {session_id}, minted {shannon_minted} Shannon")
        conn.close()

    return jsonify({"status": "received"})

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Public metrics endpoint."""
    conn = sqlite3.connect("/root/.openclaw/workspace/fundraising-backend/donations.db")
    c = conn.cursor()
    c.execute('SELECT total_raised_usd, donor_count FROM metrics ORDER BY id DESC LIMIT 1')
    row = c.fetchone()
    total_raised_usd = row[0] if row else 0
    donor_count = row[1] if row else 0
    conn.close()

    # Get agency stats from entropy economy
    agency_agents = 68  # placeholder
    agency_departments = 11
    total_shannon = 3810  # placeholder

    return jsonify({
        "total_raised_usd": total_raised_usd / 100,  # convert cents to dollars
        "total_minted_shannon": total_raised_usd,  # 1 cent = 1 Shannon
        "donor_count": donor_count,
        "goal_usd": 100000,
        "goal_percent": round((total_raised_usd / 100) / 100000 * 100, 1),
        "agency": {
            "agents": agency_agents,
            "departments": agency_departments,
            "total_shannon": total_shannon
        }
    })

@app.route('/balance', methods=['GET'])
def get_balance():
    """Current fundraising total."""
    conn = sqlite3.connect("/root/.openclaw/workspace/fundraising-backend/donations.db")
    c = conn.cursor()
    c.execute('SELECT total_raised_usd FROM metrics ORDER BY id DESC LIMIT 1')
    row = c.fetchone()
    total_cents = row[0] if row else 0
    conn.close()
    return jsonify({
        "total_usd": total_cents / 100,
        "total_cents": total_cents
    })

if __name__ == '__main__':
    logger.info(f"Starting Fiesta Fundraising Backend on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)