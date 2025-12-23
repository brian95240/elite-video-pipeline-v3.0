# Elite Video Pipeline v3.0 - Hetzner Deployment Guide

## Quick Start (One-Line Installer)

**Server:** apex-brain-ai-server (5.161.226.153)  
**Type:** CPX41 (8 vCPU, 16 GB RAM, 240 GB disk)  
**Location:** Ashburn, VA (US East)

---

## Prerequisites

- SSH access to your Hetzner server
- Root privileges
- Internet connection

---

## Installation Methods

### Method 1: One-Line Installer (Recommended)

SSH into your server and run:

```bash
export NEON_DATABASE_URL="postgresql://neondb_owner:npg_BUGW3mCOz4Iw@ep-misty-darkness-afmy9hja-pooler.c-2.us-west-2.aws.neon.tech/neondb?channel_binding=require&sslmode=require"

curl -sSL https://raw.githubusercontent.com/brian95240/elite-video-pipeline-v3.0/main/scripts/deploy_hetzner.sh | sudo bash
```

**What this does:**
1. ✅ Updates system packages
2. ✅ Installs Python 3.11, Redis, FFmpeg, PostgreSQL client
3. ✅ Clones repository from GitHub
4. ✅ Sets up virtual environment
5. ✅ Installs all Python dependencies
6. ✅ Configures Neon database integration
7. ✅ Creates systemd services
8. ✅ Sets up automatic startup

**Installation time:** ~5-10 minutes

---

### Method 2: Manual Installation

If you prefer to inspect the script first:

```bash
# Download the script
wget https://raw.githubusercontent.com/brian95240/elite-video-pipeline-v3.0/main/scripts/deploy_hetzner.sh

# Make it executable
chmod +x deploy_hetzner.sh

# Review the script
cat deploy_hetzner.sh

# Set environment variable
export NEON_DATABASE_URL="postgresql://neondb_owner:npg_BUGW3mCOz4Iw@ep-misty-darkness-afmy9hja-pooler.c-2.us-west-2.aws.neon.tech/neondb?channel_binding=require&sslmode=require"

# Run it
sudo ./deploy_hetzner.sh
```

---

## SSH Access Instructions

### From Windows (PowerShell or CMD):

```powershell
ssh root@5.161.226.153
```

When prompted for password, use the root password from Hetzner Console.

### From Mac/Linux:

```bash
ssh root@5.161.226.153
```

### From PuTTY (Windows):

1. Open PuTTY
2. Host Name: `5.161.226.153`
3. Port: `22`
4. Connection Type: SSH
5. Click "Open"
6. Login as: `root`
7. Password: (from Hetzner Console)

---

## Post-Installation Steps

After the installation completes:

### 1. Verify Installation

```bash
# Check service status
sudo systemctl status elite-pipeline

# View logs
sudo journalctl -u elite-pipeline -f

# Check Redis
redis-cli ping

# Check disk space
df -h

# Check memory
free -h
```

### 2. Run Tests

```bash
cd /opt/elite-video-pipeline
source venv/bin/activate
python tests/test_pipeline_closed_loop.py
```

Expected output:
```
✓ Passed: 8
✗ Failed: 0
✓ ALL TESTS PASSED
```

### 3. Start the Service

```bash
# Start the pipeline
sudo systemctl start elite-pipeline

# Enable auto-start on boot
sudo systemctl enable elite-pipeline

# Check status
sudo systemctl status elite-pipeline
```

### 4. Monitor Health

```bash
# Enable health check timer
sudo systemctl enable elite-pipeline-health.timer
sudo systemctl start elite-pipeline-health.timer

# View health check logs
sudo journalctl -u elite-pipeline-health -f
```

---

## Configuration

### Environment Variables

Configuration file: `/opt/elite-video-pipeline/.env`

```bash
# Edit configuration
sudo nano /opt/elite-video-pipeline/.env
```

**Key settings:**

```env
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Neon Database Configuration
NEON_DATABASE_URL=postgresql://neondb_owner:npg_BUGW3mCOz4Iw@ep-misty-darkness-afmy9hja-pooler.c-2.us-west-2.aws.neon.tech/neondb

# Pipeline Configuration
PIPELINE_MAX_RETRIES=3
PIPELINE_TIMEOUT=300
ENABLE_QUALITY_GATES=true
ENABLE_SPOT_PRICING=true

# Logging
LOG_LEVEL=INFO
```

After editing, restart the service:
```bash
sudo systemctl restart elite-pipeline
```

---

## Neon Database

### Database Details

- **Project:** Elite Video Pipeline v3.0
- **Project ID:** lively-sunset-96070079
- **Branch:** main (br-royal-rice-afcnnemd)
- **Database:** neondb
- **Region:** US West 2 (AWS)

### Database Schema

The following tables are automatically created:

1. **pipeline_jobs** - Job tracking and state management
2. **pipeline_metrics** - Performance metrics and costs
3. **emotional_profiles** - 12 emotional archetypes × 3 intensities
4. **pipeline_config** - System configuration

### Verify Database Connection

```bash
cd /opt/elite-video-pipeline
source venv/bin/activate
python -c "from src.neon_adapter import create_neon_adapter; adapter = create_neon_adapter(); print(adapter.get_pipeline_stats())"
```

---

## Service Management

### Systemd Services

Two services are installed:

1. **elite-pipeline.service** - Main pipeline service
2. **elite-pipeline-health.timer** - Health check timer (every 5 minutes)

### Common Commands

```bash
# Start service
sudo systemctl start elite-pipeline

# Stop service
sudo systemctl stop elite-pipeline

# Restart service
sudo systemctl restart elite-pipeline

# Check status
sudo systemctl status elite-pipeline

# View logs
sudo journalctl -u elite-pipeline -f

# Enable auto-start
sudo systemctl enable elite-pipeline

# Disable auto-start
sudo systemctl disable elite-pipeline
```

---

## Troubleshooting

### Issue: Service won't start

**Check logs:**
```bash
sudo journalctl -u elite-pipeline -n 50
```

**Common causes:**
- Missing dependencies: Re-run deployment script
- Database connection: Check NEON_DATABASE_URL in .env
- Redis not running: `sudo systemctl start redis-server`

### Issue: Redis connection failed

**Check Redis status:**
```bash
sudo systemctl status redis-server
redis-cli ping
```

**Restart Redis:**
```bash
sudo systemctl restart redis-server
```

### Issue: Database connection failed

**Test connection:**
```bash
psql "postgresql://neondb_owner:npg_BUGW3mCOz4Iw@ep-misty-darkness-afmy9hja-pooler.c-2.us-west-2.aws.neon.tech/neondb"
```

**Check firewall:**
```bash
sudo ufw status
```

### Issue: Out of disk space

**Check disk usage:**
```bash
df -h
du -sh /opt/elite-video-pipeline/*
```

**Clean up:**
```bash
# Remove old logs
sudo journalctl --vacuum-time=7d

# Clean pip cache
pip cache purge
```

### Issue: Out of memory

**Check memory:**
```bash
free -h
htop
```

**Adjust Redis memory:**
```bash
sudo nano /etc/redis/redis.conf.d/pipeline.conf
# Set: maxmemory 1gb
sudo systemctl restart redis-server
```

---

## Monitoring

### View Real-Time Logs

```bash
# Pipeline logs
sudo journalctl -u elite-pipeline -f

# Redis logs
sudo journalctl -u redis-server -f

# System logs
sudo tail -f /var/log/syslog
```

### Check Resource Usage

```bash
# CPU and memory
htop

# Disk I/O
iotop

# Network
iftop

# All-in-one
glances
```

### Pipeline Statistics

```bash
cd /opt/elite-video-pipeline
source venv/bin/activate
python -c "
from src.neon_adapter import create_neon_adapter
adapter = create_neon_adapter()
stats = adapter.get_pipeline_stats()
print('Total Jobs:', stats['total_jobs'])
print('Completed:', stats['completed_jobs'])
print('Failed:', stats['failed_jobs'])
print('Avg Time:', stats['avg_processing_time_ms'], 'ms')
print('Total Cost: $', stats['total_cost_usd'])
"
```

---

## Updating the Pipeline

### Update from GitHub

```bash
cd /opt/elite-video-pipeline
sudo -u pipeline git pull origin main
sudo -u pipeline venv/bin/pip install -r requirements.txt
sudo systemctl restart elite-pipeline
```

### Update Dependencies

```bash
cd /opt/elite-video-pipeline
sudo -u pipeline venv/bin/pip install --upgrade -r requirements.txt
sudo systemctl restart elite-pipeline
```

---

## Backup and Recovery

### Backup Configuration

```bash
# Backup .env file
sudo cp /opt/elite-video-pipeline/.env /root/elite-pipeline-env-backup-$(date +%Y%m%d).txt

# Backup entire installation
sudo tar -czf /root/elite-pipeline-backup-$(date +%Y%m%d).tar.gz /opt/elite-video-pipeline
```

### Database Backup

Neon automatically handles backups. To export data:

```bash
cd /opt/elite-video-pipeline
source venv/bin/activate
python -c "
from src.neon_adapter import create_neon_adapter
import json
adapter = create_neon_adapter()
jobs = adapter.list_jobs(limit=1000)
with open('jobs_backup.json', 'w') as f:
    json.dump(jobs, f, indent=2, default=str)
print('✓ Backup saved to jobs_backup.json')
"
```

---

## Uninstallation

To completely remove the pipeline:

```bash
# Stop and disable services
sudo systemctl stop elite-pipeline
sudo systemctl disable elite-pipeline
sudo systemctl stop elite-pipeline-health.timer
sudo systemctl disable elite-pipeline-health.timer

# Remove service files
sudo rm /etc/systemd/system/elite-pipeline.service
sudo rm /etc/systemd/system/elite-pipeline-health.service
sudo rm /etc/systemd/system/elite-pipeline-health.timer
sudo systemctl daemon-reload

# Remove installation directory
sudo rm -rf /opt/elite-video-pipeline

# Remove user (optional)
sudo userdel -r pipeline

# Remove Redis configuration (optional)
sudo rm /etc/redis/redis.conf.d/pipeline.conf
sudo systemctl restart redis-server
```

---

## Security Recommendations

### 1. Change Default Passwords

```bash
# Change root password
passwd
```

### 2. Set Up SSH Key Authentication

```bash
# On your local machine, generate SSH key
ssh-keygen -t ed25519 -C "elite-pipeline"

# Copy to server
ssh-copy-id root@5.161.226.153

# Disable password authentication
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

### 3. Enable Firewall

```bash
# Install UFW
sudo apt-get install -y ufw

# Allow SSH
sudo ufw allow 22/tcp

# Allow Redis (only from localhost)
sudo ufw allow from 127.0.0.1 to any port 6379

# Enable firewall
sudo ufw enable
```

### 4. Secure Redis

```bash
# Set Redis password
sudo nano /etc/redis/redis.conf
# Add: requirepass YOUR_STRONG_PASSWORD

# Update .env file
sudo nano /opt/elite-video-pipeline/.env
# Update: REDIS_PASSWORD=YOUR_STRONG_PASSWORD

# Restart services
sudo systemctl restart redis-server
sudo systemctl restart elite-pipeline
```

---

## Support

### Documentation

- **GitHub:** https://github.com/brian95240/elite-video-pipeline-v3.0
- **README:** https://github.com/brian95240/elite-video-pipeline-v3.0/blob/main/README.md
- **Architecture:** https://github.com/brian95240/elite-video-pipeline-v3.0/blob/main/docs/ARCHITECTURE.md

### Issues

- **GitHub Issues:** https://github.com/brian95240/elite-video-pipeline-v3.0/issues
- **Email:** brian95240@gmail.com

---

## Quick Reference

### Server Details

| Item | Value |
|------|-------|
| Server Name | apex-brain-ai-server |
| IP Address | 5.161.226.153 |
| Server Type | CPX41 |
| CPU | 8 vCPU (AMD) |
| RAM | 16 GB |
| Disk | 240 GB |
| Location | Ashburn, VA (US East) |
| OS | Ubuntu 22.04 LTS |

### Installation Paths

| Component | Path |
|-----------|------|
| Installation | /opt/elite-video-pipeline |
| Virtual Environment | /opt/elite-video-pipeline/venv |
| Configuration | /opt/elite-video-pipeline/.env |
| Logs | `journalctl -u elite-pipeline` |
| Service Files | /etc/systemd/system/elite-pipeline* |

### Ports

| Service | Port | Access |
|---------|------|--------|
| SSH | 22 | External |
| Redis | 6379 | Localhost only |
| Neon DB | 5432 | External (SSL) |

---

**Last Updated:** December 22, 2024  
**Version:** 3.0  
**Status:** Ready for Deployment
