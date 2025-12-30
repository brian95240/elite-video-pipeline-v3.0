"""
Elite Video Pipeline v3.0 - Vertex Cinematography Engine
Real cinematography mathematics: lighting ratios, color temperature, lens psychology
.01% Vertex Expert implementation for professional-grade cinematography
"""

import logging
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CinematographySpecs:
    """Professional cinematography specifications"""
    lighting_ratio: str  # e.g., "8:1" (key:fill ratio)
    color_temp_kelvin: int  # e.g., 5600K (daylight), 3200K (tungsten)
    focal_length_mm: int  # e.g., 35mm (intimate), 85mm (portrait)
    aperture: str  # e.g., "T1.5" (wide open), "T8" (deep focus)
    iso: int  # e.g., 800 (low light), 200 (bright)
    sensor_crop: float  # e.g., 1.0 (full frame), 1.5 (APS-C)
    shutter_angle: int  # e.g., 180° (cinematic motion blur)


class VertexCinematography:
    """
    Vertex-level cinematography calculations
    Converts emotional intent into precise technical specifications
    Based on Hollywood cinematography principles
    """
    
    def __init__(self):
        # Mood-to-lighting mapping (Director of Photography knowledge)
        self.mood_lighting_map = {
            # High contrast (dramatic, mysterious)
            "melancholy": {"ratio": "8:1", "kelvin": 4500, "iso": 800},
            "fear": {"ratio": "16:1", "kelvin": 6500, "iso": 1600},
            "tension": {"ratio": "12:1", "kelvin": 5000, "iso": 1200},
            "rage": {"ratio": "20:1", "kelvin": 2800, "iso": 3200},
            
            # Medium contrast (balanced, natural)
            "curiosity": {"ratio": "4:1", "kelvin": 5600, "iso": 400},
            "wonder": {"ratio": "3:1", "kelvin": 6000, "iso": 200},
            "serenity": {"ratio": "2:1", "kelvin": 5000, "iso": 100},
            
            # Low contrast (soft, uplifting)
            "triumph": {"ratio": "2:1", "kelvin": 3200, "iso": 200},
            "nostalgia": {"ratio": "1.5:1", "kelvin": 2800, "iso": 400},
            "joy": {"ratio": "2:1", "kelvin": 5600, "iso": 200},
        }
        
        # Visual style to LUT/color science mapping
        self.visual_style_map = {
            "future_noir": {
                "lut_profile": "kodak_2383_d65",
                "fog_density": 0.8,
                "chromatic_aberration": 0.15,
                "vignette": 0.6
            },
            "cyberpunk": {
                "lut_profile": "teal_orange_aggressive",
                "neon_glow": 0.9,
                "chromatic_aberration": 0.25,
                "grain": 0.3
            },
            "golden_age": {
                "lut_profile": "kodak_vision3_250d",
                "bloom": 0.4,
                "halation": 0.3,
                "grain": 0.15
            },
            "horror": {
                "lut_profile": "desaturated_green_shift",
                "vignette": 0.8,
                "contrast": 1.6,
                "grain": 0.4
            },
            "epic_fantasy": {
                "lut_profile": "alexa_logc_rec709",
                "bloom": 0.5,
                "lens_flare": 0.7,
                "saturation": 1.4
            }
        }
        
        # Lens psychology (focal length emotional impact)
        self.lens_psychology = {
            "intimate": 35,  # Close, personal, distorted perspective
            "natural": 50,   # Human eye perspective, neutral
            "portrait": 85,  # Flattering compression, separation
            "distant": 135,  # Voyeuristic, compressed space
            "epic": 24,      # Wide, expansive, heroic
            "claustrophobic": 18,  # Extreme wide, distorted edges
        }
    
    def calculate_mood_fingerprint(self, mood: str, intensity: str = "medium") -> Dict:
        """
        Calculate lighting and camera specs from mood
        
        Args:
            mood: Emotional mood (e.g., "melancholy", "triumph")
            intensity: "light", "medium", or "heavy"
            
        Returns:
            Dictionary with lighting_ratio, kelvin, iso, focal_length
        """
        # Get base values
        base = self.mood_lighting_map.get(mood.lower(), {
            "ratio": "4:1",
            "kelvin": 5600,
            "iso": 400
        })
        
        # Intensity modulation
        intensity_multiplier = {
            "light": 0.5,
            "medium": 1.0,
            "heavy": 1.5
        }.get(intensity, 1.0)
        
        # Calculate contrast ratio (higher = more dramatic)
        ratio_parts = base["ratio"].split(":")
        key = float(ratio_parts[0])
        fill = float(ratio_parts[1])
        
        # Increase contrast for higher intensity
        if intensity == "heavy":
            key *= 1.5
        elif intensity == "light":
            key *= 0.7
        
        lighting_ratio = f"{int(key)}:{int(fill)}"
        
        # Adjust ISO for intensity (higher = grittier)
        iso_adjusted = int(base["iso"] * intensity_multiplier)
        
        # Select focal length based on mood
        focal_length = self._select_focal_length(mood, intensity)
        
        # Select aperture (wider for dramatic, narrower for clarity)
        aperture = self._select_aperture(mood, intensity)
        
        return {
            "lighting_ratio": lighting_ratio,
            "color_temp_kelvin": base["kelvin"],
            "iso": iso_adjusted,
            "focal_length_mm": focal_length,
            "aperture": aperture,
            "shutter_angle": 180  # Standard cinematic motion blur
        }
    
    def calculate_visual_fingerprint(self, visual_style: str) -> Dict:
        """
        Calculate color science and effects from visual style
        
        Args:
            visual_style: Visual reference (e.g., "future_noir", "cyberpunk")
            
        Returns:
            Dictionary with lut_profile, fog_density, effects
        """
        return self.visual_style_map.get(visual_style.lower(), {
            "lut_profile": "rec709",
            "vignette": 0.2,
            "grain": 0.1
        })
    
    def _select_focal_length(self, mood: str, intensity: str) -> int:
        """Select focal length based on mood psychology"""
        mood_to_lens = {
            "melancholy": "intimate",
            "fear": "claustrophobic",
            "tension": "portrait",
            "rage": "intimate",
            "curiosity": "natural",
            "wonder": "epic",
            "serenity": "natural",
            "triumph": "epic",
            "nostalgia": "portrait",
            "joy": "natural"
        }
        
        lens_type = mood_to_lens.get(mood.lower(), "natural")
        focal_length = self.lens_psychology.get(lens_type, 50)
        
        # Adjust for intensity (wider for heavy, tighter for light)
        if intensity == "heavy" and focal_length > 35:
            focal_length = int(focal_length * 0.8)  # Go wider
        elif intensity == "light" and focal_length < 85:
            focal_length = int(focal_length * 1.2)  # Go tighter
        
        return focal_length
    
    def _select_aperture(self, mood: str, intensity: str) -> str:
        """Select aperture based on mood (affects depth of field)"""
        # Dramatic moods = wide open (shallow DOF)
        # Calm moods = narrower (deeper DOF)
        dramatic_moods = ["fear", "tension", "rage", "melancholy"]
        
        if mood.lower() in dramatic_moods:
            if intensity == "heavy":
                return "T1.4"  # Extremely shallow DOF
            elif intensity == "medium":
                return "T2.0"
            else:
                return "T2.8"
        else:
            if intensity == "heavy":
                return "T2.8"
            elif intensity == "medium":
                return "T4.0"
            else:
                return "T5.6"  # Deeper focus
    
    def compile_render_manifest(self, mood: str, visual_style: Optional[str] = None,
                                intensity: str = "medium") -> Dict:
        """
        Compile complete render manifest for Blender/Unreal
        
        Args:
            mood: Emotional mood
            visual_style: Optional visual style reference
            intensity: Intensity level
            
        Returns:
            Complete render manifest with camera, lighting, post-process specs
        """
        # Get mood fingerprint
        mood_specs = self.calculate_mood_fingerprint(mood, intensity)
        
        # Get visual fingerprint if provided
        visual_specs = {}
        if visual_style:
            visual_specs = self.calculate_visual_fingerprint(visual_style)
        
        # Compile manifest
        manifest = {
            "status": "compiled",
            "render_manifest": {
                "camera": {
                    "focal_length_mm": mood_specs["focal_length_mm"],
                    "aperture": mood_specs["aperture"],
                    "sensor_crop": 1.0,  # Full frame default
                    "shutter_angle": mood_specs["shutter_angle"]
                },
                "lighting": {
                    "key_fill_ratio": mood_specs["lighting_ratio"],
                    "color_temperature_kelvin": mood_specs["color_temp_kelvin"],
                    "iso": mood_specs["iso"]
                },
                "post_process": {
                    "lut": visual_specs.get("lut_profile", "rec709"),
                    "vignette": visual_specs.get("vignette", 0.2),
                    "grain": visual_specs.get("grain", 0.1),
                    "bloom": visual_specs.get("bloom", 0.0),
                    "chromatic_aberration": visual_specs.get("chromatic_aberration", 0.0)
                }
            },
            "metadata": {
                "mood": mood,
                "visual_style": visual_style or "default",
                "intensity": intensity
            }
        }
        
        return manifest
    
    def generate_ffmpeg_from_manifest(self, manifest: Dict) -> str:
        """
        Generate FFmpeg filter chain from render manifest
        
        Args:
            manifest: Render manifest dictionary
            
        Returns:
            FFmpeg filter chain string
        """
        filters = []
        render = manifest.get("render_manifest", {})
        
        # Color temperature adjustment
        lighting = render.get("lighting", {})
        kelvin = lighting.get("color_temperature_kelvin", 5600)
        
        if kelvin < 4000:  # Warm
            filters.append("colorbalance=rs=0.15:gs=0.05:bs=-0.1")
        elif kelvin > 6000:  # Cool
            filters.append("colorbalance=rs=-0.1:gs=0.0:bs=0.15")
        
        # Post-process effects
        post = render.get("post_process", {})
        
        # Vignette
        vignette = post.get("vignette", 0)
        if vignette > 0:
            filters.append(f"vignette='PI/4*{vignette}'")
        
        # Grain
        grain = post.get("grain", 0)
        if grain > 0:
            grain_strength = int(grain * 50)
            filters.append(f"noise=alls={grain_strength}:allf=t")
        
        # Bloom
        bloom = post.get("bloom", 0)
        if bloom > 0:
            filters.append(f"eq=brightness={bloom * 0.2}")
        
        # Chromatic aberration (simulated with slight RGB shift)
        chroma = post.get("chromatic_aberration", 0)
        if chroma > 0:
            filters.append("chromakey=0.1")
        
        return ",".join(filters) if filters else "null"
    
    def merge_aesthetic_kinetic(self, aesthetic_result: Dict, kinetic_result: Dict,
                                    aesthetic_tensor: 'AestheticTensor',
                                    kinetic_tensor: 'KineticTensor') -> Dict:
        """
        NEW: Vertex Convergence - Merge Aesthetic and Kinetic streams
        Maps Oracle's stylistic parameters onto Local Engine's geometric mesh
        
        Args:
            aesthetic_result: Oracle's cinematography specifications (Stream A)
            kinetic_result: Local engine's physics/geometry data (Stream B)
            aesthetic_tensor: Original aesthetic tensor
            kinetic_tensor: Original kinetic tensor
            
        Returns:
            Merged render manifest with unified cinematography + physics
        """
        logger.info("⟳ Vertex Convergence: Merging aesthetic + kinetic streams")
        
        # === STEP 1: Extract Aesthetic Parameters ===
        # Get lighting ratios, color temperature, ISO from Oracle
        aesthetic_lighting = aesthetic_result.get("lighting", {})
        aesthetic_camera = aesthetic_result.get("camera", {})
        aesthetic_color = aesthetic_result.get("color", {})
        aesthetic_audio = aesthetic_result.get("audio", {})
        aesthetic_grid = aesthetic_result.get("grid", {})
        
        # === STEP 2: Extract Kinetic Parameters ===
        # Get geometric mesh, physics simulation from Local Engine
        kinetic_scene = kinetic_result.get("scene_manifest", {})
        kinetic_mesh = kinetic_result.get("geometric_mesh", {})
        kinetic_physics = kinetic_result.get("physics_simulation", {})
        kinetic_timing = kinetic_result.get("timing_data", {})
        
        # === STEP 3: Map Aesthetic onto Kinetic ===
        # Apply Oracle's lighting ratios to Local Engine's actor positions
        merged_lighting = self._map_lighting_to_geometry(
            aesthetic_lighting,
            kinetic_mesh,
            kinetic_scene
        )
        
        # Apply Oracle's camera specs to Local Engine's blocking
        merged_camera = self._map_camera_to_blocking(
            aesthetic_camera,
            kinetic_mesh,
            kinetic_scene
        )
        
        # Apply Oracle's color grading to Local Engine's action timing
        merged_color = self._map_color_to_timing(
            aesthetic_color,
            kinetic_timing,
            aesthetic_tensor
        )
        
        # Apply Oracle's audio profile to Local Engine's physics
        merged_audio = self._map_audio_to_physics(
            aesthetic_audio,
            kinetic_physics,
            kinetic_scene
        )
        
        # Apply Oracle's composition grid to Local Engine's spatial coordinates
        merged_grid = self._map_grid_to_spatial(
            aesthetic_grid,
            kinetic_mesh,
            kinetic_scene
        )
        
        # === STEP 4: Compile Unified Manifest ===
        merged_manifest = {
            "camera": merged_camera,
            "lighting": merged_lighting,
            "post_process": merged_color,
            "audio": merged_audio,
            "grid": merged_grid,
            "physics": kinetic_physics,
            "geometry": kinetic_mesh,
            "scene": kinetic_scene,
            "timing": kinetic_timing
        }
        
        logger.info("✓ Vertex Convergence complete")
        return merged_manifest
    
    def _map_lighting_to_geometry(self, lighting: Dict, mesh: Dict, scene: Dict) -> Dict:
        """
        Map aesthetic lighting parameters onto geometric mesh
        Aligns lighting ratios with actor positions
        """
        merged = lighting.copy()
        
        # Calculate lighting zones based on actor positions
        vertices = mesh.get("vertices", [])
        
        if vertices:
            # Distribute lighting based on actor count
            num_actors = len(vertices)
            
            # Adjust key light intensity based on scene density
            if num_actors > 3:
                merged["key_light_intensity"] = 0.8  # Softer for crowded scenes
            else:
                merged["key_light_intensity"] = 1.0  # Full intensity for sparse scenes
            
            # Add positional lighting data
            merged["light_positions"] = [
                {
                    "type": "key",
                    "position": [vertices[0]["x"] + 2, vertices[0]["y"] + 3, vertices[0]["z"] + 1]
                } if vertices else {"type": "key", "position": [2, 3, 1]}
            ]
        
        return merged
    
    def _map_camera_to_blocking(self, camera: Dict, mesh: Dict, scene: Dict) -> Dict:
        """
        Map aesthetic camera parameters onto blocking zones
        Adjusts focal length and aperture based on actor positions
        """
        merged = camera.copy()
        
        # Get actor positions
        vertices = mesh.get("vertices", [])
        
        if vertices:
            # Calculate scene depth (distance between actors)
            if len(vertices) > 1:
                depth = abs(vertices[-1]["x"] - vertices[0]["x"])
                
                # Adjust focal length based on scene depth
                if depth > 5.0:
                    merged["focal_length"] = 85  # Telephoto for compressed space
                elif depth < 2.0:
                    merged["focal_length"] = 24  # Wide for intimate scenes
                else:
                    merged["focal_length"] = merged.get("focal_length", 50)  # Keep Oracle's choice
        
        # Add camera position based on blocking
        blocking_zones = mesh.get("faces", [])
        if blocking_zones:
            # Position camera to capture all blocking zones
            merged["camera_position"] = [0, 1.6, 5]  # Standard eye-level, 5 units back
        
        return merged
    
    def _map_color_to_timing(self, color: Dict, timing: Dict, aesthetic_tensor: 'AestheticTensor') -> Dict:
        """
        Map aesthetic color grading onto action timing
        Aligns lighting temperature with physical action speed
        """
        merged = color.copy()
        
        # Get speed multiplier from timing
        speed = timing.get("speed_multiplier", 1.0)
        
        # Adjust color temperature based on action speed
        # Fast action = warmer (adrenaline)
        # Slow action = cooler (contemplative)
        if speed > 1.5:  # Fast action
            merged["temperature_shift"] = "+200K"  # Warmer
            merged["saturation"] = merged.get("saturation", 1.0) * 1.1  # More saturated
        elif speed < 0.7:  # Slow action
            merged["temperature_shift"] = "-200K"  # Cooler
            merged["saturation"] = merged.get("saturation", 1.0) * 0.9  # Less saturated
        
        # Apply emotional index intensity to color grading
        if aesthetic_tensor and aesthetic_tensor.intensity:
            if aesthetic_tensor.intensity == "heavy":
                merged["contrast"] = merged.get("contrast", 1.0) * 1.2  # More contrast
            elif aesthetic_tensor.intensity == "light":
                merged["contrast"] = merged.get("contrast", 1.0) * 0.9  # Less contrast
        
        return merged
    
    def _map_audio_to_physics(self, audio: Dict, physics: Dict, scene: Dict) -> Dict:
        """
        Map aesthetic audio profile onto physics simulation
        Aligns reverb with spatial acoustics
        """
        merged = audio.copy()
        
        # Get physics forces
        forces = physics.get("forces", [])
        
        # Adjust reverb based on action intensity
        if forces:
            # High-energy actions = shorter reverb (tight space feel)
            # Low-energy actions = longer reverb (expansive space feel)
            total_force = sum(f.get("magnitude", 0) for f in forces)
            
            if total_force > 10.0:
                merged["reverb"] = "Small Room"  # Tight, energetic
            elif total_force < 5.0:
                merged["reverb"] = "Large Hall"  # Expansive, contemplative
            else:
                merged["reverb"] = merged.get("reverb", "Medium Room")  # Keep Oracle's choice
        
        # Add spatial audio based on object count
        objects = scene.get("objects", [])
        if len(objects) > 3:
            merged["spatial_audio"] = "5.1 Surround"  # Complex scene
        else:
            merged["spatial_audio"] = "Stereo"  # Simple scene
        
        return merged
    
    def _map_grid_to_spatial(self, grid: Dict, mesh: Dict, scene: Dict) -> Dict:
        """
        Map aesthetic composition grid onto spatial coordinates
        Aligns composition rules with actor blocking
        """
        merged = grid.copy()
        
        # Get actor positions
        vertices = mesh.get("vertices", [])
        
        if vertices:
            # Calculate center of mass for actors
            if len(vertices) > 0:
                center_x = sum(v["x"] for v in vertices) / len(vertices)
                center_y = sum(v["y"] for v in vertices) / len(vertices)
                
                # Determine composition zone
                if center_x < -1.0:
                    merged["primary_zone"] = "left_third"
                elif center_x > 1.0:
                    merged["primary_zone"] = "right_third"
                else:
                    merged["primary_zone"] = "center_third"
                
                # Add spatial data
                merged["center_of_mass"] = {"x": center_x, "y": center_y}
        
        # Apply composition rule based on action count
        actions = scene.get("actions", [])
        if len(actions) > 2:
            merged["composition"] = "Dynamic Asymmetry"  # Complex action
        else:
            merged["composition"] = merged.get("composition", "Rule of Thirds")  # Keep Oracle's choice
        
        return merged


def create_vertex_engine() -> VertexCinematography:
    """Factory function to create vertex cinematography engine"""
    return VertexCinematography()


if __name__ == "__main__":
    # Test vertex cinematography
    engine = create_vertex_engine()
    
    # Test mood fingerprint
    print("\n=== MOOD FINGERPRINT TEST ===")
    mood_specs = engine.calculate_mood_fingerprint("melancholy", "heavy")
    print(f"Melancholy (Heavy): {mood_specs}")
    
    # Test visual fingerprint
    print("\n=== VISUAL FINGERPRINT TEST ===")
    visual_specs = engine.calculate_visual_fingerprint("future_noir")
    print(f"Future Noir: {visual_specs}")
    
    # Test render manifest
    print("\n=== RENDER MANIFEST TEST ===")
    manifest = engine.compile_render_manifest("melancholy", "future_noir", "heavy")
    print(f"Complete Manifest:")
    import json
    print(json.dumps(manifest, indent=2))
    
    # Test FFmpeg generation
    print("\n=== FFMPEG FILTER CHAIN ===")
    ffmpeg_chain = engine.generate_ffmpeg_from_manifest(manifest)
    print(f"Filter chain: {ffmpeg_chain}")
