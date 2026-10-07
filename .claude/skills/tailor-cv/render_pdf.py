"""Render an HTML CV to PDF with headless Microsoft Edge or Google Chrome (no extra installs).

Usage:
    python .claude/skills/tailor-cv/render_pdf.py cv/tailored/<folder>/cv.html
    -> writes cv/tailored/<folder>/cv.pdf next to the HTML
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def find_browser():
    for path in BROWSERS:
        if os.path.exists(path):
            return path
    for name in ("msedge", "google-chrome", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("No Edge or Chrome found. Install one of them, or open the HTML in a browser and use Print → Save as PDF.")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    html = Path(sys.argv[1]).resolve()
    if not html.exists():
        sys.exit(f"File not found: {html}")
    pdf = html.with_suffix('.pdf')

    subprocess.run([
        find_browser(),
        '--headless=new',
        '--disable-gpu',
        '--no-pdf-header-footer',
        f'--print-to-pdf={pdf}',
        html.as_uri(),
    ], check=True, capture_output=True, timeout=120)

    if not pdf.exists() or pdf.stat().st_size == 0:
        sys.exit("The browser did not produce a PDF.")
    print(f"PDF written: {pdf} ({pdf.stat().st_size // 1024} KB)")


if __name__ == '__main__':
    main()
