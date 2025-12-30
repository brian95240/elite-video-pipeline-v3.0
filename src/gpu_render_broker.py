"""
Elite Video Pipeline v3.2 - GPU Render Broker
Cloud Render Extension: GPU spot price arbitration and provider selection
Integrates with SOTA Sentinel for cost/quality optimization
"""

import logging
import os
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GPUProvider:
    """GPU cloud provider specification"""
    name: str
    gpu_model: str
    vram_gb: int
    spot_price_per_hour: float
    uptime_sla: float  # 0.0-1.0
    region: str
    api_endpoint: str
    available: bool = True
    
    def vertex_score(self, quality_threshold: float, cost_ratio_max: float) -> float:
        """
        Calculate vertex score based on quality and cost
        Higher score = better choice
        
        Args:
            quality_threshold: Minimum quality requirement (0.0-1.0)
            cost_ratio_max: Maximum cost ratio vs. baseline
            
        Returns:
            Vertex score (0.0-1.0)
        """
        # Quality score (VRAM + uptime)
        vram_score = min(self.vram_gb / 48.0, 1.0)  # 48GB = max
        quality_score = (vram_score + self.uptime_sla) / 2.0
        
        # Cost score (inverse of price)
        baseline_price = 0.50  # $0.50/hour baseline
        cost_score = baseline_price / max(self.spot_price_per_hour, 0.01)
        cost_score = min(cost_score, 1.0)
        
        # Combined vertex score
        # Weighted: 60% quality, 40% cost (FOSS-first prioritizes quality)
        vertex_score = (quality_score * 0.6) + (cost_score * 0.4)
        
        # Penalty if below thresholds
        if quality_score < quality_threshold:
            vertex_score *= 0.5  # 50% penalty
        
        if self.spot_price_per_hour > (baseline_price * cost_ratio_max):
            vertex_score *= 0.7  # 30% penalty
        
        return vertex_score


class GPURenderBroker:
    """
    GPU Render Broker: Cost arbitration for cloud rendering
    Integrates with SOTA Sentinel protocol for dynamic provider selection
    """
    
    def __init__(self):
        # Environment variables for thresholds
        self.quality_threshold = float(os.getenv("VERTEX_QUALITY_THRESHOLD", "0.7"))
        self.cost_ratio_max = float(os.getenv("VERTEX_COST_RATIO_MAX", "2.0"))
        
        # Provider registry (will be populated from sota_manifest.json)
        self.providers: List[GPUProvider] = []
        
        # Cached best provider
        self._cached_provider: Optional[GPUProvider] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl_seconds = 300  # 5 minutes
        
        logger.info("✓ GPU Render Broker initialized")
        logger.info(f"  Quality Threshold: {self.quality_threshold}")
        logger.info(f"  Cost Ratio Max: {self.cost_ratio_max}x")
    
    def load_providers_from_manifest(self, manifest_url: str = None) -> None:
        """
        Load GPU providers from SOTA manifest
        Extends sota_manifest.json with live GPU spot prices
        
        Args:
            manifest_url: URL to SOTA manifest (defaults to env var)
        """
        if manifest_url is None:
            manifest_url = os.getenv(
                "SOTA_MANIFEST_URL",
                "https://raw.githubusercontent.com/brian95240/elite-video-pipeline-v3.0/main/examples/sota_manifest.json"
            )
        
        try:
            response = requests.get(manifest_url, timeout=5)
            response.raise_for_status()
            manifest = response.json()
            
            # Extract GPU providers from manifest
            gpu_providers_data = manifest.get("gpu_providers", [])
            
            self.providers = []
            for provider_data in gpu_providers_data:
                provider = GPUProvider(
                    name=provider_data["name"],
                    gpu_model=provider_data["gpu_model"],
                    vram_gb=provider_data["vram_gb"],
                    spot_price_per_hour=provider_data["spot_price_per_hour"],
                    uptime_sla=provider_data["uptime_sla"],
                    region=provider_data["region"],
                    api_endpoint=provider_data["api_endpoint"],
                    available=provider_data.get("available", True)
                )
                self.providers.append(provider)
            
            logger.info(f"✓ Loaded {len(self.providers)} GPU providers from manifest")
            
            # If no providers loaded, use fallback
            if not self.providers:
                logger.warning("Manifest contained no providers, using fallback")
                self._load_fallback_providers()
            
        except Exception as e:
            logger.warning(f"Failed to load providers from manifest: {e}")
            logger.info("Using fallback provider list")
            self._load_fallback_providers()
    
    def _load_fallback_providers(self) -> None:
        """
        Load fallback GPU providers when manifest is unavailable
        Includes Hetzner (preferred), Vast.ai, Tensordock
        """
        self.providers = [
            # Hetzner (preferred - user's account)
            GPUProvider(
                name="Hetzner Cloud GPU",
                gpu_model="NVIDIA RTX 4090",
                vram_gb=24,
                spot_price_per_hour=0.35,
                uptime_sla=0.99,
                region="eu-central",
                api_endpoint="https://api.hetzner.cloud/v1",
                available=True
            ),
            # Vast.ai
            GPUProvider(
                name="Vast.ai",
                gpu_model="NVIDIA RTX 4090",
                vram_gb=24,
                spot_price_per_hour=0.28,
                uptime_sla=0.85,
                region="us-west",
                api_endpoint="https://vast.ai/api/v0",
                available=True
            ),
            # Tensordock
            GPUProvider(
                name="Tensordock",
                gpu_model="NVIDIA A4000",
                vram_gb=16,
                spot_price_per_hour=0.22,
                uptime_sla=0.90,
                region="us-east",
                api_endpoint="https://marketplace.tensordock.com/api/v0",
                available=True
            ),
            # RunPod
            GPUProvider(
                name="RunPod",
                gpu_model="NVIDIA RTX 3090",
                vram_gb=24,
                spot_price_per_hour=0.25,
                uptime_sla=0.92,
                region="us-central",
                api_endpoint="https://api.runpod.io/v1",
                available=True
            )
        ]
        
        logger.info(f"✓ Loaded {len(self.providers)} fallback GPU providers")
    
    def select_best_provider(self, render_intent: 'RenderIntent') -> Tuple[Optional[GPUProvider], float]:
        """
        Select best GPU provider using vertex logic
        Considers quality threshold and cost ratio
        
        Args:
            render_intent: RenderIntent with quality requirements
            
        Returns:
            Tuple of (best_provider, estimated_cost)
        """
        # Check cache
        if self._is_cache_valid():
            logger.info(f"✓ Using cached provider: {self._cached_provider.name}")
            estimated_cost = self._estimate_render_cost(self._cached_provider, render_intent)
            return self._cached_provider, estimated_cost
        
        # Load providers if not loaded
        if not self.providers:
            self.load_providers_from_manifest()
        
        # Filter available providers
        available_providers = [p for p in self.providers if p.available]
        
        if not available_providers:
            logger.error("No available GPU providers")
            return None, 0.0
        
        # Calculate vertex scores for all providers
        scored_providers = []
        for provider in available_providers:
            score = provider.vertex_score(self.quality_threshold, self.cost_ratio_max)
            scored_providers.append((provider, score))
        
        # Sort by score (descending)
        scored_providers.sort(key=lambda x: x[1], reverse=True)
        
        # Select best provider
        best_provider, best_score = scored_providers[0]
        
        logger.info(f"✓ Selected GPU provider: {best_provider.name}")
        logger.info(f"  GPU Model: {best_provider.gpu_model}")
        logger.info(f"  VRAM: {best_provider.vram_gb}GB")
        logger.info(f"  Spot Price: ${best_provider.spot_price_per_hour:.3f}/hour")
        logger.info(f"  Uptime SLA: {best_provider.uptime_sla * 100:.1f}%")
        logger.info(f"  Vertex Score: {best_score:.3f}")
        
        # Cache result
        self._cached_provider = best_provider
        self._cache_timestamp = datetime.now()
        
        # Estimate cost
        estimated_cost = self._estimate_render_cost(best_provider, render_intent)
        
        return best_provider, estimated_cost
    
    def _estimate_render_cost(self, provider: GPUProvider, render_intent: 'RenderIntent') -> float:
        """
        Estimate rendering cost based on provider and render intent
        
        Args:
            provider: Selected GPU provider
            render_intent: RenderIntent with resolution, quality, frame range
            
        Returns:
            Estimated cost in USD
        """
        # Base render time estimates (minutes per frame)
        resolution_multipliers = {
            "720p": 0.5,
            "1080p": 1.0,
            "4k": 4.0,
            "8k": 16.0
        }
        
        quality_multipliers = {
            "preview": 0.3,
            "high": 1.0,
            "production": 2.0
        }
        
        # Get multipliers
        resolution_mult = resolution_multipliers.get(render_intent.resolution, 1.0)
        quality_mult = quality_multipliers.get(render_intent.quality, 1.0)
        
        # Calculate frame count
        if render_intent.frame_range:
            frame_count = render_intent.frame_range[1] - render_intent.frame_range[0] + 1
        else:
            frame_count = 24 * 10  # Default: 10 seconds @ 24fps
        
        # Estimate render time
        minutes_per_frame = 0.5 * resolution_mult * quality_mult  # Base: 0.5 min/frame @ 1080p
        total_minutes = minutes_per_frame * frame_count
        total_hours = total_minutes / 60.0
        
        # Calculate cost
        estimated_cost = total_hours * provider.spot_price_per_hour
        
        logger.info(f"  Estimated render time: {total_minutes:.1f} minutes ({total_hours:.2f} hours)")
        logger.info(f"  Estimated cost: ${estimated_cost:.3f}")
        
        return estimated_cost
    
    def _is_cache_valid(self) -> bool:
        """Check if cached provider is still valid"""
        if self._cached_provider is None or self._cache_timestamp is None:
            return False
        
        elapsed_seconds = (datetime.now() - self._cache_timestamp).total_seconds()
        return elapsed_seconds < self._cache_ttl_seconds
    
    def get_provider_status(self) -> Dict:
        """
        Get status of all GPU providers
        
        Returns:
            Status dictionary with provider information
        """
        if not self.providers:
            self.load_providers_from_manifest()
        
        providers_status = []
        for provider in self.providers:
            score = provider.vertex_score(self.quality_threshold, self.cost_ratio_max)
            providers_status.append({
                "name": provider.name,
                "gpu_model": provider.gpu_model,
                "vram_gb": provider.vram_gb,
                "spot_price_per_hour": provider.spot_price_per_hour,
                "uptime_sla": provider.uptime_sla,
                "region": provider.region,
                "available": provider.available,
                "vertex_score": round(score, 3)
            })
        
        # Sort by vertex score
        providers_status.sort(key=lambda x: x["vertex_score"], reverse=True)
        
        return {
            "quality_threshold": self.quality_threshold,
            "cost_ratio_max": self.cost_ratio_max,
            "providers": providers_status,
            "cached_provider": self._cached_provider.name if self._cached_provider else None
        }


def create_gpu_broker() -> GPURenderBroker:
    """Factory function to create GPU render broker"""
    return GPURenderBroker()


if __name__ == "__main__":
    # Test GPU render broker
    from prompt_parser import RenderIntent
    
    print("\n" + "=" * 80)
    print("GPU RENDER BROKER TEST")
    print("=" * 80 + "\n")
    
    broker = create_gpu_broker()
    broker.load_providers_from_manifest()
    
    # Test provider selection
    test_render_intent = RenderIntent(
        is_render_request=True,
        render_type="final",
        output_format="mp4",
        resolution="4k",
        quality="production",
        frame_range=(1, 240),  # 10 seconds @ 24fps
        fps=24
    )
    
    print("Test Render Intent:")
    print(f"  Resolution: {test_render_intent.resolution}")
    print(f"  Quality: {test_render_intent.quality}")
    print(f"  Frame Range: {test_render_intent.frame_range}")
    print(f"  FPS: {test_render_intent.fps}")
    print()
    
    best_provider, estimated_cost = broker.select_best_provider(test_render_intent)
    
    if best_provider:
        print(f"\n✓ Best provider selected: {best_provider.name}")
        print(f"  Estimated cost: ${estimated_cost:.3f}")
    else:
        print("\n✗ No suitable provider found")
    
    print("\n" + "=" * 80)
    print("Provider Status:")
    print("=" * 80 + "\n")
    
    status = broker.get_provider_status()
    for provider in status["providers"]:
        print(f"{provider['name']}:")
        print(f"  GPU: {provider['gpu_model']} ({provider['vram_gb']}GB)")
        print(f"  Price: ${provider['spot_price_per_hour']:.3f}/hour")
        print(f"  Vertex Score: {provider['vertex_score']}")
        print()
