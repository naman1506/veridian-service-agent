"""Capture the console hero states with Playwright after running the local server."""
from pathlib import Path
import subprocess, sys, time
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'docs/images'; OUT.mkdir(parents=True,exist_ok=True)
proc=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--port','8000'],cwd=ROOT)
try:
 time.sleep(2)
 with sync_playwright() as p:
  browser=p.chromium.launch(); page=browser.new_page(viewport={'width':1280,'height':800})
  page.goto('http://127.0.0.1:8000/#/case/REQ-01'); page.get_by_role('button',name='Run all cases').click(); page.wait_for_timeout(2600); page.screenshot(path=OUT/'console.png',full_page=True)
  for case,file in [('REQ-01','case-req01-conflict.png'),('REQ-08','case-req08-risk.png'),('REQ-10','case-req10-nocoverage.png')]:
   page.locator(f'[data-id="{case}"]').click(); page.wait_for_timeout(350); page.screenshot(path=OUT/file,full_page=True)
  page.screenshot(path=OUT/'metrics.png',clip={'x':0,'y':0,'width':1280,'height':120}); page.screenshot(path=OUT/'banner.png',clip={'x':0,'y':0,'width':1280,'height':640})
  browser.close()
finally: proc.terminate(); proc.wait(timeout=5)
