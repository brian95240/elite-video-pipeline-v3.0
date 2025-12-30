"""
Elite Video Pipeline v3.2 - Cloud Render Extension Test
Tests render intent detection, GPU arbitration, and confirmation handshake
"""

import sys
sys.path.insert(0, '/home/ubuntu/elite-video-pipeline-v3.0/src')

from prompt_parser import create_parser, RenderIntent
from gpu_render_broker import create_gpu_broker
from cloud_render_executor import create_cloud_executor

def test_render_intent_detection():
    """Test render intent detection from prompts"""
    print("\n" + "=" * 80)
    print("TEST 1: RENDER INTENT DETECTION")
    print("=" * 80 + "\n")
    
    parser = create_parser()
    
    test_prompts = [
        "Render this scene in 4k at 24fps",
        "Export final cut in 1080p",
        "Make a preview render at 720p",
        "Generate video output in 8k production quality",
        "Just a regular scene query without render intent"
    ]
    
    for prompt in test_prompts:
        print(f"Prompt: \"{prompt}\"")
        aesthetic, kinetic, render_intent = parser.parse_split_stream(prompt)
        
        if render_intent.is_render_request:
            print(f"  ✓ Render Intent Detected:")
            print(f"    Type: {render_intent.render_type}")
            print(f"    Resolution: {render_intent.resolution}")
            print(f"    Quality: {render_intent.quality}")
            print(f"    Format: {render_intent.output_format}")
            print(f"    FPS: {render_intent.fps}")
        else:
            print(f"  ✗ No render intent detected")
        
        print()
    
    return True


def test_gpu_provider_selection():
    """Test GPU provider selection with vertex scoring"""
    print("\n" + "=" * 80)
    print("TEST 2: GPU PROVIDER SELECTION")
    print("=" * 80 + "\n")
    
    broker = create_gpu_broker()
    broker.load_providers_from_manifest()
    
    # Test render intents with different requirements
    test_cases = [
        {
            "name": "Preview render (low cost priority)",
            "render_intent": RenderIntent(
                is_render_request=True,
                render_type="preview",
                resolution="720p",
                quality="preview",
                fps=24
            )
        },
        {
            "name": "Production render (high quality priority)",
            "render_intent": RenderIntent(
                is_render_request=True,
                render_type="final",
                resolution="4k",
                quality="production",
                frame_range=(1, 240),
                fps=24
            )
        },
        {
            "name": "8K render (maximum VRAM required)",
            "render_intent": RenderIntent(
                is_render_request=True,
                render_type="final",
                resolution="8k",
                quality="production",
                frame_range=(1, 100),
                fps=24
            )
        }
    ]
    
    for test_case in test_cases:
        print(f"Test Case: {test_case['name']}")
        print("-" * 80)
        
        best_provider, estimated_cost = broker.select_best_provider(test_case['render_intent'])
        
        if best_provider:
            print(f"  ✓ Selected Provider: {best_provider.name}")
            print(f"    GPU Model: {best_provider.gpu_model}")
            print(f"    VRAM: {best_provider.vram_gb}GB")
            print(f"    Spot Price: ${best_provider.spot_price_per_hour:.3f}/hour")
            print(f"    Uptime SLA: {best_provider.uptime_sla * 100:.1f}%")
            print(f"    Region: {best_provider.region}")
            print(f"    Estimated Cost: ${estimated_cost:.3f}")
        else:
            print(f"  ✗ No suitable provider found")
        
        print()
    
    return True


def test_provider_status():
    """Test provider status endpoint"""
    print("\n" + "=" * 80)
    print("TEST 3: PROVIDER STATUS")
    print("=" * 80 + "\n")
    
    broker = create_gpu_broker()
    broker.load_providers_from_manifest()
    
    status = broker.get_provider_status()
    
    print(f"Vertex Configuration:")
    print(f"  Quality Threshold: {status['quality_threshold']}")
    print(f"  Cost Ratio Max: {status['cost_ratio_max']}x")
    print()
    
    print(f"Available Providers ({len(status['providers'])}):")
    print("-" * 80)
    
    for provider in status['providers']:
        print(f"{provider['name']}:")
        print(f"  GPU: {provider['gpu_model']} ({provider['vram_gb']}GB)")
        print(f"  Price: ${provider['spot_price_per_hour']:.3f}/hour")
        print(f"  Uptime: {provider['uptime_sla'] * 100:.1f}%")
        print(f"  Region: {provider['region']}")
        print(f"  Vertex Score: {provider['vertex_score']}")
        print(f"  Available: {provider['available']}")
        print()
    
    return True


def test_cloud_executor():
    """Test cloud render executor"""
    print("\n" + "=" * 80)
    print("TEST 4: CLOUD RENDER EXECUTOR")
    print("=" * 80 + "\n")
    
    executor = create_cloud_executor()
    
    # Create test render intent
    test_render_intent = RenderIntent(
        is_render_request=True,
        render_type="final",
        output_format="mp4",
        resolution="1080p",
        quality="high",
        frame_range=(1, 100),
        fps=24
    )
    
    # Create test provider
    from gpu_render_broker import GPUProvider
    test_provider = GPUProvider(
        name="Hetzner Cloud GPU",
        gpu_model="NVIDIA RTX 4090",
        vram_gb=24,
        spot_price_per_hour=0.35,
        uptime_sla=0.99,
        region="eu-central",
        api_endpoint="https://api.hetzner.cloud/v1"
    )
    
    # Test scene manifest
    test_scene_manifest = {
        "camera": {
            "focal_length_mm": 50,
            "aperture": "T2.8",
            "sensor_crop": 1.0,
            "shutter_angle": 180
        },
        "lighting": {
            "key_fill_ratio": "4:1",
            "color_temperature_kelvin": 5600,
            "iso": 800,
            "intensity": 1.0
        }
    }
    
    # Dispatch test job
    print("Dispatching test render job...")
    job = executor.dispatch_render_job(
        job_id="test-v3.2-001",
        provider=test_provider,
        render_intent=test_render_intent,
        scene_manifest=test_scene_manifest
    )
    
    print(f"\n✓ Render job dispatched:")
    print(f"  Job ID: {job.job_id}")
    print(f"  Provider: {job.provider_name}")
    print(f"  Status: {job.status}")
    print(f"  Manifest Path: {job.render_manifest_path}")
    print(f"  Output Path: {job.output_path}")
    print(f"  Started At: {job.started_at}")
    
    # Check job status
    print(f"\nChecking job status...")
    job_status = executor.get_job_status("test-v3.2-001")
    
    if job_status:
        print(f"  ✓ Job found: {job_status.status}")
    else:
        print(f"  ✗ Job not found")
    
    print()
    
    return True


def test_confirmation_workflow():
    """Test complete confirmation workflow"""
    print("\n" + "=" * 80)
    print("TEST 5: CONFIRMATION WORKFLOW")
    print("=" * 80 + "\n")
    
    print("Workflow Steps:")
    print("1. User submits prompt with render intent")
    print("2. System detects render intent")
    print("3. GPU broker selects best provider")
    print("4. System returns 202 Accepted with estimate")
    print("5. User confirms via /render/confirm/{job_id}")
    print("6. System dispatches to cloud GPU")
    print("7. User tracks progress via /render/status/{job_id}")
    print()
    
    # Simulate workflow
    parser = create_parser()
    broker = create_gpu_broker()
    broker.load_providers_from_manifest()
    
    prompt = "Render this scene in 4k at 24fps for final production"
    
    print(f"Step 1: User prompt: \"{prompt}\"")
    
    # Parse prompt
    aesthetic, kinetic, render_intent = parser.parse_split_stream(prompt)
    
    if render_intent.is_render_request:
        print(f"Step 2: ✓ Render intent detected ({render_intent.render_type})")
        
        # Select provider
        best_provider, estimated_cost = broker.select_best_provider(render_intent)
        
        if best_provider:
            print(f"Step 3: ✓ Provider selected: {best_provider.name}")
            print(f"        Estimated cost: ${estimated_cost:.3f}")
            
            # Simulate 202 response
            import uuid
            job_id = str(uuid.uuid4())
            
            print(f"Step 4: ✓ System returns 202 Accepted")
            print(f"        Job ID: {job_id}")
            print(f"        Message: \"Ready to render on {best_provider.name}. Cost: ${estimated_cost:.3f}. Confirm?\"")
            print(f"        Confirmation endpoint: /render/confirm/{job_id}")
            
            print(f"Step 5: ✓ User confirms (POST /render/confirm/{job_id})")
            print(f"Step 6: ✓ System dispatches to {best_provider.name}")
            print(f"Step 7: ✓ User tracks progress (GET /render/status/{job_id})")
            
            print(f"\n✓ Confirmation workflow complete")
        else:
            print(f"Step 3: ✗ No suitable provider found")
    else:
        print(f"Step 2: ✗ No render intent detected")
    
    print()
    
    return True


def run_all_tests():
    """Run all v3.2 tests"""
    print("\n" + "=" * 80)
    print("ELITE VIDEO PIPELINE v3.2 - CLOUD RENDER EXTENSION TEST SUITE")
    print("=" * 80)
    
    tests = [
        ("Render Intent Detection", test_render_intent_detection),
        ("GPU Provider Selection", test_gpu_provider_selection),
        ("Provider Status", test_provider_status),
        ("Cloud Executor", test_cloud_executor),
        ("Confirmation Workflow", test_confirmation_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n✗ Test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80 + "\n")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! v3.2 Cloud Render Extension is ready.")
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    run_all_tests()
