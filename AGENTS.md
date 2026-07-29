# AI Agent Directives for `agentic-resume-builder`

Welcome! If you are an AI coding assistant (Cursor, Anti-Gravity CLI, OpenCode, Claude Code, OpenChamber, or Gemini CLI) helping a user generate or edit their resume using this repository, follow these core directives.

---

## 🎯 System Architecture Overview

1. **Master Source of Truth**:
   - Primary data bank: `data/resume_bank.json` (created by copying `data/resume_bank.example.json`).
   - Schema specification: `data/resume_bank.schema.json`.
2. **LaTeX Baseline Template**:
   - Located in `templates/main.tex` (based on **Jake Gutierrez's Gold-Standard Resume Template**).
3. **Compilation Pipeline**:
   - Engine script: `src/generate_resumes.py`.
   - CLI entry point: `build_resume.py`.

---

## 🤖 How to Help the User (Step-by-Step Agent Workflow)

### Step 1: Initial Setup Check
When a user asks you to explain or set up their resume:
1. Check if `data/resume_bank.json` exists. If not, instruct or run:
   ```bash
   cp data/resume_bank.example.json data/resume_bank.json
   ```
2. Run schema validation to verify environment:
   ```bash
   python3 build_resume.py --lint
   ```

### Step 2: Querying Resume Variants & Structure
- Run `python3 build_resume.py --list` to inspect active variants (`swe`, `systems`, etc.).
- Run `python3 build_resume.py --schema` to view JSON structure rules.

### Step 3: Editing Bullet Points & Experiences
When editing or adding experiences/projects to `data/resume_bank.json`:
- **Line Length Target**: Keep bullet text around **220–245 characters** so each bullet spans exactly **2 full lines** edge-to-edge across ~85%–95% of printable line width.
- **No Orphan Widows**: Avoid single-word trailing lines (<4 trailing words). Either trim 2–3 words or expand by 10–15 characters to fill the line out.
- **LaTeX Escaping**: Do NOT manually add LaTeX backslashes for `&`, `%`, `$`, `#`, `_` inside JSON strings. The python builder handles escaping automatically.

### Step 4: Compiling & Verifying
Always run `build_resume.py` after editing:
```bash
python3 build_resume.py
```
Check stdout metrics:
- Ensure all variants report `Pages: 1` and `PASSED (1 Page)`.
- If `OVERFLOW` warning occurs: trim 3–5 words from longer bullets.
- If `UNDERFLOW` warning occurs: expand bullets or add a project key to `configurations[variant]["projects"]`.
