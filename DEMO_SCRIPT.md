# AutoPilot Drift — 90-second demo voiceover

**Video:** [`demo_with_audio.mp4`](demo_with_audio.mp4) · 1280×720 · ~95 seconds (muxed narration + live UI recording)
**Silent screen-only capture:** [`demo.mp4`](demo.mp4)
**Script length:** ~212 words · ~140 words per minute (edge-tts `en-US-ChristopherNeural`, +0%)
**Visual flow:** hero + flowcard → inject drift → inspect anomaly → steer & patch → resolve → pause/resume → end card

---

## Timed script

| Time | Voiceover | On screen |
| --- | --- | --- |
| 0:00–0:14 | Autonomous agents now run your most critical workflows — CRM sync, outreach, billing. The danger is not a crash. It is silent workflow drift: a field changes upstream, and the error ships before anyone notices. | Hero headline, live flowcard, `94.2%` accuracy, log streaming |
| 0:14–0:28 | AutoPilot Drift is the remote control bridge for that world. It checks every payload against its live schema contract, detects drift the instant it appears, and hands you the steering wheel — before the damage spreads. | Scroll Workflow section: Check Payload → Detect Drift → Steer / Approve |
| 0:28–0:44 | Watch the console. I inject a workflow drift: a mismatched currency field from the EMEA region — euros where dollars were expected. AutoPilot Drift flags it instantly, quarantines the payload, and forecasts a fourteen thousand dollar refund loop downstream. | Click `⚡ Inject Workflow Drift` → anomaly card, step 2 `!` flagged, accuracy drops to 78.4% |
| 0:44–1:02 | Now I steer. From the inline editor, I force the currency to dollars, reroute the region, and arm the refund-loop guard. One click applies the patch remotely and releases the payload — with a signed audit entry. | Click `Steer Payload` → editor → `Apply Patch & Release` → resolved card, accuracy back to 98.6% |
| 1:02–1:30 | And when I need to stop the world, I pause the pipeline with one tap. That is remote control for autonomous agents: monitor drift, inspect anomalies in real time, and steer runaway workflows before errors ship. One file, zero backend. AutoPilot Drift — automation that keeps you in control. | Click `Pause Pipeline` → `Resume Pipeline`, counters update, end card |

---

## Full script — copy and paste

```text
Autonomous agents now run your most critical workflows — CRM sync, outreach, billing. The danger is not a crash. It is silent workflow drift: a field changes upstream, and the error ships before anyone notices.

AutoPilot Drift is the remote control bridge for that world. It checks every payload against its live schema contract, detects drift the instant it appears, and hands you the steering wheel — before the damage spreads.

Watch the console. I inject a workflow drift: a mismatched currency field from the EMEA region — euros where dollars were expected. AutoPilot Drift flags it instantly, quarantines the payload, and forecasts a fourteen thousand dollar refund loop downstream.

Now I steer. From the inline editor, I force the currency to dollars, reroute the region, and arm the refund-loop guard. One click applies the patch remotely and releases the payload — with a signed audit entry.

And when I need to stop the world, I pause the pipeline with one tap. That is remote control for autonomous agents: monitor drift, inspect anomalies in real time, and steer runaway workflows before errors ship. One file, zero backend. AutoPilot Drift — automation that keeps you in control.
```

---

## Delivery notes

- Voice: calm, confident US male (`en-US-ChristopherNeural`) at ~140 wpm. Pause briefly after `silent workflow drift`, `fourteen thousand dollar refund loop`, and the final tagline.
- Emphasize the numbers: **94.2%**, **78.4%**, **98.6%**, **fourteen thousand dollars**.
- Align `I inject a workflow drift` with the anomaly card appearing; align `One click applies the patch` with the resolved card; align `pause the pipeline with one tap` with the `PAUSED BY OPERATOR` state.
- Synthesis commands:

```bash
# Edge TTS (natural voice, needs internet)
python -m edge_tts --voice en-US-ChristopherNeural --rate=+0% -f demo-voice.txt --write-media narration.mp3

# Fallback offline TTS (Windows System.Speech, no internet)
powershell -ExecutionPolicy Bypass -File scripts/make-voiceover.ps1
```

- Mux:

```bash
python scripts/record-demo.py        # → demo.mp4 + demo_with_audio.mp4
```
