"""
Elite Video Pipeline v3.0 - Prompt Parser (MicroChunker)
Intelligent prompt parsing for lazy-loading cinematography modules
Detects mood keywords and visual references to minimize resource usage
"""

import logging
import re
from typing import List, Dict
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PromptChunk:
    """Parsed chunk from prompt"""
    chunk_type: str  # "mood", "visual_ref", "intensity", "technical"
    value: str
    confidence: float  # 0.0-1.0


class PromptParser:
    """
    MicroChunker: Intelligent prompt parsing for lazy-loading
    Detects emotional moods and visual references from natural language
    """
    
    def __init__(self):
        # Mood keyword mapping
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
        
        # Visual style keyword mapping
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
        
        # Intensity keywords
        self.intensity_keywords = {
            "light": ["subtle", "slight", "gentle", "mild", "soft", "light"],
            "medium": ["moderate", "medium", "balanced", "normal"],
            "heavy": ["intense", "strong", "heavy", "extreme", "dramatic", "powerful"]
        }
        
        # Technical keywords (camera, lighting, color)
        self.technical_keywords = {
            "camera": ["zoom", "pan", "tilt", "dolly", "crane", "handheld", "static", "tracking"],
            "lighting": ["lighting", "shadows", "contrast", "key light", "fill light", "backlight"],
            "color": ["color", "grade", "saturation", "temperature", "warm", "cool", "lut"]
        }
    
    def parse(self, prompt: str) -> List[PromptChunk]:
        """
        Parse prompt into chunks for lazy-loading
        
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
    
    def _detect_mood(self, prompt: str) -> PromptChunk:
        """Detect emotional mood from prompt"""
        best_match = None
        best_confidence = 0.0
        
        for mood, keywords in self.mood_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    # Calculate confidence based on keyword specificity
                    confidence = len(keyword) / 20.0  # Longer keywords = higher confidence
                    confidence = min(confidence, 1.0)
                    
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = mood
        
        if best_match:
            return PromptChunk(
                chunk_type="mood",
                value=best_match,
                confidence=best_confidence
            )
        
        return None
    
    def _detect_visual_style(self, prompt: str) -> PromptChunk:
        """Detect visual style reference from prompt"""
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
        
        if best_match:
            return PromptChunk(
                chunk_type="visual_ref",
                value=best_match,
                confidence=best_confidence
            )
        
        return None
    
    def _detect_intensity(self, prompt: str) -> PromptChunk:
        """Detect intensity level from prompt"""
        for intensity, keywords in self.intensity_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    return PromptChunk(
                        chunk_type="intensity",
                        value=intensity,
                        confidence=0.9
                    )
        
        # Default to medium if not specified
        return PromptChunk(
            chunk_type="intensity",
            value="medium",
            confidence=0.5
        )
    
    def _detect_technical(self, prompt: str) -> List[PromptChunk]:
        """Detect technical requirements from prompt"""
        chunks = []
        
        for tech_type, keywords in self.technical_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    chunks.append(PromptChunk(
                        chunk_type="technical",
                        value=f"{tech_type}:{keyword}",
                        confidence=0.8
                    ))
        
        return chunks
    
    def extract_parameters(self, chunks: List[PromptChunk]) -> Dict:
        """
        Extract structured parameters from chunks
        
        Args:
            chunks: List of parsed chunks
            
        Returns:
            Dictionary with mood, visual_style, intensity, technical
        """
        params = {
            "mood": None,
            "visual_style": None,
            "intensity": "medium",  # Default
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
        Generate Redis cache key from chunks
        
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
    # Test prompt parser
    parser = create_parser()
    
    # Test cases
    test_prompts = [
        "Make this scene feel like a funeral in the year 2049",
        "I want a sad and lonely vibe with blade runner aesthetics",
        "Create an intense horror scene with heavy shadows",
        "Gentle nostalgic feeling like old home movies",
        "Epic fantasy battle with dramatic lighting"
    ]
    
    print("\n=== PROMPT PARSER TEST ===\n")
    
    for prompt in test_prompts:
        print(f"Prompt: \"{prompt}\"")
        chunks = parser.parse(prompt)
        
        print(f"  Chunks detected: {len(chunks)}")
        for chunk in chunks:
            print(f"    - {chunk.chunk_type}: {chunk.value} (confidence: {chunk.confidence:.2f})")
        
        params = parser.extract_parameters(chunks)
        print(f"  Parameters: {params}")
        
        cache_key = parser.generate_cache_key(chunks)
        print(f"  Cache key: {cache_key}\n")
