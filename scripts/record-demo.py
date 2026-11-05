#!/usr/bin/env python3
"""Record the AutoPilot Drift live UI with headless Playwright and mux narration.

Steps:
  1. Open index.html via file:// in Chromium (1280x720), record_video.
  2. Timed interaction beats matching DEMO_SCRIPT.md (hero settle, scroll,
     inject drift, steer & patch, pause/resume, end card).
  3. Convert webm -> demo.mp4 (libx264), then mux narration.mp3 -> demo_with_audio.mp4.

Run:
    python scripts/record-demo.py
"""
import pathlib
import shutil
import subprocess

from playwright.sync_api import sync_playwright
import imageio_ffmpeg

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = (ROOT / "index.html").resolve()
VIDEO_DIR = ROOT / "video-tmp"
DEMO_MP4 = ROOT / "demo.mp4"
NARR = ROOT / "narration.mp3"
FINAL = ROOT / "demo_with_audio.mp4"

def record():
    VIDEO_DIR.mkdir(exist_ok=True)
    for f in VIDEO_DIR.glob("*.webm"):
        f.unlink()
    url = INDEX.as_uri()
    print(f"Opening {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(VIDEO_DIR),
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        # Beats synced to the ~90s narration. Total in-page holds ~88s + settle ~= 95s video.
        page.wait_for_timeout(8000)
        # Beat 1 (0:00-0:14) — hero + flowcard settle
        page.mouse.wheel(0, 80)
        page.wait_for_timeout(9000)
        # Beat 2 (0:14-0:28) — scroll workflow section into view
        try:
            page.locator("#workflow").scroll_into_view_if_needed()
        except Exception:
            pass
        page.wait_for_timeout(11000)
        # Beat 3 (0:28-0:44) — back to console, inject drift
        try:
            page.locator("#flowcard").scroll_into_view_if_needed()
        except Exception:
            pass
        page.wait_for_timeout(6000)
        page.get_by_text("Inject Workflow Drift").first.click()
        page.wait_for_timeout(11000)
        # Beat 4 (0:44-1:02) — steer: open editor, apply patch (recovery)
        page.locator("#steerBtn").click()
        page.wait_for_timeout(5000)
        page.locator("#applyPatchBtn").click()
        page.wait_for_timeout(11000)
        # Beat 5 (1:02-1:30) — pause / resume, then end card
        page.get_by_text("Pause Pipeline").first.click()
        page.wait_for_timeout(7000)
        page.get_by_text("Resume Pipeline").first.click()
        page.wait_for_timeout(7000)
        try:
            page.locator("#insights").scroll_into_view_if_needed()
        except Exception:
            pass
        page.wait_for_timeout(8000)
        page.goto(url, wait_until="networkidle")
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(9000)
        context.close()
        browser.close()
    webms = sorted(VIDEO_DIR.glob("*.webm"))
    if not webms:
        raise SystemExit(f"No video captured in {VIDEO_DIR}")
    src = webms[-1]
    print(f"Captured {src} ({src.stat().st_size/1024/1024:.2f} MB)")
    return src

def convert_and_mux(webm):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"ffmpeg: {ffmpeg}")
    cmd1 = [ffmpeg, "-y", "-i", str(webm), "-c:v", "libx264",
            "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
            "-af", "apad=pad_dur=2", str(DEMO_MP4)]
    print("Converting:", " ".join(cmd1))
    subprocess.run(cmd1, check=True)
    print(f"Wrote {DEMO_MP4} ({DEMO_MP4.stat().st_size/1024/1024:.2f} MB)")
    if NARR.exists() and NARR.stat().st_size > 10000:
        padded = ROOT / "demo_padded.mp4"
        cmd_pad = [ffmpeg, "-y", "-i", str(DEMO_MP4),
                    "-vf", "tpad=stop_mode=clone:stop_duration=60",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                    "-c:a", "copy", str(padded)]
        print("Padding video (freeze last frame):", " ".join(cmd_pad))
        subprocess.run(cmd_pad, check=True)
        cmd2 = [ffmpeg, "-y", "-i", str(padded), "-i", str(NARR),
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-shortest", str(FINAL)]
        print("Muxing:", " ".join(cmd2))
        subprocess.run(cmd2, check=True)
        print(f"Wrote {FINAL} ({FINAL.stat().st_size/1024/1024:.2f} MB)")
    else:
        print(f"WARNING: narration not found at {NARR} — skipping mux. "
              f"Run: python scripts/make-voiceover.py then re-mux manually.")
        shutil.copyfile(DEMO_MP4, FINAL)
        print(f"Copied silent demo to {FINAL}")

def main():
    webm = record()
    convert_and_mux(webm)
    print("Done. Artifacts:")
    for f in [DEMO_MP4, FINAL, NARR]:
        if f.exists():
            print(f"  {f.name}  {f.stat().st_size/1024/1024:.2f} MB")

if __name__ == "__main__":
    main()
