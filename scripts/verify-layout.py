#!/usr/bin/env python3
import pathlib
from playwright.sync_api import sync_playwright
p = pathlib.Path(__file__).resolve().parent.parent / "index.html"
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for w, h, label in [(1280, 800, "desktop"), (390, 844, "mobile")]:
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(p.as_uri(), wait_until="networkidle")
        pg.wait_for_timeout(800)
        m = pg.evaluate("({sw:document.documentElement.scrollWidth, iw:window.innerWidth, hscroll:document.documentElement.scrollWidth>window.innerWidth+1})")
        print(label, m)
        pg.locator("#injectBtn").click(); pg.wait_for_timeout(500)
        pg.locator("#steerBtn").click(); pg.wait_for_timeout(500)
        pg.locator("#applyPatchBtn").click(); pg.wait_for_timeout(500)
        pg.locator("#pauseBtn").click(); pg.wait_for_timeout(300)
        pg.locator("#pauseBtn").click(); pg.wait_for_timeout(300)
        m2 = pg.evaluate("({sw:document.documentElement.scrollWidth, iw:window.innerWidth, hscroll:document.documentElement.scrollWidth>window.innerWidth+1, metric:document.getElementById('metricVal').textContent, status:document.getElementById('statusBadge').textContent, bar:document.getElementById('accBar').style.width})")
        print(label + "/after-clicks", str(m2).encode("ascii", "backslashreplace").decode())
        pg.close()
    b.close()
print("OK")
