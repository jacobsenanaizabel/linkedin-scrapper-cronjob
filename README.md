# 🤖 Job Scraper

On-demand job scraper for **LinkedIn, Tecnoempleo, InfoJobs and Manfred**: one click in GitHub Actions, results filtered and deduplicated, using Apify.

## 🎯 What it does

- ✅ Runs **only when you start it** (Run workflow button in GitHub Actions) — nothing runs or spends Apify credit on its own
- ✅ Searches the job titles you choose, on the sites you choose
- ✅ Keeps only recent jobs that match your filters, and removes duplicates
- ✅ Produces JSON + CSV files to download (open the CSV in Excel / Google Sheets)
- ✅ Can be triggered by the Claude Code agent with `/search-jobs`

**Out of the box** it is set up for Senior / Lead software engineering jobs in Spain that mention React.
**Not a software engineer?** Everything is changed in one file — see [Make it yours](#make-it-yours) below.

> Architecture and workflow diagrams: [ARCHITECTURE.md](ARCHITECTURE.md)

<a id="make-it-yours"></a>

## ✏️ Make it yours (search for any job)

You only edit **one file: `config.json`**. No programming needed. Open it on GitHub, click the ✏️ pencil icon, change it, and click **Commit changes**. The next run uses your new settings.

> ⚠️ The `// ...` notes in the examples below are explanations only — **don't copy them into `config.json`** (JSON doesn't allow comments). Keep the quotes, commas and brackets exactly as shown.

### Step 1 — What jobs? → `titles`

Write the job titles exactly as you would type them into a job site's search box. Each title is searched separately.

```json
"titles": ["Nurse", "Enfermera", "Registered Nurse"]
```

More examples:

| You are looking for | `titles` could be |
|---|---|
| Marketing | `["Marketing Manager", "Digital Marketing", "Responsable de Marketing"]` |
| Accounting | `["Accountant", "Contable", "Financial Analyst"]` |
| Teaching | `["English Teacher", "Profesor de Inglés"]` |
| Design | `["UX Designer", "Product Designer", "Diseñador UX"]` |

💡 If you search in Spain, add the Spanish title too — many ads are only in Spanish.
💡 More titles = more results, but also more cost (see [Cost per run](#cost-per-run)).

### Step 2 — Must the ad mention something? → `descriptionMustContain`

Only keep jobs whose **description** contains at least **one** of these words (upper/lower case doesn't matter).

```json
"descriptionMustContain": ["english"]          // only ads that mention English
"descriptionMustContain": ["sap", "excel"]     // ads that mention SAP or Excel
"descriptionMustContain": []                   // keep everything (no filter)
```

⚠️ Words are matched anywhere in the text, so very short words can match inside other words. Prefer specific words.
⚠️ It only looks at the description, not the title.

### Step 3 — Anything to skip? → `excludeKeywords`

Jobs whose **title or company name** contains one of these words are dropped.

```json
"excludeKeywords": ["intern", "prácticas", "junior"]   // skip internships and junior roles
"excludeKeywords": []                                 // skip nothing
```

To skip specific companies, use `excludeCompanies`. It matches the **exact** company name (case, accents and punctuation ignored), so `"UST"` doesn't drop "Industrial Solutions":

```json
"excludeCompanies": ["Accenture", "UST", "NCC Group"]
```

### Step 4 — Which sites? → `sources`

Turn each site on or off with `"enabled": true` / `false`. **Pick the sites that fit your field:**

| Site | What jobs | Where | Keep it on if… |
|---|---|---|---|
| `linkedin` | All kinds | Any country | Almost always |
| `infojobs` | All kinds | Spain only | You search in Spain |
| `tecnoempleo` | IT / tech only | Spain only | You are in tech — **turn it off otherwise** |
| `manfred` | Software only | Spain / remote | You are a developer — **turn it off otherwise** |

### Step 5 — Where and what level? → `sources.linkedin`

```json
"linkedin": {
  "enabled": true,
  "location": "Barcelona",          // a country, region or city: "Portugal", "Lisbon", "Germany"…
  "limit": 50,                      // max jobs per title
  "experienceLevel": ["2", "3", "4"],
  "jobType": ["F"]
}
```

| `experienceLevel` | | `jobType` | |
|---|---|---|---|
| `1` | Internship | `F` | Full-time |
| `2` | Entry level | `P` | Part-time |
| `3` | Associate | `C` | Contract |
| `4` | Mid-Senior | `T` | Temporary |
| `5` | Director | `I` | Internship |
| `6` | Executive | `V` | Volunteer |

You can list several values. To accept every level, list all of them: `["1", "2", "3", "4", "5", "6"]`.

For Tecnoempleo, `province` limits the search to one Spanish province (`"Madrid"`, `"Barcelona"`, or `""` for all of Spain). InfoJobs always searches all of Spain.

### Step 6 — How recent? → `maxAgeHours`

```json
"maxAgeHours": 24     // jobs from the last day (good for daily/weekly runs)
"maxAgeHours": 168    // the last week (good for a first run, or if you get few results)
```

### Full example: marketing jobs in Barcelona

```json
{
  "titles": ["Marketing Manager", "Digital Marketing Specialist", "Responsable de Marketing"],
  "descriptionMustContain": ["english"],
  "excludeKeywords": ["intern", "prácticas", "becario"],
  "maxAgeHours": 24,
  "sources": {
    "linkedin":    { "enabled": true,  "actor": "RIGGeqD6RqKmlVoQU", "location": "Barcelona", "limit": 50, "experienceLevel": ["3", "4"], "jobType": ["F"] },
    "tecnoempleo": { "enabled": false, "actor": "blackfalcondata~tecnoempleo-scraper", "province": "", "maxResults": 25 },
    "infojobs":    { "enabled": true,  "actor": "shahidirfan~infojobs-scraper", "maxResults": 25 },
    "manfred":     { "enabled": false }
  }
}
```

Leave the `actor` values as they are — they tell Apify which scraper to use for each site.

### Before your first real run

1. Do a cheap test: **Actions → Run workflow** with `test_limit` = `5` (see [Run it](#run-it)).
2. Open `jobs_latest.csv` and check the jobs look right.
3. Too few results? Raise `maxAgeHours`, add more `titles`, or empty `descriptionMustContain`.
   Too many unrelated results? Add words to `descriptionMustContain` or `excludeKeywords`.

**Using the Claude Code agent too?** Also update the **Candidate profile** section in [AGENTS.md](AGENTS.md) (role, skills, location), so the agent ranks jobs for *your* field.

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

### Run it

The scraper **only runs when you start it** — there is no schedule.

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

### Tailor your CV to a job (Claude Code)

```
/tailor-cv 3                                   → CV for job #3 of the last /search-jobs ranking
/tailor-cv https://company.com/jobs/123        → CV for a job link
/tailor-cv 3 --cover-letter                    → also writes a cover letter
```

1. Put your current CV (PDF) in `cv/original/`.
2. The first run converts it to `cv/master.md` — review it and add everything you've done. It is the source
   of truth: tailored CVs only reorder, trim and reword what's in it, **never invent experience**.
3. Each run creates `cv/tailored/<date>-<company>-<role>/` with `cv.pdf` (ready to send) and `report.md`
   (how well you match, and the gaps).

PDFs are generated with Microsoft Edge or Google Chrome (already on most computers). The `cv/` folder is in
`.gitignore`, so your personal data never reaches GitHub.

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

## ⚙️ Configuration reference

**Everything the scraper searches for lives in `config.json`** — it is the single source of truth. The workflow only reads this file; you never need to edit the YAML to change searches or filters. Every field is explained in `_help` inside the file. For a step-by-step guide, see [Make it yours](#make-it-yours).

| Field | What it does |
|---|---|
| `titles` | Job titles searched on each site (LinkedIn, Tecnoempleo, InfoJobs). Don't put "React" in the title. |
| `descriptionMustContain` | The job **description** must contain one of these words (e.g. `react`). The title doesn't count. |
| `excludeKeywords` | Drops jobs whose title or company contains one of these words (consultoria, consulting…). |
| `excludeCompanies` | Drops jobs from these companies (exact name, case/accents/punctuation ignored). |
| `maxAgeHours` | Only jobs published in the last N hours (e.g. `24`). |
| `sources.<site>.enabled` | Turns each site on/off (`linkedin`, `tecnoempleo`, `infojobs`, `manfred`). |
| `sources.<site>.limit` / `maxResults` | Max jobs per title on each site. |
| `sources.linkedin.experienceLevel` / `jobType` | Seniority (`4` = Mid-Senior, `5` = Director) and contract type (`F` = full-time). |

Duplicate jobs (same title + company, across searches or sites) are merged into one; the `found_in` column in the CSV shows where it appeared.

### Want it to run automatically? (optional)

Add a `schedule` to the `on:` block of `.github/workflows/linkedin-scraper-advanced.yml`:

```yaml
on:
  schedule:
    - cron: '0 7 * * *'   # every day at 07:00 UTC (https://crontab.guru)
  workflow_dispatch:
```

Notes: run it daily if `maxAgeHours` is 24, otherwise jobs posted on the skipped days are never seen. On public repos,
GitHub disables schedules after 60 days without commits — re-enable the workflow in the **Actions** tab.

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

### "Resource not accessible by integration"

1. Go to **Settings** → **Actions** → **General**
2. Scroll down to **Workflow permissions**
3. Enable **Read and write permissions**
4. **Save**

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
