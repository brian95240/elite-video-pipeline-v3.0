"""
Elite Video Pipeline v3.0 - Main Pipeline Orchestrator
Coordinates all microservices and manages complete video processing workflow
"""

import logging
import json
import time
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum

from emotional_index_v3 import EmotionalIndexManager
from redis_orchestrator import RedisOrchestrator, ServiceStatus
from cinematography_engine import CinematographyEngine, QualityGateValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArchetypeRole(Enum):
    """10-Archetype Firewall Roles"""
    ORACLE = "oracle"  # Script generation + emotional arc
    TRICKSTER = "trickster"  # Voice synthesis
    CARTOGRAPHER = "cartographer"  # Retention mapping + cinematography
    SPECTACLE = "spectacle"  # Thumbnail + VFX rendering
    IRONIST = "ironist"  # Quality gates + cinematography validation
    ALCHEMIST = "alchemist"  # Budget tracking + spot pricing
    SHADOW = "shadow"  # Legal compliance
    CATALYST = "catalyst"  # Launch orchestration
    SAGE = "sage"  # Analytics + insights
    GUARDIAN = "guardian"  # Security + monitoring


@dataclass
class PipelineConfig:
    """Pipeline configuration"""
    redis_host: str = "localhost"
    redis_port: int = 6379
    max_retries: int = 3
    timeout_seconds: int = 300
    enable_quality_gates: bool = True
    enable_spot_pricing: bool = True


class PipelineOrchestrator:
    """
    Main orchestrator for Elite Video Pipeline v3.0
    Manages complete workflow from submission to delivery
    """
    
    def __init__(self, config: PipelineConfig = None):
        self.config = config or PipelineConfig()
        
        # Initialize components
        self.emotional_manager = EmotionalIndexManager()
        self.cinematography_engine = CinematographyEngine()
        self.quality_validator = QualityGateValidator()
        
        # Initialize orchestrator (may fail if Redis unavailable)
        try:
            self.orchestrator = RedisOrchestrator(
                host=self.config.redis_host,
                port=self.config.redis_port
            )
            self.redis_available = True
        except Exception as e:
            logger.warning(f"Redis unavailable: {e}")
            self.orchestrator = None
            self.redis_available = False
        
        # Statistics
        self.stats = {
            "jobs_submitted": 0,
            "jobs_completed": 0,
            "jobs_failed": 0,
            "total_processing_time": 0.0
        }
    
    def submit_video_job(self, video_id: str, emotion: str, intensity: str = "medium",
                        metadata: Dict = None) -> Optional[str]:
        """
        Submit a video for processing through the pipeline
        
        Args:
            video_id: Unique video identifier
            emotion: Emotion archetype
            intensity: 'light', 'medium', or 'heavy'
            metadata: Additional metadata
            
        Returns:
            job_id if successful, None otherwise
        """
        try:
            # Validate emotion
            if emotion not in self.emotional_manager.get_all_emotions():
                logger.error(f"Invalid emotion: {emotion}")
                return None
            
            # Validate intensity
            if intensity not in ["light", "medium", "heavy"]:
                logger.error(f"Invalid intensity: {intensity}")
                return None
            
            # Get emotional profile
            profile = self.emotional_manager.get_emotion_profile(emotion, intensity)
            
            # Validate profile
            is_valid, errors = self.cinematography_engine.validate_profile(profile)
            if not is_valid:
                logger.error(f"Profile validation failed: {errors}")
                return None
            
            # Submit to orchestrator if available
            if self.redis_available:
                job_id = self.orchestrator.submit_job(
                    video_id=video_id,
                    emotion=emotion,
                    intensity=intensity,
                    metadata=metadata
                )
            else:
                # Fallback: generate job_id locally
                job_id = f"{video_id}_{int(time.time() * 1000)}"
                logger.info(f"✓ Job created (local): {job_id}")
            
            self.stats["jobs_submitted"] += 1
            return job_id
        
        except Exception as e:
            logger.error(f"Job submission failed: {e}")
            return None
    
    def process_job(self, job_id: str) -> bool:
        """
        Process a single job through the pipeline
        
        Args:
            job_id: Job identifier
            
        Returns:
            True if successful
        """
        try:
            start_time = time.time()
            
            if not self.redis_available:
                logger.warning("Redis unavailable - cannot process job")
                return False
            
            # Get job status
            job_status = self.orchestrator.get_job_status(job_id)
            if not job_status:
                logger.error(f"Job not found: {job_id}")
                return False
            
            emotion = job_status.get("emotion")
            intensity = job_status.get("intensity")
            
            # Stage 1: Oracle (Script generation)
            logger.info(f"[{job_id}] Stage 1: Oracle (Script generation)")
            self.orchestrator.update_job_status(job_id, ServiceStatus.PROCESSING, "oracle")
            
            # Stage 2: Trickster (Voice synthesis)
            logger.info(f"[{job_id}] Stage 2: Trickster (Voice synthesis)")
            self.orchestrator.update_job_status(job_id, ServiceStatus.PROCESSING, "trickster")
            
            # Stage 3: Cartographer (Cinematography)
            logger.info(f"[{job_id}] Stage 3: Cartographer (Cinematography)")
            self.orchestrator.update_job_status(job_id, ServiceStatus.PROCESSING, "cartographer")
            
            profile = self.emotional_manager.get_emotion_profile(emotion, intensity)
            filter_chain = self.cinematography_engine.generate_filter_chain(profile)
            
            logger.info(f"[{job_id}] Generated filter chain: {filter_chain[:60]}...")
            
            # Stage 4: Spectacle (Rendering)
            logger.info(f"[{job_id}] Stage 4: Spectacle (Rendering)")
            self.orchestrator.update_job_status(job_id, ServiceStatus.PROCESSING, "spectacle")
            
            # Stage 5: Ironist (Quality validation)
            logger.info(f"[{job_id}] Stage 5: Ironist (Quality validation)")
            self.orchestrator.update_job_status(job_id, ServiceStatus.PROCESSING, "ironist")
            
            if self.config.enable_quality_gates:
                passes, warnings = self.quality_validator.validate_output(profile.get("color", {}))
                if not passes:
                    logger.warning(f"[{job_id}] Quality warnings: {warnings}")
            
            # Stage 6: Alchemist (Budget tracking)
            logger.info(f"[{job_id}] Stage 6: Alchemist (Budget tracking)")
            
            # Stage 7: Shadow (Legal compliance)
            logger.info(f"[{job_id}] Stage 7: Shadow (Legal compliance)")
            
            # Stage 8: Catalyst (Launch)
            logger.info(f"[{job_id}] Stage 8: Catalyst (Launch)")
            
            # Mark as completed
            elapsed = time.time() - start_time
            self.orchestrator.update_job_status(job_id, ServiceStatus.COMPLETED)
            
            self.stats["jobs_completed"] += 1
            self.stats["total_processing_time"] += elapsed
            
            logger.info(f"✓ Job completed: {job_id} ({elapsed:.2f}s)")
            return True
        
        except Exception as e:
            logger.error(f"Job processing failed: {e}")
            self.stats["jobs_failed"] += 1
            if self.redis_available:
                self.orchestrator.move_to_dlq(job_id, str(e))
            return False
    
    def batch_process(self, jobs: List[Dict]) -> Dict:
        """
        Process multiple jobs in batch
        
        Args:
            jobs: List of job specifications
            
        Returns:
            Results dictionary
        """
        results = {
            "total": len(jobs),
            "successful": 0,
            "failed": 0,
            "job_ids": []
        }
        
        for job_spec in jobs:
            video_id = job_spec.get("video_id")
            emotion = job_spec.get("emotion", "curiosity")
            intensity = job_spec.get("intensity", "medium")
            
            job_id = self.submit_video_job(video_id, emotion, intensity)
            if job_id:
                results["job_ids"].append(job_id)
                if self.process_job(job_id):
                    results["successful"] += 1
                else:
                    results["failed"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    def get_pipeline_status(self) -> Dict:
        """Get overall pipeline status"""
        status = {
            "redis_available": self.redis_available,
            "emotional_archetypes": len(self.emotional_manager.get_all_emotions()),
            "filter_templates": self.cinematography_engine.get_filter_statistics(),
            "statistics": self.stats
        }
        
        if self.redis_available:
            status["metrics"] = self.orchestrator.get_pipeline_metrics()
            status["health"] = self.orchestrator.health_check()
        
        return status
    
    def validate_pipeline(self) -> tuple[bool, List[str]]:
        """
        Validate entire pipeline configuration
        
        Returns:
            (is_valid, list of issues)
        """
        issues = []
        
        # Check emotional index
        emotions = self.emotional_manager.get_all_emotions()
        if len(emotions) != 12:
            issues.append(f"Expected 12 emotions, found {len(emotions)}")
        
        # Check cinematography engine
        stats = self.cinematography_engine.get_filter_statistics()
        if stats["total_templates"] == 0:
            issues.append("No filter templates available")
        
        # Check Redis (optional)
        if not self.redis_available:
            issues.append("Redis unavailable (optional, local mode available)")
        else:
            health = self.orchestrator.health_check()
            if not health.get("redis_connected"):
                issues.append("Redis connection failed")
            if not health.get("queues_accessible"):
                issues.append("Redis queues not accessible")
        
        return len(issues) == 0, issues


def create_orchestrator(config: PipelineConfig = None) -> PipelineOrchestrator:
    """Factory function to create orchestrator"""
    return PipelineOrchestrator(config)


if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = create_orchestrator()
    
    # Validate pipeline
    is_valid, issues = orchestrator.validate_pipeline()
    print(f"\n✓ Pipeline valid: {is_valid}")
    if issues:
        print(f"  Issues: {issues}")
    
    # Get status
    status = orchestrator.get_pipeline_status()
    print(f"\n✓ Pipeline status:")
    print(f"  Emotions: {status['emotional_archetypes']}")
    print(f"  Filter templates: {status['filter_templates']['total_templates']}")
    print(f"  Redis available: {status['redis_available']}")
