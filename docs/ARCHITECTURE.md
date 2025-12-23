# Elite Video Pipeline v3.0 - Architecture Documentation

## System Overview

Elite Video Pipeline v3.0 is a distributed microservices architecture designed for professional video production with emotional intelligence. The system processes videos through 8 specialized stages, each handled by a distinct archetype service.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         User Submission                           │
│                    (Video ID + Emotion + Intensity)               │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Redis Orchestrator                             │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Job Queue Management | State Tracking | Health Monitoring │  │
│  └────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    ┌────────┐          ┌────────┐          ┌────────┐
    │ Oracle │          │Trickster│         │Cartographer│
    │(Script)│          │(Voice)  │         │(Retention) │
    └────────┘          └────────┘          └────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │   Emotional Index Lookup (O(1))        │
        │  12 Archetypes × 3 Intensities = 36   │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Cinematography Engine                 │
        │  - Filter Chain Generation             │
        │  - FFmpeg Composition                  │
        │  - Quality Validation                  │
        └────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    ┌────────┐          ┌────────┐          ┌────────┐
    │Spectacle│         │ Ironist │         │Alchemist│
    │(Render) │         │(Quality)│         │(Budget) │
    └────────┘          └────────┘          └────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    ┌────────┐          ┌────────┐          ┌────────┐
    │ Shadow │          │Catalyst│         │Guardian│
    │(Legal) │          │(Launch) │         │(Monitor)│
    └────────┘          └────────┘          └────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Published     │
                    │  Video Output  │
                    └────────────────┘
```

## Core Components

### 1. Emotional Index Manager

**Location:** `src/emotional_index_v3.py`

**Responsibility:** Manage 12 emotional archetypes and their cinematographic profiles

**Features:**
- 12 pre-configured emotional archetypes
- 3 intensity levels per emotion (light, medium, heavy)
- O(1) profile lookup
- Redis integration for distributed systems

**Data Structure:**
```python
{
    "emotion_name": {
        "description": "...",
        "camera": {
            "light": {...},
            "medium": {...},
            "heavy": {...}
        },
        "color": {
            "light": {...},
            "medium": {...},
            "heavy": {...}
        },
        "vfx": {
            "light": [...],
            "medium": [...],
            "heavy": [...]
        },
        "ffmpeg": "filter_chain_string"
    }
}
```

### 2. Redis Orchestrator

**Location:** `src/redis_orchestrator.py`

**Responsibility:** Coordinate microservices and manage job state

**Features:**
- Job submission and tracking
- Queue management (8 service queues)
- State persistence
- Dead Letter Queue (DLQ) for failed jobs
- Health monitoring
- Metrics collection

**Queue Structure:**
```
pipeline:queue:oracle          → Script generation
pipeline:queue:trickster       → Voice synthesis
pipeline:queue:cartographer    → Cinematography
pipeline:queue:spectacle       → Rendering
pipeline:queue:ironist         → Quality gates
pipeline:queue:alchemist       → Budget tracking
pipeline:queue:shadow          → Legal compliance
pipeline:queue:catalyst        → Launch orchestration
pipeline:queue:dlq             → Failed jobs
```

### 3. Cinematography Engine

**Location:** `src/cinematography_engine.py`

**Responsibility:** Generate FFmpeg filter chains from emotional profiles

**Features:**
- 40+ filter templates
- Dynamic filter chain composition
- Profile validation
- Intensity modulation
- Quality gate validation

**Filter Categories:**
- Camera movements (zoom, dolly, pan, crane, orbit)
- Color grading (saturation, contrast, vignette, bloom)
- VFX effects (flare, glow, particles, distortion)
- Motion effects (blur, speed lines, strobe)

### 4. Pipeline Orchestrator

**Location:** `src/pipeline_orchestrator.py`

**Responsibility:** Main orchestration and workflow management

**Features:**
- Job submission
- Pipeline validation
- Batch processing
- Status monitoring
- Health checks
- 10-archetype firewall integration

## 10-Archetype Firewall

The pipeline uses 10 specialized microservices, each with distinct responsibilities:

| # | Archetype | Role | Input | Output | Processing |
|---|-----------|------|-------|--------|------------|
| 1 | **Oracle** | Script Generation | Trend topic | Script + emotional arc | CPU (Claude API) |
| 2 | **Trickster** | Voice Synthesis | Script + arc | Voice audio | GPU (TTS) |
| 3 | **Cartographer** | Retention Mapping | Voice + arc | Retention map + cinematography JSON | CPU |
| 4 | **Spectacle** | Rendering | Cinematography JSON | Video with effects | GPU (FFmpeg) |
| 5 | **Ironist** | Quality Control | Rendered video | Quality report | CPU (analysis) |
| 6 | **Alchemist** | Budget Tracking | Job metadata | Cost breakdown | CPU (monitoring) |
| 7 | **Shadow** | Legal Compliance | Video metadata | Compliance report | CPU (validation) |
| 8 | **Catalyst** | Launch Orchestration | Approved video | Published output | CPU (publishing) |
| 9 | **Sage** | Analytics | All job data | Performance insights | CPU (analysis) |
| 10 | **Guardian** | Security & Monitoring | System metrics | Security alerts | CPU (monitoring) |

## Data Flow

### Job Submission Flow

```
User Input
  ├─ video_id: "video_001"
  ├─ emotion: "curiosity"
  ├─ intensity: "medium"
  └─ metadata: {...}
         │
         ▼
  Job Creation
  ├─ job_id: "video_001_1703001234567"
  ├─ status: "idle"
  ├─ created_at: timestamp
  └─ metadata: {...}
         │
         ▼
  Redis Storage
  ├─ State: pipeline:state:job_id
  └─ Queue: pipeline:queue:oracle
         │
         ▼
  Enqueued for Processing
```

### Processing Pipeline Flow

```
Stage 1: Oracle (Script Generation)
  Input: Trend topic + emotional arc requirement
  Process: Generate script with emotional markers
  Output: Script + emotional arc timeline
  Cost: $0.12 (API call)
         │
         ▼
Stage 2: Trickster (Voice Synthesis)
  Input: Script + emotional arc metadata
  Process: TTS with emotional inflection
  Output: Voice audio file
  Cost: $0.05 (TTS service)
         │
         ▼
Stage 3: Cartographer (Retention Mapping)
  Input: Voice audio + emotional arc
  Process: Analyze retention points + generate cinematography
  Output: Retention map + cinematography.json
  Cost: $0.08 (Whisper + processing)
         │
         ▼
Stage 4: Spectacle (Rendering)
  Input: Base video + cinematography.json
  Process: Apply FFmpeg filters + effects
  Output: Rendered video with cinematography
  Cost: $0.017 (GPU time)
         │
         ▼
Stage 5: Ironist (Quality Control)
  Input: Rendered video
  Process: Validate color grading, effects, stability
  Output: Quality report (pass/fail/warn)
  Cost: $0.02 (analysis)
         │
         ▼
Stage 6: Alchemist (Budget Tracking)
  Input: Job metadata + costs
  Process: Track spending + monitor budget
  Output: Cost breakdown
  Cost: $0 (monitoring)
         │
         ▼
Stage 7: Shadow (Legal Compliance)
  Input: Video metadata
  Process: Copyright check + licensing validation
  Output: Compliance report
  Cost: $0.01 (validation)
         │
         ▼
Stage 8: Catalyst (Launch)
  Input: Approved video
  Process: Publishing workflow
  Output: Published video
  Cost: $0 (orchestration)
         │
         ▼
Final Output: Published Video
```

## Emotional Archetypes

### Original (v2.0)

1. **Curiosity** - Slow zoom, cool tones, mystery effects
2. **Fear** - Handheld shake, desaturated colors, glitch effects
3. **Triumph** - Crane up, warm golden tones, particle effects
4. **Tension** - Static locked, high contrast, strobe effects
5. **Wonder** - Slow pan, ethereal glow, volumetric rays
6. **Urgency** - Quick cuts, warm saturation, motion blur
7. **Melancholy** - Slow dolly back, desaturated blue, rain overlay

### New (v3.0)

8. **Romance** - Static two-shot, warm soft glow, bokeh particles
9. **Joy** - Whip pan, vibrant colors, confetti effects
10. **Nostalgia** - Handheld gentle, sepia tint, film grain
11. **Rage** - Erratic handheld, red tint, chromatic aberration
12. **Serenity** - Drone hover, natural balanced, mist layer

## Intensity Modulation

Each emotion supports 3 intensity levels:

| Level | Camera Speed | Saturation | Contrast | VFX Complexity |
|-------|--------------|-----------|----------|-----------------|
| **Light** | 0.5x | Subtle (-5%) | 1.05 | Minimal |
| **Medium** | 1.0x | Moderate (-10%) | 1.15 | Standard |
| **Heavy** | 1.5x | Strong (-20%) | 1.35 | Complex |

## Performance Characteristics

### Time Complexity
- Profile lookup: O(1)
- Filter generation: O(n) where n = number of effects
- Validation: O(m) where m = validation checks
- Overall pipeline: O(n*m) linear in job count

### Space Complexity
- Emotional index: O(12*3) = O(1) constant
- Redis state: O(j) where j = number of jobs
- Filter templates: O(40) constant

### Throughput
- Jobs per second: Limited by slowest stage (typically GPU rendering)
- Concurrent jobs: Scales with available resources
- Queue depth: Unlimited (Redis scalable)

## Failure Handling

### Retry Logic
```python
if job_fails:
    retry_count += 1
    if retry_count <= max_retries:
        requeue(job)
    else:
        move_to_dlq(job, error_message)
```

### Dead Letter Queue
- Stores failed jobs with error details
- Allows manual inspection and recovery
- Prevents infinite retry loops

### Timeout Handling
- Default: 300 seconds per job
- Configurable per stage
- Automatic job termination on timeout

## Scalability

### Horizontal Scaling
- Multiple orchestrator instances
- Redis cluster for distributed state
- Load balancing across workers

### Vertical Scaling
- Increase worker concurrency
- Optimize filter chain execution
- GPU acceleration for rendering

### Resource Management
- KEDA for Kubernetes auto-scaling
- CPU-bound stages on standard nodes
- GPU-bound stages on GPU nodes

## Security

### Data Protection
- Redis authentication (optional)
- Encrypted job state
- Secure credential storage

### Access Control
- Role-based service permissions
- API key authentication
- Rate limiting

### Compliance
- GDPR compliance for video metadata
- Copyright validation (Shadow archetype)
- Audit logging for all operations

## Monitoring & Observability

### Metrics
- Job success/failure rates
- Processing time per stage
- Queue depth and latency
- Resource utilization

### Logging
- Structured logging per service
- Centralized log aggregation
- Debug mode for troubleshooting

### Alerting
- Queue depth thresholds
- Error rate alerts
- Resource exhaustion warnings
- Budget overrun alerts

## Cost Analysis

### Per-Video Cost Breakdown

| Stage | Component | Cost | Notes |
|-------|-----------|------|-------|
| 1 | Oracle | $0.12 | Claude API call |
| 2 | Trickster | $0.05 | TTS service |
| 3 | Cartographer | $0.08 | Whisper + processing |
| 4 | Spectacle | $0.017 | GPU rendering |
| 5 | Ironist | $0.02 | Analysis |
| 6 | Alchemist | $0 | Monitoring |
| 7 | Shadow | $0.01 | Validation |
| 8 | Catalyst | $0 | Publishing |
| **Total** | **Per Video** | **$0.277** | **+$0.002 vs v2.0** |

### Monthly Cost (30 videos)
- v2.0: $8.25
- v3.0: $8.31
- Increase: $0.06 (0.7%)

## Future Enhancements

### Planned Features
- [ ] Additional emotional archetypes
- [ ] Advanced color grading LUTs
- [ ] Real-time preview rendering
- [ ] A/B testing framework
- [ ] Automated optimization
- [ ] Multi-language support

### Research Areas
- Machine learning for emotional detection
- Generative AI for custom effects
- Real-time rendering optimization
- Distributed GPU processing

---

**Document Version:** 1.0
**Last Updated:** December 2024
**Architecture Version:** 3.0
