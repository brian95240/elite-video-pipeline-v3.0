"""
Elite Video Pipeline v3.0 - Closed-Loop Test Suite
Validates entire pipeline with zero-error execution
Tests emotional index, orchestration, and cinematography
"""

import sys
import json
import time
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from emotional_index_v3 import EmotionalIndexManager, EMOTIONAL_INDEX
from redis_orchestrator import RedisOrchestrator, ServiceStatus
from cinematography_engine import CinematographyEngine, QualityGateValidator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClosedLoopTestSuite:
    """Comprehensive test suite for Elite Video Pipeline v3.0"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.errors = []
        
        # Initialize components
        self.emotional_manager = EmotionalIndexManager()
        self.cinematography_engine = CinematographyEngine()
        self.quality_validator = QualityGateValidator()
        
        # Try to initialize orchestrator (may fail if Redis unavailable)
        try:
            self.orchestrator = RedisOrchestrator()
            self.redis_available = True
        except Exception as e:
            logger.warning(f"Redis not available (expected in test mode): {e}")
            self.orchestrator = None
            self.redis_available = False
    
    def test_emotional_index_completeness(self) -> bool:
        """Test 1: Verify all 12 archetypes are present"""
        logger.info("\n[TEST 1] Emotional Index Completeness")
        
        try:
            emotions = self.emotional_manager.get_all_emotions()
            
            expected_emotions = {
                # Original (v2.0)
                "curiosity", "fear", "triumph", "tension", "wonder", "urgency", "melancholy",
                # New (v3.0)
                "romance", "joy", "nostalgia", "rage", "serenity"
            }
            
            actual_emotions = set(emotions)
            
            if actual_emotions == expected_emotions:
                logger.info(f"✓ PASS: All 12 archetypes present")
                self.tests_passed += 1
                return True
            else:
                missing = expected_emotions - actual_emotions
                extra = actual_emotions - expected_emotions
                error = f"Emotion mismatch - Missing: {missing}, Extra: {extra}"
                logger.error(f"✗ FAIL: {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
        except Exception as e:
            logger.error(f"✗ FAIL: Exception - {e}")
            self.errors.append(str(e))
            self.tests_failed += 1
            return False
    
    def test_emotional_profile_structure(self) -> bool:
        """Test 2: Verify profile structure for each emotion"""
        logger.info("\n[TEST 2] Emotional Profile Structure")
        
        try:
            required_keys = {"camera", "color", "vfx", "ffmpeg"}
            intensity_levels = {"light", "medium", "heavy"}
            
            for emotion in self.emotional_manager.get_all_emotions():
                profile = EMOTIONAL_INDEX[emotion]
                
                # Check required keys
                if not all(key in profile for key in required_keys):
                    error = f"Missing keys in {emotion}: {required_keys - set(profile.keys())}"
                    logger.error(f"✗ {error}")
                    self.errors.append(error)
                    self.tests_failed += 1
                    return False
                
                # Check intensity levels
                for intensity in intensity_levels:
                    if intensity not in profile["camera"]:
                        error = f"Missing intensity '{intensity}' in {emotion} camera"
                        logger.error(f"✗ {error}")
                        self.errors.append(error)
                        self.tests_failed += 1
                        return False
            
            logger.info(f"✓ PASS: All profiles have correct structure")
            self.tests_passed += 1
            return True
        except Exception as e:
            logger.error(f"✗ FAIL: Exception - {e}")
            self.errors.append(str(e))
            self.tests_failed += 1
            return False
    
    def test_profile_retrieval(self) -> bool:
        """Test 3: Test profile retrieval for each emotion/intensity combo"""
        logger.info("\n[TEST 3] Profile Retrieval")
        
        try:
            test_cases = [
                ("curiosity", "light"),
                ("fear", "medium"),
                ("triumph", "heavy"),
                ("romance", "light"),
                ("joy", "medium"),
                ("serenity", "heavy"),
            ]
            
            for emotion, intensity in test_cases:
                profile = self.emotional_manager.get_emotion_profile(emotion, intensity)
                
                if not profile or "emotion" not in profile:
                    error = f"Failed to retrieve profile for {emotion}/{intensity}"
                    logger.error(f"✗ {error}")
                    self.errors.append(error)
                    self.tests_failed += 1
                    return False
            
            logger.info(f"✓ PASS: All profiles retrieved successfully")
            self.tests_passed += 1
            return True
        except Exception as e:
            logger.error(f"✗ FAIL: Exception - {e}")
            self.errors.append(str(e))
            self.tests_failed += 1
            return False
    
    def test_cinematography_filter_generation(self) -> bool:
        """Test 4: Verify FFmpeg filter chain generation"""
        logger.info("\n[TEST 4] Cinematography Filter Generation")
        
        try:
            test_profile = {
                "emotion": "curiosity",
                "intensity": "medium",
                "camera": {
                    "movement": "slow_zoom_in",
                    "angle": "eye_level",
                    "speed": 0.5
                },
                "color": {
                    "grade": "mystery_teal",
                    "saturation": -10,
                    "contrast": 1.15,
                    "vignette": 0.3
                },
                "vfx": ["light_rays", "dust_particles"]
            }
            
            filter_chain = self.cinematography_engine.generate_filter_chain(test_profile)
            
            if not filter_chain or filter_chain == "null":
                error = "Filter chain generation returned empty result"
                logger.error(f"✗ {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
            
            logger.info(f"✓ PASS: Filter chain generated: {filter_chain[:80]}...")
            self.tests_passed += 1
            return True
        except Exception as e:
            logger.error(f"✗ FAIL: Exception - {e}")
            self.errors.append(str(e))
            self.tests_failed += 1
            return False
    
    def test_profile_validation(self) -> bool:
        """Test 5: Verify profile validation logic"""
        logger.info("\n[TEST 5] Profile Validation")
        
        try:
            # Valid profile
            valid_profile = {
                "camera": {"movement": "zoom"},
                "color": {"saturation": 10},
                "vfx": ["glow"]
            }
            
            is_valid, errors = self.cinematography_engine.validate_profile(valid_profile)
            if not is_valid:
                error = f"Valid profile rejected: {errors}"
                logger.error(f"✗ {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
            
            # Invalid profile (missing keys)
            invalid_profile = {"camera": {"movement": "zoom"}}
            is_valid, errors = self.cinematography_engine.validate_profile(invalid_profile)
            if is_valid:
                error = "Invalid profile accepted"
                logger.error(f"✗ {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
            
            logger.info(f"✓ PASS: Profile validation working correctly")
            self.tests_passed += 1
            return True
        except Exception as e:
            logger.error(f"✗ FAIL: Exception - {e}")
            self.errors.append(str(e))
            self.tests_failed += 1
            return False
    
    def test_intensity_modulation(self) -> bool:
        """Test 6: Verify intensity modulation"""
        logger.info("\n[TEST 6] Intensity Modulation")
        
        try:
            base_profile = {
                "camera": {"speed": 1.0},
                "color": {"saturation": 10, "contrast": 1.2},
                "vfx": []
            }
            
            light_profile = self.cinematography_engine.apply_intensity_modulation(base_profile, "light")
            medium_profile = self.cinematography_engine.apply_intensity_modulation(base_profile, "medium")
            heavy_profile = self.cinematography_engine.apply_intensity_modulation(base_profile, "heavy")
            
            # Verify modulation
            light_speed = light_profile["camera"]["speed"]
            medium_speed = medium_profile["camera"]["speed"]
            heavy_speed = heavy_profile["camera"]["speed"]
            
            if not (light_speed < medium_speed < heavy_speed):
                error = f"Intensity modulation failed: {light_speed} < {medium_speed} < {heavy_speed}"
                logger.error(f"✗ {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
            
            logger.info(f"✓ PASS: Intensity modulation working (light={light_speed}, medium={medium_speed}, heavy={heavy_speed})")
            self.tests_passed += 1
            return True
        except Exception as e:
            logger.error(f"✗ FAIL: Exception - {e}")
            self.errors.append(str(e))
            self.tests_failed += 1
            return False
    
    def test_quality_gate_validation(self) -> bool:
        """Test 7: Verify quality gate validation"""
        logger.info("\n[TEST 7] Quality Gate Validation")
        
        try:
            # Good profile
            good_profile = {
                "color": {
                    "saturation": 20,
                    "contrast": 1.5,
                    "vignette": 0.4
                }
            }
            
            passes, warnings = self.quality_validator.validate_output(good_profile)
            if not passes:
                error = f"Good profile rejected: {warnings}"
                logger.error(f"✗ {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
            
            # Extreme profile
            extreme_profile = {
                "color": {
                    "saturation": 100,
                    "contrast": 3.0,
                    "vignette": 0.9
                }
            }
            
            passes, warnings = self.quality_validator.validate_output(extreme_profile)
            if passes:
                error = "Extreme profile accepted"
                logger.error(f"✗ {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
            
            logger.info(f"✓ PASS: Quality gate validation working correctly")
            self.tests_passed += 1
            return True
        except Exception as e:
            logger.error(f"✗ FAIL: Exception - {e}")
            self.errors.append(str(e))
            self.tests_failed += 1
            return False
    
    def test_redis_orchestrator(self) -> bool:
        """Test 8: Verify Redis orchestrator (if available)"""
        logger.info("\n[TEST 8] Redis Orchestrator")
        
        if not self.redis_available:
            logger.warning("⊘ SKIP: Redis not available")
            return True
        
        try:
            # Health check
            health = self.orchestrator.health_check()
            if not health.get("redis_connected"):
                error = "Redis health check failed"
                logger.error(f"✗ {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
            
            # Submit test job
            job_id = self.orchestrator.submit_job(
                video_id="test_001",
                emotion="curiosity",
                intensity="medium"
            )
            
            if not job_id:
                error = "Job submission failed"
                logger.error(f"✗ {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
            
            # Check job status
            status = self.orchestrator.get_job_status(job_id)
            if not status:
                error = "Job status retrieval failed"
                logger.error(f"✗ {error}")
                self.errors.append(error)
                self.tests_failed += 1
                return False
            
            logger.info(f"✓ PASS: Redis orchestrator working correctly")
            self.tests_passed += 1
            return True
        except Exception as e:
            logger.error(f"✗ FAIL: Exception - {e}")
            self.errors.append(str(e))
            self.tests_failed += 1
            return False
    
    def test_end_to_end_pipeline(self) -> bool:
        """Test 9: End-to-end pipeline simulation"""
        logger.info("\n[TEST 9] End-to-End Pipeline Simulation")
        
        try:
            # Simulate pipeline flow
            emotions = ["curiosity", "fear", "triumph", "romance", "joy"]
            
            for emotion in emotions:
                # Get profile
                profile = self.emotional_manager.get_emotion_profile(emotion, "medium")
                
                # Generate filter chain
                filter_chain = self.cinematography_engine.generate_filter_chain(profile)
                
                # Validate
                is_valid, errors = self.cinematography_engine.validate_profile(profile)
                if not is_valid:
                    error = f"Profile validation failed for {emotion}: {errors}"
                    logger.error(f"✗ {error}")
                    self.errors.append(error)
                    self.tests_failed += 1
                    return False
                
                # Quality gate
                passes, warnings = self.quality_validator.validate_output(profile.get("color", {}))
                if not passes and len(warnings) > 2:
                    error = f"Quality gate failed for {emotion}: {warnings}"
                    logger.error(f"✗ {error}")
                    self.errors.append(error)
                    self.tests_failed += 1
                    return False
            
            logger.info(f"✓ PASS: End-to-end pipeline simulation successful")
            self.tests_passed += 1
            return True
        except Exception as e:
            logger.error(f"✗ FAIL: Exception - {e}")
            self.errors.append(str(e))
            self.tests_failed += 1
            return False
    
    def run_all_tests(self) -> bool:
        """Run complete test suite"""
        logger.info("=" * 80)
        logger.info("ELITE VIDEO PIPELINE v3.0 - CLOSED-LOOP TEST SUITE")
        logger.info("=" * 80)
        
        start_time = time.time()
        
        # Run all tests
        self.test_emotional_index_completeness()
        self.test_emotional_profile_structure()
        self.test_profile_retrieval()
        self.test_cinematography_filter_generation()
        self.test_profile_validation()
        self.test_intensity_modulation()
        self.test_quality_gate_validation()
        self.test_redis_orchestrator()
        self.test_end_to_end_pipeline()
        
        elapsed = time.time() - start_time
        
        # Summary
        logger.info("\n" + "=" * 80)
        logger.info("TEST SUMMARY")
        logger.info("=" * 80)
        logger.info(f"✓ Passed: {self.tests_passed}")
        logger.info(f"✗ Failed: {self.tests_failed}")
        logger.info(f"⏱ Duration: {elapsed:.2f}s")
        
        if self.errors:
            logger.info("\nErrors:")
            for i, error in enumerate(self.errors, 1):
                logger.info(f"  {i}. {error}")
        
        success = self.tests_failed == 0
        status = "✓ ALL TESTS PASSED" if success else "✗ SOME TESTS FAILED"
        logger.info(f"\n{status}")
        logger.info("=" * 80 + "\n")
        
        return success


def main():
    """Run test suite"""
    suite = ClosedLoopTestSuite()
    success = suite.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
