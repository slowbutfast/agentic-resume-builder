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

### Step 2: Querying Resume Roles, Slugs & Structure
- Run `python3 build_resume.py --summary` (or `-s`) for a clean overview tree of active roles, entry keys, and bullet IDs.
- Run `python3 build_resume.py --help` for full CLI documentation and example workflows.
- Run `python3 build_resume.py --schema` to view JSON structure rules.

### Step 3: CLI CRUD Operations & Editing Heuristics
Use deterministic CLI CRUD flags to modify `data/resume_bank.json` safely without manual formatting errors:
- **Role CRUD**: `--add-role`, `--edit-role`, `--delete-role`
- **Entry CRUD**: `--add-project`, `--add-experience`, `--delete-entry`
- **Bullet CRUD**: `--add-bullet`, `--edit-bullet`, `--delete-bullet`

**Content & Density Rules:**
- **First Bullet Rule**: Bullet #1 under any project/role MUST clearly explain what was built and what it does in plain, accessible English. Save deep technical mechanisms for Bullets #2 and #3.
- **Selective Bolding**: Bold quantitative metrics (e.g. `\textbf{97% reduction}`, `\textbf{5+ hours/week}`) and core tech stack names to draw recruiter visual focus. Do NOT bold full sentences.
- **Line Length Target**: Keep bullet text around **220–245 characters** so each bullet spans exactly **2 full lines** edge-to-edge across ~85%–95% of printable line width.
- **No Orphan Widows**: Avoid single-word trailing lines (<4 trailing words). Either trim 2–3 words or expand by 10–15 characters to fill the line out.
- **Date Consistency**: Format all dates consistently using abbreviated months (e.g. `Jun 2026 – Present`, `Aug 2025 – May 2026`).
- **LaTeX Escaping**: Do NOT manually add LaTeX backslashes for `&`, `%`, `$`, `#`, `_` inside JSON strings. The python builder handles escaping automatically.

### Step 4: Compiling & Verifying
Run single-role build or build all:
```bash
python3 build_resume.py --role swe
python3 build_resume.py
```
Check stdout metrics:
- Ensure all variants report `Pages: 1` and `PASSED (1 Page)`.
- If `OVERFLOW` warning occurs: trim 3–5 words from longer bullets using `python3 build_resume.py --edit-bullet <ID> --text "..."`.
- If `UNDERFLOW` warning occurs: expand bullets or add a project key to target role.

---

## 🛠️ Specialized Agent Skills Directory

Refer to dedicated instruction files in the `skills/` directory for detailed specialized agent loops:
- [`skills/project-auditor/SKILL.md`](file:///home/node/global-sandbox/projects/resume/skills/project-auditor/SKILL.md): Technical Resume Auditor prompt to inspect external codebases and extract raw bullet drafts.
- [`skills/resume-bank-editor/SKILL.md`](file:///home/node/global-sandbox/projects/resume/skills/resume-bank-editor/SKILL.md): Autonomous agent loop for role selection, bullet density tuning, building, and page budget verification.
- [`skills/resume-optimizer/SKILL.md`](file:///home/node/global-sandbox/projects/resume/skills/resume-optimizer/SKILL.md): Single-page height density optimizer guide.

