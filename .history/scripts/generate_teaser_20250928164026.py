#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
public = ROOT / "public"
assets = ROOT / "assets" / "png"

out_mp4 = public / "xoflipper_teaser.mp4"

frames = [
    (assets / "gold_rush_1000x1000.png", "Gold Rush"),
    (assets / "pod_power_1000x1000.png", "Pod Power"),
    (assets / "seal_of_trust_1000x1000.png", "Seal of Trust"),
]

def ensure_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
    except Exception:
        raise SystemExit("ffmpeg is required. Install with: brew install ffmpeg")

def build_slideshow():
    # Simple zoom-in + fade via ffmpeg filters; duration ~6s
    inputs = []
    filters = []
    concat_inputs = []
    for idx, (img, label) in enumerate(frames):
        if not img.exists():
            raise SystemExit(f"Missing image: {img}")
        inputs += ["-loop", "1", "-t", "2", "-i", str(img)]
        # scale to 1080p friendly box, add zoompan and fade
        filters.append(
            f"[{idx}:v]scale=1920:-1,zoompan=z='min(zoom+0.0015,1.1)':d=60:s=1920x1080,format=yuv420p,fade=t=in:st=0:d=0.4,fade=t=out:st=1.6:d=0.4[v{idx}]"
        )
        concat_inputs.append(f"[v{idx}]")

    filter_complex = ";".join(filters) + ";" + "".join(concat_inputs) + f"concat=n={len(frames)}:v=1:a=0[v]"

    cmd = [
        "ffmpeg",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-r", "30",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-y", str(out_mp4),
    ]
    subprocess.run(cmd, check=True)
    print(f"Wrote {out_mp4}")

if __name__ == "__main__":
    ensure_ffmpeg()
    public.mkdir(parents=True, exist_ok=True)
    build_slideshow()

