"""Runs the same Python script as the linkedin-scraper-advanced.yml workflow, locally.

Usage (from the repo root):
    python scripts/run_local.py                              # every site enabled in config.json
    python scripts/run_local.py tecnoempleo,infojobs 5       # only these sites, 5 jobs per title

The Apify token comes from the APIFY_TOKEN variable or from the .env file (APIFY_TOKEN=...), which is git-ignored.
Results (jobs_latest.json/.csv, summary.json, run_info.json) are written to the repo root and are git-ignored too.
"""
import os
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / '.github' / 'workflows' / 'linkedin-scraper-advanced.yml'

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(ROOT)

if not os.environ.get('APIFY_TOKEN') and (ROOT / '.env').exists():
    for line in (ROOT / '.env').read_text(encoding='utf-8').splitlines():
        key, _, value = line.partition('=')
        if key.strip() == 'APIFY_TOKEN':
            os.environ['APIFY_TOKEN'] = value.strip().strip('"\'')

if not os.environ.get('APIFY_TOKEN'):
    sys.exit("APIFY_TOKEN not found. Create a .env file in the repo root with: APIFY_TOKEN=<your token>")

if len(sys.argv) > 1:
    os.environ['SOURCES'] = sys.argv[1]
if len(sys.argv) > 2:
    os.environ['TEST_LIMIT'] = sys.argv[2]

# Extract the script between  python3 << 'EOF'  and  EOF  in the workflow
workflow = WORKFLOW.read_text(encoding='utf-8')
script = workflow.split("python3 << 'EOF'\n", 1)[1].split('\n          EOF\n', 1)[0]
exec(compile(textwrap.dedent(script), str(WORKFLOW), 'exec'), {'__name__': '__main__'})
