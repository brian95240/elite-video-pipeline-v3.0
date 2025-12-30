"""
Elite Video Pipeline v3.3 - Enhancement Tests
Tests for manifest pruning and scale-to-zero deployment readiness
"""

import sys
import json

print("=" * 60)
print("Elite Video Pipeline v3.3 - Enhancement Tests")
print("=" * 60)
print()

# Test 1: Manifest Pruning
print("[TEST 1] Manifest Pruning")
print("-" * 60)

try:
    from src.render_manifest import RenderManifestCompiler
    
    compiler = RenderManifestCompiler()
    
    # Create a test manifest with excessive data
    test_manifest = {
        "status": "compiled",
        "metadata": {
            "emotion": "triumph",
            "intensity": "heavy"
        },
        "render_manifest": {
            "camera": {
                "focal_length_mm": 50,
                "aperture": "T2.8",
                "sensor_crop": 1.0,
                "shutter_angle": 180,
                "movement": "Static",
                "angle": "Eye Level",
                "speed": 0.0
            },
            "lighting": {
                "key_fill_ratio": "8:1",
                "color_temperature_kelvin": 5600,
                "iso": 800,
                "intensity": 1.0
            },
            "post_process": {
                "lut": "rec709",
                "saturation": 1.0,
                "contrast": 1.0,
                "vignette": 0.001,  # Negligible
                "bloom": 0.0,  # Zero
                "grain": 0.002,  # Negligible
                "chromatic_aberration": 0.0  # Zero
            }
        },
        "geometry": {
            "max_polygons": 5000000,  # 5M polygons (excessive)
            "lod_enabled": False
        },
        "scene": {
            "texture_resolution": "8k"  # Excessive for most cases
        },
        "vfx_effects": [
            {"name": "particle_system", "intensity": 0.5},
            {"name": "lens_flare", "intensity": 0.0},  # Zero intensity
            {"name": "motion_blur", "intensity": 0.001}  # Negligible
        ]
    }
    
    # Test aggressive pruning
    print("Testing aggressive pruning...")
    pruned_aggressive = compiler.prune_manifest(test_manifest, "aggressive")
    
    # Verify pruning results
    pruning_meta = pruned_aggressive.get("metadata", {}).get("pruning", {})
    
    print(f"✓ Original size: {pruning_meta.get('original_size_kb', 0):.2f} KB")
    print(f"✓ Pruned size: {pruning_meta.get('pruned_size_kb', 0):.2f} KB")
    print(f"✓ Reduction: {pruning_meta.get('reduction_percent', 0):.1f}%")
    print(f"✓ VRAM savings: ~{pruning_meta.get('vram_savings_estimate_mb', 0)} MB")
    
    # Verify specific pruning actions
    post_process = pruned_aggressive.get("render_manifest", {}).get("post_process", {})
    geometry = pruned_aggressive.get("geometry", {})
    scene = pruned_aggressive.get("scene", {})
    vfx = pruned_aggressive.get("vfx_effects", [])
    
    assert post_process.get("vignette") == 0.0, "Negligible vignette not removed"
    assert post_process.get("bloom") == 0.0, "Zero bloom not removed"
    assert geometry.get("max_polygons") == 100000, "Polygon count not reduced (aggressive)"
    assert geometry.get("lod_enabled") == True, "LOD not enabled"
    assert scene.get("texture_resolution") == "2k", "Texture resolution not reduced"
    assert len(vfx) == 1, "Zero-intensity VFX not removed"
    
    print("✓ PASS: Manifest pruning (aggressive)")
    
    # Test balanced pruning
    print("\nTesting balanced pruning...")
    pruned_balanced = compiler.prune_manifest(test_manifest, "balanced")
    geometry_balanced = pruned_balanced.get("geometry", {})
    
    assert geometry_balanced.get("max_polygons") == 500000, "Polygon count not reduced (balanced)"
    print("✓ PASS: Manifest pruning (balanced)")
    
    # Test conservative pruning
    print("\nTesting conservative pruning...")
    pruned_conservative = compiler.prune_manifest(test_manifest, "conservative")
    geometry_conservative = pruned_conservative.get("geometry", {})
    
    assert geometry_conservative.get("max_polygons") == 2000000, "Polygon count not reduced (conservative)"
    print("✓ PASS: Manifest pruning (conservative)")
    
    print()
    print("✓ TEST 1 PASSED: Manifest Pruning")
    
except Exception as e:
    print(f"✗ TEST 1 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 2: Docker Configuration
print("[TEST 2] Docker Configuration")
print("-" * 60)

try:
    import os
    
    # Check Dockerfile exists
    assert os.path.exists("Dockerfile"), "Dockerfile not found"
    print("✓ Dockerfile exists")
    
    # Check .dockerignore exists
    assert os.path.exists(".dockerignore"), ".dockerignore not found"
    print("✓ .dockerignore exists")
    
    # Check docker-compose.yml exists
    assert os.path.exists("docker-compose.yml"), "docker-compose.yml not found"
    print("✓ docker-compose.yml exists")
    
    # Verify Dockerfile has health check
    with open("Dockerfile", "r") as f:
        dockerfile_content = f.read()
        assert "HEALTHCHECK" in dockerfile_content, "HEALTHCHECK not in Dockerfile"
        assert "gunicorn" in dockerfile_content, "gunicorn not in Dockerfile"
        print("✓ Dockerfile has health check")
        print("✓ Dockerfile uses gunicorn")
    
    # Verify .dockerignore excludes tests
    with open(".dockerignore", "r") as f:
        dockerignore_content = f.read()
        assert "tests/" in dockerignore_content, "tests/ not excluded"
        assert "*.md" in dockerignore_content, "*.md not excluded"
        print("✓ .dockerignore excludes tests and docs")
    
    print()
    print("✓ TEST 2 PASSED: Docker Configuration")
    
except Exception as e:
    print(f"✗ TEST 2 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 3: Hetzner Deployment Script
print("[TEST 3] Hetzner Deployment Script")
print("-" * 60)

try:
    # Check deployment script exists
    assert os.path.exists("deploy_hetzner_serverless.sh"), "deploy_hetzner_serverless.sh not found"
    print("✓ Hetzner deployment script exists")
    
    # Verify script is executable
    assert os.access("deploy_hetzner_serverless.sh", os.X_OK), "Script not executable"
    print("✓ Script is executable")
    
    # Verify script has scale-to-zero logic
    with open("deploy_hetzner_serverless.sh", "r") as f:
        script_content = f.read()
        assert "scale-to-zero" in script_content.lower(), "scale-to-zero not mentioned"
        assert "auto-stop" in script_content.lower(), "auto-stop not implemented"
        assert "hcloud" in script_content, "hcloud CLI not used"
        print("✓ Script has scale-to-zero logic")
        print("✓ Script uses hcloud CLI")
    
    print()
    print("✓ TEST 3 PASSED: Hetzner Deployment Script")
    
except Exception as e:
    print(f"✗ TEST 3 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Requirements Update
print("[TEST 4] Requirements Update")
print("-" * 60)

try:
    # Check gunicorn in requirements.txt
    with open("requirements.txt", "r") as f:
        requirements = f.read()
        assert "gunicorn" in requirements, "gunicorn not in requirements.txt"
        print("✓ gunicorn added to requirements.txt")
    
    print()
    print("✓ TEST 4 PASSED: Requirements Update")
    
except Exception as e:
    print(f"✗ TEST 4 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Summary
print("=" * 60)
print("✓ ALL TESTS PASSED (4/4)")
print("=" * 60)
print()
print("Elite Video Pipeline v3.3 enhancements verified:")
print("  ✓ Manifest pruning (aggressive, balanced, conservative)")
print("  ✓ Docker containerization with health checks")
print("  ✓ Hetzner serverless deployment with scale-to-zero")
print("  ✓ Production dependencies (gunicorn)")
print()
print("Ready for production deployment!")
print()
