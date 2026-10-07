---
name: search-jobs
description: Runs the job scraper (LinkedIn, Tecnoempleo, InfoJobs, Manfred) and returns a ranking of the jobs found.
argument-hint: "[sites] [limit] [local]  e.g. tecnoempleo,infojobs 5"
disable-model-invocation: true
context: fork
agent: job-researcher
---

# /search-jobs

Arguments received: `$ARGUMENTS`

## 1. Parse the arguments

All optional, in any order:

| Argument | Example | Meaning | If missing |
|---|---|---|---|
| sites | `tecnoempleo,infojobs` | Only these sites (`linkedin`, `tecnoempleo`, `infojobs`, `manfred`) | All sites enabled in `config.json` |
| limit | `5` | Max jobs per title on each site | Limits from `config.json` (full run) |
| `local` | `local` | Run with `scripts/run_local.py` instead of GitHub | GitHub (option A) |

Without a limit it is a **full run**: before starting, show the maximum number of jobs and the estimated cost
(rules in "Running the scraper"). Don't ask for confirmation — the user already asked by typing the command.

## 2. Check the environment

- Option A (GitHub): `gh auth status` must pass.
- Option B (`local`): the `.env` file must exist in the repo root (don't read its contents — only check it exists).
- If the chosen option isn't available and the other one is, use the other one and say so.
  If neither is available, stop and explain how to set one up (`winget install GitHub.cli` + `gh auth login`, or create `.env`).

## 3. Run the scraper

Follow "Running the scraper" in your instructions, with the sites and limit from step 1.
For option A, wait for the run to finish and download the artifact to `results/<run-id>/`.

## 4. Report

1. **Run:** where it ran (GitHub with the run link, or local), sites, limit, duration.
2. **Numbers** from `summary.json`: jobs per search, total, duplicates removed. List any `❌` lines from the log.
3. **Ranking** of the jobs in `jobs_latest.json`, in the format from the "Output" section of your instructions.
   If there are more than 20 jobs, show the top 20 and say how many were left out.
   Also save the full ranking table (with `#` and the job link) to `results/latest-ranking.md`,
   overwriting the previous one — `/tailor-cv <#>` reads it.
4. If a CSV column is always empty for a site (e.g. `company` for InfoJobs), say which one
   and show that site's `🧾 Fields:` line from the log — it means the field mapping needs adjusting.
