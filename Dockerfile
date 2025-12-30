# Elite Video Pipeline v3.3 - Scale-to-Zero Dockerfile
# Optimized for Hetzner Cloud, Cloud Run, or any serverless container platform
# 
# This Dockerfile creates a minimal, production-ready container that:
# - Starts instantly (< 1 second cold start)
# - Scales to zero when idle (collapse-to-zero cost)
# - Uses multi-stage build for minimal image size
# - Includes health checks for auto-scaling

# === STAGE 1: Builder ===
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# === STAGE 2: Runtime ===
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY src/ ./src/
COPY examples/ ./examples/
COPY requirements.txt .

# Create output directory
RUN mkdir -p /tmp/renders

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=9000 \
    WORKERS=4 \
    TIMEOUT=120

# Expose port
EXPOSE 9000

# Health check for auto-scaling
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:9000/health || exit 1

# Run with gunicorn for production
CMD exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers $WORKERS \
    --timeout $TIMEOUT \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    src.api_server:app
