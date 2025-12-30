# Elite Video Pipeline v3.2 - User Manual

**Version:** 3.2.0  
**Status:** Production Ready  
**Last Updated:** December 30, 2024  

---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the System](#running-the-system)
6. [API Usage](#api-usage)
7. [Cloud Rendering](#cloud-rendering)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Features](#advanced-features)
10. [Best Practices](#best-practices)

---

## Introduction

Elite Video Pipeline v3.2 is a professional-grade cinematography engine that combines emotional intelligence, vertex-optimized mathematics, and on-demand cloud GPU rendering to deliver Hollywood-quality cinematography specifications at collapse-to-zero cost.

### What's New in v3.2

**Cloud Render Extension** enables on-demand GPU rendering with:
- Render intent detection from natural language
- GPU spot price arbitration (Hetzner, Vast.ai, Tensordock, RunPod)
- Pre-flight cost estimates
- Confirmation handshake (no runaway costs)
- Asynchronous cloud GPU dispatch
- **92% cost reduction** vs. traditional cloud rendering

---

## System Requirements

### Minimum Requirements

**Operating System:**
- Linux (Ubuntu 22.04+ recommended)
- macOS 12.0+
- Windows 10+ (via WSL2)

**Hardware:**
- CPU: 2+ cores
- RAM: 4GB minimum, 8GB recommended
- Storage: 2GB free space
- Network: Stable internet connection

**Software:**
- Python 3.11+
- PostgreSQL 14+ (or Neon serverless)
- Redis 6.0+ (optional, for caching)

### Recommended for Production

**Hardware:**
- CPU: 4+ cores
- RAM: 16GB+
- Storage: 10GB+ SSD
- Network: 100Mbps+ bandwidth

**Cloud Providers:**
- Hetzner Cloud (preferred)
- AWS, GCP, Azure (supported)
- Neon (serverless PostgreSQL)

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/brian95240/elite-video-pipeline-v3.0.git
cd elite-video-pipeline-v3.0
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install Redis (optional, for caching)
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis                  # macOS
```

### Step 3: Set Up Database

#### Option A: Neon Serverless (Recommended)

1. Create account at https://neon.tech
2. Create new project
3. Copy connection string
4. Set environment variable:

```bash
export DATABASE_URL="postgresql://user:pass@host/dbname?sslmode=require"
```

#### Option B: Local PostgreSQL

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb elite_video_pipeline

# Set connection string
export DATABASE_URL="postgresql://localhost/elite_video_pipeline"
```

### Step 4: Configure Environment Variables

Create `.env` file in project root:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host/dbname

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379

# GPU Render Broker
VERTEX_QUALITY_THRESHOLD=0.7
VERTEX_COST_RATIO_MAX=2.0

# SOTA Manifest
SOTA_MANIFEST_URL=https://raw.githubusercontent.com/brian95240/elite-video-pipeline-v3.0/main/examples/sota_manifest_v3.2.json

# Render Output
RENDER_OUTPUT_DIR=/tmp/renders

# LLM API Keys (optional, for Oracle)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

### Step 5: Initialize Database

```bash
# Run database migrations (if applicable)
python3 src/neon_adapter.py
```

### Step 6: Verify Installation

```bash
# Run test suite
python3 test_v3.2_cloud_render.py

# Expected output:
# ✓ PASS: Render Intent Detection
# ✓ PASS: GPU Provider Selection
# ✓ PASS: Provider Status
# ✓ PASS: Cloud Executor
# ✓ PASS: Confirmation Workflow
# Total: 5/5 tests passed
```

---

## Configuration

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | Required | PostgreSQL connection string |
| `REDIS_HOST` | `localhost` | Redis server host |
| `REDIS_PORT` | `6379` | Redis server port |
| `VERTEX_QUALITY_THRESHOLD` | `0.7` | Minimum GPU quality (0.0-1.0) |
| `VERTEX_COST_RATIO_MAX` | `2.0` | Maximum cost ratio vs. baseline |
| `SOTA_MANIFEST_URL` | GitHub URL | SOTA manifest location |
| `RENDER_OUTPUT_DIR` | `/tmp/renders` | Render output directory |
| `OPENAI_API_KEY` | Optional | OpenAI API key for Oracle |
| `ANTHROPIC_API_KEY` | Optional | Anthropic API key for Oracle |
| `GOOGLE_API_KEY` | Optional | Google API key for Oracle |

### GPU Provider Configuration

Edit `examples/sota_manifest_v3.2.json` to customize GPU providers:

```json
{
  "gpu_providers": [
    {
      "name": "Hetzner Cloud GPU",
      "gpu_model": "NVIDIA RTX 4090",
      "vram_gb": 24,
      "spot_price_per_hour": 0.35,
      "uptime_sla": 0.99,
      "region": "eu-central",
      "api_endpoint": "https://api.hetzner.cloud/v1",
      "available": true
    }
  ]
}
```

---

## Running the System

### Start API Server

```bash
# Development mode
python3 src/api_server.py

# Production mode (with gunicorn)
gunicorn -w 4 -b 0.0.0.0:9000 src.api_server:app
```

**Expected Output:**
```
============================================================
Elite Video Pipeline v3.2 - API Server
Vertex-Optimized with Cloud Render Extension
============================================================
✓ Redis L1 cache connected
✓ Emotional Index Manager initialized
✓ Vertex Cinematography Engine initialized
✓ Render Manifest Compiler initialized
✓ Prompt Parser initialized
✓ Cinematography Engine initialized
✓ GPU Render Broker initialized
 * Running on http://0.0.0.0:9000
```

### Verify Server is Running

```bash
# Health check
curl http://localhost:9000/health

# Expected response:
# {"status": "healthy", "version": "3.2.0"}
```

---

## API Usage

### Basic Query

Query cinematography specifications from natural language:

```bash
curl -X POST http://localhost:9000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Make this scene feel like a funeral in the year 2049"}'
```

**Response:**
```json
{
  "status": "success",
  "emotion": "melancholy",
  "intensity": "heavy",
  "render_manifest": {
    "camera": {
      "focal_length_mm": 85,
      "aperture": "T1.4",
      "movement": "Slow Dolly"
    },
    "lighting": {
      "key_fill_ratio": "8:1",
      "color_temperature_kelvin": 4000,
      "iso": 1200
    },
    "color": {
      "saturation": 0.3,
      "contrast": 1.2
    }
  }
}
```

### Split-Stream Query

Use split-stream protocol for cost optimization:

```bash
curl -X POST http://localhost:9000/query_split_stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Two actors fighting with swords in a dark alley, Tarantino style"}'
```

**Response:**
```json
{
  "status": "compiled",
  "source": "SPLIT_STREAM",
  "protocol": "Hybrid-SOTA Split-Stream",
  "metadata": {
    "aesthetic_tensor": {
      "director_reference": "tarantino",
      "lighting_mood": "low_key"
    },
    "kinetic_tensor": {
      "objects": ["sword"],
      "actions": ["fighting"]
    }
  },
  "optimization": {
    "cost_savings": "~70%",
    "latency_reduction": "~60%"
  }
}
```

### Export Blender Script

Export cinematography as Blender Python script:

```bash
curl -X POST http://localhost:9000/export/blender \
  -H "Content-Type: application/json" \
  -d '{
    "emotion": "melancholy",
    "intensity": "heavy",
    "visual_style": "future_noir"
  }' \
  -o cinematography.py
```

---

## Cloud Rendering

### Step 1: Get Render Estimate

Submit render request to get cost estimate:

```bash
curl -X POST http://localhost:9000/render/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Render this scene in 4k at 24fps for final production"
  }'
```

**Response:** `202 Accepted`
```json
{
  "status": "pending_confirmation",
  "job_id": "abc-123-def-456",
  "message": "Ready to render on Hetzner Cloud GPU. Cost: $5.600. Confirm?",
  "render_intent": {
    "resolution": "4k",
    "quality": "production",
    "output_format": "mp4",
    "fps": 24
  },
  "provider": {
    "name": "Hetzner Cloud GPU",
    "gpu_model": "NVIDIA RTX 4090",
    "vram_gb": 24,
    "spot_price_per_hour": 0.35,
    "region": "eu-central"
  },
  "estimated_cost_usd": 5.600,
  "vertex_confidence": 0.95,
  "confirmation_endpoint": "/render/confirm/abc-123-def-456",
  "expires_in_seconds": 300
}
```

### Step 2: Confirm Render Job

Review estimate and confirm:

```bash
curl -X POST http://localhost:9000/render/confirm/abc-123-def-456
```

**Response:** `202 Accepted`
```json
{
  "status": "confirmed",
  "job_id": "abc-123-def-456",
  "message": "Render job confirmed and queued for execution",
  "provider": "Hetzner Cloud GPU",
  "estimated_cost_usd": 5.600,
  "tracking_endpoint": "/render/status/abc-123-def-456"
}
```

### Step 3: Track Render Progress

Monitor render progress:

```bash
# Single status check
curl http://localhost:9000/render/status/abc-123-def-456

# Continuous monitoring (every 5 seconds)
watch -n 5 'curl -s http://localhost:9000/render/status/abc-123-def-456 | jq .progress_percent'
```

**Response:** `200 OK`
```json
{
  "job_id": "abc-123-def-456",
  "status": "rendering",
  "provider": "Hetzner Cloud GPU",
  "estimated_cost_usd": 5.600,
  "progress_percent": 45.5,
  "created_at": "2025-01-01T00:00:00Z",
  "confirmed_at": "2025-01-01T00:01:00Z"
}
```

### Check Available GPU Providers

List all available GPU providers with vertex scores:

```bash
curl http://localhost:9000/render/providers | jq .
```

**Response:** `200 OK`
```json
{
  "quality_threshold": 0.7,
  "cost_ratio_max": 2.0,
  "providers": [
    {
      "name": "Hetzner Cloud GPU",
      "gpu_model": "NVIDIA RTX 4090",
      "vram_gb": 24,
      "spot_price_per_hour": 0.35,
      "uptime_sla": 0.99,
      "region": "eu-central",
      "available": true,
      "vertex_score": 0.892
    },
    {
      "name": "Vast.ai",
      "gpu_model": "NVIDIA RTX 4090",
      "vram_gb": 24,
      "spot_price_per_hour": 0.28,
      "uptime_sla": 0.85,
      "region": "us-west",
      "available": true,
      "vertex_score": 0.756
    }
  ],
  "cached_provider": "Hetzner Cloud GPU"
}
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solution:**
```bash
# Check DATABASE_URL is set
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1;"

# If using Neon, verify SSL mode
export DATABASE_URL="postgresql://user:pass@host/dbname?sslmode=require"
```

#### 2. Redis Connection Failed

**Error:** `redis.exceptions.ConnectionError: Error connecting to Redis`

**Solution:**
```bash
# Check Redis is running
redis-cli ping
# Expected: PONG

# Start Redis if not running
sudo systemctl start redis-server  # Ubuntu/Debian
brew services start redis           # macOS

# If Redis unavailable, system will continue without caching
```

#### 3. No GPU Providers Available

**Error:** `No suitable GPU provider available`

**Solution:**
```bash
# Check SOTA manifest is accessible
curl $SOTA_MANIFEST_URL

# Verify environment variables
echo $VERTEX_QUALITY_THRESHOLD
echo $VERTEX_COST_RATIO_MAX

# System will use fallback providers if manifest unavailable
```

#### 4. Render Job Expired

**Error:** `Job ID not found or expired`

**Solution:**
- Render estimates expire after 5 minutes
- Request new estimate via `/render/estimate`
- Confirm within 5 minutes

#### 5. API Key Missing (Oracle)

**Error:** `Oracle API key not configured`

**Solution:**
```bash
# Set API key for desired provider
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
export GOOGLE_API_KEY=your_key_here

# Restart API server
python3 src/api_server.py
```

### Debug Mode

Enable debug logging:

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Run with verbose output
python3 src/api_server.py
```

### Health Checks

```bash
# API server health
curl http://localhost:9000/health

# Database health
curl http://localhost:9000/health/database

# Redis health
curl http://localhost:9000/health/redis

# GPU providers health
curl http://localhost:9000/render/providers
```

---

## Advanced Features

### Custom GPU Provider

Add custom GPU provider to `sota_manifest_v3.2.json`:

```json
{
  "gpu_providers": [
    {
      "name": "Custom Provider",
      "gpu_model": "NVIDIA A100",
      "vram_gb": 80,
      "spot_price_per_hour": 0.50,
      "uptime_sla": 0.98,
      "region": "us-east",
      "api_endpoint": "https://api.custom-provider.com/v1",
      "available": true
    }
  ]
}
```

### Vertex Threshold Tuning

Adjust quality and cost thresholds:

```bash
# Prioritize quality (higher threshold)
export VERTEX_QUALITY_THRESHOLD=0.9
export VERTEX_COST_RATIO_MAX=3.0

# Prioritize cost (lower threshold)
export VERTEX_QUALITY_THRESHOLD=0.5
export VERTEX_COST_RATIO_MAX=1.5
```

### Custom Emotional Archetypes

Extend emotional index with custom archetypes:

```python
# Edit src/emotional_index_v3_vertex.py
CUSTOM_ARCHETYPES = {
    "cyberpunk_noir": {
        "lighting": {"ratio": "12:1", "kelvin": 3200, "iso": 1600},
        "camera": {"focal_length": 35, "aperture": "T2.0"},
        "color": {"saturation": 1.5, "contrast": 1.3}
    }
}
```

### Batch Processing

Process multiple scenes in parallel:

```bash
# Create batch request file
cat > batch_requests.json << EOF
[
  {"prompt": "Scene 1: Funeral in 2049"},
  {"prompt": "Scene 2: Car chase at night"},
  {"prompt": "Scene 3: Nostalgic home movies"}
]
EOF

# Process batch
for prompt in $(jq -r '.[] | @json' batch_requests.json); do
  curl -X POST http://localhost:9000/query \
    -H "Content-Type: application/json" \
    -d "$prompt"
done
```

---

## Best Practices

### Performance Optimization

1. **Enable Redis caching** for 80-95% database load reduction
2. **Use split-stream protocol** for 70% cost reduction
3. **Enable connection pooling** (automatic in v3.0+)
4. **Batch similar requests** to leverage cache hits

### Cost Optimization

1. **Use preview renders** for testing ($0.01 vs. $5.60)
2. **Confirm estimates** before production renders
3. **Monitor spot prices** via `/render/providers`
4. **Use FOSS models** when quality comparable (5% tolerance)

### Security

1. **Protect API keys** - Never commit to version control
2. **Use environment variables** for sensitive data
3. **Enable SSL/TLS** for production deployments
4. **Restrict API access** with authentication/rate limiting

### Scalability

1. **Deploy behind load balancer** for high traffic
2. **Use Redis cluster** for distributed caching
3. **Scale horizontally** with multiple API server instances
4. **Monitor resource usage** with Prometheus/Grafana

### Monitoring

```bash
# Monitor API server logs
tail -f /var/log/elite-video-pipeline/api.log

# Monitor render jobs
watch -n 5 'curl -s http://localhost:9000/render/providers | jq .cached_provider'

# Monitor database connections
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"

# Monitor Redis memory
redis-cli info memory
```

---

## Support

### Documentation

- **README.md** - Project overview
- **INSTALLATION.md** - Detailed installation guide
- **V3.2_CLOUD_RENDER_EXTENSION.md** - Cloud rendering guide
- **API_REFERENCE.md** - Complete API documentation
- **ARCHITECTURE.md** - System architecture

### Community

- **GitHub:** https://github.com/brian95240/elite-video-pipeline-v3.0
- **Issues:** https://github.com/brian95240/elite-video-pipeline-v3.0/issues
- **Discussions:** https://github.com/brian95240/elite-video-pipeline-v3.0/discussions

### Commercial Support

For commercial support, custom integrations, or enterprise deployments:
- Email: support@elite-video-pipeline.com
- Website: https://elite-video-pipeline.com

---

## Quick Reference

### Essential Commands

```bash
# Start server
python3 src/api_server.py

# Run tests
python3 test_v3.2_cloud_render.py

# Health check
curl http://localhost:9000/health

# Basic query
curl -X POST http://localhost:9000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your prompt here"}'

# Render estimate
curl -X POST http://localhost:9000/render/estimate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Render this scene in 4k"}'

# Check providers
curl http://localhost:9000/render/providers
```

### Environment Variables

```bash
export DATABASE_URL="postgresql://user:pass@host/dbname"
export REDIS_HOST="localhost"
export VERTEX_QUALITY_THRESHOLD=0.7
export VERTEX_COST_RATIO_MAX=2.0
export OPENAI_API_KEY="your_key_here"
```

---

**Elite Video Pipeline v3.2**  
**User Manual Version:** 1.0  
**Last Updated:** December 30, 2024  
**Status:** ✅ Production Ready

For the latest documentation, visit:  
https://github.com/brian95240/elite-video-pipeline-v3.0
