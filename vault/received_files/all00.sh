#!/bin/bash
# all00.sh - Easy installer & manager for LLM-style daemons
# Run: sudo ./all00.sh [install|status|start|stop|restart|logs|uninstall]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
DAEMONS_DIR="/root/.openclaw/workspace/daemons"
WORKSPACE="/root/.openclaw/workspace"
SERVICE_DIR="/etc/systemd/system"
SCRIPT_NAME=$(basename "$0")

# Services
SERVICES=("raise-awareness" "proactive-supervisor")

# Print colored message
msg() {
    echo -e "${GREEN}[+]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        error "This script must be run as root (use sudo)"
        exit 1
    fi
}

# Check dependencies
check_deps() {
    if ! command -v python3 &> /dev/null; then
        error "Python3 not found. Install with: apt-get install python3"
        exit 1
    fi
    
    if ! python3 -c "import requests" 2>/dev/null; then
        warn "Python requests module not found, installing..."
        pip3 install requests --quiet 2>/dev/null || {
            error "Failed to install requests. Try: pip3 install requests"
            exit 1
        }
        msg "Requests module installed"
    fi
    
    if ! systemctl --version &> /dev/null; then
        error "systemd not found. This script requires systemd."
        exit 1
    fi
}

# Install daemons
install_daemons() {
    check_root
    check_deps
    
    msg "Installing LLM-style daemons..."
    
    # Make scripts executable
    chmod +x "$DAEMONS_DIR/raise-awareness.py"
    chmod +x "$DAEMONS_DIR/proactive-supervisor.py"
    
    # Create directories
    mkdir -p "$WORKSPACE/logs"
    mkdir -p "$WORKSPACE/suggestions"
    
    # Copy service files
    msg "Installing systemd services..."
    for service in "${SERVICES[@]}"; do
        cp "$DAEMONS_DIR/$service.service" "$SERVICE_DIR/"
    done
    
    # Reload systemd
    systemctl daemon-reload
    
    # Enable services
    for service in "${SERVICES[@]}"; do
        systemctl enable "$service.service"
    done
    
    # Start services
    for service in "${SERVICES[@]}"; do
        systemctl start "$service.service"
    done
    
    msg "Daemons installed and started!"
    
    # Create convenience symlink
    if [ ! -f "/usr/local/bin/daemons" ]; then
        ln -sf "$DAEMONS_DIR/setup.sh" /usr/local/bin/daemons
        msg "Created symlink: /usr/local/bin/daemons → $DAEMONS_DIR/setup.sh"
    fi
    
    show_status
    show_next_steps
}

# Show service status
show_status() {
    echo -e "\n${BLUE}=== Daemon Status ===${NC}"
    for service in "${SERVICES[@]}"; do
        status=$(systemctl is-active "$service.service" 2>/dev/null || echo "not-installed")
        if [ "$status" = "active" ]; then
            echo -e "${GREEN}✓${NC} $service: $status"
        elif [ "$status" = "not-installed" ]; then
            echo -e "${YELLOW}?${NC} $service: $status"
        else
            echo -e "${RED}✗${NC} $service: $status"
        fi
    done
    
    # Show recent logs
    echo -e "\n${BLUE}=== Recent Logs ===${NC}"
    journalctl -u raise-awareness -u proactive-supervisor --no-pager -n 3 2>/dev/null || true
}

# Start services
start_services() {
    check_root
    msg "Starting daemons..."
    for service in "${SERVICES[@]}"; do
        systemctl start "$service.service" && msg "Started $service" || error "Failed to start $service"
    done
    show_status
}

# Stop services
stop_services() {
    check_root
    msg "Stopping daemons..."
    for service in "${SERVICES[@]}"; do
        systemctl stop "$service.service" && msg "Stopped $service" || error "Failed to stop $service"
    done
    show_status
}

# Restart services
restart_services() {
    check_root
    msg "Restarting daemons..."
    for service in "${SERVICES[@]}"; do
        systemctl restart "$service.service" && msg "Restarted $service" || error "Failed to restart $service"
    done
    show_status
}

# Show logs
show_logs() {
    echo -e "${BLUE}=== Daemon Logs (last 20 lines) ===${NC}"
    for service in "${SERVICES[@]}"; do
        echo -e "\n${YELLOW}--- $service ---${NC}"
        journalctl -u "$service.service" --no-pager -n 20 2>/dev/null || echo "No logs found"
    done
    
    echo -e "\n${YELLOW}--- Application Logs ---${NC}"
    ls -la "$WORKSPACE/logs/"*.log 2>/dev/null | head -5
}

# Uninstall services
uninstall_services() {
    check_root
    warn "This will stop and remove the daemon services."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        msg "Cancelled."
        exit 0
    fi
    
    # Stop services
    for service in "${SERVICES[@]}"; do
        systemctl stop "$service.service" 2>/dev/null || true
        systemctl disable "$service.service" 2>/dev/null || true
    done
    
    # Remove service files
    for service in "${SERVICES[@]}"; do
        rm -f "$SERVICE_DIR/$service.service"
    done
    
    # Remove symlink
    rm -f /usr/local/bin/daemons 2>/dev/null || true
    
    systemctl daemon-reload
    msg "Daemons uninstalled. Note: Python scripts and logs remain in $DAEMONS_DIR"
}

# Show next steps
show_next_steps() {
    echo -e "\n${BLUE}=== Next Steps ===${NC}"
    echo -e "${GREEN}1. Check daemon status:${NC} sudo ./$SCRIPT_NAME status"
    echo -e "${GREEN}2. View logs:${NC} sudo ./$SCRIPT_NAME logs"
    echo -e "${GREEN}3. Monitor anomalies:${NC} tail -f $WORKSPACE/logs/anomalies.log"
    echo -e "${GREEN}4. View suggestions:${NC} cat $WORKSPACE/suggestions/improvements.json 2>/dev/null || echo 'No suggestions yet'"
    echo -e "${GREEN}5. Quick commands:${NC}"
    echo -e "   sudo ./$SCRIPT_NAME start    # Start all daemons"
    echo -e "   sudo ./$SCRIPT_NAME stop     # Stop all daemons"
    echo -e "   sudo ./$SCRIPT_NAME restart  # Restart all daemons"
    echo -e "   sudo ./$SCRIPT_NAME uninstall # Remove services"
    echo -e "\n${YELLOW}Daemon files remain in: $DAEMONS_DIR${NC}"
}

# Show usage
show_usage() {
    echo -e "${BLUE}Usage:${NC} sudo ./$SCRIPT_NAME [command]"
    echo -e "Commands:"
    echo -e "  install     - Install and start daemons (default)"
    echo -e "  status      - Show daemon status"
    echo -e "  start       - Start daemons"
    echo -e "  stop        - Stop daemons"
    echo -e "  restart     - Restart daemons"
    echo -e "  logs        - Show recent logs"
    echo -e "  uninstall   - Remove daemon services"
    echo -e "  help        - Show this help"
    echo -e "\n${YELLOW}Examples:${NC}"
    echo -e "  sudo ./$SCRIPT_NAME           # Install (default)"
    echo -e "  sudo ./$SCRIPT_NAME status    # Check status"
    echo -e "  sudo ./$SCRIPT_NAME logs      # View logs"
}

# Main
case "${1:-install}" in
    install)
        install_daemons
        ;;
    status)
        show_status
        ;;
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    uninstall)
        uninstall_services
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac