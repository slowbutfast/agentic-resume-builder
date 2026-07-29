# agentic-resume-builder

**`agentic-resume-builder`** is a JSON-driven LaTeX resume generator and experimental AI agent feedback harness built on **Jake Gutierrez's Gold-Standard Resume Template** (the r/EngineeringResumes baseline).

It maintains a single source of truth (`data/resume_bank.json`) to compile role-targeted resume variants (`swe`, `systems`), renders 150 DPI PNG previews, and calculates vertical page fill metrics automatically.

---

## 📌 Current Status & Known Agent Limitations

- **Data & Build Engine**: Fully functional. Generates clean 1-page LaTeX PDFs from configurable JSON databanks.
- **Visual Agent Feedback Loop (Experimental)**: While the pipeline automatically captures image previews and computes page-fill metrics, current LLM vision models still struggle with fine-grained visual line-wrap tuning. Contributions to the visual feedback loop or bounding-box heuristic checkers are welcome!

---

## ⚡ Quickstart Guide

1. **Clone Repository & Setup Data Bank**:
   ```bash
   git clone https://github.com/slowbutfast/agentic-resume-builder.git
   cd agentic-resume-builder
   cp data/resume_bank.example.json data/resume_bank.json
   ```

2. **Compile Resumes & Check Page Metrics**:
   ```bash
   python3 build_resume.py
   ```

3. **Validate Schema & Query CLI Helpers**:
   ```bash
   python3 build_resume.py --lint     # Validate data/resume_bank.json against schema
   python3 build_resume.py --schema   # Display JSON structure cheat-sheet
   python3 build_resume.py --list     # List active variants and selected projects
   ```

---

## 🤖 Pairing with AI Coding Agents (Cursor, Antigravity, Claude Code, OpenCode)

This repository includes built-in AI directives in [`AGENTS.md`](AGENTS.md) and [`skills/resume-optimizer/SKILL.md`](skills/resume-optimizer/SKILL.md).

Simply open your AI coding agent and prompt:
> *"Read AGENTS.md and help me customize my experience and projects in `data/resume_bank.json` to generate my targeted 1-page resumes."*

---

## 📐 Project Structure

```
.
├── build_resume.py           # Root CLI entry point wrapper
├── AGENTS.md                 # System directives for AI coding agents
├── LICENSE                   # MIT License
│
├── src/                      # Engine Python scripts & core tools
│   ├── build_resume.py       # Primary CLI runner & warning evaluator
│   ├── generate_resumes.py   # TeX assembly & pdflatex/pdftoppm compiler
│   └── lint_schema.py        # Automated JSON Schema linter script
│
├── data/                     # Source-of-truth data bank & schemas
│   ├── resume_bank.example.json # Starter anonymized template
│   ├── resume_bank.json      # Master data bank for your experiences
│   └── resume_bank.schema.json # Formal JSON Schema (Draft-07 specification)
│
├── templates/                # LaTeX baseline templates
│   └── main.tex              # Baseline LaTeX template (Jake Gutierrez format)
│
└── skills/                   # Reusable agent skills
    └── resume-optimizer/     # Resume optimizer skill for CLI agents
```

---

## 📄 License
Licensed under the [MIT License](LICENSE). Baseline LaTeX template based on [Jake Gutierrez's Resume Template](https://github.com/sb2nov/resume).
