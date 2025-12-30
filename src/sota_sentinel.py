"""
Elite Video Pipeline v3.0 - SOTA Sentinel
Dynamic "Always Best" Model Selector with Vertex Upgrade Logic
Maintains 0.01% quality by auto-detecting state-of-the-art models
"""

import os
import requests
import logging
import json
from typing import Dict, Optional, Tuple
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vertex.sentinel")

# Default fallback if the "Truth Source" is unreachable
FALLBACK_SOTA = "gpt-4o"

# Vertex Upgrade Thresholds (configurable)
UPGRADE_THRESHOLD_PERCENT = float(os.getenv("VERTEX_UPGRADE_THRESHOLD", "15.0"))  # 15% improvement required
COST_RATIO_MAX = float(os.getenv("VERTEX_COST_RATIO_MAX", "2.0"))  # Max 2x cost increase allowed


class SOTASentinel:
    """
    The SOTA Sentinel: Ensures the pipeline always uses the best available model
    
    Features:
    - Delta Check: Queries remote manifest for current best model
    - Vertex Upgrade Logic: Auto-upgrades when improvement exceeds threshold
    - Cost Optimization: Rejects upgrades with excessive cost increases
    - Lazy Loading: Zero cost until actually needed
    - FOSS-First: Prefers open models when quality is comparable
    """
    
    def __init__(self):
        self.logger = logger
        
        # In production, this URL points to a JSON manifest you control
        # Example: "https://raw.githubusercontent.com/brian95240/elite-config/main/sota_manifest.json"
        self.TRUTH_SOURCE_URL = os.getenv("SOTA_MANIFEST_URL", None)
        
        # Current model state
        self.current_model = None
        self.current_metrics = {}
        self.last_check = None
        
        # Perform initial delta check
        self._delta_check()
    
    def _delta_check(self) -> str:
        """
        The 'Delta Check': Verifies the current best model for cinematography
        Runs at startup and can be triggered manually
        
        Returns:
            str: Model identifier (e.g., "gpt-4o", "claude-3-5-sonnet")
        """
        if not self.TRUTH_SOURCE_URL:
            self.logger.info(f"✓ Sentinel: No remote source configured. Using local SOTA: {FALLBACK_SOTA}")
            self.current_model = FALLBACK_SOTA
            self.current_metrics = self._get_default_metrics(FALLBACK_SOTA)
            self.last_check = datetime.now()
            return self.current_model
        
        try:
            # Fetch remote manifest
            self.logger.info(f"⟳ Sentinel: Checking remote manifest: {self.TRUTH_SOURCE_URL}")
            response = requests.get(self.TRUTH_SOURCE_URL, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract candidate model
                candidate_model = data.get("cinematography_model", FALLBACK_SOTA)
                candidate_metrics = data.get("metrics", {})
                
                # Vertex Upgrade Decision
                should_upgrade, reason = self._should_upgrade(candidate_model, candidate_metrics)
                
                if should_upgrade:
                    self.logger.info(f"✓ Sentinel: UPGRADE APPROVED - {reason}")
                    self.logger.info(f"  Previous: {self.current_model}")
                    self.logger.info(f"  New: {candidate_model}")
                    self.current_model = candidate_model
                    self.current_metrics = candidate_metrics
                else:
                    self.logger.info(f"✗ Sentinel: Upgrade rejected - {reason}")
                    if not self.current_model:
                        self.current_model = FALLBACK_SOTA
                        self.current_metrics = self._get_default_metrics(FALLBACK_SOTA)
                
                self.last_check = datetime.now()
                return self.current_model
            
        except requests.exceptions.Timeout:
            self.logger.warning("⚠ Sentinel: Network timeout. Using cached model.")
        except Exception as e:
            self.logger.warning(f"⚠ Sentinel: Delta check failed ({e}). Using fallback.")
        
        # Fallback logic
        if not self.current_model:
            self.current_model = FALLBACK_SOTA
            self.current_metrics = self._get_default_metrics(FALLBACK_SOTA)
        
        return self.current_model
    
    def _should_upgrade(self, candidate_model: str, candidate_metrics: Dict) -> Tuple[bool, str]:
        """
        Vertex Upgrade Logic: Decides if a new model should replace the current one
        
        Criteria:
        1. Quality improvement exceeds UPGRADE_THRESHOLD_PERCENT
        2. Cost increase does not exceed COST_RATIO_MAX
        3. FOSS models preferred when quality is within 5% of paid models
        
        Args:
            candidate_model: New model identifier
            candidate_metrics: Performance metrics for candidate
            
        Returns:
            Tuple[bool, str]: (should_upgrade, reason)
        """
        # First run: always accept
        if not self.current_model:
            return True, "Initial model selection"
        
        # Same model: no upgrade needed
        if candidate_model == self.current_model:
            return False, "Already using this model"
        
        # Extract metrics
        current_quality = self.current_metrics.get("quality_score", 80.0)
        candidate_quality = candidate_metrics.get("quality_score", 80.0)
        
        current_cost = self.current_metrics.get("cost_per_1k_tokens", 0.01)
        candidate_cost = candidate_metrics.get("cost_per_1k_tokens", 0.01)
        
        current_is_foss = self.current_metrics.get("is_foss", False)
        candidate_is_foss = candidate_metrics.get("is_foss", False)
        
        # Calculate improvement
        quality_improvement = ((candidate_quality - current_quality) / current_quality) * 100
        cost_ratio = candidate_cost / current_cost if current_cost > 0 else 1.0
        
        # FOSS-First Logic: Prefer FOSS if quality is within 5%
        if candidate_is_foss and not current_is_foss:
            if quality_improvement >= -5.0:  # Within 5% quality
                return True, f"FOSS upgrade (quality: {quality_improvement:+.1f}%, cost: {cost_ratio:.2f}x)"
        
        # Quality Threshold Check
        if quality_improvement < UPGRADE_THRESHOLD_PERCENT:
            return False, f"Quality improvement ({quality_improvement:.1f}%) below threshold ({UPGRADE_THRESHOLD_PERCENT}%)"
        
        # Cost Ratio Check
        if cost_ratio > COST_RATIO_MAX:
            return False, f"Cost increase ({cost_ratio:.2f}x) exceeds maximum ({COST_RATIO_MAX}x)"
        
        # Upgrade approved
        return True, f"Quality +{quality_improvement:.1f}%, Cost {cost_ratio:.2f}x"
    
    def _get_default_metrics(self, model: str) -> Dict:
        """
        Get default metrics for known models
        
        Args:
            model: Model identifier
            
        Returns:
            Dict: Default metrics
        """
        # Known model metrics (can be extended)
        known_metrics = {
            "gpt-4o": {
                "quality_score": 92.0,
                "cost_per_1k_tokens": 0.0025,
                "is_foss": False,
                "reasoning_capability": "excellent",
                "json_reliability": "excellent"
            },
            "gpt-4o-mini": {
                "quality_score": 85.0,
                "cost_per_1k_tokens": 0.00015,
                "is_foss": False,
                "reasoning_capability": "good",
                "json_reliability": "excellent"
            },
            "claude-3-5-sonnet": {
                "quality_score": 94.0,
                "cost_per_1k_tokens": 0.003,
                "is_foss": False,
                "reasoning_capability": "excellent",
                "json_reliability": "excellent"
            },
            "gemini-2.0-flash": {
                "quality_score": 88.0,
                "cost_per_1k_tokens": 0.0001,
                "is_foss": False,
                "reasoning_capability": "very_good",
                "json_reliability": "good"
            },
            "llama-3.1-70b": {
                "quality_score": 82.0,
                "cost_per_1k_tokens": 0.0,
                "is_foss": True,
                "reasoning_capability": "good",
                "json_reliability": "good"
            }
        }
        
        return known_metrics.get(model, {
            "quality_score": 80.0,
            "cost_per_1k_tokens": 0.01,
            "is_foss": False,
            "reasoning_capability": "unknown",
            "json_reliability": "unknown"
        })
    
    def get_model(self) -> str:
        """
        Get the current SOTA model
        
        Returns:
            str: Model identifier
        """
        return self.current_model
    
    def get_metrics(self) -> Dict:
        """
        Get metrics for the current model
        
        Returns:
            Dict: Current model metrics
        """
        return self.current_metrics
    
    def force_check(self) -> str:
        """
        Force a delta check (useful for manual refresh)
        
        Returns:
            str: Updated model identifier
        """
        self.logger.info("⟳ Sentinel: Forced delta check initiated")
        return self._delta_check()
    
    def get_status(self) -> Dict:
        """
        Get complete sentinel status
        
        Returns:
            Dict: Status information
        """
        return {
            "current_model": self.current_model,
            "metrics": self.current_metrics,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "truth_source": self.TRUTH_SOURCE_URL or "local_fallback",
            "upgrade_threshold": UPGRADE_THRESHOLD_PERCENT,
            "cost_ratio_max": COST_RATIO_MAX
        }


# Singleton Instance (Lazy-loaded)
_sentinel_instance = None


def get_sentinel() -> SOTASentinel:
    """
    Get or create the singleton Sentinel instance
    
    Returns:
        SOTASentinel: The sentinel instance
    """
    global _sentinel_instance
    if _sentinel_instance is None:
        _sentinel_instance = SOTASentinel()
        logger.info("✓ SOTA Sentinel initialized")
    return _sentinel_instance


# Convenience function
def get_current_model() -> str:
    """
    Get the current SOTA model (convenience function)
    
    Returns:
        str: Model identifier
    """
    return get_sentinel().get_model()


if __name__ == "__main__":
    # Test the sentinel
    print("\n" + "=" * 60)
    print("SOTA SENTINEL - DELTA CHECK TEST")
    print("=" * 60 + "\n")
    
    sentinel = get_sentinel()
    
    print(f"Current Model: {sentinel.get_model()}")
    print(f"Metrics: {json.dumps(sentinel.get_metrics(), indent=2)}")
    print(f"\nStatus: {json.dumps(sentinel.get_status(), indent=2)}")
    
    print("\n✓ Sentinel test complete")
