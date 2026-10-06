# Architecture

The system has two independent parts that share `config.json` and the result files:

1. **Automated scraper** (GitHub Actions, no AI) — searches jobs on 4 sites, filters them and publishes the results.
2. **Agents** (Claude Code, with AI) — used on demand to trigger the scraper, analyze the results and search further.

The scraper can be triggered in 4 ways: cron, the "Run workflow" button, the agent (`gh workflow run ... -f sources=... -f test_limit=...`)
or locally (`scripts/run_local.py`, also used by the agent).

```
/search-jobs tecnoempleo,infojobs 5          ← typed by the user (only the user can trigger it)
        │
        ▼
.claude/skills/search-jobs/SKILL.md          ← WHAT to do: arguments → environment → run → report
   context: fork · agent: job-researcher
        │  runs inside
        ▼
.claude/agents/job-researcher.md             ← HOW: tools, model, gh/local commands,
                                                cost rules, ranking format
```

## Overview

```
                         ┌──────────────────────────────┐
                         │         config.json          │  ◄── SINGLE SOURCE OF TRUTH
                         │  titles · descriptionMust-   │      (edit only here)
                         │  Contain · excludeKeywords · │
                         │  excludeCompanies ·          │
                         │  maxAgeHours · sources.*     │
                         └──────┬────────────────┬──────┘
                       read by  │                │   read by
          ┌─────────────────────┘                └─────────────────────┐
          ▼                                                            ▼
┌───────────────────────────────────────┐        ┌──────────────────────────────────────┐
│  AUTOMATED · GitHub Actions           │        │  ON DEMAND · Claude Code             │
│                                       │        │                                      │
│  ⏰ cron Sun/Mon/Tue 09:00 UTC         │        │  CLAUDE.md ──@import──► AGENTS.md    │
│  ▶  or "Run workflow" / gh (agent)    │        │   (context: profile, sites, rules)   │
│  💻 or scripts/run_local.py (.env)    │◄───────┤  🤖 job-researcher (subagent)        │
│            │                          │triggers│   • triggers the scraper (gh/local)  │
│            ▼                          │        │   • reads config + jobs_latest.json  │
│  linkedin-scraper-advanced.yml        │        │   • extra web search                 │
│  (Python script)                      │        │   • verifies, scores 1–5, ranks      │
│            │                          │        │   • never edits config or workflow   │
│            ▼                          │        └──────────────────▲───────────────────┘
│  ┌─────────── Apify ───────────┐      │                           │
│  │ LinkedIn    valig/...       │      │                           │
│  │ Tecnoempleo blackfalcon/... │      │      gh run download      │
│  │ InfoJobs    shahidirfan/... │      │      → results/<run-id>/  │
│  └─────────────────────────────┘      │                           │
│  ┌── Public API (free) ────────┐      │                           │
│  │ Manfred  getmanfred.com     │      │                           │
│  └─────────────────────────────┘      │                           │
│            │                          │                           │
│            ▼                          │                           │
│  📦 Artifact (90 days) ───────────────┼───────────────────────────┘
│   jobs_latest.json / .csv             │
│   summary.json · run_info.json        │
└───────────────────────────────────────┘
```

## Workflow flow

```
 ① CONFIG          read config.json ─► titles × enabled sites = number of searches
                   (SOURCES / TEST_LIMIT reduce it, for tests)
        │
        ▼
 ② STEP 1 START    POST /acts/{actor}/runs for each search  (they run in parallel on Apify)
        │            LinkedIn:    keywords + location + datePosted + f_E/f_JT
        │            Tecnoempleo: query + date_start + includeDetails
        │            InfoJobs:    searchUrl (keyword + sinceDate + sortBy)
        ▼
 ③ STEP 2 WAIT     poll each run's status every 15 s (max 10 min per run)
        │
        ▼
 ④ STEP 3 FETCH    GET /datasets/{id}/items  ──►  for EACH search:
        │
        │     ┌──────────────┐   ┌──────────────────┐   ┌───────────────────┐
        │     │ 🕐 published  │──►│ 🔎 "react" in     │──►│ 🚫 title/company   │──► ✅ kept
        │     │ < maxAge?    │   │ description/tech?│   │ not excluded?     │
        │     └──────┬───────┘   └────────┬─────────┘   └─────────┬─────────┘
        │            ✗ dropped            ✗ dropped               ✗ dropped
        │
        │     + Manfred: list ─► open each offer ─► same 3 filters
        ▼
 ⑤ DEDUPE          normalized title + company ─► 1 job, with found_in = [every search]
        │
        ▼
 ⑥ STEP 4 SAVE     jobs_latest.json (full) · jobs_latest.csv (same columns for all sites)
        │          summary.json (per search, duplicates removed) · run_info.json
        ▼
 ⑦ PUBLISH         upload-artifact + summary on the GitHub run page
```

## Files

| File | Role |
|---|---|
| `config.json` | Titles, filters, time window and per-site settings. Single source of truth. |
| `.github/workflows/linkedin-scraper-advanced.yml` | The scraper (Python script inside the YAML). No hardcoded search values. |
| `.github/workflows/linkedin-scraper.yml` | Legacy version, LinkedIn only, no schedule. |
| `scripts/run_local.py` | Runs the workflow script locally (token in `.env`). |
| `AGENTS.md` / `CLAUDE.md` | Context for AI agents. |
| `.claude/skills/search-jobs/SKILL.md` | `/search-jobs` command: runs the scraper and ranks the results inside the agent. |
| `.claude/agents/job-researcher.md` | Job research and ranking subagent. |

## Notes

- Apify charges **per downloaded job, before the filters**.
- Unknown dates are not dropped by the age filter.
- Dedupe is by title + company: the same company posting the same title in two cities counts as one job.
