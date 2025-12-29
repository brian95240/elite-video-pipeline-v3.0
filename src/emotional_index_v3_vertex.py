"""
Elite Video Pipeline v3.0 - VERTEX-ENHANCED Emotional Index
12 Archetypes with COMPLETE fingerprint metadata:
- Camera (movement, angle, speed, focal length)
- Lighting (key:fill ratio, color temperature Kelvin, ISO)
- Color (grade, saturation, contrast, LUT profile)
- VFX (effects list)
- Audio (psychoacoustic profile, reverb, mix)
- Grid (composition rules, rule of thirds)

.01% Vertex Expert Enhancement - Professional Hollywood Cinematography
"""

EMOTIONAL_INDEX_VERTEX = {
    # --- ORIGINAL ARCHETYPES (v2.0) + VERTEX ENHANCEMENTS ---
    "curiosity": {
        "description": "Viewer investigating unknown",
        "camera": {
            "light": {"movement": "slow_zoom_in", "angle": "eye_level", "speed": 0.3, "focal_length": 35},
            "medium": {"movement": "dolly_forward", "angle": "slightly_low", "speed": 0.5, "focal_length": 50},
            "heavy": {"movement": "push_in_dramatic", "angle": "dutch_tilt_15deg", "speed": 0.8, "focal_length": 85}
        },
        "lighting": {
            "light": {"ratio": "3:1", "kelvin": 5600, "iso": 400, "aperture": "T2.8"},
            "medium": {"ratio": "4:1", "kelvin": 5600, "iso": 400, "aperture": "T2.0"},
            "heavy": {"ratio": "6:1", "kelvin": 5000, "iso": 800, "aperture": "T1.5"}
        },
        "color": {
            "light": {"grade": "neutral_cool", "saturation": -5, "contrast": 1.05, "vignette": 0.1, "lut": "rec709"},
            "medium": {"grade": "mystery_teal", "saturation": -10, "contrast": 1.15, "vignette": 0.3, "lut": "teal_shadows"},
            "heavy": {"grade": "noir_blue", "saturation": -20, "contrast": 1.35, "vignette": 0.5, "lut": "kodak_2383_d65"}
        },
        "vfx": {
            "light": ["subtle_glow_edges"],
            "medium": ["light_rays", "dust_particles"],
            "heavy": ["lens_flare_mystery", "depth_fog", "chromatic_aberration"]
        },
        "audio": {
            "light": {"profile": "ambient_quiet", "reverb": "small_room", "mix": "stereo"},
            "medium": {"profile": "investigative_tension", "reverb": "medium_hall", "mix": "stereo_wide"},
            "heavy": {"profile": "mystery_drone", "reverb": "large_cathedral", "mix": "surround_5.1"}
        },
        "grid": {
            "composition": "rule_of_thirds",
            "focus_zone": "center_weighted",
            "negative_space": "moderate"
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
        "lighting": {
            "light": {"ratio": "8:1", "kelvin": 6500, "iso": 800, "aperture": "T2.8"},
            "medium": {"ratio": "12:1", "kelvin": 6500, "iso": 1600, "aperture": "T2.0"},
            "heavy": {"ratio": "16:1", "kelvin": 7000, "iso": 3200, "aperture": "T1.4"}
        },
        "color": {
            "light": {"grade": "slightly_desaturated", "saturation": -10, "contrast": 1.10, "lut": "cool_shadows"},
            "medium": {"grade": "cold_blue_shadows", "saturation": -20, "contrast": 1.25, "vignette": 0.4, "lut": "horror_blue"},
            "heavy": {"grade": "horror_green_tint", "saturation": -30, "contrast": 1.5, "vignette": 0.7, "lut": "desaturated_green_shift"}
        },
        "vfx": {
            "light": ["vignette_crawl"],
            "medium": ["shadow_flicker", "screen_glitch"],
            "heavy": ["chromatic_shift", "distortion_waves", "static_burst"]
        },
        "audio": {
            "light": {"profile": "tension_building", "reverb": "tight_space", "mix": "mono_centered"},
            "medium": {"profile": "creeping_dread", "reverb": "empty_warehouse", "mix": "stereo_narrow"},
            "heavy": {"profile": "panic_attack", "reverb": "metallic_echo", "mix": "disorienting_surround"}
        },
        "grid": {
            "composition": "off_center_unbalanced",
            "focus_zone": "edge_weighted",
            "negative_space": "claustrophobic"
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
        "lighting": {
            "light": {"ratio": "2:1", "kelvin": 3800, "iso": 200, "aperture": "T4.0"},
            "medium": {"ratio": "2:1", "kelvin": 3200, "iso": 200, "aperture": "T2.8"},
            "heavy": {"ratio": "1.5:1", "kelvin": 2800, "iso": 400, "aperture": "T2.0"}
        },
        "color": {
            "light": {"grade": "warm_lift", "saturation": 10, "contrast": 1.05, "lut": "warm_glow"},
            "medium": {"grade": "golden_hour", "saturation": 20, "contrast": 1.15, "bloom": 0.2, "lut": "golden_magic_hour"},
            "heavy": {"grade": "epic_teal_orange", "saturation": 35, "contrast": 1.30, "bloom": 0.4, "lut": "blockbuster_teal_orange"}
        },
        "vfx": {
            "light": ["soft_glow"],
            "medium": ["light_rays_strong", "particle_sparkle"],
            "heavy": ["epic_lens_flare", "light_streak", "particle_explosion"]
        },
        "audio": {
            "light": {"profile": "uplifting_strings", "reverb": "concert_hall", "mix": "stereo_wide"},
            "medium": {"profile": "heroic_brass", "reverb": "stadium", "mix": "surround_5.1"},
            "heavy": {"profile": "epic_orchestral", "reverb": "cathedral_massive", "mix": "atmos_7.1.4"}
        },
        "grid": {
            "composition": "centered_hero",
            "focus_zone": "subject_dominant",
            "negative_space": "expansive_sky"
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
        "lighting": {
            "light": {"ratio": "6:1", "kelvin": 5000, "iso": 800, "aperture": "T2.8"},
            "medium": {"ratio": "10:1", "kelvin": 5000, "iso": 1200, "aperture": "T2.0"},
            "heavy": {"ratio": "12:1", "kelvin": 4500, "iso": 1600, "aperture": "T1.5"}
        },
        "color": {
            "light": {"grade": "neutral_sharp", "saturation": 0, "contrast": 1.15, "lut": "high_contrast"},
            "medium": {"grade": "high_contrast_cold", "saturation": -15, "contrast": 1.35, "lut": "stark_shadows"},
            "heavy": {"grade": "stark_black_white", "saturation": -50, "contrast": 1.6, "vignette": 0.6, "lut": "monochrome"}
        },
        "vfx": {
            "light": ["frame_jitter"],
            "medium": ["time_remap_subtle", "sound_visualizer"],
            "heavy": ["strobe_flash", "frame_skip", "reverse_time_glitch"]
        },
        "audio": {
            "light": {"profile": "quiet_anticipation", "reverb": "dead_room", "mix": "mono"},
            "medium": {"profile": "ticking_clock", "reverb": "tight_space", "mix": "stereo_narrow"},
            "heavy": {"profile": "heartbeat_bass", "reverb": "claustrophobic", "mix": "binaural"}
        },
        "grid": {
            "composition": "extreme_closeup",
            "focus_zone": "eyes_dominant",
            "negative_space": "minimal"
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
        "lighting": {
            "light": {"ratio": "2:1", "kelvin": 5600, "iso": 200, "aperture": "T4.0"},
            "medium": {"ratio": "3:1", "kelvin": 6000, "iso": 200, "aperture": "T2.8"},
            "heavy": {"ratio": "2:1", "kelvin": 6500, "iso": 400, "aperture": "T2.0"}
        },
        "color": {
            "light": {"grade": "pastel_dream", "saturation": 15, "contrast": 0.95, "lut": "soft_pastels"},
            "medium": {"grade": "ethereal_glow", "saturation": 25, "contrast": 0.90, "bloom": 0.3, "lut": "magic_hour"},
            "heavy": {"grade": "magic_hour_amplified", "saturation": 40, "contrast": 0.85, "bloom": 0.6, "lut": "fantasy_glow"}
        },
        "vfx": {
            "light": ["soft_bokeh"],
            "medium": ["particle_float", "light_beams_soft"],
            "heavy": ["god_rays_volumetric", "particle_galaxy", "lens_orbs"]
        },
        "audio": {
            "light": {"profile": "ambient_wonder", "reverb": "natural_space", "mix": "stereo"},
            "medium": {"profile": "celestial_choir", "reverb": "cathedral", "mix": "surround_5.1"},
            "heavy": {"profile": "cosmic_symphony", "reverb": "infinite_space", "mix": "atmos_7.1.4"}
        },
        "grid": {
            "composition": "expansive_vista",
            "focus_zone": "horizon_line",
            "negative_space": "vast_sky"
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
        "lighting": {
            "light": {"ratio": "4:1", "kelvin": 5600, "iso": 800, "aperture": "T4.0"},
            "medium": {"ratio": "6:1", "kelvin": 6000, "iso": 1600, "aperture": "T2.8"},
            "heavy": {"ratio": "8:1", "kelvin": 6500, "iso": 3200, "aperture": "T2.0"}
        },
        "color": {
            "light": {"grade": "high_contrast_warm", "saturation": 5, "contrast": 1.20, "lut": "action_warm"},
            "medium": {"grade": "action_orange_crush", "saturation": 15, "contrast": 1.40, "lut": "orange_teal_action"},
            "heavy": {"grade": "explosive_color_pop", "saturation": 30, "contrast": 1.60, "lut": "adrenaline_rush"}
        },
        "vfx": {
            "light": ["speed_lines"],
            "medium": ["motion_trails", "frame_blending"],
            "heavy": ["strobe_cuts", "whip_transitions", "zoom_blur"]
        },
        "audio": {
            "light": {"profile": "quick_tempo", "reverb": "tight_space", "mix": "stereo"},
            "medium": {"profile": "racing_pulse", "reverb": "industrial", "mix": "surround_5.1"},
            "heavy": {"profile": "adrenaline_overload", "reverb": "metallic_chaos", "mix": "aggressive_surround"}
        },
        "grid": {
            "composition": "dynamic_diagonal",
            "focus_zone": "motion_blur",
            "negative_space": "compressed"
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
        "lighting": {
            "light": {"ratio": "6:1", "kelvin": 4500, "iso": 400, "aperture": "T2.8"},
            "medium": {"ratio": "8:1", "kelvin": 4500, "iso": 800, "aperture": "T2.0"},
            "heavy": {"ratio": "10:1", "kelvin": 4000, "iso": 1200, "aperture": "T1.5"}
        },
        "color": {
            "light": {"grade": "muted_cool", "saturation": -10, "contrast": 0.95, "lut": "desaturated_cool"},
            "medium": {"grade": "desaturated_blue", "saturation": -25, "contrast": 0.85, "vignette": 0.3, "lut": "melancholy_blue"},
            "heavy": {"grade": "monochrome_blue_tint", "saturation": -40, "contrast": 0.75, "vignette": 0.6, "lut": "blue_monochrome"}
        },
        "vfx": {
            "light": ["rain_overlay_light"],
            "medium": ["rain_medium", "window_droplets"],
            "heavy": ["heavy_rain", "fog_dense", "chromatic_aberration_subtle"]
        },
        "audio": {
            "light": {"profile": "somber_piano", "reverb": "empty_room", "mix": "stereo"},
            "medium": {"profile": "mournful_strings", "reverb": "large_hall", "mix": "stereo_wide"},
            "heavy": {"profile": "desolate_drone", "reverb": "cathedral_empty", "mix": "surround_5.1"}
        },
        "grid": {
            "composition": "isolated_subject",
            "focus_zone": "off_center",
            "negative_space": "overwhelming"
        },
        "ffmpeg": "eq=saturation=0.6:contrast=0.75,colorchannelmixer=rr=0.3:rg=0.3:rb=0.4:gr=0.3:gg=0.3:gb=0.4:br=0.3:bg=0.3:bb=0.4,vignette='PI/4*0.6'"
    },

    # --- NEW ARCHETYPES (v3.0) + VERTEX ENHANCEMENTS ---

    "romance": {
        "description": "Intimacy and affection (Tame/Hollywood Safe)",
        "camera": {
            "light": {"movement": "static_two_shot", "angle": "eye_level", "speed": 0.0, "focal_length": 50},
            "medium": {"movement": "slow_dolly_in", "angle": "shoulder_level", "speed": 0.2, "focal_length": 85},
            "heavy": {"movement": "orbit_slow_close", "angle": "eye_level_tight", "speed": 0.3, "focal_length": 100}
        },
        "lighting": {
            "light": {"ratio": "2:1", "kelvin": 3200, "iso": 200, "aperture": "T2.8"},
            "medium": {"ratio": "1.5:1", "kelvin": 2800, "iso": 400, "aperture": "T2.0"},
            "heavy": {"ratio": "1.5:1", "kelvin": 2500, "iso": 800, "aperture": "T1.4"}
        },
        "color": {
            "light": {"grade": "warm_soft", "saturation": 10, "contrast": 1.0, "bloom": 0.1, "lut": "romantic_glow"},
            "medium": {"grade": "golden_glow", "saturation": 15, "contrast": 1.1, "vignette": 0.2, "lut": "candlelight"},
            "heavy": {"grade": "deep_passion", "saturation": 20, "contrast": 1.2, "blur_edges": True, "lut": "intimate_warmth"}
        },
        "vfx": {
            "light": ["soft_glow_subtle"],
            "medium": ["bokeh_particles", "light_leak_warm"],
            "heavy": ["dreamy_haze", "heartbeat_vignette"]
        },
        "audio": {
            "light": {"profile": "acoustic_guitar", "reverb": "intimate_room", "mix": "stereo"},
            "medium": {"profile": "romantic_strings", "reverb": "small_hall", "mix": "stereo_wide"},
            "heavy": {"profile": "passionate_orchestral", "reverb": "concert_hall", "mix": "surround_5.1"}
        },
        "grid": {
            "composition": "two_shot_balanced",
            "focus_zone": "eyes_connection",
            "negative_space": "intimate_framing"
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
        "lighting": {
            "light": {"ratio": "2:1", "kelvin": 5600, "iso": 200, "aperture": "T4.0"},
            "medium": {"ratio": "2:1", "kelvin": 5600, "iso": 200, "aperture": "T2.8"},
            "heavy": {"ratio": "1.5:1", "kelvin": 6000, "iso": 400, "aperture": "T2.0"}
        },
        "color": {
            "light": {"grade": "bright_natural", "saturation": 5, "contrast": 1.0, "brightness": 0.05, "lut": "natural_bright"},
            "medium": {"grade": "vibrant_pop", "saturation": 20, "contrast": 1.1, "brightness": 0.1, "lut": "candy_colors"},
            "heavy": {"grade": "candy_crush", "saturation": 35, "contrast": 1.2, "gamma": 1.1, "lut": "hyper_saturated"}
        },
        "vfx": {
            "light": ["clean_sharp"],
            "medium": ["confetti_subtle", "lens_flare_bright"],
            "heavy": ["speed_lines_comic", "star_burst"]
        },
        "audio": {
            "light": {"profile": "upbeat_acoustic", "reverb": "bright_room", "mix": "stereo"},
            "medium": {"profile": "comedy_bounce", "reverb": "lively_space", "mix": "stereo_wide"},
            "heavy": {"profile": "carnival_energy", "reverb": "festival", "mix": "surround_5.1"}
        },
        "grid": {
            "composition": "centered_subject",
            "focus_zone": "full_frame",
            "negative_space": "balanced"
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
        "lighting": {
            "light": {"ratio": "2:1", "kelvin": 3200, "iso": 400, "aperture": "T2.8"},
            "medium": {"ratio": "1.5:1", "kelvin": 2800, "iso": 400, "aperture": "T2.0"},
            "heavy": {"ratio": "1.5:1", "kelvin": 2500, "iso": 800, "aperture": "T1.5"}
        },
        "color": {
            "light": {"grade": "sepia_tint_light", "saturation": -10, "contrast": 0.95, "warmth": 0.1, "lut": "vintage_fade"},
            "medium": {"grade": "faded_film", "saturation": -25, "contrast": 0.9, "grain": 0.2, "lut": "super8_film"},
            "heavy": {"grade": "memory_lane", "saturation": -40, "contrast": 0.85, "blur": 0.1, "grain": 0.4, "lut": "old_photograph"}
        },
        "vfx": {
            "light": ["dust_motes"],
            "medium": ["film_grain_16mm", "vignette_soft"],
            "heavy": ["film_burn", "projector_flicker", "heavy_grain"]
        },
        "audio": {
            "light": {"profile": "music_box", "reverb": "vintage_room", "mix": "mono"},
            "medium": {"profile": "vinyl_crackle", "reverb": "old_theater", "mix": "stereo_narrow"},
            "heavy": {"profile": "distant_memories", "reverb": "echo_chamber", "mix": "lo_fi_stereo"}
        },
        "grid": {
            "composition": "vintage_framing",
            "focus_zone": "soft_center",
            "negative_space": "dreamy"
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
        "lighting": {
            "light": {"ratio": "8:1", "kelvin": 4000, "iso": 800, "aperture": "T2.8"},
            "medium": {"ratio": "12:1", "kelvin": 3200, "iso": 1600, "aperture": "T2.0"},
            "heavy": {"ratio": "20:1", "kelvin": 2800, "iso": 3200, "aperture": "T1.4"}
        },
        "color": {
            "light": {"grade": "cold_steel", "saturation": -10, "contrast": 1.2, "lut": "desaturated_harsh"},
            "medium": {"grade": "simmering_heat", "saturation": 0, "contrast": 1.4, "red_tint": 0.1, "lut": "red_shadows"},
            "heavy": {"grade": "seeing_red", "saturation": 20, "contrast": 1.7, "red_crush": 0.3, "lut": "blood_red"}
        },
        "vfx": {
            "light": ["heat_haze_subtle"],
            "medium": ["camera_shake_impact", "distortion_edges"],
            "heavy": ["chromatic_aberration_strong", "red_flash", "screen_tear"]
        },
        "audio": {
            "light": {"profile": "tension_strings", "reverb": "tight_space", "mix": "stereo"},
            "medium": {"profile": "aggressive_percussion", "reverb": "industrial", "mix": "surround_5.1"},
            "heavy": {"profile": "chaos_distortion", "reverb": "metallic_destruction", "mix": "aggressive_atmos"}
        },
        "grid": {
            "composition": "aggressive_framing",
            "focus_zone": "confrontational",
            "negative_space": "compressed_tension"
        },
        "ffmpeg": "eq=saturation=1.2:contrast=1.7,colorbalance=rs=0.3:gs=-0.1:bs=-0.2,transform='sin(2*PI*t*4)*8'"
    },

    "serenity": {
        "description": "Calm, peace, and nature",
        "camera": {
            "light": {"movement": "static_locked", "angle": "eye_level", "speed": 0.0, "focal_length": 35},
            "medium": {"movement": "slow_pan_landscape", "angle": "wide_angle", "speed": 0.1, "focal_length": 24},
            "heavy": {"movement": "drone_hover", "angle": "god_view", "speed": 0.05, "focal_length": 16}
        },
        "lighting": {
            "light": {"ratio": "2:1", "kelvin": 5000, "iso": 100, "aperture": "T5.6"},
            "medium": {"ratio": "2:1", "kelvin": 5000, "iso": 100, "aperture": "T4.0"},
            "heavy": {"ratio": "1.5:1", "kelvin": 5200, "iso": 200, "aperture": "T2.8"}
        },
        "color": {
            "light": {"grade": "natural_balanced", "saturation": 0, "contrast": 1.0, "lut": "natural"},
            "medium": {"grade": "cool_breeze", "saturation": 5, "contrast": 0.95, "blue_tint": 0.05, "lut": "peaceful_blue"},
            "heavy": {"grade": "zen_garden", "saturation": 10, "contrast": 0.9, "diffusion": 0.2, "lut": "tranquil_green"}
        },
        "vfx": {
            "light": ["clean_frame"],
            "medium": ["mist_layer", "slow_particles"],
            "heavy": ["god_rays_subtle", "water_shimmer"]
        },
        "audio": {
            "light": {"profile": "nature_ambient", "reverb": "open_air", "mix": "stereo"},
            "medium": {"profile": "meditation_tones", "reverb": "natural_space", "mix": "stereo_wide"},
            "heavy": {"profile": "zen_soundscape", "reverb": "temple_garden", "mix": "binaural_immersive"}
        },
        "grid": {
            "composition": "balanced_symmetry",
            "focus_zone": "horizon_centered",
            "negative_space": "peaceful_expanse"
        },
        "ffmpeg": "eq=contrast=0.95:saturation=1.1,colorbalance=bs=0.1"
    }
}


class EmotionalIndexManagerVertex:
    """
    VERTEX-ENHANCED Emotional Index Manager
    Manages access to complete cinematography fingerprints with Redis L1 caching
    """
    
    def __init__(self, redis_client=None):
        self.index = EMOTIONAL_INDEX_VERTEX
        self.redis_client = redis_client
        
    def get_emotion_profile(self, emotion: str, intensity: str = "medium"):
        """
        Retrieve complete emotion profile with all fingerprints
        
        Args:
            emotion: Emotion name (e.g., 'curiosity', 'fear')
            intensity: 'light', 'medium', or 'heavy'
            
        Returns:
            Dict with camera, lighting, color, vfx, audio, grid, and ffmpeg settings
        """
        # Check Redis L1 cache first
        if self.redis_client:
            cache_key = f"vertex:{emotion}:{intensity}"
            cached = self.redis_client.get(cache_key)
            if cached:
                import json
                return json.loads(cached)
        
        # Fallback to index
        if emotion not in self.index:
            emotion = "curiosity"  # Default fallback
            
        profile = self.index[emotion]
        
        result = {
            "emotion": emotion,
            "intensity": intensity,
            "description": profile.get("description"),
            "camera": profile.get("camera", {}).get(intensity, {}),
            "lighting": profile.get("lighting", {}).get(intensity, {}),
            "color": profile.get("color", {}).get(intensity, {}),
            "vfx": profile.get("vfx", {}).get(intensity, []),
            "audio": profile.get("audio", {}).get(intensity, {}),
            "grid": profile.get("grid", {}),
            "ffmpeg": profile.get("ffmpeg", "")
        }
        
        # Cache in Redis L1 (1 hour TTL)
        if self.redis_client:
            import json
            self.redis_client.setex(cache_key, 3600, json.dumps(result))
        
        return result
    
    def get_all_emotions(self):
        """Return list of all available emotions"""
        return list(self.index.keys())
    
    def get_lighting_specs(self, emotion: str, intensity: str = "medium"):
        """Get only lighting specifications"""
        profile = self.get_emotion_profile(emotion, intensity)
        return profile.get("lighting", {})
    
    def get_audio_specs(self, emotion: str, intensity: str = "medium"):
        """Get only audio specifications"""
        profile = self.get_emotion_profile(emotion, intensity)
        return profile.get("audio", {})
    
    def get_grid_specs(self, emotion: str):
        """Get composition grid specifications"""
        if emotion not in self.index:
            emotion = "curiosity"
        return self.index[emotion].get("grid", {})
    
    def seed_redis(self):
        """Populate Redis with complete emotional index (for distributed systems)"""
        if not self.redis_client:
            return False
        
        import json
        for emotion, profile in self.index.items():
            for intensity in ["light", "medium", "heavy"]:
                key = f"vertex:{emotion}:{intensity}"
                value = {
                    "camera": profile.get("camera", {}).get(intensity, {}),
                    "lighting": profile.get("lighting", {}).get(intensity, {}),
                    "color": profile.get("color", {}).get(intensity, {}),
                    "vfx": profile.get("vfx", {}).get(intensity, []),
                    "audio": profile.get("audio", {}).get(intensity, {}),
                    "grid": profile.get("grid", {}),
                    "ffmpeg": profile.get("ffmpeg", "")
                }
                self.redis_client.setex(key, 3600, json.dumps(value))
        
        return True


if __name__ == "__main__":
    manager = EmotionalIndexManagerVertex()
    print(f"✓ VERTEX-Enhanced Emotional Index v3.0 loaded: {len(manager.get_all_emotions())} archetypes")
    print(f"  Emotions: {', '.join(manager.get_all_emotions())}")
    
    # Test complete profile retrieval
    print("\n=== COMPLETE PROFILE TEST: Melancholy (Heavy) ===")
    profile = manager.get_emotion_profile("melancholy", "heavy")
    import json
    print(json.dumps(profile, indent=2))
