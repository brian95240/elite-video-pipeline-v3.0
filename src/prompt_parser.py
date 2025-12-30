"""
Elite Video Pipeline v3.0 - Prompt Parser (MicroChunker)
Hybrid-SOTA Split-Stream Protocol: Dual-stream micro-chunking
Separates Aesthetic Tensors from Kinetic Tensors for optimized routing
"""

import logging
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PromptChunk:
    """Parsed chunk from prompt"""
    chunk_type: str  # "mood", "visual_ref", "intensity", "technical"
    value: str
    confidence: float  # 0.0-1.0


@dataclass
class AestheticTensor:
    """
    Stream A: Abstract stylistic data for Oracle processing
    Contains only aesthetic/emotional/stylistic information
    """
    mood: str = None
    visual_style: str = None
    intensity: str = "medium"
    lighting_mood: str = None  # e.g., "soft", "harsh", "dramatic"
    film_grain: str = None  # e.g., "35mm", "16mm", "digital"
    camera_motion_type: str = None  # e.g., "static", "handheld", "crane"
    director_reference: str = None  # e.g., "Wes Anderson", "Tarantino"
    color_palette: str = None  # e.g., "pastel", "monochrome", "saturated"
    audio_profile: str = None  # e.g., "ambient", "dramatic", "minimalist"
    technical_style: List[str] = None  # e.g., ["shallow DOF", "wide angle"]
    
    def __post_init__(self):
        if self.technical_style is None:
            self.technical_style = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API transmission"""
        return {
            "mood": self.mood,
            "visual_style": self.visual_style,
            "intensity": self.intensity,
            "lighting_mood": self.lighting_mood,
            "film_grain": self.film_grain,
            "camera_motion_type": self.camera_motion_type,
            "director_reference": self.director_reference,
            "color_palette": self.color_palette,
            "audio_profile": self.audio_profile,
            "technical_style": self.technical_style
        }
    
    def is_empty(self) -> bool:
        """Check if tensor has any meaningful data"""
        return not any([
            self.mood, self.visual_style, self.lighting_mood,
            self.film_grain, self.camera_motion_type, self.director_reference,
            self.color_palette, self.audio_profile, self.technical_style
        ])


@dataclass
class KineticTensor:
    """
    Stream B: Physical/geometric data for local processing
    Contains only physics, geometry, and action information
    """
    objects: List[str] = None  # Physical objects in scene
    actors: List[Dict] = None  # Actor positions and attributes
    actions: List[str] = None  # Action verbs (running, jumping, fighting)
    blocking: Dict = None  # Spatial blocking data
    movements: List[Dict] = None  # Movement vectors and velocities
    velocities: List[float] = None  # Speed data
    collision_data: Dict = None  # Collision/interaction data
    spatial_coordinates: Dict = None  # 3D coordinate system
    timing: Dict = None  # Temporal data (duration, pacing)
    physics_constraints: List[str] = None  # Physical limitations
    
    def __post_init__(self):
        if self.objects is None:
            self.objects = []
        if self.actors is None:
            self.actors = []
        if self.actions is None:
            self.actions = []
        if self.movements is None:
            self.movements = []
        if self.velocities is None:
            self.velocities = []
        if self.physics_constraints is None:
            self.physics_constraints = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API transmission"""
        return {
            "objects": self.objects,
            "actors": self.actors,
            "actions": self.actions,
            "blocking": self.blocking,
            "movements": self.movements,
            "velocities": self.velocities,
            "collision_data": self.collision_data,
            "spatial_coordinates": self.spatial_coordinates,
            "timing": self.timing,
            "physics_constraints": self.physics_constraints
        }
    
    def is_empty(self) -> bool:
        """Check if tensor has any meaningful data"""
        return not any([
            self.objects, self.actors, self.actions, self.blocking,
            self.movements, self.velocities, self.collision_data,
            self.spatial_coordinates, self.timing, self.physics_constraints
        ])


class PromptParser:
    """
    MicroChunker: Intelligent prompt parsing with Hybrid-SOTA Split-Stream Protocol
    Separates aesthetic reasoning from geometric computation
    """
    
    def __init__(self):
        # Mood keyword mapping (Aesthetic)
        self.mood_keywords = {
            "melancholy": ["sad", "lonely", "depressed", "melancholy", "somber", "gloomy", "mournful"],
            "fear": ["scared", "afraid", "terrified", "fearful", "anxious", "dread", "horror"],
            "tension": ["tense", "suspense", "anticipation", "edge", "nervous", "uneasy"],
            "rage": ["angry", "furious", "rage", "mad", "enraged", "violent", "aggressive"],
            "curiosity": ["curious", "intrigued", "wondering", "investigating", "exploring"],
            "wonder": ["awe", "wonder", "amazed", "astonished", "magical", "breathtaking"],
            "serenity": ["calm", "peaceful", "serene", "tranquil", "relaxed", "zen"],
            "triumph": ["victory", "triumph", "winning", "success", "champion", "glorious"],
            "nostalgia": ["nostalgic", "memories", "past", "reminiscing", "vintage", "retro"],
            "joy": ["happy", "joyful", "delighted", "cheerful", "ecstatic", "blissful"],
            "urgency": ["urgent", "rush", "hurry", "fast", "quick", "emergency"],
            "mystery": ["mysterious", "enigmatic", "cryptic", "unknown", "secretive"]
        }
        
        # Visual style keyword mapping (Aesthetic)
        self.visual_keywords = {
            "future_noir": ["blade runner", "cyberpunk", "neo-noir", "dystopian", "2049"],
            "cyberpunk": ["cyberpunk", "neon", "tech noir", "futuristic city"],
            "golden_age": ["golden age", "classic hollywood", "technicolor", "vintage film"],
            "horror": ["horror", "scary", "creepy", "haunted", "nightmare"],
            "epic_fantasy": ["epic", "fantasy", "lord of the rings", "heroic", "mythical"],
            "documentary": ["documentary", "realistic", "natural", "observational"],
            "music_video": ["music video", "stylized", "abstract", "artistic"],
            "noir": ["noir", "black and white", "high contrast", "detective"]
        }
        
        # Director references (Aesthetic)
        self.director_keywords = {
            "wes_anderson": ["wes anderson", "anderson", "symmetrical", "pastel", "whimsical"],
            "tarantino": ["tarantino", "pulp fiction", "reservoir dogs", "stylized violence"],
            "nolan": ["nolan", "christopher nolan", "inception", "interstellar", "dark knight"],
            "kubrick": ["kubrick", "stanley kubrick", "2001", "shining", "clockwork orange"],
            "villeneuve": ["villeneuve", "denis villeneuve", "arrival", "dune"],
            "fincher": ["fincher", "david fincher", "fight club", "se7en", "social network"],
            "spielberg": ["spielberg", "steven spielberg", "jaws", "et", "jurassic park"],
            "scorsese": ["scorsese", "martin scorsese", "goodfellas", "taxi driver"]
        }
        
        # Lighting mood (Aesthetic)
        self.lighting_keywords = {
            "soft": ["soft light", "diffused", "gentle", "natural light"],
            "harsh": ["harsh light", "hard light", "dramatic shadows", "high contrast"],
            "dramatic": ["dramatic lighting", "chiaroscuro", "moody", "theatrical"],
            "natural": ["natural", "daylight", "ambient", "realistic"],
            "neon": ["neon", "colorful", "vibrant", "glowing"],
            "low_key": ["low key", "dark", "shadowy", "noir lighting"],
            "high_key": ["high key", "bright", "even", "flat lighting"]
        }
        
        # Film grain (Aesthetic)
        self.film_grain_keywords = {
            "35mm": ["35mm", "film grain", "cinematic", "grainy"],
            "16mm": ["16mm", "documentary style", "rough grain"],
            "digital": ["digital", "clean", "sharp", "crisp"],
            "8mm": ["8mm", "home movie", "vintage", "super 8"]
        }
        
        # Camera motion type (Aesthetic)
        self.camera_motion_keywords = {
            "static": ["static", "locked off", "tripod", "still"],
            "handheld": ["handheld", "shaky", "documentary", "raw"],
            "crane": ["crane", "jib", "sweeping", "aerial"],
            "dolly": ["dolly", "tracking", "smooth", "gliding"],
            "steadicam": ["steadicam", "floating", "fluid"],
            "zoom": ["zoom", "zooming", "push in", "pull out"]
        }
        
        # Color palette (Aesthetic)
        self.color_palette_keywords = {
            "pastel": ["pastel", "soft colors", "muted", "desaturated"],
            "monochrome": ["monochrome", "black and white", "grayscale"],
            "saturated": ["saturated", "vibrant", "bold colors", "vivid"],
            "warm": ["warm tones", "orange", "golden", "sunset"],
            "cool": ["cool tones", "blue", "teal", "cold"],
            "neon": ["neon colors", "electric", "fluorescent"]
        }
        
        # Intensity keywords (Aesthetic)
        self.intensity_keywords = {
            "light": ["subtle", "slight", "gentle", "mild", "soft", "light"],
            "medium": ["moderate", "medium", "balanced", "normal"],
            "heavy": ["intense", "strong", "heavy", "extreme", "dramatic", "powerful"]
        }
        
        # Action verbs (Kinetic)
        self.action_keywords = [
            "running", "jumping", "fighting", "walking", "dancing", "falling",
            "climbing", "swimming", "flying", "driving", "shooting", "punching",
            "kicking", "throwing", "catching", "dodging", "rolling", "sliding",
            "crawling", "spinning", "leaping", "diving", "charging", "attacking",
            "defending", "blocking", "striking", "grappling", "chasing", "fleeing"
        ]
        
        # Object keywords (Kinetic)
        self.object_keywords = [
            "car", "building", "tree", "table", "chair", "door", "window",
            "weapon", "gun", "sword", "knife", "vehicle", "motorcycle", "truck",
            "helicopter", "plane", "boat", "ship", "train", "bicycle",
            "furniture", "wall", "floor", "ceiling", "stairs", "elevator",
            "computer", "phone", "screen", "monitor", "keyboard", "mouse"
        ]
        
        # Movement descriptors (Kinetic)
        self.movement_keywords = {
            "fast": ["fast", "quick", "rapid", "swift", "speedy"],
            "slow": ["slow", "gradual", "leisurely", "unhurried"],
            "smooth": ["smooth", "fluid", "graceful", "flowing"],
            "jerky": ["jerky", "abrupt", "sudden", "sharp"],
            "circular": ["circular", "rotating", "spinning", "revolving"],
            "linear": ["linear", "straight", "direct"]
        }
        
        # Spatial keywords (Kinetic)
        self.spatial_keywords = [
            "left", "right", "up", "down", "forward", "backward",
            "north", "south", "east", "west", "above", "below",
            "near", "far", "close", "distant", "center", "corner",
            "edge", "middle", "top", "bottom", "front", "back"
        ]
    
    def parse(self, prompt: str) -> List[PromptChunk]:
        """
        Parse prompt into chunks for lazy-loading (backward compatibility)
        
        Args:
            prompt: Natural language prompt
            
        Returns:
            List of PromptChunk objects
        """
        chunks = []
        prompt_lower = prompt.lower()
        
        # Detect mood
        mood_chunk = self._detect_mood(prompt_lower)
        if mood_chunk:
            chunks.append(mood_chunk)
        
        # Detect visual style
        visual_chunk = self._detect_visual_style(prompt_lower)
        if visual_chunk:
            chunks.append(visual_chunk)
        
        # Detect intensity
        intensity_chunk = self._detect_intensity(prompt_lower)
        if intensity_chunk:
            chunks.append(intensity_chunk)
        
        # Detect technical requirements
        technical_chunks = self._detect_technical(prompt_lower)
        chunks.extend(technical_chunks)
        
        logger.info(f"Parsed {len(chunks)} chunks from prompt")
        return chunks
    
    def parse_split_stream(self, prompt: str) -> Tuple[AestheticTensor, KineticTensor]:
        """
        NEW: Hybrid-SOTA Split-Stream Protocol
        Parse prompt into separate Aesthetic and Kinetic tensors
        
        Args:
            prompt: Natural language prompt
            
        Returns:
            Tuple of (AestheticTensor, KineticTensor)
        """
        prompt_lower = prompt.lower()
        
        # Initialize tensors
        aesthetic = AestheticTensor()
        kinetic = KineticTensor()
        
        # === AESTHETIC TENSOR EXTRACTION ===
        
        # Detect mood
        aesthetic.mood = self._extract_mood(prompt_lower)
        
        # Detect visual style
        aesthetic.visual_style = self._extract_visual_style(prompt_lower)
        
        # Detect intensity
        aesthetic.intensity = self._extract_intensity(prompt_lower)
        
        # Detect lighting mood
        aesthetic.lighting_mood = self._extract_lighting_mood(prompt_lower)
        
        # Detect film grain
        aesthetic.film_grain = self._extract_film_grain(prompt_lower)
        
        # Detect camera motion type
        aesthetic.camera_motion_type = self._extract_camera_motion(prompt_lower)
        
        # Detect director reference
        aesthetic.director_reference = self._extract_director(prompt_lower)
        
        # Detect color palette
        aesthetic.color_palette = self._extract_color_palette(prompt_lower)
        
        # Detect technical style
        aesthetic.technical_style = self._extract_technical_style(prompt_lower)
        
        # === KINETIC TENSOR EXTRACTION ===
        
        # Extract objects
        kinetic.objects = self._extract_objects(prompt_lower)
        
        # Extract actions
        kinetic.actions = self._extract_actions(prompt_lower)
        
        # Extract movements
        kinetic.movements = self._extract_movements(prompt_lower)
        
        # Extract spatial data
        kinetic.spatial_coordinates = self._extract_spatial_data(prompt_lower)
        
        # Extract timing/velocity hints
        kinetic.velocities = self._extract_velocities(prompt_lower)
        
        # Log split results
        logger.info(f"Split-Stream Parse Complete:")
        logger.info(f"  Aesthetic Tensor: {not aesthetic.is_empty()}")
        logger.info(f"  Kinetic Tensor: {not kinetic.is_empty()}")
        
        return aesthetic, kinetic
    
    # === AESTHETIC EXTRACTION METHODS ===
    
    def _extract_mood(self, prompt: str) -> str:
        """Extract mood from prompt"""
        best_match = None
        best_confidence = 0.0
        
        for mood, keywords in self.mood_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    confidence = len(keyword) / 20.0
                    confidence = min(confidence, 1.0)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = mood
        
        return best_match
    
    def _extract_visual_style(self, prompt: str) -> str:
        """Extract visual style from prompt"""
        best_match = None
        best_confidence = 0.0
        
        for style, keywords in self.visual_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    confidence = len(keyword) / 20.0
                    confidence = min(confidence, 1.0)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = style
        
        return best_match
    
    def _extract_intensity(self, prompt: str) -> str:
        """Extract intensity from prompt"""
        for intensity, keywords in self.intensity_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    return intensity
        return "medium"  # Default
    
    def _extract_lighting_mood(self, prompt: str) -> str:
        """Extract lighting mood from prompt"""
        for mood, keywords in self.lighting_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    return mood
        return None
    
    def _extract_film_grain(self, prompt: str) -> str:
        """Extract film grain type from prompt"""
        for grain, keywords in self.film_grain_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    return grain
        return None
    
    def _extract_camera_motion(self, prompt: str) -> str:
        """Extract camera motion type from prompt"""
        for motion, keywords in self.camera_motion_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    return motion
        return None
    
    def _extract_director(self, prompt: str) -> str:
        """Extract director reference from prompt"""
        for director, keywords in self.director_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    return director
        return None
    
    def _extract_color_palette(self, prompt: str) -> str:
        """Extract color palette from prompt"""
        for palette, keywords in self.color_palette_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    return palette
        return None
    
    def _extract_technical_style(self, prompt: str) -> List[str]:
        """Extract technical style elements from prompt"""
        technical = []
        
        # Aperture/DOF
        if any(word in prompt for word in ["shallow", "bokeh", "blur"]):
            technical.append("shallow_dof")
        if any(word in prompt for word in ["deep focus", "sharp"]):
            technical.append("deep_focus")
        
        # Lens choice
        if any(word in prompt for word in ["wide angle", "wide lens"]):
            technical.append("wide_angle")
        if any(word in prompt for word in ["telephoto", "long lens"]):
            technical.append("telephoto")
        if any(word in prompt for word in ["fisheye"]):
            technical.append("fisheye")
        
        return technical
    
    # === KINETIC EXTRACTION METHODS ===
    
    def _extract_objects(self, prompt: str) -> List[str]:
        """Extract physical objects from prompt"""
        objects = []
        for obj in self.object_keywords:
            if obj in prompt:
                objects.append(obj)
        return objects
    
    def _extract_actions(self, prompt: str) -> List[str]:
        """Extract action verbs from prompt"""
        actions = []
        for action in self.action_keywords:
            if action in prompt:
                actions.append(action)
        return actions
    
    def _extract_movements(self, prompt: str) -> List[Dict]:
        """Extract movement descriptors from prompt"""
        movements = []
        for movement_type, keywords in self.movement_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    movements.append({
                        "type": movement_type,
                        "descriptor": keyword
                    })
        return movements
    
    def _extract_spatial_data(self, prompt: str) -> Dict:
        """Extract spatial coordinates/directions from prompt"""
        spatial = {
            "directions": [],
            "positions": []
        }
        
        for spatial_word in self.spatial_keywords:
            if spatial_word in prompt:
                if spatial_word in ["left", "right", "up", "down", "forward", "backward"]:
                    spatial["directions"].append(spatial_word)
                else:
                    spatial["positions"].append(spatial_word)
        
        return spatial if (spatial["directions"] or spatial["positions"]) else None
    
    def _extract_velocities(self, prompt: str) -> List[float]:
        """Extract velocity/speed hints from prompt"""
        velocities = []
        
        # Simple heuristic: fast = 2.0, slow = 0.5, normal = 1.0
        if any(word in prompt for word in ["fast", "quick", "rapid", "swift"]):
            velocities.append(2.0)
        elif any(word in prompt for word in ["slow", "gradual", "leisurely"]):
            velocities.append(0.5)
        else:
            velocities.append(1.0)  # Normal speed
        
        return velocities
    
    # === BACKWARD COMPATIBILITY METHODS ===
    
    def _detect_mood(self, prompt: str) -> PromptChunk:
        """Detect emotional mood from prompt (backward compatibility)"""
        mood = self._extract_mood(prompt)
        if mood:
            return PromptChunk(
                chunk_type="mood",
                value=mood,
                confidence=0.8
            )
        return None
    
    def _detect_visual_style(self, prompt: str) -> PromptChunk:
        """Detect visual style reference from prompt (backward compatibility)"""
        style = self._extract_visual_style(prompt)
        if style:
            return PromptChunk(
                chunk_type="visual_ref",
                value=style,
                confidence=0.8
            )
        return None
    
    def _detect_intensity(self, prompt: str) -> PromptChunk:
        """Detect intensity level from prompt (backward compatibility)"""
        intensity = self._extract_intensity(prompt)
        return PromptChunk(
            chunk_type="intensity",
            value=intensity,
            confidence=0.9 if intensity != "medium" else 0.5
        )
    
    def _detect_technical(self, prompt: str) -> List[PromptChunk]:
        """Detect technical requirements from prompt (backward compatibility)"""
        chunks = []
        technical = self._extract_technical_style(prompt)
        for tech in technical:
            chunks.append(PromptChunk(
                chunk_type="technical",
                value=tech,
                confidence=0.8
            ))
        return chunks
    
    def extract_parameters(self, chunks: List[PromptChunk]) -> Dict:
        """
        Extract structured parameters from chunks (backward compatibility)
        
        Args:
            chunks: List of parsed chunks
            
        Returns:
            Dictionary with mood, visual_style, intensity, technical
        """
        params = {
            "mood": None,
            "visual_style": None,
            "intensity": "medium",
            "technical": []
        }
        
        for chunk in chunks:
            if chunk.chunk_type == "mood":
                params["mood"] = chunk.value
            elif chunk.chunk_type == "visual_ref":
                params["visual_style"] = chunk.value
            elif chunk.chunk_type == "intensity":
                params["intensity"] = chunk.value
            elif chunk.chunk_type == "technical":
                params["technical"].append(chunk.value)
        
        return params
    
    def generate_cache_key(self, chunks: List[PromptChunk]) -> str:
        """
        Generate Redis cache key from chunks (backward compatibility)
        
        Args:
            chunks: List of parsed chunks
            
        Returns:
            Cache key string
        """
        key_parts = []
        
        for chunk in chunks:
            key_parts.append(f"{chunk.chunk_type}:{chunk.value}")
        
        return "|".join(key_parts) if key_parts else "default"


def create_parser() -> PromptParser:
    """Factory function to create parser"""
    return PromptParser()


if __name__ == "__main__":
    # Test prompt parser with split-stream protocol
    parser = create_parser()
    
    # Test cases
    test_prompts = [
        "Make this scene feel like a funeral in the year 2049",
        "Two actors fighting with swords in a dark alley, Tarantino style",
        "A car chase through the city at night, fast and intense with neon lights",
        "Gentle nostalgic feeling like old home movies, person walking slowly through a park",
        "Epic fantasy battle with dramatic lighting, warriors charging forward with weapons"
    ]
    
    print("\n" + "=" * 80)
    print("HYBRID-SOTA SPLIT-STREAM PROTOCOL TEST")
    print("=" * 80 + "\n")
    
    for prompt in test_prompts:
        print(f"Prompt: \"{prompt}\"")
        print("-" * 80)
        
        # Parse with split-stream protocol
        aesthetic, kinetic = parser.parse_split_stream(prompt)
        
        print("\n[AESTHETIC TENSOR - Stream A → Oracle]")
        if not aesthetic.is_empty():
            for key, value in aesthetic.to_dict().items():
                if value:
                    print(f"  {key}: {value}")
        else:
            print("  (empty)")
        
        print("\n[KINETIC TENSOR - Stream B → Local Engine]")
        if not kinetic.is_empty():
            for key, value in kinetic.to_dict().items():
                if value:
                    print(f"  {key}: {value}")
        else:
            print("  (empty)")
        
        print("\n" + "=" * 80 + "\n")
