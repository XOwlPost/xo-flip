#!/usr/bin/env python3
"""
Generate XOFlipper teaser MOV from banner + glyphs.
Writes XOFlipper_source.mov in repo root.
"""

import os
from moviepy import ImageClip, CompositeVideoClip

# Paths relative to repo root
repo_root = os.path.abspath(os.path.dirname(__file__) + "/..")
banner = os.path.join(repo_root, "public", "dolphin_seals_banner_1500x500.jpg")
glyphs = [
    os.path.join(repo_root, "assets/png/gold_rush_1000x1000.png"),
    os.path.join(repo_root, "assets/png/pod_power_1000x1000.png"),
    os.path.join(repo_root, "assets/png/seal_of_trust_1000x1000.png"),
]

# Output
out_mov = os.path.join(repo_root, "XOFlipper_source.mov")

# 1) Banner base (zoom-in effect)
banner_clip = (
    ImageClip(banner, duration=6)
    .resize(width=1920)
    .fx(lambda clip: clip.resize(lambda t: 1 + 0.02 * t))  # slow zoom
)

# 2) Each glyph fade-in
glyph_clips = []
for i, g in enumerate(glyphs):
    if os.path.exists(g):
        glyph = (
            ImageClip(g, duration=2)
            .resize(width=500)
            .set_start(2 + i * 2)
            .set_position(("center", "center"))
            .crossfadein(0.8)
        )
        glyph_clips.append(glyph)

# 3) Compose
final = CompositeVideoClip([banner_clip] + glyph_clips)
final = final.set_duration(8)

# 4) Export as MOV (source for ffmpeg)
final.write_videofile(out_mov, codec="libx264", fps=30, preset="slow")
print("Saved", out_mov)