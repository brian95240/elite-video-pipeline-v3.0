"""
Elite Video Pipeline v3.0 - Vertex Upgrade Controller
System-wide upgrade logic that maintains 0.01% quality across all components
Applies SOTA Sentinel logic to FOSS tool selection and cost optimization
"""

import logging
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vertex.upgrade")

# Vertex upgrade thresholds (configurable via environment)
QUALITY_IMPROVEMENT_THRESHOLD = float(os.getenv("VERTEX_QUALITY_THRESHOLD", "15.0"))  # 15%
COST_RATIO_MAX = float(os.getenv("VERTEX_COST_RATIO_MAX", "2.0"))  # 2x max cost increase
FOSS_PREFERENCE_DELTA = float(os.getenv("VERTEX_FOSS_DELTA", "5.0"))  # 5% quality tolerance for FOSS


class ComponentRegistry:
    """
    Registry of all system components with quality/cost metrics
    """
    
    def __init__(self):
        self.components = {
            # LLM Models (for Oracle)
            "llm": {
                "gpt-4o": {
                    "quality": 92.0,
                    "cost_per_1k": 0.0025,
                    "is_foss": False,
                    "category": "llm"
                },
                "gpt-4o-mini": {
                    "quality": 85.0,
                    "cost_per_1k": 0.00015,
                    "is_foss": False,
                    "category": "llm"
                },
                "claude-3-5-sonnet": {
                    "quality": 94.0,
                    "cost_per_1k": 0.003,
                    "is_foss": False,
                    "category": "llm"
                },
                "gemini-2.0-flash": {
                    "quality": 88.0,
                    "cost_per_1k": 0.0001,
                    "is_foss": False,
                    "category": "llm"
                },
                "llama-3.1-70b": {
                    "quality": 82.0,
                    "cost_per_1k": 0.0,
                    "is_foss": True,
                    "category": "llm"
                },
                "mixtral-8x7b": {
                    "quality": 80.0,
                    "cost_per_1k": 0.0,
                    "is_foss": True,
                    "category": "llm"
                }
            },
            
            # Video Processing Tools
            "video_processor": {
                "ffmpeg": {
                    "quality": 95.0,
                    "cost_per_hour": 0.0,
                    "is_foss": True,
                    "category": "video_processor"
                },
                "adobe_premiere": {
                    "quality": 98.0,
                    "cost_per_hour": 22.99,  # Monthly subscription amortized
                    "is_foss": False,
                    "category": "video_processor"
                },
                "davinci_resolve": {
                    "quality": 97.0,
                    "cost_per_hour": 0.0,  # Free version
                    "is_foss": False,
                    "category": "video_processor"
                }
            },
            
            # 3D Rendering Engines
            "render_engine": {
                "blender_cycles": {
                    "quality": 93.0,
                    "cost_per_hour": 0.0,
                    "is_foss": True,
                    "category": "render_engine"
                },
                "blender_eevee": {
                    "quality": 85.0,
                    "cost_per_hour": 0.0,
                    "is_foss": True,
                    "category": "render_engine"
                },
                "unreal_engine": {
                    "quality": 96.0,
                    "cost_per_hour": 0.0,  # Free until revenue threshold
                    "is_foss": False,
                    "category": "render_engine"
                },
                "arnold": {
                    "quality": 98.0,
                    "cost_per_hour": 45.0,  # Subscription
                    "is_foss": False,
                    "category": "render_engine"
                }
            },
            
            # Color Grading Tools
            "color_grading": {
                "davinci_resolve_free": {
                    "quality": 95.0,
                    "cost_per_hour": 0.0,
                    "is_foss": False,
                    "category": "color_grading"
                },
                "davinci_resolve_studio": {
                    "quality": 99.0,
                    "cost_per_hour": 0.4,  # One-time purchase amortized
                    "is_foss": False,
                    "category": "color_grading"
                },
                "ffmpeg_lut": {
                    "quality": 80.0,
                    "cost_per_hour": 0.0,
                    "is_foss": True,
                    "category": "color_grading"
                }
            },
            
            # Database Systems
            "database": {
                "neon_postgres": {
                    "quality": 90.0,
                    "cost_per_gb": 0.0,  # Free tier
                    "is_foss": True,
                    "category": "database"
                },
                "supabase": {
                    "quality": 92.0,
                    "cost_per_gb": 0.0,  # Free tier
                    "is_foss": True,
                    "category": "database"
                },
                "aws_rds": {
                    "quality": 95.0,
                    "cost_per_gb": 0.115,
                    "is_foss": False,
                    "category": "database"
                }
            },
            
            # Cache Systems
            "cache": {
                "redis": {
                    "quality": 95.0,
                    "cost_per_gb": 0.0,  # Self-hosted
                    "is_foss": True,
                    "category": "cache"
                },
                "redis_cloud": {
                    "quality": 96.0,
                    "cost_per_gb": 0.0,  # Free tier
                    "is_foss": False,
                    "category": "cache"
                },
                "memcached": {
                    "quality": 88.0,
                    "cost_per_gb": 0.0,
                    "is_foss": True,
                    "category": "cache"
                }
            }
        }
    
    def get_category(self, category: str) -> Dict:
        """Get all components in a category"""
        return self.components.get(category, {})
    
    def get_component(self, category: str, name: str) -> Optional[Dict]:
        """Get specific component metrics"""
        return self.components.get(category, {}).get(name)


class VertexUpgradeController:
    """
    System-wide upgrade controller that applies vertex logic to all components
    
    Features:
    - Quality improvement threshold enforcement
    - Cost ratio limits
    - FOSS-first preference with quality tolerance
    - Automatic component selection
    - Upgrade recommendations
    """
    
    def __init__(self):
        self.registry = ComponentRegistry()
        self.logger = logger
        self.current_selections = {}
        
        # Load default selections (FOSS-first)
        self._initialize_defaults()
    
    def _initialize_defaults(self):
        """Initialize with FOSS-first defaults"""
        self.current_selections = {
            "llm": "gpt-4o-mini",  # Lowest cost with good quality
            "video_processor": "ffmpeg",  # FOSS, excellent quality
            "render_engine": "blender_cycles",  # FOSS, excellent quality
            "color_grading": "davinci_resolve_free",  # Free, excellent quality
            "database": "neon_postgres",  # FOSS, free tier
            "cache": "redis"  # FOSS, self-hosted
        }
        
        self.logger.info("✓ Initialized with FOSS-first defaults")
    
    def evaluate_upgrade(self, category: str, candidate: str) -> Tuple[bool, str, Dict]:
        """
        Evaluate if a component upgrade should be accepted
        
        Args:
            category: Component category (e.g., "llm", "video_processor")
            candidate: Candidate component name
            
        Returns:
            Tuple[bool, str, Dict]: (should_upgrade, reason, metrics)
        """
        current_name = self.current_selections.get(category)
        if not current_name:
            return True, "Initial selection", {}
        
        current = self.registry.get_component(category, current_name)
        candidate_metrics = self.registry.get_component(category, candidate)
        
        if not current or not candidate_metrics:
            return False, "Invalid component", {}
        
        # Same component: no upgrade
        if current_name == candidate:
            return False, "Already using this component", {}
        
        # Extract metrics
        current_quality = current.get("quality", 80.0)
        candidate_quality = candidate_metrics.get("quality", 80.0)
        
        current_cost = current.get("cost_per_hour", current.get("cost_per_1k", current.get("cost_per_gb", 0.0)))
        candidate_cost = candidate_metrics.get("cost_per_hour", candidate_metrics.get("cost_per_1k", candidate_metrics.get("cost_per_gb", 0.0)))
        
        current_is_foss = current.get("is_foss", False)
        candidate_is_foss = candidate_metrics.get("is_foss", False)
        
        # Calculate improvement
        quality_improvement = ((candidate_quality - current_quality) / current_quality) * 100
        cost_ratio = candidate_cost / current_cost if current_cost > 0 else 1.0
        
        # FOSS-First Logic: Prefer FOSS if quality is within tolerance
        if candidate_is_foss and not current_is_foss:
            if quality_improvement >= -FOSS_PREFERENCE_DELTA:
                return True, f"FOSS upgrade (quality: {quality_improvement:+.1f}%, cost: {cost_ratio:.2f}x)", {
                    "quality_improvement": quality_improvement,
                    "cost_ratio": cost_ratio,
                    "foss_upgrade": True
                }
        
        # Quality Threshold Check
        if quality_improvement < QUALITY_IMPROVEMENT_THRESHOLD:
            return False, f"Quality improvement ({quality_improvement:.1f}%) below threshold ({QUALITY_IMPROVEMENT_THRESHOLD}%)", {
                "quality_improvement": quality_improvement,
                "cost_ratio": cost_ratio
            }
        
        # Cost Ratio Check
        if cost_ratio > COST_RATIO_MAX:
            return False, f"Cost increase ({cost_ratio:.2f}x) exceeds maximum ({COST_RATIO_MAX}x)", {
                "quality_improvement": quality_improvement,
                "cost_ratio": cost_ratio
            }
        
        # Upgrade approved
        return True, f"Quality +{quality_improvement:.1f}%, Cost {cost_ratio:.2f}x", {
            "quality_improvement": quality_improvement,
            "cost_ratio": cost_ratio
        }
    
    def recommend_best(self, category: str) -> Tuple[str, Dict]:
        """
        Recommend the best component in a category based on vertex logic
        
        Args:
            category: Component category
            
        Returns:
            Tuple[str, Dict]: (component_name, metrics)
        """
        components = self.registry.get_category(category)
        if not components:
            return None, {}
        
        # Score each component
        scored = []
        for name, metrics in components.items():
            quality = metrics.get("quality", 0.0)
            cost = metrics.get("cost_per_hour", metrics.get("cost_per_1k", metrics.get("cost_per_gb", 0.0)))
            is_foss = metrics.get("is_foss", False)
            
            # Vertex scoring formula:
            # Score = Quality + (FOSS_bonus) - (Cost_penalty)
            foss_bonus = 10.0 if is_foss else 0.0
            cost_penalty = cost * 5.0  # Penalize cost
            
            score = quality + foss_bonus - cost_penalty
            
            scored.append((name, score, metrics))
        
        # Sort by score (descending)
        scored.sort(key=lambda x: x[1], reverse=True)
        
        best_name, best_score, best_metrics = scored[0]
        
        self.logger.info(f"✓ Best {category}: {best_name} (score: {best_score:.1f})")
        return best_name, best_metrics
    
    def apply_upgrade(self, category: str, component: str) -> bool:
        """
        Apply an upgrade if it passes vertex logic
        
        Args:
            category: Component category
            component: Component name
            
        Returns:
            bool: True if upgrade was applied
        """
        should_upgrade, reason, metrics = self.evaluate_upgrade(category, component)
        
        if should_upgrade:
            previous = self.current_selections.get(category)
            self.current_selections[category] = component
            self.logger.info(f"✓ UPGRADE APPLIED: {category} ({previous} → {component})")
            self.logger.info(f"  Reason: {reason}")
            return True
        else:
            self.logger.info(f"✗ UPGRADE REJECTED: {category} ({component})")
            self.logger.info(f"  Reason: {reason}")
            return False
    
    def get_current_stack(self) -> Dict:
        """
        Get the current technology stack
        
        Returns:
            Dict: Current selections with metrics
        """
        stack = {}
        for category, component in self.current_selections.items():
            metrics = self.registry.get_component(category, component)
            stack[category] = {
                "component": component,
                "metrics": metrics
            }
        return stack
    
    def get_recommendations(self) -> Dict:
        """
        Get upgrade recommendations for all categories
        
        Returns:
            Dict: Recommendations for each category
        """
        recommendations = {}
        
        for category in self.registry.components.keys():
            best_name, best_metrics = self.recommend_best(category)
            current_name = self.current_selections.get(category)
            
            should_upgrade, reason, upgrade_metrics = self.evaluate_upgrade(category, best_name)
            
            recommendations[category] = {
                "current": current_name,
                "recommended": best_name,
                "should_upgrade": should_upgrade,
                "reason": reason,
                "metrics": upgrade_metrics
            }
        
        return recommendations


# Singleton instance
_controller_instance = None


def get_controller() -> VertexUpgradeController:
    """
    Get or create the singleton controller instance
    
    Returns:
        VertexUpgradeController: The controller instance
    """
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = VertexUpgradeController()
        logger.info("✓ Vertex Upgrade Controller initialized")
    return _controller_instance


if __name__ == "__main__":
    # Test the controller
    print("\n" + "=" * 60)
    print("VERTEX UPGRADE CONTROLLER - TEST")
    print("=" * 60 + "\n")
    
    controller = get_controller()
    
    print("--- Current Stack ---")
    stack = controller.get_current_stack()
    print(json.dumps(stack, indent=2))
    
    print("\n--- Upgrade Recommendations ---")
    recommendations = controller.get_recommendations()
    for category, rec in recommendations.items():
        print(f"\n{category}:")
        print(f"  Current: {rec['current']}")
        print(f"  Recommended: {rec['recommended']}")
        print(f"  Should Upgrade: {rec['should_upgrade']}")
        print(f"  Reason: {rec['reason']}")
    
    print("\n✓ Controller test complete")
