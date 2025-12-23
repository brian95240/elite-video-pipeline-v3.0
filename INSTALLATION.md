# Elite Video Pipeline v3.0 - Installation & Setup Guide

## System Requirements

### Minimum Requirements
- **OS:** Linux, macOS, or Windows (WSL2)
- **Python:** 3.8 or higher
- **Memory:** 2GB RAM minimum
- **Disk:** 500MB for installation

### Recommended Requirements
- **Python:** 3.11+
- **Memory:** 4GB+ RAM
- **Disk:** 1GB+ for caching
- **Redis:** 6.0+ (optional, for distributed processing)
- **FFmpeg:** 4.0+ (optional, for video rendering)

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/elite-video-pipeline-v3.0.git
cd elite-video-pipeline-v3.0
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Run test suite
python tests/test_pipeline_closed_loop.py
```

Expected output:
```
✓ Passed: 8
✗ Failed: 0
✓ ALL TESTS PASSED
```

## Dependency Versions

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| redis | 5.0.1+ | Redis client for orchestration |
| python-dotenv | 1.0.0+ | Environment variable management |
| async-timeout | 4.0.0+ | Async timeout handling |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 7.4.3+ | Testing framework |
| pytest-cov | 4.1.0+ | Code coverage |
| black | 23.12.0+ | Code formatting |
| flake8 | 6.1.0+ | Linting |
| mypy | 1.7.1+ | Type checking |

### Optional Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| FFmpeg | 4.0+ | Video processing (system package) |
| Redis | 6.0+ | Data store (system package) |

## Optional Setup

### Install FFmpeg

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### On macOS (with Homebrew):
```bash
brew install ffmpeg
```

#### On Windows:
Download from https://ffmpeg.org/download.html

### Install Redis

#### On Ubuntu/Debian:
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

#### On macOS (with Homebrew):
```bash
brew install redis
brew services start redis
```

#### Using Docker:
```bash
docker run -d -p 6379:6379 redis:latest
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Pipeline Configuration
PIPELINE_MAX_RETRIES=3
PIPELINE_TIMEOUT=300
ENABLE_QUALITY_GATES=true
ENABLE_SPOT_PRICING=true

# Logging
LOG_LEVEL=INFO
```

### Load Environment Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
```

## Quick Start

### Basic Usage

```python
from src.pipeline_orchestrator import create_orchestrator

# Create orchestrator
orchestrator = create_orchestrator()

# Submit a job
job_id = orchestrator.submit_video_job(
    video_id="video_001",
    emotion="curiosity",
    intensity="medium"
)

# Process the job
success = orchestrator.process_job(job_id)

# Get status
status = orchestrator.get_pipeline_status()
print(f"Status: {status}")
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test
python -m pytest tests/test_pipeline_closed_loop.py::ClosedLoopTestSuite::test_emotional_index_completeness -v
```

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'redis'

**Solution:**
```bash
pip install redis async-timeout
```

### Issue: Connection refused (Redis)

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# Start Redis if not running
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:latest
```

### Issue: Permission denied (venv creation)

**Solution:**
```bash
# Use sudo
sudo python3 -m venv venv

# Or use alternative method
python3 -m venv --without-pip venv
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
```

### Issue: Tests fail with warnings

**Solution:**
The warnings about unknown VFX effects are expected in test mode. They indicate that some advanced effects are not yet implemented in the filter templates. This is normal and does not affect core functionality.

## Docker Setup

### Build Docker Image

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 6379 8000

# Run pipeline
CMD ["python", "src/pipeline_orchestrator.py"]
```

### Build and Run

```bash
# Build image
docker build -t elite-pipeline-v3:latest .

# Run container
docker run -d -p 6379:6379 elite-pipeline-v3:latest

# Run with volume mount
docker run -d -v $(pwd):/app -p 6379:6379 elite-pipeline-v3:latest
```

## Kubernetes Deployment

### Create ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: elite-pipeline-config
data:
  REDIS_HOST: redis-service
  REDIS_PORT: "6379"
  PIPELINE_MAX_RETRIES: "3"
  PIPELINE_TIMEOUT: "300"
```

### Create Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elite-pipeline-v3
spec:
  replicas: 3
  selector:
    matchLabels:
      app: elite-pipeline
  template:
    metadata:
      labels:
        app: elite-pipeline
    spec:
      containers:
      - name: pipeline
        image: elite-pipeline-v3:latest
        envFrom:
        - configMapRef:
            name: elite-pipeline-config
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Development Setup

### Install Development Tools

```bash
pip install -r requirements.txt
pip install black flake8 mypy pytest pytest-cov
```

### Code Quality Checks

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

## Verification Checklist

After installation, verify:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Virtual environment activated: `which python` shows venv path
- [ ] Dependencies installed: `pip list | grep redis`
- [ ] Tests pass: `python tests/test_pipeline_closed_loop.py`
- [ ] Emotional index loads: `python -c "from src.emotional_index_v3 import EmotionalIndexManager; print(EmotionalIndexManager().get_all_emotions())"`
- [ ] Cinematography engine works: `python -c "from src.cinematography_engine import CinematographyEngine; print(CinematographyEngine().get_filter_statistics())"`

## Support

For installation issues:

1. Check the troubleshooting section above
2. Review error messages carefully
3. Verify all system requirements are met
4. Check GitHub Issues: https://github.com/yourusername/elite-video-pipeline-v3.0/issues
5. Contact support: support@example.com

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for overview
2. Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design
3. Review example usage in [examples/](examples/)
4. Run the test suite to verify functionality
5. Start building your video processing pipeline!

---

**Last Updated:** December 2024
**Version:** 3.0
