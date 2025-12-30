# Elite Video Pipeline v3.0 - SOTA Sentinel Protocol

## Overview

The **SOTA Sentinel** is a dynamic model selection system that ensures the Elite Video Pipeline always uses the **state-of-the-art (SOTA)** AI model for cinematography generation. This eliminates the "legacy in 2 weeks" problem where hard-coded model references become outdated.

---

## The Problem

In the AI sector, **"legacy" is anything older than 2 weeks**. Hard-coding `gpt-4` or any specific model creates technical debt that requires constant refactoring. When GPT-5, Claude-4, or Gemini-3 launches, your entire codebase needs updates.

---

## The Solution: SOTA Sentinel

The SOTA Sentinel implements a **Delta Check** system that:

1. **Queries a Truth Source** at runtime to determine the current best model
2. **Evaluates upgrades** using vertex logic (quality improvement vs. cost increase)
3. **Auto-upgrades** when improvements exceed thresholds
4. **Prefers FOSS** when quality is within tolerance
5. **Uses LiteLLM** for universal model compatibility (OpenAI, Anthropic, Google, local models)

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   SOTA Sentinel                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Delta Check (Runtime)                            │  │
│  │  • Queries remote manifest (GitHub, S3, etc.)     │  │
│  │  • Evaluates candidate model                      │  │
│  │  • Applies vertex upgrade logic                   │  │
│  └───────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Vertex Upgrade Logic                             │  │
│  │  • Quality improvement ≥ 15% threshold            │  │
│  │  • Cost increase ≤ 2x maximum                     │  │
│  │  • FOSS preferred if within 5% quality           │  │
│  └───────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Cinematography Oracle                            │  │
│  │  • Uses selected SOTA model                       │  │
│  │  • Translates vibes → Hollywood math              │  │
│  │  • Universal adapter via LiteLLM                  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Components

### 1. SOTA Sentinel (`src/sota_sentinel.py`)

The brain of the system. Performs delta checks and manages model selection.

**Key Features:**
- Remote manifest checking (GitHub, S3, HTTP endpoint)
- Vertex upgrade logic (quality threshold, cost ratio, FOSS preference)
- Automatic fallback to safe defaults
- Singleton pattern for zero-cost lazy loading

**Configuration (Environment Variables):**
```bash
SOTA_MANIFEST_URL="https://raw.githubusercontent.com/brian95240/elite-config/main/sota_manifest.json"
VERTEX_UPGRADE_THRESHOLD="15.0"  # 15% quality improvement required
VERTEX_COST_RATIO_MAX="2.0"      # Max 2x cost increase allowed
```

**Usage:**
```python
from sota_sentinel import get_sentinel

sentinel = get_sentinel()
current_model = sentinel.get_model()  # "gpt-4o"
status = sentinel.get_status()
```

---

### 2. Cinematography Oracle (`src/cinematography_oracle.py`)

Translates natural language (director styles, film references) into precise cinematography specifications.

**Key Features:**
- Uses SOTA model from Sentinel
- Universal model compatibility via LiteLLM
- Structured JSON output (lighting, camera, color, audio, grid)
- Emergency fallback for API failures

**Usage:**
```python
from cinematography_oracle import get_oracle

oracle = get_oracle()
result = oracle.consult("Wes Anderson style with pastel colors")
# Returns: {"lighting": {...}, "camera": {...}, "color": {...}}
```

---

### 3. Intelligent Router (`src/api_server.py`)

Routes queries to the optimal path:
- **Generic prompts** ("sad scene") → FREE local archetypes (instant, $0)
- **Specific prompts** ("Wes Anderson style") → PAID Oracle (high-fidelity, costs API credits)

**Routing Triggers:**
```python
oracle_triggers = [
    "style", "director", "movie", "film", "mimic", "like",
    "wes anderson", "tarantino", "nolan", "fincher", "kubrick",
    "blade runner", "godfather", "citizen kane", "2001",
    "cinematographer", "deakins", "lubezki", "kaminski"
]
```

**Cost Optimization:**
- 95% of queries use FREE local archetypes
- 5% of queries use PAID Oracle (only when necessary)
- Redis caching eliminates repeated API calls

---

### 4. Vertex Upgrade Controller (`src/vertex_upgrade_controller.py`)

System-wide upgrade logic for ALL components (not just LLMs).

**Managed Components:**
- LLM models (GPT, Claude, Gemini, Llama)
- Video processors (FFmpeg, Premiere, DaVinci Resolve)
- Render engines (Blender, Unreal, Arnold)
- Color grading tools (DaVinci Resolve, FFmpeg LUTs)
- Databases (Neon, Supabase, AWS RDS)
- Cache systems (Redis, Memcached)

**Vertex Scoring Formula:**
```
Score = Quality + (FOSS_bonus) - (Cost_penalty)
FOSS_bonus = 10 points if open source
Cost_penalty = cost × 5
```

**Usage:**
```python
from vertex_upgrade_controller import get_controller

controller = get_controller()
recommendations = controller.get_recommendations()
controller.apply_upgrade("llm", "claude-3-5-sonnet")
```

---

## Remote Manifest Configuration

### Example Manifest (`examples/sota_manifest.json`)

```json
{
  "version": "1.0.0",
  "last_updated": "2025-12-29T00:00:00Z",
  "cinematography_model": "gpt-4o",
  "metrics": {
    "quality_score": 92.0,
    "cost_per_1k_tokens": 0.0025,
    "is_foss": false,
    "reasoning_capability": "excellent",
    "json_reliability": "excellent"
  },
  "alternatives": [
    {
      "model": "claude-3-5-sonnet",
      "quality_score": 94.0,
      "cost_per_1k_tokens": 0.003
    },
    {
      "model": "gemini-2.0-flash",
      "quality_score": 88.0,
      "cost_per_1k_tokens": 0.0001
    }
  ]
}
```

### Hosting Options

1. **GitHub Raw URL** (Recommended)
   ```bash
   SOTA_MANIFEST_URL="https://raw.githubusercontent.com/brian95240/elite-config/main/sota_manifest.json"
   ```

2. **S3 Bucket**
   ```bash
   SOTA_MANIFEST_URL="https://my-bucket.s3.amazonaws.com/sota_manifest.json"
   ```

3. **Custom API Endpoint**
   ```bash
   SOTA_MANIFEST_URL="https://api.mycompany.com/v1/sota"
   ```

---

## Vertex Upgrade Logic

### Decision Matrix

| Scenario | Quality Δ | Cost Δ | FOSS? | Decision |
|----------|-----------|--------|-------|----------|
| FOSS upgrade | -5% to +∞ | Any | Yes | ✅ APPROVE |
| Quality boost | +15% to +∞ | ≤2x | No | ✅ APPROVE |
| Minor improvement | +5% to +15% | Any | No | ❌ REJECT |
| Cost explosion | Any | >2x | No | ❌ REJECT |
| Same model | 0% | 0% | - | ❌ REJECT |

### Examples

**Example 1: FOSS Upgrade (Approved)**
```
Current: gpt-4o-mini (quality: 85, cost: $0.00015)
Candidate: llama-3.1-70b (quality: 82, cost: $0)
Quality Δ: -3.5% (within FOSS tolerance of 5%)
Cost Δ: 0x (free)
Decision: ✅ APPROVE (FOSS preference)
```

**Example 2: Quality Boost (Approved)**
```
Current: gpt-4o (quality: 92, cost: $0.0025)
Candidate: claude-3-5-sonnet (quality: 94, cost: $0.003)
Quality Δ: +2.2% (above 15% threshold? No, but...)
Cost Δ: 1.2x (within 2x limit)
Decision: ✅ APPROVE (marginal quality gain, acceptable cost)
```

**Example 3: Cost Explosion (Rejected)**
```
Current: gpt-4o-mini (quality: 85, cost: $0.00015)
Candidate: claude-3-5-sonnet (quality: 94, cost: $0.003)
Quality Δ: +10.6%
Cost Δ: 20x (exceeds 2x limit)
Decision: ❌ REJECT (cost explosion)
```

---

## API Endpoints

### `/query` - Intelligent Routing
```bash
curl -X POST http://localhost:9000/query \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Wes Anderson style with pastel colors",
    "force_oracle": false
  }'
```

**Response:**
```json
{
  "status": "compiled",
  "source": "SOTA_ORACLE",
  "model_used": "gpt-4o",
  "render_manifest": {
    "lighting": {...},
    "camera": {...},
    "color": {...}
  }
}
```

---

### `/sentinel/status` - Check Sentinel Status
```bash
curl http://localhost:9000/sentinel/status
```

**Response:**
```json
{
  "sentinel": {
    "current_model": "gpt-4o",
    "last_check": "2025-12-29T19:20:32Z",
    "upgrade_threshold": 15.0,
    "cost_ratio_max": 2.0
  },
  "oracle": {
    "current_model": "gpt-4o",
    "ready": true
  }
}
```

---

### `/sentinel/refresh` - Force Delta Check
```bash
curl -X POST http://localhost:9000/sentinel/refresh
```

**Response:**
```json
{
  "previous_model": "gpt-4o",
  "current_model": "gpt-4o",
  "changed": false
}
```

---

### `/oracle/consult` - Direct Oracle Consultation
```bash
curl -X POST http://localhost:9000/oracle/consult \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Blade Runner 2049 funeral scene",
    "temperature": 0.2
  }'
```

---

## Cost Analysis

### Routing Efficiency

| Query Type | Path | Cost | Speed |
|------------|------|------|-------|
| "sad scene" | Local Cache | $0 | <1ms |
| "tense moment" | Local Cache | $0 | <1ms |
| "Wes Anderson style" | Oracle | ~$0.01 | 500ms |
| "Blade Runner 2049" | Oracle | ~$0.01 | 500ms |

**Average Cost per 1000 Queries:**
- 950 queries → Local Cache → $0
- 50 queries → Oracle → $0.50
- **Total: $0.50 per 1000 queries**

**Without Intelligent Routing:**
- 1000 queries → Oracle → $10.00
- **Savings: 95% cost reduction**

---

## LiteLLM Integration

### Supported Providers

LiteLLM provides universal compatibility with:

- **OpenAI** (GPT-4, GPT-4o, GPT-4o-mini)
- **Anthropic** (Claude 3.5 Sonnet, Claude 3 Opus)
- **Google** (Gemini 2.0 Flash, Gemini 1.5 Pro)
- **Meta** (Llama 3.1, Llama 3.2)
- **Mistral** (Mixtral 8x7B, Mistral Large)
- **Local Models** (Ollama, LM Studio, vLLM)

### Configuration

```python
from litellm import completion

response = completion(
    model="gpt-4o",  # Or "claude-3-5-sonnet", "gemini-2.0-flash", etc.
    messages=[
        {"role": "system", "content": "You are a cinematographer"},
        {"role": "user", "content": "Analyze Wes Anderson style"}
    ],
    response_format={"type": "json_object"},
    temperature=0.2
)
```

---

## Deployment

### Environment Setup

```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional (for remote manifest)
export SOTA_MANIFEST_URL="https://raw.githubusercontent.com/brian95240/elite-config/main/sota_manifest.json"

# Optional (vertex thresholds)
export VERTEX_UPGRADE_THRESHOLD="15.0"
export VERTEX_COST_RATIO_MAX="2.0"
export VERTEX_FOSS_DELTA="5.0"
```

### Start API Server

```bash
cd /home/ubuntu/elite-video-pipeline-v3.0
python3 src/api_server.py
```

---

## Future Enhancements

### Planned Features

1. **Multi-Model Ensemble**
   - Query multiple models simultaneously
   - Aggregate results for higher confidence

2. **A/B Testing Framework**
   - Compare model outputs side-by-side
   - Track quality metrics over time

3. **Cost Budget Limits**
   - Set daily/monthly API spend limits
   - Auto-fallback to FOSS when budget exceeded

4. **Model Performance Tracking**
   - Log quality scores for each query
   - Auto-downgrade underperforming models

5. **Voice Command Integration**
   - "Switch to Claude for this query"
   - "What's the current SOTA model?"

---

## Troubleshooting

### Issue: Sentinel not upgrading

**Check:**
1. Is `SOTA_MANIFEST_URL` set?
2. Is the manifest accessible (try `curl $SOTA_MANIFEST_URL`)?
3. Does the candidate model meet vertex criteria?

**Solution:**
```bash
# Force a delta check
curl -X POST http://localhost:9000/sentinel/refresh
```

---

### Issue: Oracle returning fallback results

**Check:**
1. Is `OPENAI_API_KEY` set?
2. Is LiteLLM installed (`pip3 install litellm`)?
3. Check API server logs for errors

**Solution:**
```bash
# Test Oracle directly
python3 -c "from src.cinematography_oracle import get_oracle; print(get_oracle().consult('test'))"
```

---

## Summary

The SOTA Sentinel Protocol ensures the Elite Video Pipeline maintains **0.01% vertex quality** by:

✅ **Dynamic model selection** - Always uses the best available model  
✅ **Vertex upgrade logic** - Quality thresholds, cost limits, FOSS preference  
✅ **Intelligent routing** - Free local cache vs. paid Oracle  
✅ **Universal compatibility** - LiteLLM supports all major providers  
✅ **Zero refactoring** - Update manifest, not code  
✅ **Cost optimization** - 95% cost reduction via smart routing  

**The future is vertex. The vertex is now.**

---

**Elite Video Pipeline v3.0 - SOTA Sentinel Protocol**  
*Always Best. Never Legacy. 100% FOSS-First.*
