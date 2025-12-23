#!/bin/bash
#
# Elite Video Pipeline v3.0 - Hetzner Cloud Deployment Script
# Automated installation on Hetzner C31X instance
#

set -e  # Exit on error

echo "=========================================="
echo "Elite Video Pipeline v3.0 Deployment"
echo "Target: Hetzner Cloud C31X"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/opt/elite-video-pipeline"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_USER="pipeline"
GITHUB_REPO="https://github.com/brian95240/elite-video-pipeline-v3.0.git"

# Neon Database Connection (will be set from environment)
NEON_DATABASE_URL="${NEON_DATABASE_URL:-}"

echo -e "${GREEN}[1/10]${NC} Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

echo -e "${GREEN}[2/10]${NC} Installing system dependencies..."
sudo apt-get install -y -qq \
    python3.11 \
    python3.11-venv \
    python3-pip \
    redis-server \
    ffmpeg \
    git \
    curl \
    wget \
    build-essential \
    libpq-dev \
    postgresql-client

echo -e "${GREEN}[3/10]${NC} Configuring Redis..."
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Configure Redis for production
sudo tee /etc/redis/redis.conf.d/pipeline.conf > /dev/null <<EOF
# Elite Video Pipeline Redis Configuration
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
EOF

sudo systemctl restart redis-server

echo -e "${GREEN}[4/10]${NC} Creating service user..."
if ! id "$SERVICE_USER" &>/dev/null; then
    sudo useradd -r -m -s /bin/bash "$SERVICE_USER"
fi

echo -e "${GREEN}[5/10]${NC} Cloning repository..."
sudo rm -rf "$PROJECT_DIR"
sudo git clone "$GITHUB_REPO" "$PROJECT_DIR"
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "$PROJECT_DIR"

echo -e "${GREEN}[6/10]${NC} Setting up Python virtual environment..."
cd "$PROJECT_DIR"
sudo -u "$SERVICE_USER" python3.11 -m venv "$VENV_DIR"
sudo -u "$SERVICE_USER" "$VENV_DIR/bin/pip" install --upgrade pip

echo -e "${GREEN}[7/10]${NC} Installing Python dependencies..."
sudo -u "$SERVICE_USER" "$VENV_DIR/bin/pip" install -r requirements.txt
sudo -u "$SERVICE_USER" "$VENV_DIR/bin/pip" install psycopg2-binary

echo -e "${GREEN}[8/10]${NC} Configuring environment..."
sudo -u "$SERVICE_USER" tee "$PROJECT_DIR/.env" > /dev/null <<EOF
# Elite Video Pipeline v3.0 Configuration
# Generated: $(date)

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Neon Database Configuration
NEON_DATABASE_URL=${NEON_DATABASE_URL}

# Pipeline Configuration
PIPELINE_MAX_RETRIES=3
PIPELINE_TIMEOUT=300
ENABLE_QUALITY_GATES=true
ENABLE_SPOT_PRICING=true

# Logging
LOG_LEVEL=INFO
EOF

echo -e "${GREEN}[9/10]${NC} Creating systemd services..."

# Main pipeline service
sudo tee /etc/systemd/system/elite-pipeline.service > /dev/null <<EOF
[Unit]
Description=Elite Video Pipeline v3.0
After=network.target redis-server.service
Wants=redis-server.service

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
EnvironmentFile=$PROJECT_DIR/.env
ExecStart=$VENV_DIR/bin/python src/pipeline_orchestrator.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Health check service
sudo tee /etc/systemd/system/elite-pipeline-health.service > /dev/null <<EOF
[Unit]
Description=Elite Video Pipeline Health Check
After=elite-pipeline.service

[Service]
Type=oneshot
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
EnvironmentFile=$PROJECT_DIR/.env
ExecStart=$VENV_DIR/bin/python -c "from src.pipeline_orchestrator import create_orchestrator; o = create_orchestrator(); print(o.get_pipeline_status())"
EOF

# Health check timer (every 5 minutes)
sudo tee /etc/systemd/system/elite-pipeline-health.timer > /dev/null <<EOF
[Unit]
Description=Elite Video Pipeline Health Check Timer

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
EOF

echo -e "${GREEN}[10/10]${NC} Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable elite-pipeline.service
sudo systemctl enable elite-pipeline-health.timer

# Don't start yet - need to verify configuration
echo ""
echo -e "${YELLOW}⚠ Services configured but not started${NC}"
echo -e "${YELLOW}  Run 'sudo systemctl start elite-pipeline' after verifying configuration${NC}"

echo ""
echo -e "${GREEN}✓ Deployment complete!${NC}"
echo ""
echo "=========================================="
echo "Installation Summary"
echo "=========================================="
echo "Project Directory: $PROJECT_DIR"
echo "Virtual Environment: $VENV_DIR"
echo "Service User: $SERVICE_USER"
echo "Configuration: $PROJECT_DIR/.env"
echo ""
echo "Services:"
echo "  - elite-pipeline.service (main pipeline)"
echo "  - elite-pipeline-health.timer (health checks)"
echo ""
echo "Next Steps:"
echo "1. Verify configuration: cat $PROJECT_DIR/.env"
echo "2. Run tests: cd $PROJECT_DIR && $VENV_DIR/bin/python tests/test_pipeline_closed_loop.py"
echo "3. Start service: sudo systemctl start elite-pipeline"
echo "4. Check status: sudo systemctl status elite-pipeline"
echo "5. View logs: sudo journalctl -u elite-pipeline -f"
echo ""
echo "=========================================="
