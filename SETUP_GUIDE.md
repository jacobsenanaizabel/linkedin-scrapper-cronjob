# 📝 Step-by-Step Setup Guide

## ⏱️ Estimated time: 15 minutes

---

## 🎯 STEP 1: Get the repository (2 min)

Fork or clone this repository into your GitHub account:

```bash
git clone https://github.com/<your-username>/linkedin-scrapper-cronjob.git
```

**Visibility:** public repos get unlimited GitHub Actions minutes; private repos get 2,000 min/month for free.

---

## 🔐 STEP 2: Create the Apify token (3 min)

1. **Go to** https://console.apify.com (create an account if you don't have one — the free tier gives $5/month)
2. **Settings** → **API & Integrations** → **Personal API tokens**
3. Click **+ Create a new token** (e.g. `job-scraper`) and copy it — it starts with `apify_api_`

⚠️ Never paste the token into a file that gets committed, an issue or a chat.

---

## 🔑 STEP 3: Add the token to GitHub (2 min)

1. **In your repository**, click the **Settings** tab (🔧)
2. **Left menu** → **Secrets and variables** → **Actions**
3. Click the green **New repository secret** button
4. **Fill in:**
   ```
   Name:   APIFY_TOKEN
   Secret: YOUR_APIFY_TOKEN_HERE
   ```
5. Click **Add secret**

✅ **Secret configured!** It will show up in the list as `APIFY_TOKEN`.

---

## ✅ STEP 4: Enable GitHub Actions (1 min)

1. **Click the** `Actions` tab (▶️)
2. If a confirmation message appears, click **I understand my workflows, go ahead and enable them**
3. You'll see the workflows:
   - `LinkedIn Scraper Advanced (...)` — the main one
   - `LinkedIn Job Scraper (...)` — legacy, LinkedIn only

---

## 🚀 STEP 5: First run (5 min)

Start with a cheap test run:

1. **In the Actions tab**, click **`LinkedIn Scraper Advanced`**
2. **On the right**, click `Run workflow`
3. Fill in the optional inputs:
   ```
   Branch:     main
   sources:    tecnoempleo,infojobs
   test_limit: 5
   ```
4. Click the green `Run workflow`
5. **Wait a few seconds** → refresh the page; a new run appears (🟡 = running)
6. **Click the run** to follow the logs live
7. **Wait 3–10 minutes** → status changes to ✅ (success) or ❌ (error)

### 📊 See the results

1. **Scroll down** on the run page
2. **Artifacts** section → `📦 linkedin-jobs-<number>`
3. **Click** to download (ZIP)
4. **Unzip** → you get:
   - `jobs_latest.json` - Full data
   - `jobs_latest.csv` - For Excel/Sheets
   - `summary.json` - Jobs per search, duplicates removed
   - `run_info.json` - Links to each Apify run

The run page also shows a summary, and the log explains what each filter dropped:
```
🕐 Kept 12/25 from the last 24h
🔎 Kept 5/12 with ['react'] in the description
🚫 Kept 4/5 without ['consultoria', ...]
🧹 Removed 3 duplicates → 21 unique jobs
```

✅ **First run done!**

---

## 🔄 STEP 6: Automatic runs

Already configured! 🎉 The workflow runs **automatically**:
- ⏰ **When:** Sunday, Monday and Tuesday
- 🕐 **Time:** 09:00 UTC

To **check the next run**: Actions tab → workflow → the schedule is shown on the right.

---

## ⚙️ STEP 7: Customize (optional)

### Change what is searched

Edit `config.json` (the single source of truth — never edit searches in the workflow):

```json
"titles": [
  "Senior Frontend Engineer",   ← edit
  "Your title here"             ← add more
],
"descriptionMustContain": ["react"],
"excludeKeywords": ["consulting", "outsourcing"],
"maxAgeHours": 24
```

Every field is explained in `_help` inside the file. Commit the change and the next run uses it.

### Change the schedule

1. Edit `.github/workflows/linkedin-scraper-advanced.yml`
2. Find the line:
   ```yaml
   cron: '0 9 * * 0,1,2'
   ```
3. Change it, e.g.:
   - `'0 9 * * 1'` - Every Monday
   - `'0 9 * * 1-5'` - Weekdays
   - `'0 9 1 * *'` - 1st day of the month

Use https://crontab.guru for help.

---

## 💻 STEP 8: Run locally / from Claude Code (optional)

1. Create `.env` in the repo root with `APIFY_TOKEN=<your token>` (git-ignored)
2. `pip install requests pandas`
3. `python scripts/run_local.py tecnoempleo,infojobs 5`

In Claude Code, `/search-jobs` runs the scraper and ranks the results (see `AGENTS.md`).
For runs on GitHub it needs the GitHub CLI: `winget install GitHub.cli` then `gh auth login`.

---

## 🐛 Problems?

### The workflow doesn't show up in Actions
→ Check the file path: `.github/workflows/linkedin-scraper-advanced.yml`

### "Resource not accessible by integration"
→ Settings → Actions → General → Workflow permissions → Read and write

### The scraper fails
→ Check:
1. Is the `APIFY_TOKEN` secret correct?
2. Do you have Apify credit? https://console.apify.com/billing
3. `❌` lines in the run log

### Empty results
→ Raise `maxAgeHours` or relax the filters in `config.json`.
