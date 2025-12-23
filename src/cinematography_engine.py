"""
Elite Video Pipeline v3.0 - Cinematography Engine
Generates FFmpeg filter chains from emotional profiles
Applies camera movements, color grading, and VFX effects
"""

import json
import logging
from typing import Dict, List, Optional
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CameraMovement(Enum):
    """Camera movement types"""
    STATIC = "static"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DOLLY_FORWARD = "dolly_forward"
    DOLLY_BACK = "dolly_back"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    CRANE_UP = "crane_up"
    CRANE_DOWN = "crane_down"
    ORBIT = "orbit"
    HANDHELD = "handheld"


class CinematographyEngine:
    """
    Generates FFmpeg filter chains from emotional cinematography profiles
    Supports camera movements, color grading, and VFX overlays
    """
    
    def __init__(self):
        self.filter_templates = {
            # Camera movements
            "slow_zoom_in": "zoompan=z='min(zoom+0.0015,1.5)':d=900:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080",
            "push_in_dramatic": "zoompan=z='min(zoom+0.003,2.0)':d=900:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080",
            "dolly_forward": "scale=iw*1.1:ih*1.1,crop=1920:1080",
            "slow_rise": "zoompan=z='1':y='max(ih-ih/zoom,0-t*20)':d=900:s=1920x1080",
            "crane_up_hero": "zoompan=z='1':y='max(ih-ih/zoom,0-t*40)':d=900:s=1920x1080",
            
            # Color grading
            "neutral_cool": "eq=saturation=0.95:contrast=1.05",
            "mystery_teal": "eq=saturation=0.9:contrast=1.15,colorbalance=bs=0.1:gs=0.05",
            "noir_blue": "eq=saturation=0.8:contrast=1.35,colorbalance=bs=0.2",
            "warm_lift": "eq=saturation=1.1:contrast=1.05,colorbalance=rs=0.1:gs=0.05",
            "golden_hour": "eq=saturation=1.2:contrast=1.15,colorbalance=rs=0.15:gs=0.1",
            "epic_teal_orange": "eq=saturation=1.35:contrast=1.3,colorbalance=rs=0.2:bs=-0.1",
            
            # VFX effects
            "lens_flare": "flare=0.5:0.5:2.0",
            "vignette_light": "vignette='PI/4*0.2'",
            "vignette_heavy": "vignette='PI/4*0.6'",
            "chromatic_aberration": "chromakey=0.1",
            "depth_fog": "gblur=sigma=5:steps=2",
            "particle_glow": "eq=brightness=0.1",
            
            # Distortion effects
            "handheld_shake": "transform='sin(2*PI*t*2)*2'",
            "dutch_tilt": "rotate=15*PI/180",
            "screen_glitch": "noise=alls=20:allf=t",
            "strobe_flash": "eq=brightness='if(lt(t,0.1),1.5,1.0)'",
            
            # Motion effects
            "speed_lines": "scale=iw:ih,fps=120",
            "motion_blur": "minterpolate='fps=120:mi_mode=mci'",
            "zoom_blur": "zoompan=z='if(eq(on,1),1.5,zoom-0.01)':d=1",
        }
    
    def generate_filter_chain(self, profile: Dict) -> str:
        """
        Generate complete FFmpeg filter chain from emotional profile
        
        Args:
            profile: Emotional profile dict with camera, color, vfx
            
        Returns:
            FFmpeg filter chain string
        """
        filters = []
        
        # Extract components
        camera = profile.get("camera", {})
        color = profile.get("color", {})
        vfx = profile.get("vfx", [])
        
        # Add camera movement
        if camera.get("movement"):
            movement = camera["movement"]
            if movement in self.filter_templates:
                filters.append(self.filter_templates[movement])
            else:
                logger.warning(f"Unknown camera movement: {movement}")
        
        # Add color grading
        if color.get("grade"):
            grade = color["grade"]
            if grade in self.filter_templates:
                filters.append(self.filter_templates[grade])
            else:
                # Build custom color grade
                saturation = color.get("saturation", 0)
                contrast = color.get("contrast", 1.0)
                filters.append(f"eq=saturation={1.0 + saturation/100}:contrast={contrast}")
        
        # Add vignette if specified
        if color.get("vignette"):
            vignette_amount = color["vignette"]
            filters.append(f"vignette='PI/4*{vignette_amount}'")
        
        # Add VFX effects
        for effect in vfx:
            if effect in self.filter_templates:
                filters.append(self.filter_templates[effect])
            else:
                logger.warning(f"Unknown VFX effect: {effect}")
        
        # Combine filters with comma separator
        return ",".join(filters) if filters else "null"
    
    def build_ffmpeg_command(self, input_file: str, output_file: str, 
                            profile: Dict, duration: Optional[float] = None) -> str:
        """
        Build complete FFmpeg command with cinematography
        
        Args:
            input_file: Input video file path
            output_file: Output video file path
            profile: Emotional profile
            duration: Optional duration limit in seconds
            
        Returns:
            Complete FFmpeg command string
        """
        filter_chain = self.generate_filter_chain(profile)
        
        # Build command
        cmd = f"ffmpeg -i {input_file}"
        
        if duration:
            cmd += f" -t {duration}"
        
        cmd += f" -filter_complex \"{filter_chain}\""
        cmd += f" -c:v libx264 -preset medium -crf 23"
        cmd += f" -c:a aac -b:a 128k"
        cmd += f" {output_file}"
        
        return cmd
    
    def validate_profile(self, profile: Dict) -> tuple[bool, List[str]]:
        """
        Validate emotional profile structure
        
        Args:
            profile: Profile to validate
            
        Returns:
            (is_valid, list of errors)
        """
        errors = []
        
        if not isinstance(profile, dict):
            errors.append("Profile must be a dictionary")
            return False, errors
        
        required_keys = ["camera", "color", "vfx"]
        for key in required_keys:
            if key not in profile:
                errors.append(f"Missing required key: {key}")
        
        # Validate camera
        camera = profile.get("camera", {})
        if not isinstance(camera, dict):
            errors.append("Camera must be a dictionary")
        elif "movement" not in camera:
            errors.append("Camera must have 'movement' field")
        
        # Validate color
        color = profile.get("color", {})
        if not isinstance(color, dict):
            errors.append("Color must be a dictionary")
        
        # Validate VFX
        vfx = profile.get("vfx", [])
        if not isinstance(vfx, list):
            errors.append("VFX must be a list")
        
        return len(errors) == 0, errors
    
    def apply_intensity_modulation(self, profile: Dict, intensity: str) -> Dict:
        """
        Adjust profile parameters based on intensity level
        
        Args:
            profile: Base profile
            intensity: 'light', 'medium', or 'heavy'
            
        Returns:
            Modified profile
        """
        modulated = json.loads(json.dumps(profile))  # Deep copy
        
        intensity_map = {
            "light": 0.5,
            "medium": 1.0,
            "heavy": 1.5
        }
        
        multiplier = intensity_map.get(intensity, 1.0)
        
        # Modulate camera speed
        if "camera" in modulated and "speed" in modulated["camera"]:
            modulated["camera"]["speed"] *= multiplier
        
        # Modulate color saturation
        if "color" in modulated and "saturation" in modulated["color"]:
            modulated["color"]["saturation"] *= multiplier
        
        # Modulate contrast
        if "color" in modulated and "contrast" in modulated["color"]:
            base_contrast = modulated["color"]["contrast"]
            modulated["color"]["contrast"] = 1.0 + (base_contrast - 1.0) * multiplier
        
        return modulated
    
    def get_filter_statistics(self) -> Dict:
        """Get statistics about available filters"""
        return {
            "total_templates": len(self.filter_templates),
            "camera_movements": sum(1 for k in self.filter_templates if "zoom" in k or "dolly" in k or "pan" in k or "crane" in k),
            "color_grades": sum(1 for k in self.filter_templates if any(x in k for x in ["cool", "warm", "golden", "noir", "epic"])),
            "vfx_effects": sum(1 for k in self.filter_templates if any(x in k for x in ["flare", "vignette", "glow", "fog", "glitch"])),
            "distortion_effects": sum(1 for k in self.filter_templates if any(x in k for x in ["shake", "tilt", "glitch", "strobe"])),
            "motion_effects": sum(1 for k in self.filter_templates if any(x in k for x in ["speed", "blur", "motion"]))
        }


class QualityGateValidator:
    """Validates cinematography output quality"""
    
    def __init__(self):
        self.thresholds = {
            "max_saturation": 200,
            "max_contrast": 2.0,
            "max_vignette": 0.8,
            "min_brightness": -0.5,
            "max_brightness": 0.5
        }
    
    def validate_output(self, profile: Dict) -> tuple[bool, List[str]]:
        """
        Validate cinematography output against quality gates
        
        Args:
            profile: Applied cinematography profile
            
        Returns:
            (passes_validation, list of warnings)
        """
        warnings = []
        
        color = profile.get("color", {})
        
        # Check saturation
        saturation = color.get("saturation", 0)
        if abs(saturation) > 50:
            warnings.append(f"High saturation adjustment: {saturation}%")
        
        # Check contrast
        contrast = color.get("contrast", 1.0)
        if contrast > self.thresholds["max_contrast"]:
            warnings.append(f"Contrast exceeds safe threshold: {contrast}")
        
        # Check vignette
        vignette = color.get("vignette", 0)
        if vignette > self.thresholds["max_vignette"]:
            warnings.append(f"Vignette too heavy: {vignette}")
        
        return len(warnings) <= 2, warnings  # Pass if <= 2 warnings


def create_cinematography_engine() -> CinematographyEngine:
    """Factory function to create engine instance"""
    return CinematographyEngine()


if __name__ == "__main__":
    engine = create_cinematography_engine()
    
    # Test profile
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
    
    # Generate filter chain
    filter_chain = engine.generate_filter_chain(test_profile)
    print(f"✓ Filter chain generated:\n  {filter_chain}\n")
    
    # Validate profile
    is_valid, errors = engine.validate_profile(test_profile)
    print(f"✓ Profile valid: {is_valid}")
    if errors:
        print(f"  Errors: {errors}")
    
    # Get statistics
    stats = engine.get_filter_statistics()
    print(f"\n✓ Filter statistics: {stats}")
