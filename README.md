# Elite Video Pipeline v3.0

**Professional-grade video processing pipeline with 12 emotional archetypes and Hollywood-level cinematography**

## Overview

Elite Video Pipeline v3.0 is a distributed microservices architecture for automated video production with emotional intelligence. It combines:

- **12 Emotional Archetypes** (7 original + 5 new)
- **Redis-based Orchestration** for distributed processing
- **FFmpeg Cinematography Engine** for professional visual effects
- **Quality Gate Validation** for consistent output
- **10-Archetype Firewall** for specialized processing roles

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Pipeline Orchestrator                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │ Emotional Index  │  │ Cinematography   │                 │
│  │ (12 Archetypes)  │  │ Engine           │                 │
│  └──────────────────┘  └──────────────────┘                 │
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │ Redis            │  │ Quality Gate     │                 │
│  │ Orchestrator     │  │ Validator        │                 │
│  └──────────────────┘  └──────────────────┘                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Microservices (10-Archetype Firewall)

| Archetype | Role | Responsibility |
|-----------|------|-----------------|
| **Oracle** | Script Generation | Emotional arc extraction |
| **Trickster** | Voice Synthesis | TTS with metadata passing |
| **Cartographer** | Retention Mapping | Cinematography JSON generation |
| **Spectacle** | Rendering | SD thumbnail + FFmpeg effects |
| **Ironist** | Quality Control | Cinematography validation |
| **Alchemist** | Budget Tracking | Spot price monitoring |
| **Shadow** | Legal Compliance | Copyright/licensing |
| **Catalyst** | Launch Orchestration | Publishing workflow |
| **Sage** | Analytics | Performance insights |
| **Guardian** | Security | Monitoring & alerts |

## Emotional Archetypes (v3.0)

### Original (v2.0)
1. **Curiosity** - Viewer investigating unknown
2. **Fear** - Viewer anticipating threat
3. **Triumph** - Viewer experiencing victory
4. **Tension** - Viewer on edge, awaiting resolution
5. **Wonder** - Viewer experiencing awe
6. **Urgency** - Viewer feeling time pressure
7. **Melancholy** - Viewer experiencing sadness/loss

### New (v3.0)
8. **Romance** - Intimacy and affection
9. **Joy** - Happiness, humor, and comedy
10. **Nostalgia** - Sentimental memories and flashbacks
11. **Rage** - Anger, fury, and revenge
12. **Serenity** - Calm, peace, and nature

## Installation

### Requirements

- Python 3.8+
- Redis 6.0+ (optional, for distributed processing)
- FFmpeg 4.0+
- pip

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/elite-video-pipeline-v3.0.git
cd elite-video-pipeline-v3.0

# Install dependencies
pip install -r requirements.txt

# (Optional) Start Redis
redis-server

# Run tests
python -m pytest tests/
```

## Quick Start

### Basic Usage

```python
from src.pipeline_orchestrator import create_orchestrator, PipelineConfig

# Create orchestrator
config = PipelineConfig(redis_host="localhost", redis_port=6379)
orchestrator = create_orchestrator(config)

# Submit a video job
job_id = orchestrator.submit_video_job(
    video_id="video_001",
    emotion="curiosity",
    intensity="medium"
)

# Process the job
success = orchestrator.process_job(job_id)

# Get pipeline status
status = orchestrator.get_pipeline_status()
print(f"Pipeline status: {status}")
```

### Emotional Profile Retrieval

```python
from src.emotional_index_v3 import EmotionalIndexManager

manager = EmotionalIndexManager()

# Get profile for specific emotion/intensity
profile = manager.get_emotion_profile("curiosity", "heavy")

# Access components
camera = profile["camera"]  # Camera movement parameters
color = profile["color"]    # Color grading settings
vfx = profile["vfx"]        # VFX effects list
```

### Cinematography Filter Generation

```python
from src.cinematography_engine import CinematographyEngine

engine = CinematographyEngine()

# Generate FFmpeg filter chain
filter_chain = engine.generate_filter_chain(profile)

# Build complete FFmpeg command
cmd = engine.build_ffmpeg_command(
    input_file="input.mp4",
    output_file="output.mp4",
    profile=profile,
    duration=60.0
)
```

## Configuration

### Pipeline Configuration

```python
from src.pipeline_orchestrator import PipelineConfig

config = PipelineConfig(
    redis_host="localhost",      # Redis server host
    redis_port=6379,             # Redis server port
    max_retries=3,               # Max retry attempts
    timeout_seconds=300,         # Job timeout
    enable_quality_gates=True,   # Enable quality validation
    enable_spot_pricing=True     # Enable spot price monitoring
)
```

### Redis Configuration

```python
from src.redis_orchestrator import RedisOrchestrator

orchestrator = RedisOrchestrator(
    host="localhost",
    port=6379,
    db=0
)
```

## Testing

### Run Full Test Suite

```bash
python tests/test_pipeline_closed_loop.py
```

### Test Coverage

- ✓ Emotional index completeness (12 archetypes)
- ✓ Profile structure validation
- ✓ Profile retrieval (all emotion/intensity combos)
- ✓ FFmpeg filter generation
- ✓ Profile validation logic
- ✓ Intensity modulation
- ✓ Quality gate validation
- ✓ Redis orchestrator (if available)
- ✓ End-to-end pipeline simulation

## API Reference

### PipelineOrchestrator

#### `submit_video_job(video_id, emotion, intensity, metadata)`
Submit a video for processing.

**Parameters:**
- `video_id` (str): Unique video identifier
- `emotion` (str): Emotion archetype
- `intensity` (str): 'light', 'medium', or 'heavy'
- `metadata` (dict): Optional metadata

**Returns:** job_id (str) or None

#### `process_job(job_id)`
Process a single job through the pipeline.

**Parameters:**
- `job_id` (str): Job identifier

**Returns:** bool (success)

#### `batch_process(jobs)`
Process multiple jobs in batch.

**Parameters:**
- `jobs` (list): List of job specifications

**Returns:** Results dictionary

#### `get_pipeline_status()`
Get overall pipeline status.

**Returns:** Status dictionary

#### `validate_pipeline()`
Validate pipeline configuration.

**Returns:** (is_valid, issues_list)

### EmotionalIndexManager

#### `get_emotion_profile(emotion, intensity)`
Retrieve emotion profile.

**Parameters:**
- `emotion` (str): Emotion name
- `intensity` (str): 'light', 'medium', or 'heavy'

**Returns:** Profile dictionary

#### `get_all_emotions()`
Get list of available emotions.

**Returns:** List of emotion names

### CinematographyEngine

#### `generate_filter_chain(profile)`
Generate FFmpeg filter chain.

**Parameters:**
- `profile` (dict): Emotional profile

**Returns:** FFmpeg filter string

#### `build_ffmpeg_command(input_file, output_file, profile, duration)`
Build complete FFmpeg command.

**Returns:** Command string

#### `validate_profile(profile)`
Validate profile structure.

**Returns:** (is_valid, errors_list)

## Performance Metrics

| Metric | Value |
|--------|-------|
| **Emotional Archetypes** | 12 |
| **Intensity Levels** | 3 (light, medium, heavy) |
| **Total Profiles** | 36 |
| **Filter Templates** | 40+ |
| **Redis Lookup Time** | O(1) microseconds |
| **Filter Generation Time** | <100ms |
| **Quality Gate Checks** | 5+ validations |

## Cost Analysis

| Component | Cost | Notes |
|-----------|------|-------|
| **Emotional Index** | $0 | Pre-computed lookup |
| **Cinematography** | $0 | CPU-bound FFmpeg |
| **Quality Gates** | $0 | Local validation |
| **Redis** | $0-20/mo | Optional, scalable |
| **Total (30 videos)** | $0.277/video | +$0.002 vs v2.0 |

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ src/
COPY config/ config/

CMD ["python", "src/pipeline_orchestrator.py"]
```

### Kubernetes

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
        env:
        - name: REDIS_HOST
          value: redis-service
        - name: REDIS_PORT
          value: "6379"
```

## Licensing

This project uses **dual licensing**:

- **GPL v3** - For open-source use
- **Commercial License** - For proprietary use

See `LICENSE.md` for details.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## Support

For issues, questions, or suggestions:

- GitHub Issues: https://github.com/yourusername/elite-video-pipeline-v3.0/issues
- Email: support@example.com
- Documentation: https://docs.example.com

## Changelog

### v3.0 (Current)
- ✨ Added 5 new emotional archetypes (romance, joy, nostalgia, rage, serenity)
- ✨ Enhanced cinematography engine with 40+ filter templates
- ✨ Improved quality gate validation
- ✨ Redis orchestrator for distributed processing
- 🔧 Optimized FFmpeg filter chains
- 📊 Enhanced performance metrics

### v2.0
- Initial emotional cinematography system
- 7 core emotional archetypes
- GPU spot price monitoring
- FFmpeg integration

## Authors

- **Manus AI** - Architecture & Development

## Acknowledgments

- FFmpeg community for excellent video processing tools
- Redis team for robust data structures
- Hollywood cinematography best practices

---

**Elite Video Pipeline v3.0** - Professional Video Production at Scale
