# ⚡ Quick Start - Job Scraper

## 🎯 What you get

✅ Job scraper for LinkedIn, Tecnoempleo, InfoJobs and Manfred (GitHub Actions + Apify)
✅ Runs only when you click **Run workflow** (no schedule, no surprise costs)
✅ Only jobs from the last 24h that mention React in the description
✅ No consultancies, no duplicates
✅ Results as JSON + CSV

---

## 🚀 Quick setup (10 min)

### 1️⃣ Get an Apify token
→ https://console.apify.com/settings/integrations → **Personal API tokens**

### 2️⃣ Add the GitHub secret
```
Repo → Settings → Secrets and variables → Actions → New repository secret

Name:  APIFY_TOKEN
Value: YOUR_APIFY_TOKEN_HERE
```

### 3️⃣ Enable Actions
```
Actions tab → "I understand my workflows, go ahead and enable them"
```

### 4️⃣ Test with a cheap run
```
Actions → LinkedIn Scraper Advanced → Run workflow
  sources:    tecnoempleo,infojobs
  test_limit: 5
```

Wait 3–10 min → check the results!

---

## 📊 Where to see results

### Option 1: GitHub Artifacts
```
Actions → most recent run → scroll down → Artifacts
Download: jobs_latest.json + jobs_latest.csv + summary.json
```

### Option 2: Apify Console (raw, before filters)
```
https://console.apify.com/actors/runs
→ Latest run → Dataset → Export
```

---

## ⚙️ Customize

Everything is in `config.json`:

```json
"titles": ["Senior Frontend Engineer", "Tech Lead"],   ← titles to search
"descriptionMustContain": ["react"],                   ← required in the description
"excludeKeywords": ["consulting", "body shop"],        ← dropped if in title/company
"maxAgeHours": 24,                                     ← only recent jobs
"sources": { "linkedin": { "enabled": true, "limit": 50 } }
```

There is no schedule: the scraper runs only when you start it (Actions → Run workflow).
To make it automatic, see "Want it to run automatically?" in `README.md`.

---

## 💰 Costs

Apify charges per downloaded job, before filters. Max per run =
`titles × (linkedin.limit + tecnoempleo.maxResults + infojobs.maxResults)`.

**Apify free tier:** $5/month
**GitHub free tier:** 2,000 min/month (public repos: unlimited)

---

## 🆘 Help

### "Resource not accessible"
```
Settings → Actions → General
→ Workflow permissions
→ ✅ Read and write permissions
→ Save
```

### Empty results
```
→ Raise maxAgeHours in config.json (e.g. 168 = one week)
→ Relax descriptionMustContain / excludeKeywords
```

---

## 📚 Docs

- **Full docs:** `README.md`
- **Step-by-step setup:** `SETUP_GUIDE.md`
- **Architecture:** `ARCHITECTURE.md`
- **Configuration:** `config.json` (see `_help` inside)

---

## ✅ Checklist

- [ ] `APIFY_TOKEN` secret added
- [ ] Actions enabled
- [ ] Test run with `test_limit: 5` succeeded
- [ ] Results checked (Artifacts)
- [ ] `config.json` adjusted to your profile
