# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Cursor, etc.) working in this repository.

## What this repo is

A job scraper for LinkedIn, Tecnoempleo, InfoJobs and Manfred. GitHub Actions runs it **only on demand**
(Run workflow button / `workflow_dispatch` — there is deliberately no schedule; don't add one unless the user asks), triggers [Apify](https://apify.com) actors for a set of search queries
(Manfred is read from its public API), downloads the results and
publishes them as workflow artifacts (`jobs_latest.json`, `jobs_latest.csv`, `summary.json`,
`run_info.json`).

The Python scraper lives inline in the workflow YAML; all search settings come from `config.json`.

## Layout

| Path | Purpose |
|------|---------|
| `config.json` | **Single source of truth**: titles, `descriptionMustContain`, `excludeKeywords`, `excludeCompanies`, `maxAgeHours`, per-site settings (`sources.*`: `enabled`, `actor`, limits). `_help` documents every field. |
| `.github/workflows/linkedin-scraper-advanced.yml` | Main workflow (manual `workflow_dispatch` only, optional inputs `sources`, `test_limit`): reads `config.json`, starts the searches, waits, downloads, filters, dedupes, saves JSON/CSV, uploads artifacts. No search values are hardcoded here. |
| `.github/workflows/linkedin-scraper.yml` | Legacy LinkedIn-only workflow (manual only) |
| `scripts/run_local.py` | Runs the workflow's inline Python locally. Token from `APIFY_TOKEN` or `.env`. `python scripts/run_local.py tecnoempleo,infojobs 5` = only those sites, 5 results per title. |
| `ARCHITECTURE.md` | Architecture and workflow diagrams — update when the pipeline changes |
| `README.md`, `QUICKSTART.md`, `SETUP_GUIDE.md` | User docs |
| `.claude/agents/` | Claude Code subagents for this repo |

## Candidate profile (the "who are we searching for")

Use this when searching, filtering or ranking jobs:

- **Roles:** Senior / Staff Frontend Engineer, Frontend Lead, Tech Lead, Senior Fullstack / Software Engineer
- **Stack:** React (required in the job description), Next.js, TypeScript, Node.js
- **Location:** Madrid / Spain, or Remote (EU timezone)
- **Contract:** Full-time
- **Seniority:** Mid-Senior and above
- **Exclude:** consultancies and body shops (`excludeKeywords` / `excludeCompanies` in `config.json`). Outsourcing companies are welcome.

`config.json` is the source of truth — if it changes, it wins over this section.

## Job sources

Every entry in `config.json` → `titles` is searched on each enabled Apify site (LinkedIn, Tecnoempleo, InfoJobs):
one Apify run per title per site. Manfred is read in full from its API.

| Site | How | Payload the workflow builds |
|------|-----|----------------|
| LinkedIn | Apify actor `RIGGeqD6RqKmlVoQU` (valig/linkedin-jobs-scraper) | `keywords`, `location`, `limit`, `datePosted` (`r86400`/`r604800`/`r2592000`), `urlParam` with `f_E` (experience) and `f_JT` (job type). The actor has NO `title`/`contractType`/`experienceLevel` fields. Returns `description`. |
| Tecnoempleo | Apify actor `blackfalcondata~tecnoempleo-scraper` (~$0.0015/result) | `query`, `province`, `date_start` (YYYY-MM-DD only), `maxResults`, `includeDetails: true` (needed for `description`/`technologies`) |
| InfoJobs | Apify actor `shahidirfan~infojobs-scraper` (~$0.001/result) | `searchUrl` (InfoJobs URL with `keyword`, `sinceDate` = `_24_HOURS`/`_7_DAYS`/`_15_DAYS`/`ANY`, `sortBy=PUBLICATION_DATE`), `results_wanted`. Returns `description_text`, `published_at`. |
| Manfred | Free public API `https://www.getmanfred.com/api/v2/public/offers` + `/offers/{id}` for details (no Apify) | No search params — list returns all active offers (~20); detail has full text, `techs` and `lastStatusChange` (publish date) |

## Pipeline (STEP 3, applied to every source, in this order)

1. **Age** — keep jobs published in the last `maxAgeHours` (each site's native filter is rounded up; the
   script re-checks `publishDateISO` / `published_at` / `postedAt` / Manfred `lastStatusChange`). Unknown dates are kept.
2. **`descriptionMustContain`** — at least one word in the description or technologies list. The title does NOT count,
   so titles in `config.json` must not contain "React".
3. **`excludeKeywords` / `excludeCompanies`** — dropped if the title or company contains a keyword, or the company
   name (normalized like the dedupe key) is exactly one of `excludeCompanies`.
4. **Dedupe** — key = normalized title + company (no accents/case/punctuation; falls back to URL). The kept job
   gets `_found_in` with every `source: search` that returned it. `summary.json` has `duplicates_removed`.

Every job gets `_source` and `_search_name`. `jobs_latest.csv` normalizes all sites to the same columns
(`source, search, found_in, title, company, location, remote, salary, postedAt, url`); `jobs_latest.json` keeps the raw fields.
The log prints `🧾 Fields:` for the first result of each search — use it to fix field mappings in `pick(...)` helpers.

Apify endpoints: start `POST /v2/acts/{actor}/runs`, status `GET /v2/actor-runs/{runId}`,
items `GET /v2/datasets/{datasetId}/items`. Apify charges per downloaded result, before filters — watch `titles × limits`.

## Rules for agents

- **Never commit secrets.** The Apify token is only `secrets.APIFY_TOKEN` on GitHub or the git-ignored `.env` locally.
- Don't commit scraper output (`jobs_latest.*`, `summary.json`, `run_info.json`) — it's delivered as artifacts.
- **Never commit or copy anything from `cv/`** (personal data; git-ignored). Only the template and renderer in `.claude/skills/tailor-cv/` are committed.
- **Change searches/filters in `config.json`, never in the workflow.** Update `_help` when adding a field.
- When editing the workflow, keep the inline Python valid and test with `scripts/run_local.py` (small `TEST_LIMIT`) or `workflow_dispatch`.
- Everything in the repo is in English: docs, comments, log messages, `config.json` `_help`, skills and agents.

## Agents

| Agent | File | Use it for |
|-------|------|------------|
| `/tailor-cv` (skill) | `.claude/skills/tailor-cv/SKILL.md` | User-only. `/tailor-cv <job URL | text | ranking #> [--cover-letter]` rewrites the CV from `cv/master.md` for one job and renders a PDF (`render_pdf.py`, headless Edge/Chrome) into `cv/tailored/`. Never invents experience. Runs in the main conversation so the user can iterate. |
| `/search-jobs` (skill) | `.claude/skills/search-jobs/SKILL.md` | User-only entry point (`disable-model-invocation`). `/search-jobs [sites] [limite] [local]` runs the scraper and ranks the results, executing inside `job-researcher` (`context: fork`) |
| `job-researcher` | `.claude/agents/job-researcher.md` | Running the scraper (GitHub via `gh workflow run`, or `scripts/run_local.py`), then finding, filtering and ranking job openings that match the candidate profile |
