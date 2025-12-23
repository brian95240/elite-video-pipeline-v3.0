# Elite Video Pipeline v3.0 - API Reference

This document provides a detailed reference for the core APIs of the Elite Video Pipeline. For a higher-level overview, please see the main [README.md](../README.md).

---

## 1. Pipeline Orchestrator

**Class:** `src.pipeline_orchestrator.PipelineOrchestrator`

**Description:** The main entry point for submitting and managing video processing jobs. It coordinates the various microservices and manages the job lifecycle.

### Initialization

```python
from src.pipeline_orchestrator import create_orchestrator, PipelineConfig

# Default configuration (local processing)
config = PipelineConfig()

# Configuration with Redis for distributed processing
config = PipelineConfig(redis_host="localhost", redis_port=6379)

orchestrator = create_orchestrator(config)
```

### Methods

#### `submit_video_job(video_path, output_path, emotion, intensity, metadata=None)`

Submits a new video for emotional processing.

- **Parameters:**
  - `video_path` (str): Absolute path to the input video file.
  - `output_path` (str): Absolute path for the processed output video.
  - `emotion` (str): The target emotion. Must be one of the 12 supported archetypes.
  - `intensity` (str): The desired emotional intensity (`light`, `medium`, or `heavy`).
  - `metadata` (dict, optional): Custom metadata to attach to the job.
- **Returns:** `str` - The unique ID of the submitted job.

#### `process_job(job_id)`

Processes a single job from the queue. This method is typically called by a worker process.

- **Parameters:**
  - `job_id` (str): The ID of the job to process.
- **Returns:** `bool` - `True` on success, `False` on failure.

#### `get_job_status(job_id)`

Retrieves the current status and details of a specific job.

- **Parameters:**
  - `job_id` (str): The ID of the job.
- **Returns:** `dict` - A dictionary containing job status, metadata, and processing history.

#### `get_pipeline_status()`

Provides an overview of the entire pipeline's health and workload.

- **Returns:** `dict` - A dictionary with queue lengths, active workers, and error rates.

---

## 2. Emotional Index Manager

**Class:** `src.emotional_index_v3.EmotionalIndexManager`

**Description:** Provides access to the 36 pre-defined emotional profiles. This is the core of the pipeline's emotional intelligence.

### Initialization

```python
from src.emotional_index_v3 import EmotionalIndexManager

manager = EmotionalIndexManager()
```

### Methods

#### `get_emotion_profile(emotion, intensity)`

Retrieves the detailed cinematographic profile for a given emotion and intensity.

- **Parameters:**
  - `emotion` (str): The target emotion archetype.
  - `intensity` (str): The desired intensity (`light`, `medium`, `heavy`).
- **Returns:** `dict` - A dictionary containing the complete profile with `camera`, `color`, and `vfx` keys.

**Example Profile Structure:**
```json
{
  "emotion": "nostalgia",
  "intensity": "medium",
  "camera": {
    "movement": "slow_pan",
    "zoom": "gentle_zoom_in",
    "focus": "soft"
  },
  "color": {
    "grading": "sepia_tone",
    "saturation": 0.8,
    "contrast": 0.9
  },
  "vfx": {
    "effects": ["vignette", "light_leak"],
    "grain_opacity": 0.1
  },
  "pacing": {
    "speed": 0.95
  }
}
```

#### `get_all_emotions()`

Returns a list of all available emotional archetypes.

- **Returns:** `list[str]` - A list of the 12 emotion names.

---

## 3. Cinematography Engine

**Class:** `src.cinematography_engine.CinematographyEngine`

**Description:** The engine that translates an emotional profile into a concrete FFmpeg filter chain.

### Initialization

```python
from src.cinematography_engine import CinematographyEngine

engine = CinematographyEngine()
```

### Methods

#### `generate_filter_chain(profile)`

Generates a complex FFmpeg filter string from an emotional profile.

- **Parameters:**
  - `profile` (dict): The emotional profile obtained from the `EmotionalIndexManager`.
- **Returns:** `str` - A string formatted for use with FFmpeg's `-vf` flag.

#### `build_ffmpeg_command(input_file, output_file, profile, duration)`

Constructs the full FFmpeg command for processing a video.

- **Parameters:**
  - `input_file` (str): Path to the input video.
  - `output_file` (str): Path for the output video.
  - `profile` (dict): The emotional profile.
  - `duration` (float): The duration of the video in seconds.
- **Returns:** `str` - The complete, executable FFmpeg command.

---

## 4. Emotional Archetypes API

This section details the 12 emotional archetypes and their corresponding cinematic language. You can request these profiles via the `EmotionalIndexManager`.

| Emotion | Description | Cinematic Language |
|---|---|---|
| **Triumph** | Victory, success, and overcoming obstacles. | Uplifting slow-motion, warm & saturated colors, epic zooms, lens flares. |
| **Nostalgia** | Sentimental longing for the past. | Soft focus, vintage color grading (sepia/faded), gentle vignettes, slow pans. |
| **Rage** | Intense anger and fury. | High contrast, desaturated colors with red hues, shaky cam effects, rapid cuts. |
| **Serenity** | Calm, peace, and tranquility. | Smooth, slow pans; natural, soft lighting; calm and balanced color palettes. |
| **Urgency** | Feeling of time pressure and high stakes. | Rapid cuts, quick zooms, high-energy camera movements, cool color tones. |
| **Fear** | Anticipation of threat, suspense. | Dark and underexposed lighting, cool blue/green tones, dutch angles, slow dolly-ins. |
| **Joy** | Happiness, humor, and lightheartedness. | Bright, vibrant colors; warm lighting; dynamic but smooth camera work. |
| **Melancholy** | Sadness, loss, and reflection. | Desaturated and cool colors, slow pacing, static shots, focus on empty spaces. |
| **Wonder** | Awe, amazement, and discovery. | Wide shots, vibrant and magical colors, slow and majestic camera movements. |
| **Tension** | On edge, awaiting resolution. | Extreme close-ups, shallow depth of field, dissonant colors, handheld camera. |
| **Curiosity** | Investigating the unknown, mystery. | Point-of-view shots, rack focus, selective lighting to hide/reveal information. |
| **Romance** | Intimacy, affection, and connection. | Soft lighting, warm color palettes (pinks/reds), shallow depth of field, close-ups. |

### Intensity Levels

Each archetype can be modulated by one of three intensity levels:

- **Light:** A subtle application of the emotional style. Good for background mood.
- **Medium:** A balanced and noticeable application of the style. The default choice.
- **Heavy:** An intense and immersive application of the style, making the emotion the central focus of the experience.
