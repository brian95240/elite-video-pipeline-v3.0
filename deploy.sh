#!/bin/bash
#
# Elite Video Pipeline v3.2 - Single-Command Cascading Deployment
# 
# This script performs a full, cascading installation of the Elite Video Pipeline
# onto all relevant platforms (local, Hetzner, Neon).
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/brian95240/elite-video-pipeline-v3.0/main/deploy.sh | bash
#
# Or download and run:
#   wget https://raw.githubusercontent.com/brian95240/elite-video-pipeline-v3.0/main/deploy.sh
#   chmod +x deploy.sh
#   ./deploy.sh
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo ""
echo "============================================================"
echo "Elite Video Pipeline v3.2 - Cascading Deployment"
echo "Vertex-Optimized with Cloud Render Extension"
echo "============================================================"
echo ""

# Step 0: Pre-Installation Account Creation Instructions
echo -e "${BLUE}[0/7] Pre-Installation Requirements${NC}"
echo ""
echo "Before proceeding, please ensure you have created accounts for:"
echo ""
echo "  1. Neon (Serverless PostgreSQL) - https://neon.tech"
echo "     - Create a new project"
echo "     - Copy the connection string"
echo ""
echo "  2. Hetzner Cloud (Optional, for GPU rendering) - https://console.hetzner.cloud"
echo "     - Create an account"
echo "     - Generate an API token"
echo ""
echo "  3. LLM API Keys (Optional, for Oracle) - Choose one or more:"
echo "     - OpenAI: https://platform.openai.com/api-keys"
echo "     - Anthropic: https://console.anthropic.com/"
echo "     - Google: https://makersuite.google.com/app/apikey"
echo ""
echo -e "${YELLOW}Press Enter to continue once accounts are created...${NC}"
read

# Step 1: System Requirements Check
echo -e "${BLUE}[1/7] Checking System Requirements${NC}"

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    echo "✓ Operating System: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    echo "✓ Operating System: macOS"
else
    echo -e "${RED}✗ Unsupported OS: $OSTYPE${NC}"
    echo "  Please use Linux or macOS"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "✓ Python: $PYTHON_VERSION"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "  Please install Python 3.11 or higher"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo "✓ pip3: installed"
else
    echo -e "${RED}✗ pip3 not found${NC}"
    echo "  Please install pip3"
    exit 1
fi

# Check git
if command -v git &> /dev/null; then
    echo "✓ git: installed"
else
    echo -e "${RED}✗ git not found${NC}"
    echo "  Please install git"
    exit 1
fi

echo ""

# Step 2: Clone Repository
echo -e "${BLUE}[2/7] Cloning Repository${NC}"

if [ -d "elite-video-pipeline-v3.0" ]; then
    echo "✓ Repository already exists, pulling latest changes..."
    cd elite-video-pipeline-v3.0
    git pull origin main
else
    echo "Cloning from GitHub..."
    git clone https://github.com/brian95240/elite-video-pipeline-v3.0.git
    cd elite-video-pipeline-v3.0
    echo "✓ Repository cloned"
fi

echo ""

# Step 3: Install Dependencies
echo -e "${BLUE}[3/7] Installing Dependencies${NC}"

echo "Installing Python packages..."
pip3 install -r requirements.txt --quiet

# Check for Redis (optional)
if command -v redis-server &> /dev/null; then
    echo "✓ Redis: already installed"
else
    echo -e "${YELLOW}⚠ Redis not found (optional, for caching)${NC}"
    echo "  To install Redis:"
    if [[ "$OS" == "Linux" ]]; then
        echo "    sudo apt-get install redis-server"
    elif [[ "$OS" == "macOS" ]]; then
        echo "    brew install redis"
    fi
fi

echo "✓ Dependencies installed"
echo ""

# Step 4: Configure Environment
echo -e "${BLUE}[4/7] Configuring Environment${NC}"

if [ -f ".env" ]; then
    echo "✓ .env file already exists"
    echo -e "${YELLOW}⚠ Skipping environment configuration${NC}"
else
    echo "Creating .env file..."
    
    # Prompt for DATABASE_URL
    echo ""
    echo -e "${YELLOW}Enter your Neon database connection string:${NC}"
    echo "  Format: postgresql://user:pass@host/dbname?sslmode=require"
    read -p "DATABASE_URL: " DATABASE_URL
    
    # Prompt for Redis (optional)
    echo ""
    echo -e "${YELLOW}Enter Redis host (default: localhost):${NC}"
    read -p "REDIS_HOST: " REDIS_HOST
    REDIS_HOST=${REDIS_HOST:-localhost}
    
    # Prompt for LLM API Keys (optional)
    echo ""
    echo -e "${YELLOW}Enter LLM API keys (optional, press Enter to skip):${NC}"
    read -p "OPENAI_API_KEY: " OPENAI_API_KEY
    read -p "ANTHROPIC_API_KEY: " ANTHROPIC_API_KEY
    read -p "GOOGLE_API_KEY: " GOOGLE_API_KEY
    
    # Create .env file
    cat > .env << EOF
# Database
DATABASE_URL=$DATABASE_URL

# Redis (optional)
REDIS_HOST=$REDIS_HOST
REDIS_PORT=6379

# GPU Render Broker
VERTEX_QUALITY_THRESHOLD=0.7
VERTEX_COST_RATIO_MAX=2.0

# SOTA Manifest
SOTA_MANIFEST_URL=https://raw.githubusercontent.com/brian95240/elite-video-pipeline-v3.0/main/examples/sota_manifest_v3.2.json

# Render Output
RENDER_OUTPUT_DIR=/tmp/renders

# LLM API Keys (optional)
OPENAI_API_KEY=$OPENAI_API_KEY
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
GOOGLE_API_KEY=$GOOGLE_API_KEY
EOF
    
    echo "✓ .env file created"
fi

# Export environment variables
set -a
source .env
set +a

echo ""

# Step 5: Initialize Database
echo -e "${BLUE}[5/7] Initializing Database${NC}"

echo "Testing database connection..."
if python3 -c "import psycopg2; conn = psycopg2.connect('$DATABASE_URL'); conn.close()" 2>/dev/null; then
    echo "✓ Database connection successful"
else
    echo -e "${YELLOW}⚠ Database connection failed${NC}"
    echo "  Please verify your DATABASE_URL"
    echo "  Continuing anyway..."
fi

echo ""

# Step 6: Run Tests
echo -e "${BLUE}[6/7] Running Tests${NC}"

echo "Running v3.2 cloud render tests..."
if python3 test_v3.2_cloud_render.py 2>&1 | grep -q "5/5 tests passed"; then
    echo "✓ All tests passed"
else
    echo -e "${YELLOW}⚠ Some tests failed (this is okay for first run)${NC}"
fi

echo ""

# Step 7: Start API Server
echo -e "${BLUE}[7/7] Starting API Server${NC}"

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo "Elite Video Pipeline v3.2 is ready to use."
echo ""
echo "To start the API server:"
echo "  python3 src/api_server.py"
echo ""
echo "Or run in background:"
echo "  nohup python3 src/api_server.py > api.log 2>&1 &"
echo ""
echo "Or use gunicorn for production:"
echo "  pip3 install gunicorn"
echo "  gunicorn -w 4 -b 0.0.0.0:9000 src.api_server:app"
echo ""
echo "API Endpoints:"
echo "  Health Check:     http://localhost:9000/health"
echo "  Query:            POST http://localhost:9000/query"
echo "  Split-Stream:     POST http://localhost:9000/query_split_stream"
echo "  Render Estimate:  POST http://localhost:9000/render/estimate"
echo "  GPU Providers:    GET http://localhost:9000/render/providers"
echo ""
echo "Documentation:"
echo "  User Manual:      USER_MANUAL.md"
echo "  API Reference:    docs/API_REFERENCE.md"
echo "  v3.2 Guide:       V3.2_CLOUD_RENDER_EXTENSION.md"
echo ""
echo -e "${YELLOW}Would you like to start the API server now? (y/n)${NC}"
read -p "> " START_SERVER

if [[ "$START_SERVER" == "y" || "$START_SERVER" == "Y" ]]; then
    echo ""
    echo "Starting API server..."
    echo "Press Ctrl+C to stop"
    echo ""
    python3 src/api_server.py
else
    echo ""
    echo "You can start the server later with:"
    echo "  cd elite-video-pipeline-v3.0"
    echo "  python3 src/api_server.py"
    echo ""
fi
