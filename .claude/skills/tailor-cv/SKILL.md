---
name: tailor-cv
description: Rewrites the user's CV for a specific job (from a URL, pasted text, or a number from the last /search-jobs ranking) and exports it as PDF. Never invents experience.
argument-hint: "<job URL | pasted job text | ranking number> [--cover-letter]"
disable-model-invocation: true
---

# /tailor-cv

Arguments received: `$ARGUMENTS`

Everything lives in `cv/` (git-ignored — the repo is public, never commit or copy CV data elsewhere):

```
cv/
├── original/            the user's original PDF CV(s)
├── master.md            the full, true CV — single source of truth for every tailored version
└── tailored/<YYYY-MM-DD>-<company>-<role>/
    ├── job.md           the job description used
    ├── cv.html          tailored CV (from the template)
    ├── cv.pdf           tailored CV — the file to send
    ├── report.md        match report
    └── cover-letter.md  only with --cover-letter
```

## 0. Make sure `cv/master.md` exists

If it doesn't:
1. Read the PDF in `cv/original/` (if there are several, ask which one is the current CV).
2. Convert it **faithfully** to `cv/master.md`: contact details, summary, every role (title, company, location,
   dates, all bullets), projects, skills, education, certifications, languages. Copy, don't rewrite or improve.
3. Stop and ask the user to review `cv/master.md` and add anything missing (more achievements, numbers,
   tools used). Explain that the richer the master, the better every tailored CV. Do not tailor in this run.

If there is no PDF in `cv/original/` either, ask the user to put their CV there.

## 1. Get the job

- **URL** → WebFetch it. If the page is blocked or empty (LinkedIn often is), ask the user to paste the text.
- **Number** → the job with that `#` in `results/latest-ranking.md` (written by `/search-jobs`); fetch its link.
- **Pasted text** → use it as is.

Extract: job title, company, location/remote, seniority, language of the ad, must-have requirements,
nice-to-haves, and the exact keywords/technologies used. Save the description to `job.md`.

## 2. Tailor — rules

**Never invent.** Every fact in the tailored CV must be in `cv/master.md`. No new skills, tools, titles,
employers, dates, numbers or responsibilities. If the job asks for something the master doesn't show, it goes to
the "Gaps" section of the report, never into the CV.

Allowed:
- **Headline** = the job's title (if it honestly matches the user's level), e.g. "Senior Frontend Engineer".
- **Summary** rewritten for this job: 3–4 lines, leading with the experience that matters most here.
- **Reorder** skills and bullets so the most relevant come first; **trim** what's irrelevant to keep it to
  1 page (2 max for 10+ years of experience). Older roles can shrink to 1–2 bullets.
- **Reword** true bullets using the job's exact keywords when they describe the same thing
  (e.g. master says "component library", job says "design system", and it was one → "design system").
- **Language:** write the CV in the language of the job ad (Spanish ad → Spanish CV, English → English).
- Keep dates, titles and company names exactly as in the master.

ATS: one column, standard section names, the job's keywords written out in full (e.g. "TypeScript", not "TS"),
no text in images.

## 3. Build the PDF

1. Copy `.claude/skills/tailor-cv/template.html` to `cv/tailored/<folder>/cv.html` and fill every `{{...}}`
   (repeat the `.job` block per role; remove blocks/links that don't apply; set `lang`; translate section names).
2. Run: `python .claude/skills/tailor-cv/render_pdf.py cv/tailored/<folder>/cv.html`
3. Read the generated `cv.pdf` to check it: page count, nothing cut off, extracted text in the right order.
   If it's over the page limit, trim and render again.

## 4. Report (`report.md`, and summarize it in chat)

- **Match:** must-haves covered / total, with a short honest assessment (strong / reasonable / stretch).
- **What was emphasized** and why.
- **Gaps:** requirements the master doesn't show. For each, ask: "Have you done this? If so, add it to
  `cv/master.md` and run /tailor-cv again."
- **Keywords** from the ad that are now in the CV, and any that couldn't be used.
- The path to `cv.pdf`.

## 5. Cover letter (only with `--cover-letter`)

`cover-letter.md`: 3 short paragraphs in the ad's language — why this company/role, 2–3 proofs from the master
that match the must-haves, closing. Same rule: nothing invented. Don't use generic filler.

## Iterating

The user may follow up with "shorter", "more leadership", "in English", etc. Edit `cv.html`, re-render, and
re-check the PDF. If they tell you a new fact about their experience, also add it to `cv/master.md` so future
CVs get it.
