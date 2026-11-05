#!/usr/bin/env python3
"""Generate the 90-second AutoPilot Drift narration track.

Primary: edge-tts (natural US voice, needs internet):
    python -m edge_tts --voice en-US-ChristopherNeural -f demo-voice.txt --write-media narration.mp3

Fallback (Windows, offline): PowerShell System.Speech -> narration.wav.
Usage:
    python scripts/make-voiceover.py [--voice NAME] [--out PATH]
"""
import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

FULL_SCRIPT = """Autonomous agents now run your most critical workflows — CRM sync, outreach, billing. The danger is not a crash. It is silent workflow drift: a field changes upstream, and the error ships before anyone notices.

AutoPilot Drift is the remote control bridge for that world. It checks every payload against its live schema contract, detects drift the instant it appears, and hands you the steering wheel — before the damage spreads.

Watch the console. I inject a workflow drift: a mismatched currency field from the EMEA region — euros where dollars were expected. AutoPilot Drift flags it instantly, quarantines the payload, and forecasts a fourteen thousand dollar refund loop downstream.

Now I steer. From the inline editor, I force the currency to dollars, reroute the region, and arm the refund-loop guard. One click applies the patch remotely and releases the payload — with a signed audit entry.

And when I need to stop the world, I pause the pipeline with one tap. That is remote control for autonomous agents: monitor drift, inspect anomalies in real time, and steer runaway workflows before errors ship. One file, zero backend. AutoPilot Drift — automation that keeps you in control.
"""

def try_edge_tts(voice, text_file, out_file):
    cmd = [sys.executable, "-m", "edge_tts", "--voice", voice,
           "-f", str(text_file), "--write-media", str(out_file)]
    print("Running:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True, timeout=120)
        if out_file.exists() and out_file.stat().st_size > 10000:
            print(f"OK edge-tts -> {out_file} ({out_file.stat().st_size/1024:.0f} KB)")
            return True
    except Exception as e:
        print(f"edge-tts failed: {e}")
    return False

def fallback_ps_tts(text_file, out_file):
    wav = out_file.with_suffix(".wav")
    ps1 = ROOT / "scripts" / "make-voiceover.ps1"
    print("Falling back to Windows System.Speech ->", wav)
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps1),
                    str(text_file), str(wav)], check=True, timeout=180)
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg, "-y", "-i", str(wav), "-codec:a", "libmp3lame",
                    "-q:a", "4", str(out_file)], check=True)
    print(f"OK System.Speech -> {out_file}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="en-US-ChristopherNeural")
    ap.add_argument("--out", type=pathlib.Path, default=ROOT / "narration.mp3")
    args = ap.parse_args()
    text_file = ROOT / "demo-voice.txt"
    text_file.write_text(FULL_SCRIPT, encoding="utf-8")
    print(f"Wrote {text_file} ({len(FULL_SCRIPT.split())} words)")
    if try_edge_tts(args.voice, text_file, args.out):
        return
    fallback_ps_tts(text_file, args.out)

if __name__ == "__main__":
    main()
