"""
Elite Video Pipeline v3.0 - Render Manifest Compiler
Compiles cinematography fingerprints into structured JSON blueprints for render engines
Output format compatible with Blender Python API and Unreal Engine Sequencer
"""

import logging
import json
from typing import Dict, Optional
from dataclasses import dataclass, asdict

from emotional_index_v3_vertex import EmotionalIndexManagerVertex
from vertex_cinematography import VertexCinematography

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CameraManifest:
    """Camera specifications for render engine"""
    focal_length_mm: int
    aperture: str
    sensor_crop: float
    shutter_angle: int
    movement: str
    angle: str
    speed: float


@dataclass
class LightingManifest:
    """Lighting specifications for render engine"""
    key_fill_ratio: str
    color_temperature_kelvin: int
    iso: int
    intensity: float = 1.0


@dataclass
class PostProcessManifest:
    """Post-process specifications for render engine"""
    lut: str
    saturation: float
    contrast: float
    vignette: float
    bloom: float
    grain: float
    chromatic_aberration: float


@dataclass
class AudioManifest:
    """Audio specifications for render engine"""
    profile: str
    reverb: str
    mix: str


@dataclass
class GridManifest:
    """Composition grid specifications"""
    composition: str
    focus_zone: str
    negative_space: str


class RenderManifestCompiler:
    """
    Compiles complete render manifests from emotional profiles
    Bridges emotional intent → technical specifications → render engine
    """
    
    def __init__(self, redis_client=None):
        self.emotional_manager = EmotionalIndexManagerVertex(redis_client)
        self.vertex_engine = VertexCinematography()
        self.redis_client = redis_client
    
    def compile(self, emotion: str, intensity: str = "medium",
                visual_style: Optional[str] = None) -> Dict:
        """
        Compile complete render manifest
        
        Args:
            emotion: Emotional archetype
            intensity: 'light', 'medium', or 'heavy'
            visual_style: Optional visual style reference
            
        Returns:
            Complete render manifest dictionary
        """
        # Get emotional profile
        profile = self.emotional_manager.get_emotion_profile(emotion, intensity)
        
        # Extract specifications
        camera_data = profile.get("camera", {})
        lighting_data = profile.get("lighting", {})
        color_data = profile.get("color", {})
        audio_data = profile.get("audio", {})
        grid_data = profile.get("grid", {})
        
        # Build camera manifest
        camera = CameraManifest(
            focal_length_mm=camera_data.get("focal_length", 50),
            aperture=lighting_data.get("aperture", "T2.8"),
            sensor_crop=1.0,  # Full frame default
            shutter_angle=180,  # Cinematic motion blur
            movement=camera_data.get("movement", "static"),
            angle=camera_data.get("angle", "eye_level"),
            speed=camera_data.get("speed", 0.0)
        )
        
        # Build lighting manifest
        lighting = LightingManifest(
            key_fill_ratio=lighting_data.get("ratio", "4:1"),
            color_temperature_kelvin=lighting_data.get("kelvin", 5600),
            iso=lighting_data.get("iso", 400),
            intensity=1.0
        )
        
        # Build post-process manifest
        post_process = PostProcessManifest(
            lut=color_data.get("lut", "rec709"),
            saturation=1.0 + (color_data.get("saturation", 0) / 100.0),
            contrast=color_data.get("contrast", 1.0),
            vignette=color_data.get("vignette", 0.0),
            bloom=color_data.get("bloom", 0.0),
            grain=color_data.get("grain", 0.0),
            chromatic_aberration=color_data.get("chromatic_aberration", 0.0)
        )
        
        # Build audio manifest
        audio = AudioManifest(
            profile=audio_data.get("profile", "neutral"),
            reverb=audio_data.get("reverb", "medium_hall"),
            mix=audio_data.get("mix", "stereo")
        )
        
        # Build grid manifest
        grid = GridManifest(
            composition=grid_data.get("composition", "rule_of_thirds"),
            focus_zone=grid_data.get("focus_zone", "center_weighted"),
            negative_space=grid_data.get("negative_space", "balanced")
        )
        
        # Apply visual style overrides if provided
        if visual_style:
            visual_specs = self.vertex_engine.calculate_visual_fingerprint(visual_style)
            post_process.lut = visual_specs.get("lut_profile", post_process.lut)
            post_process.vignette = visual_specs.get("vignette", post_process.vignette)
            post_process.grain = visual_specs.get("grain", post_process.grain)
            post_process.bloom = visual_specs.get("bloom", post_process.bloom)
        
        # Compile final manifest
        manifest = {
            "status": "compiled",
            "metadata": {
                "emotion": emotion,
                "intensity": intensity,
                "visual_style": visual_style or "default",
                "description": profile.get("description", "")
            },
            "render_manifest": {
                "camera": asdict(camera),
                "lighting": asdict(lighting),
                "post_process": asdict(post_process),
                "audio": asdict(audio),
                "grid": asdict(grid)
            },
            "vfx_effects": profile.get("vfx", []),
            "ffmpeg_filter": profile.get("ffmpeg", "null")
        }
        
        logger.info(f"✓ Compiled render manifest: {emotion} ({intensity})")
        return manifest
    
    def compile_from_prompt(self, prompt: str) -> Dict:
        """
        Compile render manifest from natural language prompt
        
        Args:
            prompt: Natural language description
            
        Returns:
            Complete render manifest dictionary
        """
        from prompt_parser import PromptParser
        
        parser = PromptParser()
        chunks = parser.parse(prompt)
        params = parser.extract_parameters(chunks)
        
        emotion = params.get("mood", "curiosity")
        intensity = params.get("intensity", "medium")
        visual_style = params.get("visual_style")
        
        return self.compile(emotion, intensity, visual_style)
    
    def compile_split_stream(self, merged_manifest: Dict, aesthetic_tensor: 'AestheticTensor',
                            kinetic_tensor: 'KineticTensor', prompt: str) -> Dict:
        """
        NEW: Compile unified render manifest from split-stream protocol
        Ensures Emotional Index intensity aligns lighting temperature with physical action speed
        
        Args:
            merged_manifest: Merged result from vertex convergence
            aesthetic_tensor: Original aesthetic tensor
            kinetic_tensor: Original kinetic tensor
            prompt: Original user prompt
            
        Returns:
            Complete unified render manifest for Blender/Unreal
        """
        logger.info("⟳ Compiling split-stream manifest")
        
        # === STEP 1: Extract Merged Components ===
        camera_data = merged_manifest.get("camera", {})
        lighting_data = merged_manifest.get("lighting", {})
        color_data = merged_manifest.get("post_process", {})
        audio_data = merged_manifest.get("audio", {})
        grid_data = merged_manifest.get("grid", {})
        physics_data = merged_manifest.get("physics", {})
        geometry_data = merged_manifest.get("geometry", {})
        scene_data = merged_manifest.get("scene", {})
        timing_data = merged_manifest.get("timing", {})
        
        # === STEP 2: Align Emotional Index Intensity with Action Speed ===
        # This is the critical alignment: lighting temperature ↔ physical action speed
        
        # Get intensity from aesthetic tensor
        intensity = aesthetic_tensor.intensity if aesthetic_tensor else "medium"
        
        # Get action speed from timing data
        speed_multiplier = timing_data.get("speed_multiplier", 1.0)
        
        # Align lighting temperature with action speed
        base_kelvin = lighting_data.get("kelvin", lighting_data.get("color_temperature_kelvin", 5600))
        
        if intensity == "heavy":
            # Heavy intensity = dramatic lighting
            if speed_multiplier > 1.5:  # Fast action
                # Fast + heavy = warm, high-energy (action scenes)
                adjusted_kelvin = base_kelvin + 400  # Warmer
                lighting_intensity = 1.3
            else:  # Slow action
                # Slow + heavy = cool, ominous (suspense scenes)
                adjusted_kelvin = base_kelvin - 400  # Cooler
                lighting_intensity = 1.1
        elif intensity == "light":
            # Light intensity = subtle lighting
            if speed_multiplier > 1.5:  # Fast action
                # Fast + light = neutral, energetic (chase scenes)
                adjusted_kelvin = base_kelvin + 200
                lighting_intensity = 0.9
            else:  # Slow action
                # Slow + light = soft, contemplative (dialogue scenes)
                adjusted_kelvin = base_kelvin - 200
                lighting_intensity = 0.7
        else:  # medium
            # Medium intensity = balanced lighting
            adjusted_kelvin = base_kelvin
            lighting_intensity = 1.0
        
        # Update lighting with aligned values
        lighting_data["color_temperature_kelvin"] = adjusted_kelvin
        lighting_data["intensity"] = lighting_intensity
        
        # === STEP 3: Create Structured Manifests ===
        
        # Camera manifest
        camera = CameraManifest(
            focal_length_mm=camera_data.get("focal_length", camera_data.get("focal_length_mm", 50)),
            aperture=camera_data.get("aperture", "T2.8"),
            sensor_crop=camera_data.get("sensor_crop", 1.0),
            shutter_angle=camera_data.get("shutter_angle", 180),
            movement=camera_data.get("movement", "Static"),
            angle=camera_data.get("angle", "Eye Level"),
            speed=camera_data.get("speed", 0.0)
        )
        
        # Lighting manifest
        lighting = LightingManifest(
            key_fill_ratio=lighting_data.get("ratio", lighting_data.get("key_fill_ratio", "4:1")),
            color_temperature_kelvin=adjusted_kelvin,
            iso=lighting_data.get("iso", 800),
            intensity=lighting_intensity
        )
        
        # Post-process manifest
        post_process = PostProcessManifest(
            lut=color_data.get("lut", color_data.get("lut_ref", "rec709")),
            saturation=color_data.get("saturation", 1.0),
            contrast=color_data.get("contrast", 1.0),
            vignette=color_data.get("vignette", 0.2),
            bloom=color_data.get("bloom", 0.0),
            grain=color_data.get("grain", 0.1),
            chromatic_aberration=color_data.get("chromatic_aberration", 0.0)
        )
        
        # Audio manifest
        audio = AudioManifest(
            profile=audio_data.get("profile", "Neutral Ambient"),
            reverb=audio_data.get("reverb", "Medium Room"),
            mix=audio_data.get("mix", "Stereo")
        )
        
        # Grid manifest
        grid = GridManifest(
            composition=grid_data.get("composition", "Rule of Thirds"),
            focus_zone=grid_data.get("focus_zone", "Center Weighted"),
            negative_space=grid_data.get("negative_space", "Balanced")
        )
        
        # === STEP 4: Generate Description ===
        description = self._generate_split_stream_description(
            aesthetic_tensor,
            kinetic_tensor,
            intensity,
            speed_multiplier
        )
        
        # === STEP 5: Compile Final Unified Manifest ===
        unified_manifest = {
            "status": "compiled",
            "source": "SPLIT_STREAM",
            "protocol": "Hybrid-SOTA Split-Stream",
            "metadata": {
                "prompt": prompt,
                "description": description,
                "aesthetic_tensor": aesthetic_tensor.to_dict() if aesthetic_tensor else {},
                "kinetic_tensor": kinetic_tensor.to_dict() if kinetic_tensor else {},
                "intensity": intensity,
                "speed_multiplier": speed_multiplier,
                "alignment": {
                    "base_kelvin": base_kelvin,
                    "adjusted_kelvin": adjusted_kelvin,
                    "kelvin_shift": adjusted_kelvin - base_kelvin,
                    "lighting_intensity": lighting_intensity
                }
            },
            "render_manifest": {
                "camera": asdict(camera),
                "lighting": asdict(lighting),
                "post_process": asdict(post_process),
                "audio": asdict(audio),
                "grid": asdict(grid)
            },
            "physics": physics_data,
            "geometry": geometry_data,
            "scene": scene_data,
            "timing": timing_data,
            "ffmpeg_filter": self._generate_ffmpeg_from_split_stream(camera, lighting, post_process)
        }
        
        logger.info(f"✓ Split-stream manifest compiled (Kelvin: {base_kelvin}K → {adjusted_kelvin}K)")
        return unified_manifest
    
    def _generate_split_stream_description(self, aesthetic_tensor: 'AestheticTensor',
                                          kinetic_tensor: 'KineticTensor',
                                          intensity: str, speed_multiplier: float) -> str:
        """
        Generate natural language description of split-stream result
        """
        parts = []
        
        # Aesthetic description
        if aesthetic_tensor and not aesthetic_tensor.is_empty():
            if aesthetic_tensor.mood:
                parts.append(f"{aesthetic_tensor.mood} mood")
            if aesthetic_tensor.director_reference:
                parts.append(f"{aesthetic_tensor.director_reference} style")
            if aesthetic_tensor.visual_style:
                parts.append(f"{aesthetic_tensor.visual_style} aesthetic")
        
        # Kinetic description
        if kinetic_tensor and not kinetic_tensor.is_empty():
            if kinetic_tensor.actions:
                parts.append(f"with {', '.join(kinetic_tensor.actions[:3])}")
            if kinetic_tensor.objects:
                parts.append(f"featuring {', '.join(kinetic_tensor.objects[:3])}")
        
        # Intensity and speed
        speed_desc = "fast-paced" if speed_multiplier > 1.5 else ("slow-paced" if speed_multiplier < 0.7 else "medium-paced")
        parts.append(f"{intensity} intensity, {speed_desc}")
        
        return "Scene with " + ", ".join(parts) if parts else "Default scene"
    
    def _generate_ffmpeg_from_split_stream(self, camera: CameraManifest,
                                          lighting: LightingManifest,
                                          post: PostProcessManifest) -> str:
        """
        Generate FFmpeg filter chain from split-stream manifest
        """
        filters = []
        
        # Color temperature adjustment
        kelvin = lighting.color_temperature_kelvin
        if kelvin < 4000:  # Warm
            filters.append("colorbalance=rs=0.15:gs=0.05:bs=-0.1")
        elif kelvin > 6000:  # Cool
            filters.append("colorbalance=rs=-0.1:gs=0.0:bs=0.15")
        
        # Saturation
        if post.saturation != 1.0:
            filters.append(f"eq=saturation={post.saturation}")
        
        # Contrast
        if post.contrast != 1.0:
            filters.append(f"eq=contrast={post.contrast}")
        
        # Vignette
        if post.vignette > 0:
            filters.append(f"vignette='PI/4*{post.vignette}'")
        
        # Grain
        if post.grain > 0:
            grain_strength = int(post.grain * 50)
            filters.append(f"noise=alls={grain_strength}:allf=t")
        
        # Bloom
        if post.bloom > 0:
            filters.append(f"eq=brightness={post.bloom * 0.2}")
        
        return ",".join(filters) if filters else "null"
    
    def export_blender_script(self, manifest: Dict, output_path: str) -> str:
        """
        Export Blender Python script from manifest
        
        Args:
            manifest: Render manifest dictionary
            output_path: Path to save Blender script
            
        Returns:
            Path to generated script
        """
        render = manifest.get("render_manifest", {})
        camera = render.get("camera", {})
        lighting = render.get("lighting", {})
        post = render.get("post_process", {})
        
        script = f'''"""
Blender Auto-Generated Cinematography Script
Generated from Elite Video Pipeline v3.0
"""

import bpy

# Camera Setup
camera = bpy.data.cameras.new("AutoCamera")
camera.lens = {camera.get("focal_length_mm", 50)}
camera.sensor_width = 36.0  # Full frame
camera.dof.aperture_fstop = {self._parse_aperture(camera.get("aperture", "T2.8"))}

camera_obj = bpy.data.objects.new("AutoCamera", camera)
bpy.context.scene.collection.objects.link(camera_obj)
bpy.context.scene.camera = camera_obj

# Lighting Setup
key_light = bpy.data.lights.new("KeyLight", "AREA")
key_light.energy = {self._calculate_key_energy(lighting.get("key_fill_ratio", "4:1"))}
key_light.color = {self._kelvin_to_rgb(lighting.get("color_temperature_kelvin", 5600))}

key_obj = bpy.data.objects.new("KeyLight", key_light)
bpy.context.scene.collection.objects.link(key_obj)
key_obj.location = (5, -5, 5)

# Fill Light
fill_light = bpy.data.lights.new("FillLight", "AREA")
fill_light.energy = {self._calculate_fill_energy(lighting.get("key_fill_ratio", "4:1"))}
fill_light.color = {self._kelvin_to_rgb(lighting.get("color_temperature_kelvin", 5600))}

fill_obj = bpy.data.objects.new("FillLight", fill_light)
bpy.context.scene.collection.objects.link(fill_obj)
fill_obj.location = (-5, -5, 3)

# Compositor Setup (Post-Process)
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
tree.nodes.clear()

render_layers = tree.nodes.new("CompositorNodeRLayers")
composite = tree.nodes.new("CompositorNodeComposite")

# Saturation
saturation_node = tree.nodes.new("CompositorNodeHueSat")
saturation_node.inputs["Saturation"].default_value = {post.get("saturation", 1.0)}

# Vignette
if {post.get("vignette", 0.0)} > 0:
    vignette_node = tree.nodes.new("CompositorNodeLensdist")
    vignette_node.inputs["Dispersion"].default_value = {post.get("vignette", 0.0)}

# Link nodes
tree.links.new(render_layers.outputs["Image"], saturation_node.inputs["Image"])
tree.links.new(saturation_node.outputs["Image"], composite.inputs["Image"])

print("✓ Cinematography applied to Blender scene")
'''
        
        with open(output_path, 'w') as f:
            f.write(script)
        
        logger.info(f"✓ Exported Blender script: {output_path}")
        return output_path
    
    def _parse_aperture(self, aperture: str) -> float:
        """Parse T-stop to f-stop value"""
        # T2.8 → 2.8
        return float(aperture.replace("T", ""))
    
    def _calculate_key_energy(self, ratio: str) -> float:
        """Calculate key light energy from ratio"""
        parts = ratio.split(":")
        key = float(parts[0])
        return key * 100.0  # Blender energy units
    
    def _calculate_fill_energy(self, ratio: str) -> float:
        """Calculate fill light energy from ratio"""
        parts = ratio.split(":")
        fill = float(parts[1])
        return fill * 100.0  # Blender energy units
    
    def _kelvin_to_rgb(self, kelvin: int) -> tuple:
        """Convert Kelvin to RGB color"""
        # Simplified conversion for Blender
        if kelvin < 3500:
            return (1.0, 0.8, 0.6)  # Warm
        elif kelvin > 6000:
            return (0.8, 0.9, 1.0)  # Cool
        else:
            return (1.0, 1.0, 1.0)  # Neutral


def create_compiler(redis_client=None) -> RenderManifestCompiler:
    """Factory function to create compiler"""
    return RenderManifestCompiler(redis_client)


if __name__ == "__main__":
    # Test render manifest compilation
    compiler = create_compiler()
    
    # Test 1: Compile from emotion
    print("\n=== TEST 1: Compile from emotion ===")
    manifest = compiler.compile("melancholy", "heavy", "future_noir")
    print(json.dumps(manifest, indent=2))
    
    # Test 2: Compile from prompt
    print("\n=== TEST 2: Compile from prompt ===")
    manifest = compiler.compile_from_prompt("Make this scene feel like a funeral in the year 2049")
    print(json.dumps(manifest, indent=2))
    
    # Test 3: Export Blender script
    print("\n=== TEST 3: Export Blender script ===")
    script_path = "/tmp/blender_cinematography.py"
    compiler.export_blender_script(manifest, script_path)
    print(f"✓ Blender script exported to: {script_path}")
