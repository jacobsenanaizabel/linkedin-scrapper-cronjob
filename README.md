# 🤖 Job Scraper - Automated

Automated job scraper for **LinkedIn, Tecnoempleo, InfoJobs and Manfred**, using GitHub Actions + Apify.

## 🎯 What it does

- ✅ Runs **automatically on Sunday, Monday and Tuesday** at 09:00 UTC
- ✅ Searches Senior / Staff / Lead engineering roles in Spain (titles in `config.json`)
- ✅ Keeps only jobs from the **last 24 hours** whose **description mentions React**
- ✅ Drops consultancies / outsourcing and removes duplicates across searches and sites
- ✅ Produces JSON + CSV files to download
- ✅ Can be triggered by the Claude Code agent with `/search-jobs`

> Architecture and workflow diagrams: [ARCHITECTURE.md](ARCHITECTURE.md)

## 📋 Initial Setup

### 1. Clone this repo

```bash
git clone https://github.com/<your-username>/linkedin-scrapper-cronjob.git
```

### 2. Configure the Apify token

1. Get your token at https://console.apify.com/settings/integrations (**Personal API tokens**)
2. In the GitHub repo go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `APIFY_TOKEN`
5. Value: `YOUR_APIFY_TOKEN_HERE`
6. **Add secret**

### 3. Enable GitHub Actions

1. Go to the **Actions** tab
2. If asked, click **I understand my workflows, go ahead and enable them**

## 🚀 How to Use

### Automatic run

The scraper runs **automatically**:
- **Days:** Sunday, Monday and Tuesday
- **Time:** 09:00 UTC
- **Nothing to do!**

### Manual run

To run it now (without waiting for the next schedule):

1. Go to the **Actions** tab
2. Click the **"LinkedIn Scraper Advanced"** workflow
3. Click **Run workflow**. Optional inputs:
   - `sources` — only these sites, e.g. `tecnoempleo,infojobs` (empty = all enabled in `config.json`)
   - `test_limit` — max jobs per title on each site, e.g. `5` for a cheap test (empty = limits from `config.json`)
4. Wait 3–15 minutes

### From Claude Code

```
/search-jobs                              → full run on GitHub
/search-jobs tecnoempleo,infojobs 5       → only those sites, 5 jobs per title
/search-jobs linkedin 10 local            → runs on your machine using .env
```

Requires the GitHub CLI (`gh auth login`) or a local `.env` file. See [AGENTS.md](AGENTS.md).

## 📥 Getting the Results

### Option 1: GitHub (recommended)

1. Go to the **Actions** tab
2. Click the most recent run
3. Scroll down to **Artifacts**
4. Download:
   - `jobs_latest.json` - Full data (raw fields from each site)
   - `jobs_latest.csv` - Same columns for every site, for Excel/Sheets
   - `summary.json` - Jobs per search and duplicates removed
   - `run_info.json` - Links to each Apify run

**Files expire after 90 days.**

### Option 2: Apify Console

1. Go to https://console.apify.com/actors/runs
2. Find the most recent run
3. **Dataset** → **Export** → JSON/CSV/Excel (raw results, before the filters)

## ⚙️ Configuration

**Everything the scraper searches for lives in `config.json`** — it is the single source of truth. The workflow only reads this file; you never need to edit the YAML to change searches or filters. Every field is explained in `_help` inside the file.

| Field | What it does |
|---|---|
| `titles` | Job titles searched on each site (LinkedIn, Tecnoempleo, InfoJobs). Don't put "React" in the title. |
| `descriptionMustContain` | The job **description** must contain one of these words (e.g. `react`). The title doesn't count. |
| `excludeKeywords` | Drops jobs whose title or company contains one of these words (consultoria, outsourcing…). |
| `maxAgeHours` | Only jobs published in the last N hours (e.g. `24`). |
| `sources.<site>.enabled` | Turns each site on/off (`linkedin`, `tecnoempleo`, `infojobs`, `manfred`). |
| `sources.<site>.limit` / `maxResults` | Max jobs per title on each site. |
| `sources.linkedin.experienceLevel` / `jobType` | Seniority (`4` = Mid-Senior, `5` = Director) and contract type (`F` = full-time). |

Duplicate jobs (same title + company, across searches or sites) are merged into one; the `found_in` column in the CSV shows where it appeared.

### Change the schedule

In `.github/workflows/linkedin-scraper-advanced.yml`, change the cron:

```yaml
schedule:
  - cron: '0 9 * * 0,1,2'  # Sunday, Monday and Tuesday at 09:00 UTC
```

Examples:
- `'0 9 * * 1'` - Every Monday at 09:00
- `'0 9 * * 1-5'` - Monday to Friday at 09:00
- `'0 9 1 * *'` - 1st day of every month at 09:00

**Cron calculator:** https://crontab.guru

### Cost per run

Apify charges **per downloaded job, before the filters**. Maximum per run = `number of titles × (linkedin.limit + tecnoempleo.maxResults + infojobs.maxResults)`. With the 24h window the real number is usually much lower.

| Site | Approx. price |
|---|---|
| LinkedIn | depends on the actor's plan |
| Tecnoempleo | ~$0.0015 per job + $0.01 per run |
| InfoJobs | ~$0.001 per job |
| Manfred | free (public API) |

Apify's free tier gives $5 of credit per month. Check usage at https://console.apify.com/billing.

### Test locally

1. Create a `.env` file in the repo root with `APIFY_TOKEN=<your token>` (it's in `.gitignore`)
2. `pip install requests pandas`
3. `python scripts/run_local.py tecnoempleo,infojobs 5` — only those sites, 5 jobs per title (cheap)
4. `python scripts/run_local.py` — everything, same as on GitHub

## 🔔 Notifications

### Get an email after each run

Add at the end of the workflow:

```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.GMAIL_USER }}
    password: ${{ secrets.GMAIL_PASSWORD }}
    subject: 🎯 New jobs found
    body: Check GitHub Actions for results!
    to: your-email@example.com
```

**Required secrets:**
- `GMAIL_USER`: your Gmail address
- `GMAIL_PASSWORD`: a Gmail App Password

## 📚 File Structure

```
linkedin-scrapper-cronjob/
├── .github/workflows/
│   ├── linkedin-scraper-advanced.yml   # Main workflow (reads config.json)
│   └── linkedin-scraper.yml            # Legacy LinkedIn-only workflow (manual only)
├── .claude/
│   ├── agents/job-researcher.md        # Claude Code agent
│   └── skills/search-jobs/SKILL.md     # /search-jobs command
├── scripts/run_local.py                # Runs the workflow script locally
├── config.json                         # Searches and filters (single source of truth)
├── AGENTS.md / CLAUDE.md               # Context for AI agents
├── ARCHITECTURE.md                     # Diagrams
└── README.md                           # This file
```

## 🐛 Troubleshooting

### The workflow doesn't run automatically

1. Go to **Settings** → **Actions** → **General**
2. Scroll down to **Workflow permissions**
3. Enable **Read and write permissions**
4. **Save**

GitHub also disables scheduled workflows after 60 days without commits in the repo — re-enable it in the **Actions** tab.

### "Resource not accessible by integration"

Same as above — insufficient permissions.

### The scraper fails

Check:
1. Is the `APIFY_TOKEN` secret correct?
2. Do you have enough credit? (https://console.apify.com/billing)
3. The run log: lines starting with `❌` show which search failed

### Empty results

Possible causes:
- No new jobs in the last `maxAgeHours`
- `descriptionMustContain` / `excludeKeywords` too strict

**Fix:** raise `maxAgeHours` (e.g. `168` for a week) or relax the filters in `config.json`. The log shows how many jobs each filter dropped (`🕐`, `🔎`, `🚫`).

## 📖 Useful Links

- **Apify Console:** https://console.apify.com
- **Cron calculator:** https://crontab.guru
