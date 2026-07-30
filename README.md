# 🚀 agentic-resume-builder

> **An Agentic-Native Resume Engineering Engine built around *you* and *your AI assistant*—not the other way around.**

`agentic-resume-builder` is a data-driven system for engineering, auditing, tailoring, and compiling role-focused 1-page software engineering resumes using LaTeX (`templates/main.tex`). 

Rather than forcing developers into rigid web forms or third-party SaaS tools, this project is built from the ground up for seamless human-AI pair programming. It provides deterministic CLI CRUD flags, formal JSON Schema validation (`data/resume_bank.schema.json`), 150 DPI PNG preview rendering (`build/previews/`), and specialized AI agent skills (`skills/`) that allow your AI coding assistant (Cursor, Antigravity, Claude Code, OpenCode) to autonomously inspect, tailor, and optimize resume line density for targeted job listings.

---

## 🏁 New User Quickstart Guide

Getting started takes less than two minutes:

### 1. Initialize Your Master Data Bank
Copy the starter anonymized data bank to create your single-source-of-truth JSON file:
```bash
cp data/resume_bank.example.json data/resume_bank.json
```

### 2. Inspect Active Roles & Entry Slugs
Run the CLI summary tool to view all configured job roles, project keys, experience keys, and bullet IDs:
```bash
python3 build_resume.py --summary
# or simply: python3 build_resume.py -s
```

### 3. Compile Tailored PDFs & Render Previews
Compile all resume roles into PDFs (`build/pdf/`) and 150 DPI PNG previews (`build/previews/`), or compile a single target role:
```bash
# Build all configured resume roles
python3 build_resume.py

# Or build a specific tailored role profile (e.g. swe, ai_ml, backend_eng)
python3 build_resume.py --role swe
```

### 4. Validate Data Bank Schema
Run automated JSON Schema validation and 2-line bullet density diagnostics anytime:
```bash
python3 build_resume.py --lint
```

---

## 🛠️ CLI Operations & Deterministic Agent Flags

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

## 🤖 Pairing with AI Coding Assistants

This repository contains dedicated agent directives in [`AGENTS.md`](AGENTS.md) and modular skills in `skills/`:

- **[`skills/project-auditor/SKILL.md`](skills/project-auditor/SKILL.md)**: Technical Resume Auditor & Analyst skill to audit software project codebases and extract raw bullet material.
- **[`skills/resume-bank-editor/SKILL.md`](skills/resume-bank-editor/SKILL.md)**: Autonomous agent optimization loop for job tailoring, bullet density tuning, and page height budget verification.
- **[`skills/resume-optimizer/SKILL.md`](skills/resume-optimizer/SKILL.md)**: Single-page height density optimizer guide.

---

## 📐 Project Structure & Directory Layout

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

## ⚠️ Important Directives, Shortcomings & Open Source Contributions

### 1. Human Inspection & Authenticity Mandate (Do NOT Trust LLMs 100%)
- **Always Manually Review Generated Resumes**: While `agentic-resume-builder` automates formatting, character density diagnostics, and data bank CRUD operations, **you must always manually inspect your compiled PDF resumes (`build/pdf/`) and verify technical metrics before applying or interviewing**.
- **Zero Fabricated Data**: AI agents must never hallucinate fake production metrics (e.g., fake user counts or unverified benchmark numbers). Frame achievements around real architectural implementations or derived code characteristics.

### 2. Known Limitations & Features Needing Work
- **Line-Wrap & Character Width Heuristics**: The CLI linter evaluates raw character lengths, but variable-width proportional fonts and LaTeX formatting tags (`\textbf{...}`) can cause edge cases. Work is underway to calculate printable character widths strictly ([Issue #11](https://github.com/slowbutfast/resume/issues/11)).
- **Zero-Install NPX Package**: CLI commands currently run via Python. Packaging into a zero-install `npx agentic-resume-builder` executable wrapper is tracked in [Issue #8](https://github.com/slowbutfast/resume/issues/8).
- **Automated Resume Importer**: Parsing existing raw PDFs/Word docs automatically into `data/resume_bank.json` is tracked in [Issue #10](https://github.com/slowbutfast/resume/issues/10).

### 3. Community Contributions Welcome!
We welcome open-source contributions! Whether you want to improve visual bounding-box checkers, enhance LaTeX baseline templates, expand AI agent skills, or contribute bug fixes, feel free to open a Pull Request or Issue.

---

## 📜 License & Credits

Licensed under the [MIT License](LICENSE). Baseline LaTeX formatting adapted from **Jake Gutierrez's Gold-Standard Resume Template** (`r/EngineeringResumes`).

