"""
Elite Video Pipeline v3.0 - Vertex Integration Tests
Comprehensive test suite for vertex-optimized enhancements
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
import json
from unittest.mock import Mock, MagicMock

# Import modules to test
from vertex_cinematography import VertexCinematography, create_vertex_engine
from prompt_parser import PromptParser, create_parser
from emotional_index_v3_vertex import EmotionalIndexManagerVertex
from render_manifest import RenderManifestCompiler, create_compiler


class TestVertexCinematography:
    """Test vertex cinematography calculations"""
    
    def setup_method(self):
        self.engine = create_vertex_engine()
    
    def test_mood_fingerprint_calculation(self):
        """Test mood fingerprint calculation with lighting ratios"""
        specs = self.engine.calculate_mood_fingerprint("melancholy", "heavy")
        
        assert "lighting_ratio" in specs
        assert "color_temp_kelvin" in specs
        assert "iso" in specs
        assert "focal_length_mm" in specs
        assert "aperture" in specs
        
        # Verify heavy intensity increases contrast
        assert specs["iso"] >= 800
        
        print(f"✓ Mood fingerprint: {specs}")
    
    def test_visual_fingerprint_calculation(self):
        """Test visual style fingerprint calculation"""
        specs = self.engine.calculate_visual_fingerprint("future_noir")
        
        assert "lut_profile" in specs
        assert specs["lut_profile"] == "kodak_2383_d65"
        assert "fog_density" in specs
        
        print(f"✓ Visual fingerprint: {specs}")
    
    def test_render_manifest_compilation(self):
        """Test complete render manifest compilation"""
        manifest = self.engine.compile_render_manifest("melancholy", "future_noir", "heavy")
        
        assert manifest["status"] == "compiled"
        assert "render_manifest" in manifest
        assert "camera" in manifest["render_manifest"]
        assert "lighting" in manifest["render_manifest"]
        assert "post_process" in manifest["render_manifest"]
        
        print(f"✓ Render manifest compiled")
    
    def test_ffmpeg_generation_from_manifest(self):
        """Test FFmpeg filter chain generation from manifest"""
        manifest = self.engine.compile_render_manifest("triumph", None, "heavy")
        ffmpeg_chain = self.engine.generate_ffmpeg_from_manifest(manifest)
        
        assert isinstance(ffmpeg_chain, str)
        assert len(ffmpeg_chain) > 0
        
        print(f"✓ FFmpeg chain: {ffmpeg_chain}")
    
    def test_intensity_modulation(self):
        """Test that intensity properly modulates specs"""
        light = self.engine.calculate_mood_fingerprint("fear", "light")
        heavy = self.engine.calculate_mood_fingerprint("fear", "heavy")
        
        # Heavy should have higher ISO and wider aperture
        assert heavy["iso"] > light["iso"]
        
        print(f"✓ Intensity modulation works: Light ISO={light['iso']}, Heavy ISO={heavy['iso']}")


class TestPromptParser:
    """Test prompt parsing and chunking"""
    
    def setup_method(self):
        self.parser = create_parser()
    
    def test_mood_detection(self):
        """Test mood keyword detection"""
        chunks = self.parser.parse("Make this scene feel sad and lonely")
        
        mood_chunks = [c for c in chunks if c.chunk_type == "mood"]
        assert len(mood_chunks) > 0
        assert mood_chunks[0].value == "melancholy"
        
        print(f"✓ Mood detected: {mood_chunks[0].value}")
    
    def test_visual_style_detection(self):
        """Test visual style reference detection"""
        chunks = self.parser.parse("Create a scene like blade runner with cyberpunk aesthetics")
        
        visual_chunks = [c for c in chunks if c.chunk_type == "visual_ref"]
        assert len(visual_chunks) > 0
        assert visual_chunks[0].value == "future_noir"
        
        print(f"✓ Visual style detected: {visual_chunks[0].value}")
    
    def test_intensity_detection(self):
        """Test intensity level detection"""
        chunks = self.parser.parse("Create an intense dramatic scene")
        
        intensity_chunks = [c for c in chunks if c.chunk_type == "intensity"]
        assert len(intensity_chunks) > 0
        assert intensity_chunks[0].value in ["light", "medium", "heavy"]
        
        print(f"✓ Intensity detected: {intensity_chunks[0].value}")
    
    def test_parameter_extraction(self):
        """Test structured parameter extraction from chunks"""
        chunks = self.parser.parse("Make this feel like a funeral in the year 2049")
        params = self.parser.extract_parameters(chunks)
        
        assert "mood" in params
        assert "intensity" in params
        assert "visual_style" in params or params["mood"] is not None
        
        print(f"✓ Parameters extracted: {params}")
    
    def test_cache_key_generation(self):
        """Test Redis cache key generation"""
        chunks = self.parser.parse("Sad blade runner scene")
        cache_key = self.parser.generate_cache_key(chunks)
        
        assert isinstance(cache_key, str)
        assert len(cache_key) > 0
        
        print(f"✓ Cache key: {cache_key}")


class TestEmotionalIndexVertex:
    """Test vertex-enhanced emotional index"""
    
    def setup_method(self):
        self.manager = EmotionalIndexManagerVertex()
    
    def test_all_emotions_loaded(self):
        """Test that all 12 emotions are loaded"""
        emotions = self.manager.get_all_emotions()
        
        assert len(emotions) == 12
        assert "melancholy" in emotions
        assert "triumph" in emotions
        assert "fear" in emotions
        
        print(f"✓ Loaded {len(emotions)} emotions: {emotions}")
    
    def test_complete_profile_retrieval(self):
        """Test complete profile retrieval with all fingerprints"""
        profile = self.manager.get_emotion_profile("melancholy", "heavy")
        
        assert "camera" in profile
        assert "lighting" in profile
        assert "color" in profile
        assert "vfx" in profile
        assert "audio" in profile
        assert "grid" in profile
        
        # Verify lighting specs exist
        assert "ratio" in profile["lighting"]
        assert "kelvin" in profile["lighting"]
        assert "iso" in profile["lighting"]
        assert "aperture" in profile["lighting"]
        
        print(f"✓ Complete profile retrieved with all fingerprints")
    
    def test_lighting_specs_extraction(self):
        """Test lighting specifications extraction"""
        lighting = self.manager.get_lighting_specs("fear", "heavy")
        
        assert "ratio" in lighting
        assert "kelvin" in lighting
        assert "iso" in lighting
        
        print(f"✓ Lighting specs: {lighting}")
    
    def test_audio_specs_extraction(self):
        """Test audio specifications extraction"""
        audio = self.manager.get_audio_specs("triumph", "heavy")
        
        assert "profile" in audio
        assert "reverb" in audio
        assert "mix" in audio
        
        print(f"✓ Audio specs: {audio}")
    
    def test_grid_specs_extraction(self):
        """Test composition grid specifications"""
        grid = self.manager.get_grid_specs("wonder")
        
        assert "composition" in grid
        assert "focus_zone" in grid
        assert "negative_space" in grid
        
        print(f"✓ Grid specs: {grid}")


class TestRenderManifestCompiler:
    """Test render manifest compilation"""
    
    def setup_method(self):
        self.compiler = create_compiler()
    
    def test_manifest_compilation(self):
        """Test complete manifest compilation"""
        manifest = self.compiler.compile("melancholy", "heavy", "future_noir")
        
        assert manifest["status"] == "compiled"
        assert "metadata" in manifest
        assert "render_manifest" in manifest
        assert "vfx_effects" in manifest
        assert "ffmpeg_filter" in manifest
        
        render = manifest["render_manifest"]
        assert "camera" in render
        assert "lighting" in render
        assert "post_process" in render
        assert "audio" in render
        assert "grid" in render
        
        print(f"✓ Manifest compiled successfully")
    
    def test_compile_from_prompt(self):
        """Test manifest compilation from natural language prompt"""
        manifest = self.compiler.compile_from_prompt("Make this scene feel like a funeral in the year 2049")
        
        assert manifest["status"] == "compiled"
        assert "render_manifest" in manifest
        
        print(f"✓ Compiled from prompt: {manifest['metadata']}")
    
    def test_blender_script_export(self):
        """Test Blender Python script export"""
        manifest = self.compiler.compile("triumph", "heavy")
        script_path = "/tmp/test_blender_export.py"
        
        result_path = self.compiler.export_blender_script(manifest, script_path)
        
        assert os.path.exists(result_path)
        
        with open(result_path, 'r') as f:
            content = f.read()
            assert "import bpy" in content
            assert "camera" in content.lower()
            assert "lighting" in content.lower()
        
        print(f"✓ Blender script exported: {result_path}")
    
    def test_visual_style_override(self):
        """Test that visual style properly overrides color settings"""
        manifest_default = self.compiler.compile("curiosity", "medium", None)
        manifest_noir = self.compiler.compile("curiosity", "medium", "future_noir")
        
        lut_default = manifest_default["render_manifest"]["post_process"]["lut"]
        lut_noir = manifest_noir["render_manifest"]["post_process"]["lut"]
        
        assert lut_default != lut_noir
        assert "noir" in lut_noir.lower() or "kodak" in lut_noir.lower()
        
        print(f"✓ Visual style override works: {lut_default} → {lut_noir}")


class TestIntegration:
    """Integration tests for complete workflow"""
    
    def test_end_to_end_prompt_to_manifest(self):
        """Test complete workflow from prompt to render manifest"""
        # Parse prompt
        parser = create_parser()
        chunks = parser.parse("Create an intense horror scene with heavy shadows")
        params = parser.extract_parameters(chunks)
        
        # Compile manifest
        compiler = create_compiler()
        manifest = compiler.compile(
            emotion=params.get("mood", "fear"),
            intensity=params.get("intensity", "heavy"),
            visual_style=params.get("visual_style")
        )
        
        # Verify complete pipeline
        assert manifest["status"] == "compiled"
        assert manifest["metadata"]["emotion"] in ["fear", "tension", "horror"]
        assert manifest["metadata"]["intensity"] == "heavy"
        
        print(f"✓ End-to-end workflow successful")
        print(f"  Detected: {params}")
        print(f"  Compiled: {manifest['metadata']}")
    
    def test_cache_key_consistency(self):
        """Test that same prompts generate same cache keys"""
        parser = create_parser()
        
        chunks1 = parser.parse("sad blade runner scene")
        chunks2 = parser.parse("sad blade runner scene")
        
        key1 = parser.generate_cache_key(chunks1)
        key2 = parser.generate_cache_key(chunks2)
        
        assert key1 == key2
        
        print(f"✓ Cache key consistency verified: {key1}")


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 60)
    print("ELITE VIDEO PIPELINE v3.0 - VERTEX INTEGRATION TESTS")
    print("=" * 60 + "\n")
    
    test_classes = [
        TestVertexCinematography,
        TestPromptParser,
        TestEmotionalIndexVertex,
        TestRenderManifestCompiler,
        TestIntegration
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n--- {test_class.__name__} ---")
        instance = test_class()
        instance.setup_method()
        
        # Get all test methods
        test_methods = [m for m in dir(instance) if m.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(instance, method_name)
                method()
                passed_tests += 1
            except Exception as e:
                failed_tests += 1
                print(f"✗ {method_name} FAILED: {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed_tests}/{total_tests} passed, {failed_tests} failed")
    print("=" * 60 + "\n")
    
    return failed_tests == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
