# agentic-resume-builder

> **An Agentic-Native Resume Engineering Engine built around *you* and *your AI assistant*—not the other way around.**

`agentic-resume-builder` is a data-driven system for engineering, auditing, tailoring, and compiling role-focused 1-page software engineering resumes using LaTeX (`templates/main.tex`). 

Rather than forcing developers into rigid web forms or third-party SaaS tools, this project is built to work with your agentic workflow. It provides deterministic CLI CRUD flags, formal JSON Schema validation (`data/resume_bank.schema.json`), 150 DPI PNG preview rendering (`build/previews/`), and specialized AI agent skills (`skills/`) that allow your AI coding assistant (OpenCode, Antigravity, Claude Code, Codex, Cursor) to autonomously inspect, tailor, and optimize resume line density for targeted job listings.

> **Project Goal**: Whether adapting an existing resume or engineering a new one from scratch, this system gets you **~90% of the way there** automatically. From there, you can fine-tune, iterate, and tailor it to your exact needs.

---

## New User Quickstart Guide

Getting started takes less than two minutes:

> Note: you can also make your agent set this up for you instead.

### 1. Install Agent Skills
Install the repository skills to equip your AI coding assistant:
```bash
npx skills
```

> Note: If this doesn't work, ask your agent to install the skills for you.

### 2. Create Markdown Source of Truth
Have your AI assistant parse your existing project codebases or current resume to generate a Markdown file (e.g., `docs/PROJECT_SPECS.md` or `docs/EXPERIENCE_BANK.md`). This Markdown document serves as your master source of truth for all raw project specifications, metrics, and background experience, making manual review, CRUD updates, formatting decisions, and fine-tune tailoring intuitive.

### 3. Populate Resume Bank JSON
From the Markdown source of truth, have the agent extract and format targeted bullet points into `data/resume_bank.json` structured specifically for your target resume roles.

*(Alternatively, initialize manually by copying the starter template: `cp data/resume_bank.example.json data/resume_bank.json`)*

### 4. Inspect Active Roles & Entry Slugs
Run the CLI summary tool to view all configured job roles, project keys, experience keys, and bullet IDs:
```bash
python3 build_resume.py --summary
# or simply: python3 build_resume.py -s
```

### 5. Compile Tailored PDFs & Render Previews
Compile all resume roles into PDFs (`build/pdf/`) and 150 DPI PNG previews (`build/previews/`), or compile a single target role:
```bash
# Build all configured resume roles
python3 build_resume.py

# Or build a specific tailored role profile (e.g. swe, ai_ml, backend_eng)
python3 build_resume.py --role swe
```

### 6. Validate Data Bank Schema
Run automated JSON Schema validation and 2-line bullet density diagnostics anytime:
```bash
python3 build_resume.py --lint
```

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

---

## Project Structure & Directory Layout

```
.
├── build_resume.py           # Root CLI entry point wrapper & CRUD engine
│
├── src/                      # Engine Python scripts & core tools
│   ├── build_resume.py       # Primary CLI runner & bank CRUD evaluator
│   ├── generate_resumes.py   # TeX assembly & pdflatex/pdftoppm compiler
│   └── lint_schema.py        # Automated JSON Schema linter script
│
├── data/                     # Source-of-truth data bank & schemas
│   ├── resume_bank.json      # Master database for all experiences & projects
│   ├── resume_bank.example.json # Starter anonymized template
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
│   ├── PROJECT_SPECS.md      # Comprehensive project technical specs & audit notes
│   ├── PEER_REVIEW_FEEDBACK.md # Peer review heuristics & wording guidelines
│   └── BULLET_DENSITY_TRADE_OFFS.md # Portfolio layout math & trade-off guide
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
Community contributions are welcome. Feel free to submit pull requests or issues for expanding agent skills, refining LaTeX templates, or improving build tools and diagnostics.

---

## License & Credits

Licensed under the [MIT License](LICENSE). Baseline LaTeX formatting adapted from **Jake Gutierrez's Gold-Standard Resume Template** (`r/EngineeringResumes`).


