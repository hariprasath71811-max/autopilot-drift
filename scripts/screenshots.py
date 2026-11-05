#!/usr/bin/env python3
"""Capture README screenshots from index.html via Playwright."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
url = (ROOT / "index.html").resolve().as_uri()

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1280, "height": 800})
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(2500)
    page.locator("#flowcard").scroll_into_view_if_needed()
    page.wait_for_timeout(600)
    page.screenshot(path=str(OUT / "console.png"))
    page.get_by_text("Inject Workflow Drift").first.click()
    page.wait_for_timeout(1800)
    page.screenshot(path=str(OUT / "drift-flagged.png"))
    page.locator("#steerBtn").click()
    page.wait_for_timeout(800)
    page.screenshot(path=str(OUT / "steer-editor.png"))
    page.get_by_text("Apply Patch & Release").first.click()
    page.wait_for_timeout(1200)
    page.screenshot(path=str(OUT / "steered-safe.png"))
    b.close()
print(f"Saved screenshots to {OUT}")
