"""
Elite Video Pipeline v3.0 - Cinematography Oracle
Bridges Natural Language → Hollywood Math via SOTA LLM
Uses LiteLLM for universal model compatibility
"""

import json
import logging
from typing import Dict, Optional
from litellm import completion

from sota_sentinel import get_sentinel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vertex.oracle")


class CinematographyOracle:
    """
    The Cinematography Oracle: Translates director styles and film references
    into precise technical specifications using SOTA AI models
    
    Features:
    - Dynamic model selection via SOTA Sentinel
    - Universal model compatibility via LiteLLM
    - Structured JSON output with cinematography specs
    - Emergency fallback for API failures
    - Lazy-loaded (zero cost until invoked)
    """
    
    def __init__(self):
        # Hot-load the best model at initialization
        self.sentinel = get_sentinel()
        self.model = self.sentinel.get_model()
        self.logger = logger
        
        # System prompt for cinematography analysis
        self.system_prompt = """You are a World-Class Cinematographer and Color Scientist (.01% Vertex Expert).

Your task: Analyze the USER REQUEST (a movie scene, director style, film reference, or vibe).
Output: A JSON object containing the exact technical specifications to recreate this cinematic look.

STRICT JSON SCHEMA REQUIRED:
{
    "lighting": {
        "ratio": "String (e.g. '8:1', '2:1', '16:1', 'Negative Fill')",
        "kelvin": "Integer (2000-10000, color temperature)",
        "iso": "Integer (100-3200, sensor sensitivity)",
        "hard_soft": "String ('Hard', 'Soft', 'Diffused', 'Mixed')",
        "aperture": "String (e.g. 'T1.4', 'T2.8', 'T5.6')",
        "notes": "String (Short strategy, e.g. 'Rembrandt key with rim light')"
    },
    "camera": {
        "focal_length": "Integer (mm, e.g. 35, 50, 85)",
        "shutter_angle": "Integer (degrees, usually 180, 90, 45, 360)",
        "aperture": "String (e.g. 'T1.4', 'T2.8')",
        "movement": "String (e.g. 'Dolly In', 'Handheld Shaky', 'Steadicam Float', 'Static')",
        "angle": "String (e.g. 'Eye Level', 'Low Angle', 'High Angle', 'Dutch Tilt')"
    },
    "color": {
        "palette": "String (e.g. 'Teal/Orange', 'Bleach Bypass', 'Sepia', 'Desaturated')",
        "saturation": "Float (0.0 - 2.0, where 1.0 is neutral)",
        "contrast": "Float (0.0 - 2.0, where 1.0 is neutral)",
        "lut_ref": "String (Closest film stock emulation, e.g. 'Kodak 2383', 'Fuji 8553', 'Rec709')",
        "vignette": "Float (0.0 - 1.0, edge darkening)",
        "bloom": "Float (0.0 - 1.0, highlight glow)",
        "grain": "Float (0.0 - 1.0, film grain intensity)"
    },
    "audio": {
        "profile": "String (e.g. 'Ambient Drone', 'Epic Orchestral', 'Minimalist Piano')",
        "reverb": "String (e.g. 'Cathedral', 'Small Room', 'Outdoor Open')",
        "mix": "String (e.g. 'Stereo', 'Surround 5.1', 'Atmos 7.1.4')"
    },
    "grid": {
        "composition": "String (e.g. 'Rule of Thirds', 'Centered Hero', 'Golden Ratio')",
        "focus_zone": "String (e.g. 'Center Weighted', 'Off Center', 'Edge Weighted')",
        "negative_space": "String (e.g. 'Balanced', 'Claustrophobic', 'Expansive')"
    },
    "description": "String (Brief summary of the cinematic style)",
    "reference_films": "Array of strings (Similar films or scenes)"
}

CRITICAL RULES:
1. RETURN VALID JSON ONLY. NO MARKDOWN. NO EXPLANATIONS.
2. Use realistic cinematography values (no impossible specs).
3. Ensure all numeric values are within professional ranges.
4. If uncertain, use conservative/neutral values.

EXAMPLES OF GREAT RESPONSES:
- Blade Runner 2049: High contrast (8:1), cool kelvin (4500K), wide lens (24mm), teal/orange palette
- Wes Anderson: Centered composition, pastel palette, static camera, medium lens (50mm)
- Roger Deakins: Natural lighting (3:1), warm kelvin (3200K), slow dolly, shallow DOF (T1.4)
"""
    
    def consult(self, prompt: str, temperature: float = 0.2) -> Dict:
        """
        Query the SOTA model to reverse-engineer a film style
        
        Args:
            prompt: Natural language description (e.g., "Wes Anderson style", "Blade Runner 2049 funeral scene")
            temperature: Model temperature (0.0-1.0, lower = more deterministic)
            
        Returns:
            Dict: Structured cinematography specifications
        """
        self.logger.info(f"⟳ Oracle: Consulting {self.model} for: '{prompt[:50]}...'")
        
        try:
            # API call via LiteLLM (universal adapter)
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Analyze and reconstruct this cinematic style: {prompt}"}
                ],
                response_format={"type": "json_object"},  # Force JSON mode if supported
                temperature=temperature  # Low temp for precision
            )
            
            # Extract and parse JSON
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # Validate structure
            if not self._validate_structure(result):
                self.logger.warning("⚠ Oracle: Invalid structure, using fallback")
                return self._emergency_fallback(prompt)
            
            self.logger.info(f"✓ Oracle: Successfully analyzed style")
            return result
            
        except json.JSONDecodeError as e:
            self.logger.error(f"✗ Oracle: JSON parsing failed - {e}")
            return self._emergency_fallback(prompt)
        
        except Exception as e:
            self.logger.error(f"✗ Oracle: API call failed - {e}")
            return self._emergency_fallback(prompt)
    
    def _validate_structure(self, result: Dict) -> bool:
        """
        Validate that the Oracle response has required fields
        
        Args:
            result: Oracle response dictionary
            
        Returns:
            bool: True if valid structure
        """
        required_keys = ["lighting", "camera", "color"]
        return all(key in result for key in required_keys)
    
    def _emergency_fallback(self, prompt: str) -> Dict:
        """
        Emergency fallback when Oracle fails
        Returns a safe neutral cinematography profile
        
        Args:
            prompt: Original prompt (for logging)
            
        Returns:
            Dict: Safe fallback profile
        """
        self.logger.warning(f"⚠ Oracle: Using emergency fallback for: '{prompt[:50]}...'")
        
        return {
            "lighting": {
                "ratio": "2:1",
                "kelvin": 5600,
                "iso": 400,
                "hard_soft": "Soft",
                "aperture": "T2.8",
                "notes": "Neutral safe lighting (fallback)"
            },
            "camera": {
                "focal_length": 50,
                "shutter_angle": 180,
                "aperture": "T2.8",
                "movement": "Static",
                "angle": "Eye Level"
            },
            "color": {
                "palette": "Neutral",
                "saturation": 1.0,
                "contrast": 1.0,
                "lut_ref": "Rec709",
                "vignette": 0.0,
                "bloom": 0.0,
                "grain": 0.0
            },
            "audio": {
                "profile": "Neutral Ambient",
                "reverb": "Medium Room",
                "mix": "Stereo"
            },
            "grid": {
                "composition": "Rule of Thirds",
                "focus_zone": "Center Weighted",
                "negative_space": "Balanced"
            },
            "description": "Neutral cinematography (fallback mode)",
            "reference_films": []
        }
    
    def refresh_model(self) -> str:
        """
        Refresh the model from Sentinel (useful after delta check)
        
        Returns:
            str: Updated model identifier
        """
        self.model = self.sentinel.get_model()
        self.logger.info(f"✓ Oracle: Model refreshed to {self.model}")
        return self.model
    
    def get_current_model(self) -> str:
        """
        Get the current model being used
        
        Returns:
            str: Model identifier
        """
        return self.model
    
    def get_status(self) -> Dict:
        """
        Get Oracle status information
        
        Returns:
            Dict: Status information
        """
        return {
            "current_model": self.model,
            "sentinel_status": self.sentinel.get_status(),
            "ready": True
        }


# Singleton instance (lazy-loaded)
_oracle_instance = None


def get_oracle() -> CinematographyOracle:
    """
    Get or create the singleton Oracle instance
    
    Returns:
        CinematographyOracle: The oracle instance
    """
    global _oracle_instance
    if _oracle_instance is None:
        _oracle_instance = CinematographyOracle()
        logger.info("✓ Cinematography Oracle initialized")
    return _oracle_instance


if __name__ == "__main__":
    # Test the oracle
    print("\n" + "=" * 60)
    print("CINEMATOGRAPHY ORACLE - TEST")
    print("=" * 60 + "\n")
    
    oracle = get_oracle()
    
    print(f"Current Model: {oracle.get_current_model()}")
    print(f"Status: {json.dumps(oracle.get_status(), indent=2)}")
    
    # Test consultation (will use fallback if no API key)
    print("\n--- Test Consultation ---")
    result = oracle.consult("Wes Anderson style with pastel colors")
    print(json.dumps(result, indent=2))
    
    print("\n✓ Oracle test complete")
