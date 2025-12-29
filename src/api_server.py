"""
Elite Video Pipeline v3.0 - REST API Server
Flask-based API for cinematography query and render manifest generation
Vertex-optimized with connection pooling and Redis L1 caching
"""

import logging
import json
from flask import Flask, request, jsonify, Response
from typing import Dict, Optional
import redis

from emotional_index_v3_vertex import EmotionalIndexManagerVertex
from vertex_cinematography import VertexCinematography
from render_manifest import RenderManifestCompiler
from prompt_parser import PromptParser
from cinematography_engine import CinematographyEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# === ZERO-POINT INITIALIZATION: Lazy-loaded singletons ===
_redis_client = None
_emotional_manager = None
_vertex_engine = None
_manifest_compiler = None
_prompt_parser = None
_cinematography_engine = None


def get_redis_client():
    """Lazy-load Redis client (singleton)"""
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            _redis_client.ping()
            logger.info("✓ Redis L1 cache connected")
        except Exception as e:
            logger.warning(f"Redis unavailable: {e}")
            _redis_client = None
    return _redis_client


def get_emotional_manager():
    """Lazy-load emotional index manager (singleton)"""
    global _emotional_manager
    if _emotional_manager is None:
        _emotional_manager = EmotionalIndexManagerVertex(get_redis_client())
        logger.info("✓ Emotional Index Manager initialized")
    return _emotional_manager


def get_vertex_engine():
    """Lazy-load vertex cinematography engine (singleton)"""
    global _vertex_engine
    if _vertex_engine is None:
        _vertex_engine = VertexCinematography()
        logger.info("✓ Vertex Cinematography Engine initialized")
    return _vertex_engine


def get_manifest_compiler():
    """Lazy-load render manifest compiler (singleton)"""
    global _manifest_compiler
    if _manifest_compiler is None:
        _manifest_compiler = RenderManifestCompiler(get_redis_client())
        logger.info("✓ Render Manifest Compiler initialized")
    return _manifest_compiler


def get_prompt_parser():
    """Lazy-load prompt parser (singleton)"""
    global _prompt_parser
    if _prompt_parser is None:
        _prompt_parser = PromptParser()
        logger.info("✓ Prompt Parser initialized")
    return _prompt_parser


def get_cinematography_engine():
    """Lazy-load cinematography engine (singleton)"""
    global _cinematography_engine
    if _cinematography_engine is None:
        _cinematography_engine = CinematographyEngine()
        logger.info("✓ Cinematography Engine initialized")
    return _cinematography_engine


# === API ENDPOINTS ===

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    redis_status = "connected" if get_redis_client() else "unavailable"
    
    return jsonify({
        "status": "healthy",
        "service": "Elite Video Pipeline v3.0 API",
        "redis": redis_status,
        "emotional_archetypes": len(get_emotional_manager().get_all_emotions())
    })


@app.route('/query', methods=['POST'])
def query_endpoint():
    """
    Main query endpoint for cinematography generation
    Accepts natural language prompts and returns render manifest
    
    Request body:
    {
        "prompt": "Make this scene feel like a funeral in the year 2049"
    }
    
    Response:
    {
        "status": "compiled",
        "render_manifest": {...},
        "ffmpeg_filter": "..."
    }
    """
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({"error": "Missing 'prompt' field"}), 400
        
        # Parse prompt
        parser = get_prompt_parser()
        chunks = parser.parse(prompt)
        params = parser.extract_parameters(chunks)
        
        # Check Redis cache
        redis_client = get_redis_client()
        cache_key = parser.generate_cache_key(chunks)
        
        if redis_client:
            cached = redis_client.get(f"query:{cache_key}")
            if cached:
                logger.info(f"✓ Cache hit: {cache_key}")
                return Response(cached, mimetype='application/json')
        
        # Compile render manifest
        compiler = get_manifest_compiler()
        manifest = compiler.compile(
            emotion=params.get("mood", "curiosity"),
            intensity=params.get("intensity", "medium"),
            visual_style=params.get("visual_style")
        )
        
        # Cache result (1 hour TTL)
        if redis_client:
            redis_client.setex(f"query:{cache_key}", 3600, json.dumps(manifest))
        
        return jsonify(manifest)
    
    except Exception as e:
        logger.error(f"Query failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/render_manifest', methods=['POST'])
def render_manifest_endpoint():
    """
    Direct render manifest generation from emotion and intensity
    
    Request body:
    {
        "emotion": "melancholy",
        "intensity": "heavy",
        "visual_style": "future_noir"  // optional
    }
    """
    try:
        data = request.json
        emotion = data.get('emotion')
        intensity = data.get('intensity', 'medium')
        visual_style = data.get('visual_style')
        
        if not emotion:
            return jsonify({"error": "Missing 'emotion' field"}), 400
        
        # Validate emotion
        manager = get_emotional_manager()
        if emotion not in manager.get_all_emotions():
            return jsonify({
                "error": f"Invalid emotion. Available: {manager.get_all_emotions()}"
            }), 400
        
        # Compile manifest
        compiler = get_manifest_compiler()
        manifest = compiler.compile(emotion, intensity, visual_style)
        
        return jsonify(manifest)
    
    except Exception as e:
        logger.error(f"Render manifest generation failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/ffmpeg_filter', methods=['POST'])
def ffmpeg_filter_endpoint():
    """
    Generate FFmpeg filter chain from emotion
    
    Request body:
    {
        "emotion": "triumph",
        "intensity": "heavy"
    }
    
    Response:
    {
        "emotion": "triumph",
        "intensity": "heavy",
        "filter_chain": "zoompan=...,eq=..."
    }
    """
    try:
        data = request.json
        emotion = data.get('emotion')
        intensity = data.get('intensity', 'medium')
        
        if not emotion:
            return jsonify({"error": "Missing 'emotion' field"}), 400
        
        # Get profile
        manager = get_emotional_manager()
        profile = manager.get_emotion_profile(emotion, intensity)
        
        # Generate filter chain
        engine = get_cinematography_engine()
        filter_chain = engine.generate_filter_chain(profile)
        
        return jsonify({
            "emotion": emotion,
            "intensity": intensity,
            "filter_chain": filter_chain,
            "ffmpeg_preset": profile.get("ffmpeg", "")
        })
    
    except Exception as e:
        logger.error(f"FFmpeg filter generation failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/emotions', methods=['GET'])
def list_emotions():
    """List all available emotional archetypes"""
    manager = get_emotional_manager()
    emotions = manager.get_all_emotions()
    
    return jsonify({
        "total": len(emotions),
        "emotions": emotions,
        "intensities": ["light", "medium", "heavy"]
    })


@app.route('/emotion/<emotion>', methods=['GET'])
def get_emotion_details(emotion: str):
    """Get complete details for a specific emotion"""
    manager = get_emotional_manager()
    
    if emotion not in manager.get_all_emotions():
        return jsonify({"error": f"Emotion '{emotion}' not found"}), 404
    
    # Get all intensity levels
    profiles = {
        "light": manager.get_emotion_profile(emotion, "light"),
        "medium": manager.get_emotion_profile(emotion, "medium"),
        "heavy": manager.get_emotion_profile(emotion, "heavy")
    }
    
    return jsonify({
        "emotion": emotion,
        "profiles": profiles
    })


@app.route('/parse_prompt', methods=['POST'])
def parse_prompt_endpoint():
    """
    Parse natural language prompt into structured parameters
    
    Request body:
    {
        "prompt": "Create a sad scene like blade runner"
    }
    
    Response:
    {
        "chunks": [...],
        "parameters": {...}
    }
    """
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({"error": "Missing 'prompt' field"}), 400
        
        parser = get_prompt_parser()
        chunks = parser.parse(prompt)
        params = parser.extract_parameters(chunks)
        
        return jsonify({
            "prompt": prompt,
            "chunks": [{"type": c.chunk_type, "value": c.value, "confidence": c.confidence} for c in chunks],
            "parameters": params,
            "cache_key": parser.generate_cache_key(chunks)
        })
    
    except Exception as e:
        logger.error(f"Prompt parsing failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/lighting_specs/<emotion>', methods=['GET'])
def get_lighting_specs(emotion: str):
    """Get lighting specifications for an emotion"""
    manager = get_emotional_manager()
    
    if emotion not in manager.get_all_emotions():
        return jsonify({"error": f"Emotion '{emotion}' not found"}), 404
    
    intensity = request.args.get('intensity', 'medium')
    specs = manager.get_lighting_specs(emotion, intensity)
    
    return jsonify({
        "emotion": emotion,
        "intensity": intensity,
        "lighting": specs
    })


@app.route('/audio_specs/<emotion>', methods=['GET'])
def get_audio_specs(emotion: str):
    """Get audio specifications for an emotion"""
    manager = get_emotional_manager()
    
    if emotion not in manager.get_all_emotions():
        return jsonify({"error": f"Emotion '{emotion}' not found"}), 404
    
    intensity = request.args.get('intensity', 'medium')
    specs = manager.get_audio_specs(emotion, intensity)
    
    return jsonify({
        "emotion": emotion,
        "intensity": intensity,
        "audio": specs
    })


@app.route('/export/blender', methods=['POST'])
def export_blender_script():
    """
    Export Blender Python script from emotion
    
    Request body:
    {
        "emotion": "melancholy",
        "intensity": "heavy",
        "visual_style": "future_noir"
    }
    
    Response: Blender Python script as text
    """
    try:
        data = request.json
        emotion = data.get('emotion')
        intensity = data.get('intensity', 'medium')
        visual_style = data.get('visual_style')
        
        if not emotion:
            return jsonify({"error": "Missing 'emotion' field"}), 400
        
        # Compile manifest
        compiler = get_manifest_compiler()
        manifest = compiler.compile(emotion, intensity, visual_style)
        
        # Export Blender script
        script_path = f"/tmp/blender_{emotion}_{intensity}.py"
        compiler.export_blender_script(manifest, script_path)
        
        # Read and return script
        with open(script_path, 'r') as f:
            script_content = f.read()
        
        return Response(script_content, mimetype='text/x-python')
    
    except Exception as e:
        logger.error(f"Blender export failed: {e}")
        return jsonify({"error": str(e)}), 500


# === ERROR HANDLERS ===

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# === STARTUP ===

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("Elite Video Pipeline v3.0 - API Server")
    logger.info("Vertex-Optimized with Connection Pooling & Redis L1 Cache")
    logger.info("=" * 60)
    
    # Warm up singletons
    get_emotional_manager()
    get_vertex_engine()
    get_manifest_compiler()
    get_prompt_parser()
    get_cinematography_engine()
    
    logger.info("\n✓ All systems initialized")
    logger.info("✓ Starting API server on http://0.0.0.0:9000\n")
    
    app.run(host='0.0.0.0', port=9000, debug=False, threaded=True)
