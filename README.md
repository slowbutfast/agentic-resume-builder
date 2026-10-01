> Note: After using this tool myself for a little bit, I've found it easier to format my resume by copying the cleaned up bullet points into my native LaTex editor (e.g., Overleaf, IDE, etc.), with the original Jake's Engineering Template since it comes out cleaner.

# agentic-resume-builder

> **An Agentic-Native Resume Engineering Engine built around *you* and *your AI assistant*—not the other way around.**

`agentic-resume-builder` is a data-driven system for engineering, auditing, tailoring, and compiling role-focused 1-page software engineering resumes using LaTeX (`templates/main.tex`). 

Rather than forcing developers into rigid web forms or third-party SaaS tools, this project is built to work with your agentic workflow. It provides deterministic CLI CRUD flags, formal JSON Schema validation (`data/resume_bank.schema.json`), 150 DPI PNG preview rendering (`build/previews/`), and specialized AI agent skills (`skills/`) that allow your AI coding assistant (OpenCode, Antigravity, Claude Code, Codex, Cursor) to autonomously inspect, tailor, and optimize resume line density for targeted job listings.

> **Project Goal**: Whether adapting an existing resume or engineering a new one from scratch, this system gets you **~90% of the way there** automatically. From there, you can fine-tune, iterate, and tailor it to your exact needs.

---

## Prerequisites

| Requirement | Why it's needed | Install |
| --- | --- | --- |
| Python 3.9+ | Runs the CLI and build engine | Preinstalled on most systems |
| `pdflatex` | Compiles the LaTeX resume into PDF | **macOS**: `brew install --cask mactex-no-gui` · **Debian/Ubuntu**: `sudo apt install texlive-latex-extra` · **Windows**: [MiKTeX](https://miktex.org/download) |
| `pdftoppm` | Renders 150 DPI PNG previews for agent inspection | **macOS**: `brew install poppler` · **Debian/Ubuntu**: `sudo apt install poppler-utils` |

Verify the two binaries are on your `PATH` before building:
```bash
pdflatex --version && pdftoppm -v
```

> **On Windows**, the interpreter is usually `python` or `py`, not `python3`. Every command below is written as `python3` — substitute accordingly, or run them inside WSL.

---

## New User Quickstart Guide

> Note: you can also make your agent set this up for you instead.

### 1. Get the Code
```bash
git clone https://github.com/slowbutfast/agentic-resume-builder.git
cd agentic-resume-builder
```

> Use a plain `git clone` (or the green **Use this template** button) for your own resume. Only *fork* if you intend to contribute changes back — forks of a public repo are themselves public and cannot be made private, which is the last thing you want holding your contact details.

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs `jsonschema` (schema validation) and `Pillow` (preview fill analysis).

> On newer Debian/Ubuntu and Homebrew Pythons, `pip` refuses to install into the system interpreter ([PEP 668](https://peps.python.org/pep-0668/)). Use a virtual environment:
> ```bash
> python3 -m venv .venv && source .venv/bin/activate
> pip install -r requirements.txt
> ```

### 3. Install Agent Skills
Install the repository skills to equip your AI coding assistant:
```bash
npx skills
```

> Note: If this doesn't work, ask your agent to install the skills for you.

### 4. Create Your Data Bank
`data/resume_bank.json` is your private working copy and is **not tracked by git** — create it from the anonymized starter template:
```bash
cp data/resume_bank.example.json data/resume_bank.json
```

> This file is listed in `.gitignore`, so the real name, phone, email, and GPA you put in it stay on your machine and can never be committed by accident. Only `data/resume_bank.example.json` is tracked in the repository.

### 5. Build the Starter Resumes
Before touching any of your own material, compile what ships with the repo:
```bash
python3 build_resume.py
```

You get four PDFs in `build/pdf/` and four 150 DPI previews in `build/previews/`:

```text
Variant      | Pages  | Vertical Fill %  | Status
swe          | 1      | 68.2           % | PASSED (1 Page)
systems      | 1      | 62.9           % | PASSED (1 Page)
frontend     | 1      | 59.8           % | PASSED (1 Page)
ai_ml        | 1      | 62.9           % | PASSED (1 Page)
```

Four role profiles ship out of the box — `swe` (full-stack), `systems` (distributed systems & infrastructure), `frontend`, and `ai_ml`. Each selects from the *same* underlying `experience_bank` and `project_bank`, so editing a bullet once updates every role that references it. Build a single role with `python3 build_resume.py --role swe`.

### 6. Run Your First Optimization Loop
Now run the linter:
```bash
python3 build_resume.py --lint
```

It reports 8 warnings. That is deliberate:

```text
⚠️  [Project:vector-search-engine:vector_fastapi_tests] 144 chars (< 175 min target).
💡 [Project:smart-task-dashboard] Has 1 bullet (recommended: 2-3 bullets per project).
...
```

**The starter bank is intentionally unoptimized.** Every bullet runs short, two entries have only one bullet, and the pages sit at 59–68% vertical fill against the 85–95% target. It's a realistic first draft — the same shape your resume will be in when you first import it — so you can practice the loop here before your own content is on the line.

There are two distinct problems to fix, and they behave differently:

**Horizontal — a bullet too short to fill its last line.** Expand it with a real technical specific:
```bash
python3 build_resume.py --edit-bullet vector_fastapi_tests \
  --text "Exposed async search endpoints via FastAPI with 40+ Pytest cases covering filter, pagination, and cold-start paths, delivering sub-15ms p99 vector query latencies under 200 concurrent connections."
```
That takes it from 144 to 196 chars and clears the warning. Note the page is still 68.2% full — tightening a bullet fixes the right margin, not the page height.

**Vertical — a page that doesn't reach the bottom.** For that you need *more* bullets, not longer ones:
```bash
python3 build_resume.py --add-bullet smart-task-dashboard --id task_vite_perf \
  --text "Optimized the Vite production build with route-level code splitting and lazy-loaded chart bundles, cutting first-contentful-paint from 2.4s to 0.9s on throttled 3G device profiles."
```
Rebuild and the `swe` variant moves 68.2% → 71.3%, with the one-bullet hint gone.

Then look at the result — this step is not optional:
```bash
python3 build_resume.py --role swe
# open build/previews/preview_resume_swe-1.png
```

Repeat until the page is edge-to-edge and no line ends in a one-word orphan. Fix a few by hand to get the feel, then hand the rest to your agent — `skills/resume-optimizer` and `docs/prompts/prompt_looping.md` automate exactly this loop.

> **On the diagnostics:** they're heuristics, not verdicts. The character thresholds approximate how a line will wrap, but bold spans and long unbreakable tokens throw them off in both directions ([#1](https://github.com/slowbutfast/agentic-resume-builder/issues/1)). A bullet can be flagged and render fine, or pass and wrap badly. **The rendered PNG is the source of truth** — always look at the preview before trusting a number.

### 7. Inspect Roles, Entries & Bullet IDs
Print the full tree of role configurations, entry keys, and bullet IDs (with char counts) — this is how you find the slug to pass to any CRUD flag:
```bash
python3 build_resume.py --summary
# or simply: python3 build_resume.py -s
```

### 8. Build Your Markdown Source of Truth
Now make it yours. Have your AI assistant parse your existing project codebases or current resume into a Markdown file (e.g. `docs/PROJECT_SPECS.md` or `docs/EXPERIENCE_BANK.md`). This document is your master record of raw project specifications, metrics, and background experience — richer than any single resume, and the thing you draw from when tailoring. `skills/project-auditor` is built for this.

### 9. Populate the Bank & Tailor
From that Markdown source, have the agent extract and format targeted bullets into `data/resume_bank.json` for each role you're applying to, then run the loop from step 6 until every variant is one clean page. `skills/resume-bank-editor` handles the tailoring pass against a specific job description.

---

## CLI Operations & Deterministic Agent Flags

`build_resume.py` includes a self-documenting CLI helper interface with full `--help` documentation:

```text
Inspection & Diagnostics:
  --summary, -s       Print overview tree of roles, entries, and bullet IDs with char counts
  --lint              Run JSON Schema validation and bullet density diagnostics
  --list              List active resume role profiles and selected projects
  --schema            Display human-readable JSON schema structure cheat-sheet
  --help              Display complete CLI documentation and example LLM workflows

Compilation Targets:
  python3 build_resume.py              Build all configured resume roles
  python3 build_resume.py --role <KEY> Build only the specified tailored role (e.g. backend_eng)
  python3 build_resume.py --role <KEY> --sanitize [FIELDS]
                                     Build with personal contact fields masked.
                                     Comma-separated subset of name,phone,email,linkedin,github
                                     (default: phone,email,linkedin,github). PDF is saved as
                                     <name>_sanitized.pdf so the real resume is never overwritten.

Job-Tailored Role CRUD:
  --add-role --key <KEY> --title "<TITLE>" --out <FILENAME> --experiences <KEY1,KEY2> --projects <KEY1,KEY2>
  --edit-role <KEY> [--title "<TITLE>"] [--out <FILENAME>] [--experiences <KEYS>] [--projects <KEYS>]
  --delete-role <KEY>

Entry CRUD (Projects & Experiences):
  --add-project --key <KEY> --name "<NAME>" --tech "<STACK>" --dates "<DATES>"
  --add-experience --key <KEY> --company "<COMPANY>" --title "<TITLE>" --location "<LOC>" --dates "<DATES>"
  --delete-entry <KEY>

Bullet CRUD (Auto-resolves Parent Key):
  --add-bullet <PARENT_KEY> --id <ID> --text "<TEXT>" [--line-count <N>]
  --edit-bullet <ID> --text "<TEXT>" [--line-count <N>] [--status <STATUS>]
  --delete-bullet <ID>
```

---

## Pairing with AI Coding Assistants

This repository contains dedicated agent directives in [`AGENTS.md`](AGENTS.md) and modular skills in `skills/`:

- **[`skills/project-auditor/SKILL.md`](skills/project-auditor/SKILL.md)**: Technical Resume Auditor & Analyst skill to audit software project codebases and extract raw bullet material.
- **[`skills/resume-bank-editor/SKILL.md`](skills/resume-bank-editor/SKILL.md)**: Autonomous agent optimization loop for job tailoring, bullet density tuning, and page height budget verification.
- **[`skills/resume-optimizer/SKILL.md`](skills/resume-optimizer/SKILL.md)**: Single-page height density optimizer guide.

Standalone prompts you can paste into any assistant live in `docs/prompts/`:

- **[`prompt_bullet_generator.md`](docs/prompts/prompt_bullet_generator.md)**: Bullet-writing formula, verb/stack/mechanism/metric structure, and ATS-friendly phrasing guidelines.
- **[`prompt_looping.md`](docs/prompts/prompt_looping.md)**: The autonomous edit → compile → inspect-preview loop for hitting 1-page and edge-to-edge density targets.

---

## Project Structure & Directory Layout

```
.
├── build_resume.py           # Root CLI entry point wrapper & CRUD engine
├── requirements.txt          # Python dependencies (jsonschema, Pillow)
│
├── src/                      # Engine Python scripts & core tools
│   ├── build_resume.py       # Primary CLI runner & bank CRUD evaluator
│   ├── generate_resumes.py   # TeX assembly & pdflatex/pdftoppm compiler
│   └── lint_schema.py        # Automated JSON Schema linter script
│
├── data/                     # Source-of-truth data bank & schemas
│   ├── resume_bank.json      # YOUR private bank — git ignored, created from the example
│   ├── resume_bank.example.json # Anonymized starter template — deliberately unoptimized
│   └── resume_bank.schema.json # Formal JSON Schema (Draft-07 specification)
│
├── templates/                # LaTeX baseline templates
│   └── main.tex              # Baseline LaTeX template (Jake Gutierrez format)
│
├── skills/                   # Reusable AI Agent Skills
│   ├── project-auditor/      # Codebase auditing & bullet extraction skill
│   ├── resume-bank-editor/   # Autonomous bank CRUD & job tailoring loop
│   └── resume-optimizer/     # Page budget & visual height density optimizer
│
├── docs/                     # Technical specifications & guidelines
│   ├── PEER_REVIEW_FEEDBACK.md # Peer review heuristics & wording guidelines
│   ├── BULLET_DENSITY_TRADE_OFFS.md # Portfolio layout math & trade-off guide
│   └── prompts/              # Reusable prompts for bullet writing & agent loops
│
├── tests/                    # Automated regression test suite
│   └── test_cli_crud.py      # CLI CRUD automated test runner
│
└── build/                    # Generated build artifacts (Git ignored)
    ├── tex/                  # Assembled TeX source files (resume_swe.tex, etc.)
    ├── pdf/                  # Final compiled PDF resumes (resume_swe.pdf, etc.)
    └── previews/             # 150 DPI PNG screenshot previews for visual inspection
```

---

## Important Guidelines

### 1. Mandatory Human Verification
AI agents assist with extraction, bullet auditing, line-density tuning, and LaTeX compilation, but final outputs must be thoroughly reviewed by a human. Always verify the accuracy of metrics, dates, and claims in compiled PDF resumes (`build/pdf/`) prior to job applications.

### 2. Open Source Contributions
Community contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started. Feel free to submit pull requests or issues for expanding agent skills, refining LaTeX templates, or improving build tools and diagnostics.

---

## License & Credits

Licensed under the [MIT License](LICENSE).

Baseline LaTeX formatting adapted from **[Jake Gutierrez's](https://github.com/jakegut/resume) Gold-Standard Resume Template** (`r/EngineeringResumes`), which is itself based on **[Sourabh Bajaj's](https://github.com/sb2nov/resume) original LaTeX resume template**. Both are MIT licensed.


