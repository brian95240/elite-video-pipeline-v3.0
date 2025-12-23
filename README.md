# Elite Video Pipeline v3.0: Emotional Direction as Code

**Turn raw video footage into emotionally resonant stories with a single command. This is not just a video processor—it's an automated Hollywood director in a box.**

---

<p align="center">
  <img src="https://raw.githubusercontent.com/brian95240/elite-video-pipeline-v3.0/main/docs/assets/elite-pipeline-hero.png" alt="Elite Video Pipeline v3.0 Hero Image" width="800">
</p>

---

## 🎬 What is the Elite Video Pipeline?

The Elite Video Pipeline is a revolutionary system that automates the art of cinematography. It analyzes your desired emotion and applies a corresponding suite of cinematic effects—camera movements, color grading, pacing, and visual effects—to transform your raw footage into a polished, emotionally compelling video.

**Input:** Raw video + a desired emotion (e.g., "Triumph", "Nostalgia", "Rage")

**Output:** A professionally graded and edited video that evokes that specific feeling.

### How It Works: The Cinematography Engine

At its core, the pipeline uses a sophisticated **Cinematography Engine** that translates emotional concepts into technical FFmpeg filter chains. It draws from a library of 40+ cinematic techniques, all mapped to a rich emotional taxonomy.

```
User Input: "Make this video feel like TRIUMPH (Heavy)"
                          ↓
              Emotional Index Lookup
                          ↓
         Cinematography Engine Generates:
         - Camera: Slow-motion hero shot
         - Color: High saturation, warm tones
         - VFX: Lens flare, dramatic lighting
         - Pacing: Ramped slow-motion
                          ↓
              FFmpeg Filter Chain:
              "scale=1920:1080,fps=24,
               curves=vintage,
               zoompan=z=\'min(zoom+0.0015,1.5)\',
               colorbalance=rs=0.3:gs=0.1:bs=-0.2,
               vignette=PI/4"
                          ↓
              Rendered Video Output
```

---

## ✨ Key Features

### 1. **A Palette of 12 Emotional Archetypes**

Direct your videos with a rich emotional vocabulary. Each archetype has been meticulously designed with corresponding cinematic language.

| Archetype | Cinematic Style |
|---|---|
| **Triumph** | Uplifting slow-motion, warm & saturated colors, epic zooms |
| **Nostalgia** | Soft focus, vintage color grading (sepia/faded), gentle vignettes |
| **Rage** | High contrast, desaturated colors with red hues, shaky cam effects |
| **Serenity** | Smooth, slow pans; natural, soft lighting; calm color palettes |
| **Urgency** | Rapid cuts, quick zooms, high-energy camera movements |

**3 Intensity Levels (Light, Medium, Heavy)** allow for nuanced control, from a subtle hint of emotion to a powerful, immersive experience.

### 2. **Automated Hollywood Cinematography**

The pipeline automates techniques used by professional cinematographers:

- **Camera Movements:** Pans, tilts, zooms, dolly shots, and shaky cam effects.
- **Color Grading:** Emotional color palettes, LUT-inspired curves, saturation, and contrast adjustments.
- **Visual Effects (VFX):** Lens flares, vignettes, blurs, chromatic aberration, and light leaks.
- **Pacing & Rhythm:** Frame rate adjustments, slow-motion, and time-lapses to control the energy of the scene.

### 3. **Robust Microservices Architecture (10-Archetype Firewall)**

Inspired by Jungian archetypes, the pipeline is built on a robust, scalable microservices architecture. Each service has a distinct role, ensuring reliability and specialization.

| Archetype | Role | Responsibility |
|---|---|---|
| **Oracle** | Script Generation | Extracts emotional arcs and metadata |
| **Trickster** | Voice Synthesis | Generates TTS with emotional context |
| **Spectacle** | Rendering | Executes FFmpeg filter chains |
| **Ironist** | Quality Control | Validates cinematic and technical quality |
| **Alchemist** | Budget Tracking | Monitors processing costs |
| **Guardian** | Security | Monitors system health and security |

### 4. **Cloud-Native & Scalable**

- **Redis Orchestration:** Manages job queues for high-throughput, asynchronous processing.
- **Neon Serverless DB:** Uses a serverless PostgreSQL database for state management, metrics, and emotional profile storage.
- **Ready for Scale:** Designed for containerization (Docker/Kubernetes) and horizontal scaling.

---

## 🚀 Who Is This For?

- **Content Creators:** Instantly elevate your social media videos, YouTube content, and marketing materials.
- **Marketing Agencies:** Produce emotionally resonant ad campaigns at scale.
- **AI Video Developers:** Integrate as a post-processing layer for AI-generated video to add cinematic flair.
- **Media Platforms:** Automate the production of trailers, highlight reels, and promotional content.
- **Indie Filmmakers:** Achieve professional-grade color grading and effects without a big budget.

---

## 🛠️ Getting Started

### Quick Install

This project is designed for a Linux environment with Python 3.11, Redis, and FFmpeg. For a complete, one-line deployment to a Hetzner cloud server, see our **[Hetzner Deployment Guide](HETZNER_DEPLOYMENT.md)**.

```bash
# 1. Clone the repository
git clone https://github.com/brian95240/elite-video-pipeline-v3.0.git
cd elite-video-pipeline-v3.0

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run tests to verify setup
python tests/test_pipeline_closed_loop.py
```

### Quick Start Example

```python
from src.pipeline_orchestrator import create_orchestrator, PipelineConfig

# Configure the pipeline (assumes local Redis)
config = PipelineConfig(redis_host="localhost", redis_port=6379)
orchestrator = create_orchestrator(config)

# Submit a job to transform a video with the "Triumph" emotion
job_id = orchestrator.submit_video_job(
    video_path="./input/raw_footage.mp4",
    output_path="./output/triumph_heavy.mp4",
    emotion="triumph",
    intensity="heavy"
)

# Process the job
success = orchestrator.process_job(job_id)

if success:
    print(f"Successfully created emotionally enhanced video: ./output/triumph_heavy.mp4")
```

---

## 📚 Documentation

- **[API Reference](docs/API_REFERENCE.md):** Detailed documentation for all classes, methods, and emotional profiles.
- **[Architecture Deep Dive](docs/ARCHITECTURE.md):** An in-depth look at the system design, microservices, and data flow.
- **[Hetzner Deployment Guide](HETZNER_DEPLOYMENT.md):** Step-by-step instructions for deploying to a production environment on Hetzner Cloud.

---

## 🤝 Contributing

Contributions are welcome! Whether it's adding new emotional archetypes, improving filter chains, or enhancing the architecture, we encourage you to fork the repository and submit a pull request.

---

## 📜 Licensing

This project is dual-licensed under **GPL v3** for open-source projects and a **Commercial License** for proprietary use. See `LICENSE.md` for details.

---

## 🧠 Acknowledgments

- **Project Architect & Lead Developer:** Manus AI
- **Inspiration:** The art of Hollywood cinematography and the power of emotional storytelling.
