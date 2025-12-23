"""
Elite Video Pipeline v3.0 - Neon Database Adapter
PostgreSQL adapter for pipeline state management using Neon serverless database
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor, Json
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    logger.warning("psycopg2 not available - install with: pip install psycopg2-binary")


class NeonDatabaseAdapter:
    """
    Adapter for Neon PostgreSQL database
    Provides persistent storage for pipeline state, metrics, and configuration
    """
    
    def __init__(self, connection_string: str = None):
        """
        Initialize Neon database connection
        
        Args:
            connection_string: PostgreSQL connection string
                             If not provided, reads from NEON_DATABASE_URL env var
        """
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2 is required. Install with: pip install psycopg2-binary")
        
        self.connection_string = connection_string or os.getenv('NEON_DATABASE_URL')
        
        if not self.connection_string:
            raise ValueError("Connection string required. Set NEON_DATABASE_URL or pass connection_string")
        
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.connection_string)
            logger.info("✓ Connected to Neon database")
        except Exception as e:
            logger.error(f"✗ Failed to connect to Neon: {e}")
            raise
    
    def _execute(self, query: str, params: tuple = None, fetch: bool = False) -> Any:
        """Execute SQL query with automatic reconnection"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                self.conn.commit()
                return cur.rowcount
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Query execution failed: {e}")
            raise
    
    # ==================== JOB MANAGEMENT ====================
    
    def create_job(self, job_id: str, video_id: str, emotion: str, 
                   intensity: str, metadata: Dict = None) -> bool:
        """Create a new pipeline job"""
        query = """
            INSERT INTO pipeline_jobs 
            (job_id, video_id, emotion, intensity, status, metadata)
            VALUES (%s, %s, %s, %s, 'idle', %s)
        """
        try:
            self._execute(query, (job_id, video_id, emotion, intensity, Json(metadata or {})))
            logger.info(f"✓ Job created: {job_id}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to create job: {e}")
            return False
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Retrieve job by ID"""
        query = "SELECT * FROM pipeline_jobs WHERE job_id = %s"
        results = self._execute(query, (job_id,), fetch=True)
        return dict(results[0]) if results else None
    
    def update_job_status(self, job_id: str, status: str, 
                         error: str = None) -> bool:
        """Update job status"""
        if status == 'processing':
            query = """
                UPDATE pipeline_jobs 
                SET status = %s, started_at = CURRENT_TIMESTAMP
                WHERE job_id = %s
            """
            params = (status, job_id)
        elif status == 'completed':
            query = """
                UPDATE pipeline_jobs 
                SET status = %s, completed_at = CURRENT_TIMESTAMP
                WHERE job_id = %s
            """
            params = (status, job_id)
        elif status == 'failed':
            query = """
                UPDATE pipeline_jobs 
                SET status = %s, error = %s, completed_at = CURRENT_TIMESTAMP
                WHERE job_id = %s
            """
            params = (status, error, job_id)
        else:
            query = "UPDATE pipeline_jobs SET status = %s WHERE job_id = %s"
            params = (status, job_id)
        
        try:
            self._execute(query, params)
            return True
        except Exception as e:
            logger.error(f"✗ Failed to update job status: {e}")
            return False
    
    def list_jobs(self, status: str = None, limit: int = 100) -> List[Dict]:
        """List jobs with optional status filter"""
        if status:
            query = """
                SELECT * FROM pipeline_jobs 
                WHERE status = %s 
                ORDER BY created_at DESC 
                LIMIT %s
            """
            params = (status, limit)
        else:
            query = """
                SELECT * FROM pipeline_jobs 
                ORDER BY created_at DESC 
                LIMIT %s
            """
            params = (limit,)
        
        results = self._execute(query, params, fetch=True)
        return [dict(row) for row in results]
    
    # ==================== METRICS ====================
    
    def record_metric(self, job_id: str, service_name: str, 
                     processing_time_ms: int, cost_usd: float,
                     metadata: Dict = None) -> bool:
        """Record processing metrics"""
        query = """
            INSERT INTO pipeline_metrics 
            (job_id, service_name, processing_time_ms, cost_usd, metadata)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self._execute(query, (
                job_id, service_name, processing_time_ms, 
                cost_usd, Json(metadata or {})
            ))
            return True
        except Exception as e:
            logger.error(f"✗ Failed to record metric: {e}")
            return False
    
    def get_job_metrics(self, job_id: str) -> List[Dict]:
        """Get all metrics for a job"""
        query = """
            SELECT * FROM pipeline_metrics 
            WHERE job_id = %s 
            ORDER BY timestamp ASC
        """
        results = self._execute(query, (job_id,), fetch=True)
        return [dict(row) for row in results]
    
    def get_service_metrics(self, service_name: str, 
                           limit: int = 100) -> List[Dict]:
        """Get metrics for a specific service"""
        query = """
            SELECT * FROM pipeline_metrics 
            WHERE service_name = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
        """
        results = self._execute(query, (service_name, limit), fetch=True)
        return [dict(row) for row in results]
    
    # ==================== EMOTIONAL PROFILES ====================
    
    def store_emotional_profile(self, emotion: str, intensity: str,
                               camera_settings: Dict, color_settings: Dict,
                               vfx_settings: List, ffmpeg_filter: str) -> bool:
        """Store emotional profile in database"""
        query = """
            INSERT INTO emotional_profiles 
            (emotion, intensity, camera_settings, color_settings, vfx_settings, ffmpeg_filter)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (emotion, intensity) 
            DO UPDATE SET 
                camera_settings = EXCLUDED.camera_settings,
                color_settings = EXCLUDED.color_settings,
                vfx_settings = EXCLUDED.vfx_settings,
                ffmpeg_filter = EXCLUDED.ffmpeg_filter
        """
        try:
            self._execute(query, (
                emotion, intensity,
                Json(camera_settings), Json(color_settings),
                Json(vfx_settings), ffmpeg_filter
            ))
            return True
        except Exception as e:
            logger.error(f"✗ Failed to store profile: {e}")
            return False
    
    def get_emotional_profile(self, emotion: str, intensity: str) -> Optional[Dict]:
        """Retrieve emotional profile"""
        query = """
            SELECT * FROM emotional_profiles 
            WHERE emotion = %s AND intensity = %s
        """
        results = self._execute(query, (emotion, intensity), fetch=True)
        return dict(results[0]) if results else None
    
    def seed_emotional_profiles(self, profiles: Dict) -> int:
        """Seed all emotional profiles from EMOTIONAL_INDEX"""
        count = 0
        for emotion, profile_data in profiles.items():
            for intensity in ['light', 'medium', 'heavy']:
                camera = profile_data.get('camera', {}).get(intensity, {})
                color = profile_data.get('color', {}).get(intensity, {})
                vfx = profile_data.get('vfx', {}).get(intensity, [])
                ffmpeg = profile_data.get('ffmpeg', '')
                
                if self.store_emotional_profile(
                    emotion, intensity, camera, color, vfx, ffmpeg
                ):
                    count += 1
        
        logger.info(f"✓ Seeded {count} emotional profiles")
        return count
    
    # ==================== CONFIGURATION ====================
    
    def set_config(self, key: str, value: str, description: str = None) -> bool:
        """Set configuration value"""
        query = """
            INSERT INTO pipeline_config (config_key, config_value, description)
            VALUES (%s, %s, %s)
            ON CONFLICT (config_key) 
            DO UPDATE SET 
                config_value = EXCLUDED.config_value,
                description = EXCLUDED.description,
                updated_at = CURRENT_TIMESTAMP
        """
        try:
            self._execute(query, (key, value, description))
            return True
        except Exception as e:
            logger.error(f"✗ Failed to set config: {e}")
            return False
    
    def get_config(self, key: str) -> Optional[str]:
        """Get configuration value"""
        query = "SELECT config_value FROM pipeline_config WHERE config_key = %s"
        results = self._execute(query, (key,), fetch=True)
        return results[0]['config_value'] if results else None
    
    def get_all_config(self) -> Dict[str, str]:
        """Get all configuration values"""
        query = "SELECT config_key, config_value FROM pipeline_config"
        results = self._execute(query, fetch=True)
        return {row['config_key']: row['config_value'] for row in results}
    
    # ==================== STATISTICS ====================
    
    def get_pipeline_stats(self) -> Dict:
        """Get overall pipeline statistics"""
        stats = {
            'total_jobs': 0,
            'completed_jobs': 0,
            'failed_jobs': 0,
            'processing_jobs': 0,
            'avg_processing_time_ms': 0,
            'total_cost_usd': 0.0
        }
        
        # Job counts
        query = """
            SELECT status, COUNT(*) as count 
            FROM pipeline_jobs 
            GROUP BY status
        """
        results = self._execute(query, fetch=True)
        for row in results:
            stats['total_jobs'] += row['count']
            if row['status'] == 'completed':
                stats['completed_jobs'] = row['count']
            elif row['status'] == 'failed':
                stats['failed_jobs'] = row['count']
            elif row['status'] == 'processing':
                stats['processing_jobs'] = row['count']
        
        # Metrics aggregation
        query = """
            SELECT 
                AVG(processing_time_ms) as avg_time,
                SUM(cost_usd) as total_cost
            FROM pipeline_metrics
        """
        results = self._execute(query, fetch=True)
        if results and results[0]['avg_time']:
            stats['avg_processing_time_ms'] = int(results[0]['avg_time'])
            stats['total_cost_usd'] = float(results[0]['total_cost'] or 0)
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("✓ Database connection closed")


def create_neon_adapter(connection_string: str = None) -> NeonDatabaseAdapter:
    """Factory function to create Neon adapter"""
    return NeonDatabaseAdapter(connection_string)


if __name__ == "__main__":
    # Test adapter
    import os
    
    # Set connection string (use environment variable in production)
    conn_str = os.getenv('NEON_DATABASE_URL')
    
    if not conn_str:
        print("⚠ Set NEON_DATABASE_URL environment variable to test")
        exit(1)
    
    adapter = create_neon_adapter(conn_str)
    
    # Test job creation
    job_id = f"test_{int(datetime.now().timestamp())}"
    adapter.create_job(job_id, "video_001", "curiosity", "medium", {"test": True})
    
    # Test job retrieval
    job = adapter.get_job(job_id)
    print(f"✓ Job retrieved: {job}")
    
    # Test metrics
    adapter.record_metric(job_id, "oracle", 1200, 0.12)
    metrics = adapter.get_job_metrics(job_id)
    print(f"✓ Metrics: {metrics}")
    
    # Test stats
    stats = adapter.get_pipeline_stats()
    print(f"✓ Stats: {stats}")
    
    adapter.close()
