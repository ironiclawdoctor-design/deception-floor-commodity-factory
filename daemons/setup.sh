#!/bin/bash
# Setup script for LLM-style daemons

set -e

DAEMONS_DIR="$(dirname "$0")"
WORKSPACE="/root/.openclaw/workspace"
SERVICE_DIR="/etc/systemd/system"

echo "Setting up LLM-style daemons..."

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Please install python3."
    exit 1
fi

# Check dependencies
pip3 install requests --quiet 2>/dev/null || echo "Requests already installed or pip not available"

# Make scripts executable
chmod +x "$DAEMONS_DIR/raise-awareness.py"
chmod +x "$DAEMONS_DIR/proactive-supervisor.py"

# Create logs directory
mkdir -p "$WORKSPACE/logs"
mkdir -p "$WORKSPACE/suggestions"

# Install systemd services (requires root)
if [ "$EUID" -eq 0 ]; then
    echo "Installing systemd services..."
    cp "$DAEMONS_DIR/raise-awareness.service" "$SERVICE_DIR/"
    cp "$DAEMONS_DIR/proactive-supervisor.service" "$SERVICE_DIR/"
    
    systemctl daemon-reload
    
    echo "Enabling services..."
    systemctl enable raise-awareness.service
    systemctl enable proactive-supervisor.service
    
    echo "Starting services..."
    systemctl start raise-awareness.service
    systemctl start proactive-supervisor.service
    
    echo "Daemons installed and started."
    echo "Check status with:"
    echo "  systemctl status raise-awareness"
    echo "  systemctl status proactive-supervisor"
else
    echo "Run as root to install systemd services."
    echo "Manual steps:"
    echo "1. Copy .service files to $SERVICE_DIR/"
    echo "2. systemctl daemon-reload"
    echo "3. systemctl enable --now raise-awareness.service"
    echo "4. systemctl enable --now proactive-supervisor.service"
fi

echo "Setup complete."