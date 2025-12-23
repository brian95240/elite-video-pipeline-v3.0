"""
Elite Video Pipeline v3.0 - Emotional Index
12 Archetypes: 7 Original (v2.0) + 5 New (v3.0)
Complete cinematographic profiles with camera, color, VFX, and audio layers
"""

EMOTIONAL_INDEX = {
    # --- ORIGINAL ARCHETYPES (v2.0) ---
    "curiosity": {
        "description": "Viewer investigating unknown",
        "camera": {
            "light": {"movement": "slow_zoom_in", "angle": "eye_level", "speed": 0.3, "focal_length": 35},
            "medium": {"movement": "dolly_forward", "angle": "slightly_low", "speed": 0.5, "focal_length": 50},
            "heavy": {"movement": "push_in_dramatic", "angle": "dutch_tilt_15deg", "speed": 0.8, "focal_length": 85}
        },
        "color": {
            "light": {"grade": "neutral_cool", "saturation": -5, "contrast": 1.05, "vignette": 0.1},
            "medium": {"grade": "mystery_teal", "saturation": -10, "contrast": 1.15, "vignette": 0.3},
            "heavy": {"grade": "noir_blue", "saturation": -20, "contrast": 1.35, "vignette": 0.5}
        },
        "vfx": {
            "light": ["subtle_glow_edges"],
            "medium": ["light_rays", "dust_particles"],
            "heavy": ["lens_flare_mystery", "depth_fog", "chromatic_aberration"]
        },
        "ffmpeg": "zoompan=z='min(zoom+0.0015,1.5)':d=900,eq=saturation=0.9:contrast=1.15"
    },

    "fear": {
        "description": "Viewer anticipating threat",
        "camera": {
            "light": {"movement": "handheld_slight_shake", "angle": "slightly_low", "speed": 0.6, "focal_length": 24},
            "medium": {"movement": "dutch_angle_creep", "angle": "tilted_20deg", "speed": 0.4, "focal_length": 35},
            "heavy": {"movement": "erratic_handheld", "angle": "extreme_dutch_45deg", "speed": 1.0, "focal_length": 18}
        },
        "color": {
            "light": {"grade": "slightly_desaturated", "saturation": -10, "contrast": 1.10},
            "medium": {"grade": "cold_blue_shadows", "saturation": -20, "contrast": 1.25, "vignette": 0.4},
            "heavy": {"grade": "horror_green_tint", "saturation": -30, "contrast": 1.5, "vignette": 0.7}
        },
        "vfx": {
            "light": ["vignette_crawl"],
            "medium": ["shadow_flicker", "screen_glitch"],
            "heavy": ["chromatic_shift", "distortion_waves", "static_burst"]
        },
        "ffmpeg": "transform='sin(2*PI*t*1.5)*5',eq=saturation=0.7:contrast=1.5,noise=alls=20:allf=t"
    },

    "triumph": {
        "description": "Viewer experiencing victory",
        "camera": {
            "light": {"movement": "slow_rise", "angle": "slightly_low", "speed": 0.5, "focal_length": 50},
            "medium": {"movement": "crane_up_hero", "angle": "low_angle_power", "speed": 0.7, "focal_length": 35},
            "heavy": {"movement": "drone_orbit_ascend", "angle": "low_heroic", "speed": 1.0, "focal_length": 24}
        },
        "color": {
            "light": {"grade": "warm_lift", "saturation": 10, "contrast": 1.05},
            "medium": {"grade": "golden_hour", "saturation": 20, "contrast": 1.15, "bloom": 0.2},
            "heavy": {"grade": "epic_teal_orange", "saturation": 35, "contrast": 1.30, "bloom": 0.4}
        },
        "vfx": {
            "light": ["soft_glow"],
            "medium": ["light_rays_strong", "particle_sparkle"],
            "heavy": ["epic_lens_flare", "light_streak", "particle_explosion"]
        },
        "ffmpeg": "zoompan=z='1':y='max(ih-ih/zoom,0-t*40)':d=900,eq=saturation=1.35:contrast=1.3,flare=0.5:0.5:2.0"
    },

    "tension": {
        "description": "Viewer on edge, awaiting resolution",
        "camera": {
            "light": {"movement": "static_locked", "angle": "eye_level_tight", "speed": 0.0, "focal_length": 85},
            "medium": {"movement": "micro_shake_anticipation", "angle": "close_up", "speed": 0.2, "focal_length": 100},
            "heavy": {"movement": "zoom_in_aggressive", "angle": "extreme_close_up", "speed": 1.5, "focal_length": 135}
        },
        "color": {
            "light": {"grade": "neutral_sharp", "saturation": 0, "contrast": 1.15},
            "medium": {"grade": "high_contrast_cold", "saturation": -15, "contrast": 1.35},
            "heavy": {"grade": "stark_black_white", "saturation": -50, "contrast": 1.6, "vignette": 0.6}
        },
        "vfx": {
            "light": ["frame_jitter"],
            "medium": ["time_remap_subtle", "sound_visualizer"],
            "heavy": ["strobe_flash", "frame_skip", "reverse_time_glitch"]
        },
        "ffmpeg": "zoompan=z='min(zoom+0.003,2.0)':d=900,eq=saturation=0.5:contrast=1.6,vignette='PI/4*0.6'"
    },

    "wonder": {
        "description": "Viewer experiencing awe",
        "camera": {
            "light": {"movement": "slow_pan_reveal", "angle": "eye_level_wide", "speed": 0.3, "focal_length": 24},
            "medium": {"movement": "crane_rise_majestic", "angle": "ascending", "speed": 0.5, "focal_length": 35},
            "heavy": {"movement": "orbital_360_slow", "angle": "god_view_high", "speed": 0.7, "focal_length": 16}
        },
        "color": {
            "light": {"grade": "pastel_dream", "saturation": 15, "contrast": 0.95},
            "medium": {"grade": "ethereal_glow", "saturation": 25, "contrast": 0.90, "bloom": 0.3},
            "heavy": {"grade": "magic_hour_amplified", "saturation": 40, "contrast": 0.85, "bloom": 0.6}
        },
        "vfx": {
            "light": ["soft_bokeh"],
            "medium": ["particle_float", "light_beams_soft"],
            "heavy": ["god_rays_volumetric", "particle_galaxy", "lens_orbs"]
        },
        "ffmpeg": "eq=saturation=1.4:contrast=0.85:brightness=0.08,gblur=sigma=7:steps=4,flare=0.4:0.4:1.8"
    },

    "urgency": {
        "description": "Viewer feeling time pressure",
        "camera": {
            "light": {"movement": "quick_cuts_static", "angle": "varying_rapid", "speed": 2.0, "focal_length": 50},
            "medium": {"movement": "chase_cam_forward", "angle": "pov_handheld", "speed": 3.0, "focal_length": 28},
            "heavy": {"movement": "frenetic_multi_angle", "angle": "extreme_pov", "speed": 5.0, "focal_length": "variable"}
        },
        "color": {
            "light": {"grade": "high_contrast_warm", "saturation": 5, "contrast": 1.20},
            "medium": {"grade": "action_orange_crush", "saturation": 15, "contrast": 1.40},
            "heavy": {"grade": "explosive_color_pop", "saturation": 30, "contrast": 1.60}
        },
        "vfx": {
            "light": ["speed_lines"],
            "medium": ["motion_trails", "frame_blending"],
            "heavy": ["strobe_cuts", "whip_transitions", "zoom_blur"]
        },
        "ffmpeg": "eq=saturation=1.3:contrast=1.6,minterpolate='fps=120:mi_mode=mci',zoompan=z='if(eq(on,1),1.5,zoom-0.01)':d=1"
    },

    "melancholy": {
        "description": "Viewer experiencing sadness/loss",
        "camera": {
            "light": {"movement": "slow_dolly_back", "angle": "eye_level_distant", "speed": 0.2, "focal_length": 50},
            "medium": {"movement": "crane_descend_slow", "angle": "high_looking_down", "speed": 0.3, "focal_length": 85},
            "heavy": {"movement": "static_hold_long", "angle": "isolated_wide", "speed": 0.0, "focal_length": 24}
        },
        "color": {
            "light": {"grade": "muted_cool", "saturation": -10, "contrast": 0.95},
            "medium": {"grade": "desaturated_blue", "saturation": -25, "contrast": 0.85, "vignette": 0.3},
            "heavy": {"grade": "monochrome_blue_tint", "saturation": -40, "contrast": 0.75, "vignette": 0.6}
        },
        "vfx": {
            "light": ["rain_overlay_light"],
            "medium": ["rain_medium", "window_droplets"],
            "heavy": ["heavy_rain", "fog_dense", "chromatic_aberration_subtle"]
        },
        "ffmpeg": "eq=saturation=0.6:contrast=0.75,colorchannelmixer=rr=0.3:rg=0.3:rb=0.4:gr=0.3:gg=0.3:gb=0.4:br=0.3:bg=0.3:bb=0.4,vignette='PI/4*0.6'"
    },

    # --- NEW ARCHETYPES (v3.0) ---

    "romance": {
        "description": "Intimacy and affection (Tame/Hollywood Safe)",
        "camera": {
            "light": {"movement": "static_two_shot", "angle": "eye_level", "speed": 0.0, "focal_length": 50},
            "medium": {"movement": "slow_dolly_in", "angle": "shoulder_level", "speed": 0.2, "focal_length": 85},
            "heavy": {"movement": "orbit_slow_close", "angle": "eye_level_tight", "speed": 0.3, "focal_length": 100}
        },
        "color": {
            "light": {"grade": "warm_soft", "saturation": 10, "contrast": 1.0, "bloom": 0.1},
            "medium": {"grade": "golden_glow", "saturation": 15, "contrast": 1.1, "vignette": 0.2},
            "heavy": {"grade": "deep_passion", "saturation": 20, "contrast": 1.2, "blur_edges": True}
        },
        "vfx": {
            "light": ["soft_glow_subtle"],
            "medium": ["bokeh_particles", "light_leak_warm"],
            "heavy": ["dreamy_haze", "heartbeat_vignette"]
        },
        "ffmpeg": "eq=saturation=1.2:contrast=1.1,gblur=sigma=2:steps=1,vignette='PI/4*0.2'"
    },

    "joy": {
        "description": "Happiness, humor, and comedy",
        "camera": {
            "light": {"movement": "static_wide", "angle": "eye_level", "speed": 0.0, "focal_length": 35},
            "medium": {"movement": "whip_pan_reveal", "angle": "slightly_low", "speed": 1.5, "focal_length": 24},
            "heavy": {"movement": "snap_zoom_funny", "angle": "high_angle_exaggerated", "speed": 3.0, "focal_length": 18}
        },
        "color": {
            "light": {"grade": "bright_natural", "saturation": 5, "contrast": 1.0, "brightness": 0.05},
            "medium": {"grade": "vibrant_pop", "saturation": 20, "contrast": 1.1, "brightness": 0.1},
            "heavy": {"grade": "candy_crush", "saturation": 35, "contrast": 1.2, "gamma": 1.1}
        },
        "vfx": {
            "light": ["clean_sharp"],
            "medium": ["confetti_subtle", "lens_flare_bright"],
            "heavy": ["speed_lines_comic", "star_burst"]
        },
        "ffmpeg": "eq=brightness=0.1:saturation=1.3:contrast=1.1"
    },

    "nostalgia": {
        "description": "Sentimental memories and flashbacks",
        "camera": {
            "light": {"movement": "handheld_gentle", "angle": "eye_level", "speed": 0.4, "focal_length": 50},
            "medium": {"movement": "slow_pan_drift", "angle": "varying", "speed": 0.3, "focal_length": 35},
            "heavy": {"movement": "floating_cam", "angle": "subjective_pov", "speed": 0.2, "focal_length": 28}
        },
        "color": {
            "light": {"grade": "sepia_tint_light", "saturation": -10, "contrast": 0.95, "warmth": 0.1},
            "medium": {"grade": "faded_film", "saturation": -25, "contrast": 0.9, "grain": 0.2},
            "heavy": {"grade": "memory_lane", "saturation": -40, "contrast": 0.85, "blur": 0.1, "grain": 0.4}
        },
        "vfx": {
            "light": ["dust_motes"],
            "medium": ["film_grain_16mm", "vignette_soft"],
            "heavy": ["film_burn", "projector_flicker", "heavy_grain"]
        },
        "ffmpeg": "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131,noise=alls=20:allf=t,vignette='PI/4*0.4'"
    },

    "rage": {
        "description": "Anger, fury, and revenge",
        "camera": {
            "light": {"movement": "static_tense", "angle": "eye_level", "speed": 0.0, "focal_length": 50},
            "medium": {"movement": "shaky_cam_build", "angle": "low_angle", "speed": 1.0, "focal_length": 35},
            "heavy": {"movement": "erratic_chaos", "angle": "dutch_extreme", "speed": 4.0, "focal_length": 24}
        },
        "color": {
            "light": {"grade": "cold_steel", "saturation": -10, "contrast": 1.2},
            "medium": {"grade": "simmering_heat", "saturation": 0, "contrast": 1.4, "red_tint": 0.1},
            "heavy": {"grade": "seeing_red", "saturation": 20, "contrast": 1.7, "red_crush": 0.3}
        },
        "vfx": {
            "light": ["heat_haze_subtle"],
            "medium": ["camera_shake_impact", "distortion_edges"],
            "heavy": ["chromatic_aberration_strong", "red_flash", "screen_tear"]
        },
        "ffmpeg": "colorbalance=rs=0.2:rm=0.2:rh=0.2,eq=contrast=1.5:saturation=1.2,transform='sin(2*PI*t*10)*5'"
    },

    "serenity": {
        "description": "Calm, peace, and nature",
        "camera": {
            "light": {"movement": "static_locked", "angle": "eye_level", "speed": 0.0, "focal_length": 35},
            "medium": {"movement": "slow_pan_landscape", "angle": "wide_angle", "speed": 0.1, "focal_length": 24},
            "heavy": {"movement": "drone_hover", "angle": "god_view", "speed": 0.05, "focal_length": 16}
        },
        "color": {
            "light": {"grade": "natural_balanced", "saturation": 0, "contrast": 1.0},
            "medium": {"grade": "cool_breeze", "saturation": 5, "contrast": 0.95, "blue_tint": 0.05},
            "heavy": {"grade": "zen_garden", "saturation": 10, "contrast": 0.9, "diffusion": 0.2}
        },
        "vfx": {
            "light": ["clean_frame"],
            "medium": ["mist_layer", "slow_particles"],
            "heavy": ["god_rays_subtle", "water_shimmer"]
        },
        "ffmpeg": "eq=contrast=0.95:saturation=1.1,colorbalance=bs=0.1"
    }
}


class EmotionalIndexManager:
    """Manages access to emotional index with Redis integration"""
    
    def __init__(self, redis_client=None):
        self.index = EMOTIONAL_INDEX
        self.redis_client = redis_client
        
    def get_emotion_profile(self, emotion: str, intensity: str = "medium"):
        """
        Retrieve emotion profile from index
        
        Args:
            emotion: Emotion name (e.g., 'curiosity', 'fear')
            intensity: 'light', 'medium', or 'heavy'
            
        Returns:
            Dict with camera, color, vfx, and ffmpeg settings
        """
        if emotion not in self.index:
            return self.index.get("curiosity", {})  # Default fallback
            
        profile = self.index[emotion]
        
        return {
            "emotion": emotion,
            "intensity": intensity,
            "description": profile.get("description"),
            "camera": profile.get("camera", {}).get(intensity, {}),
            "color": profile.get("color", {}).get(intensity, {}),
            "vfx": profile.get("vfx", {}).get(intensity, []),
            "ffmpeg": profile.get("ffmpeg", "")
        }
    
    def get_all_emotions(self):
        """Return list of all available emotions"""
        return list(self.index.keys())
    
    def seed_redis(self):
        """Populate Redis with emotional index (for distributed systems)"""
        if not self.redis_client:
            return False
            
        for emotion, profile in self.index.items():
            for intensity in ["light", "medium", "heavy"]:
                key = f"emotional_vertices:{emotion}:{intensity}"
                value = {
                    "camera": profile.get("camera", {}).get(intensity, {}),
                    "color": profile.get("color", {}).get(intensity, {}),
                    "vfx": profile.get("vfx", {}).get(intensity, []),
                    "ffmpeg": profile.get("ffmpeg", "")
                }
                self.redis_client.hset(key, mapping=value)
        
        return True


if __name__ == "__main__":
    manager = EmotionalIndexManager()
    print(f"✓ Emotional Index v3.0 loaded: {len(manager.get_all_emotions())} archetypes")
    print(f"  Emotions: {', '.join(manager.get_all_emotions())}")
