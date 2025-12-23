"""
Elite Video Pipeline v3.0 - Redis Orchestrator
Manages microservices communication and state via Redis
Supports 12 emotional archetypes with distributed processing
"""

import redis
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service lifecycle states"""
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class PipelineJob:
    """Represents a single video processing job"""
    job_id: str
    video_id: str
    emotion: str
    intensity: str
    status: str = ServiceStatus.IDLE.value
    created_at: float = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
        if self.metadata is None:
            self.metadata = {}


class RedisOrchestrator:
    """
    Central orchestrator for Elite Video Pipeline v3.0
    Manages job queues, state, and microservice coordination
    """
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        """Initialize Redis connection"""
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        
        # Test connection
        try:
            self.redis_client.ping()
            logger.info(f"✓ Connected to Redis at {host}:{port}")
        except redis.ConnectionError:
            logger.error(f"✗ Failed to connect to Redis at {host}:{port}")
            raise
        
        # Queue names
        self.queues = {
            "oracle": "pipeline:queue:oracle",
            "trickster": "pipeline:queue:trickster",
            "cartographer": "pipeline:queue:cartographer",
            "spectacle": "pipeline:queue:spectacle",
            "ironist": "pipeline:queue:ironist",
            "dlq": "pipeline:queue:dlq"  # Dead Letter Queue
        }
        
        # State keys
        self.state_prefix = "pipeline:state"
        self.metrics_prefix = "pipeline:metrics"
    
    def submit_job(self, video_id: str, emotion: str, intensity: str = "medium", 
                   metadata: Dict = None) -> str:
        """
        Submit a new video processing job
        
        Args:
            video_id: Unique video identifier
            emotion: Emotion archetype (curiosity, fear, triumph, etc.)
            intensity: 'light', 'medium', or 'heavy'
            metadata: Additional job metadata
            
        Returns:
            job_id: Unique job identifier
        """
        job_id = f"{video_id}_{int(time.time() * 1000)}"
        
        job = PipelineJob(
            job_id=job_id,
            video_id=video_id,
            emotion=emotion,
            intensity=intensity,
            metadata=metadata or {}
        )
        
        # Store job state
        job_key = f"{self.state_prefix}:{job_id}"
        self.redis_client.hset(job_key, mapping=asdict(job))
        self.redis_client.expire(job_key, 86400)  # 24h TTL
        
        # Enqueue to Oracle (first stage)
        self.redis_client.rpush(
            self.queues["oracle"],
            json.dumps(asdict(job))
        )
        
        logger.info(f"✓ Job submitted: {job_id} (emotion={emotion}, intensity={intensity})")
        return job_id
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Retrieve job status and metadata"""
        job_key = f"{self.state_prefix}:{job_id}"
        job_data = self.redis_client.hgetall(job_key)
        return job_data if job_data else None
    
    def update_job_status(self, job_id: str, status: ServiceStatus, 
                         service: str = None, error: str = None):
        """Update job status as it progresses through pipeline"""
        job_key = f"{self.state_prefix}:{job_id}"
        
        update = {
            "status": status.value,
            "updated_at": time.time()
        }
        
        if status == ServiceStatus.PROCESSING and service:
            update["current_service"] = service
            update["started_at"] = time.time()
        elif status == ServiceStatus.COMPLETED:
            update["completed_at"] = time.time()
        elif status == ServiceStatus.FAILED and error:
            update["error"] = error
        
        self.redis_client.hset(job_key, mapping=update)
    
    def enqueue(self, service: str, job_data: Dict) -> bool:
        """
        Enqueue job to a specific service queue
        
        Args:
            service: Service name (oracle, trickster, cartographer, etc.)
            job_data: Job data dictionary
            
        Returns:
            True if successful
        """
        if service not in self.queues:
            logger.error(f"✗ Unknown service: {service}")
            return False
        
        queue_key = self.queues[service]
        self.redis_client.rpush(queue_key, json.dumps(job_data))
        
        logger.info(f"✓ Enqueued to {service}: {job_data.get('job_id', 'unknown')}")
        return True
    
    def dequeue(self, service: str, timeout: int = 0) -> Optional[Dict]:
        """
        Dequeue job from service queue (blocking)
        
        Args:
            service: Service name
            timeout: Blocking timeout in seconds (0 = infinite)
            
        Returns:
            Job data dictionary or None
        """
        if service not in self.queues:
            return None
        
        queue_key = self.queues[service]
        result = self.redis_client.blpop(queue_key, timeout=timeout)
        
        if result:
            _, job_json = result
            return json.loads(job_json)
        
        return None
    
    def move_to_dlq(self, job_id: str, error: str):
        """Move failed job to Dead Letter Queue"""
        job_key = f"{self.state_prefix}:{job_id}"
        job_data = self.redis_client.hgetall(job_key)
        
        if job_data:
            job_data["error"] = error
            job_data["moved_to_dlq_at"] = time.time()
            self.redis_client.rpush(self.queues["dlq"], json.dumps(job_data))
            logger.warning(f"⚠ Moved to DLQ: {job_id} - {error}")
    
    def get_queue_length(self, service: str) -> int:
        """Get current queue length for a service"""
        if service not in self.queues:
            return 0
        return self.redis_client.llen(self.queues[service])
    
    def get_pipeline_metrics(self) -> Dict[str, Any]:
        """Get overall pipeline metrics"""
        metrics = {
            "timestamp": time.time(),
            "queue_lengths": {},
            "total_jobs": 0,
            "failed_jobs": 0
        }
        
        # Queue lengths
        for service, queue_key in self.queues.items():
            length = self.redis_client.llen(queue_key)
            metrics["queue_lengths"][service] = length
        
        # Count jobs by status
        pattern = f"{self.state_prefix}:*"
        for key in self.redis_client.scan_iter(match=pattern):
            job_data = self.redis_client.hgetall(key)
            status = job_data.get("status", "unknown")
            
            if status == ServiceStatus.FAILED.value:
                metrics["failed_jobs"] += 1
            
            metrics["total_jobs"] += 1
        
        return metrics
    
    def health_check(self) -> Dict[str, bool]:
        """Perform health check on pipeline"""
        health = {
            "redis_connected": False,
            "queues_accessible": False,
            "emotional_index_loaded": False
        }
        
        try:
            self.redis_client.ping()
            health["redis_connected"] = True
        except Exception as e:
            logger.error(f"✗ Redis health check failed: {e}")
            return health
        
        try:
            # Check if queues are accessible
            for service, queue_key in self.queues.items():
                self.redis_client.llen(queue_key)
            health["queues_accessible"] = True
        except Exception as e:
            logger.error(f"✗ Queue access failed: {e}")
        
        try:
            # Check if emotional index is seeded
            pattern = "emotional_vertices:*"
            count = sum(1 for _ in self.redis_client.scan_iter(match=pattern))
            health["emotional_index_loaded"] = count >= 24  # 12 emotions × 2+ intensities
        except Exception as e:
            logger.error(f"✗ Emotional index check failed: {e}")
        
        return health
    
    def reset_pipeline(self, confirm: bool = False):
        """
        Reset entire pipeline (clear all queues and state)
        
        Args:
            confirm: Must be True to execute
        """
        if not confirm:
            logger.warning("⚠ Pipeline reset requires confirmation=True")
            return False
        
        try:
            # Clear all queues
            for service, queue_key in self.queues.items():
                self.redis_client.delete(queue_key)
            
            # Clear all job state
            pattern = f"{self.state_prefix}:*"
            for key in self.redis_client.scan_iter(match=pattern):
                self.redis_client.delete(key)
            
            logger.info("✓ Pipeline reset complete")
            return True
        except Exception as e:
            logger.error(f"✗ Pipeline reset failed: {e}")
            return False


def create_orchestrator(host: str = "localhost", port: int = 6379) -> RedisOrchestrator:
    """Factory function to create orchestrator instance"""
    return RedisOrchestrator(host=host, port=port)


if __name__ == "__main__":
    # Test orchestrator
    orchestrator = create_orchestrator()
    
    # Health check
    health = orchestrator.health_check()
    print(f"\n✓ Pipeline Health: {health}")
    
    # Submit test job
    job_id = orchestrator.submit_job(
        video_id="test_001",
        emotion="curiosity",
        intensity="medium",
        metadata={"test": True}
    )
    
    # Check status
    status = orchestrator.get_job_status(job_id)
    print(f"\n✓ Job Status: {status}")
    
    # Get metrics
    metrics = orchestrator.get_pipeline_metrics()
    print(f"\n✓ Pipeline Metrics: {metrics}")
