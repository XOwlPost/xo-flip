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
#!/usr/bin/env python3
"""
Generate XOFlipper teaser MOV from banner + glyphs + tagline.
Writes XOFlipper_source.mov in repo root.
Compatible with moviepy v2.x API.
"""

import os
from moviepy import ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont

# Paths relative to repo root
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
banner = os.path.join(repo_root, "public", "dolphin_seals_banner_1500x500.jpg")
glyphs = [
    os.path.join(repo_root, "assets/png/gold_rush_1000x1000.png"),
    os.path.join(repo_root, "assets/png/pod_power_1000x1000.png"),
    os.path.join(repo_root, "assets/png/seal_of_trust_1000x1000.png"),
]

# Output
out_mov = os.path.join(repo_root, "XOFlipper_source.mov")

# Safety checks
if not os.path.exists(banner):
    raise FileNotFoundError(f"Banner not found at {banner}")
missing = [g for g in glyphs if not os.path.exists(g)]
if missing:
    print("Warning: missing glyphs (will continue without some):")
    for m in missing:
        print(" -", m)

# --- Build tagline overlay as a transparent PNG via PIL (avoids ImageMagick) ---

tagline_text = "One flip, you’re rich. Two flips, you’re legendary."
tagline_png_dir = os.path.join(repo_root, "public", "tmp")
os.makedirs(tagline_png_dir, exist_ok=True)
tagline_png_path = os.path.join(tagline_png_dir, "tagline_overlay.png")

# Create a wide transparent image for the text overlay
W, H = 1920, 200
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Try to load a nicer font; fall back to default if unavailable
font = None
for candidate in [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/Library/Fonts/Arial.ttf",
]:
    if os.path.exists(candidate):
        try:
            font = ImageFont.truetype(candidate, 56)
            break
        except Exception:
            pass
if font is None:
    font = ImageFont.load_default()

# Draw text with a subtle shadow for readability
bbox = draw.textbbox((0, 0), tagline_text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
x = (W - tw) // 2
y = (H - th) // 2

shadow_offsets = [(-2, -2), (2, 2), (-2, 2), (2, -2)]
for dx, dy in shadow_offsets:
    draw.text((x + dx, y + dy), tagline_text, font=font, fill=(0, 0, 0, 190))
draw.text((x, y), tagline_text, font=font, fill=(255, 255, 255, 235))

img.save(tagline_png_path)

# --- Build clips ---

# 1) Banner base (1920 width). Note: moviepy v2 uses `.resized(...)` instead of `.resize(...)`.
banner_clip = ImageClip(banner, duration=8).resized(width=1920)

# 2) Glyphs appear in sequence in center. Use set_start for staggered timing.
glyph_clips = []
for i, g in enumerate(glyphs):
    if os.path.exists(g):
        clip = (
            ImageClip(g, duration=2)
            .resized(width=500)
            .set_start(2 + i * 2)
            .set_position(("center", "center"))
        )
        glyph_clips.append(clip)

# 3) Tagline overlay along the bottom for full duration
tagline_clip = (
    ImageClip(tagline_png_path, duration=8)
    .set_position(("center", "bottom"))
)

# 4) Compose and export
final = CompositeVideoClip([banner_clip, tagline_clip] + glyph_clips).with_duration(8)

# Export as MOV (H.264 in MOV container) as source for later MP4 transcode
final.write_videofile(out_mov, codec="libx264", fps=30, preset="slow")
print("Saved", out_mov)