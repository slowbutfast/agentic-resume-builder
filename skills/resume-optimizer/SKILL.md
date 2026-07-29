---
name: resume-optimizer
description: Autonomous bullet-tuning and 1-page visual height density optimizer for Jake Gutierrez LaTeX resumes.
---

# Resume Optimizer Skill

This skill provides step-by-step instructions for AI agents to edit `data/resume_bank.json`, run schema linting, build PDFs, and verify single-page layout metrics.

## Execution Workflow

1. **Verify Data Bank & Schema**:
   Run schema validation to ensure JSON integrity:
   ```bash
   python3 build_resume.py --lint
   ```

2. **Inspect Current Configurations**:
   Check active variants and project selections:
   ```bash
   python3 build_resume.py --list
   ```

3. **Format Bullet Point Text**:
   - Target character count per bullet: ~220–245 characters (2 full lines across `0.97\textwidth` / `1.0\textwidth`).
   - Line Widow Threshold: Never leave fewer than 4 trailing words on the last line of a bullet.

4. **Execute Build & Evaluate Page Budget**:
   ```bash
   python3 build_resume.py
   ```
   - Standard output must report `PASSED (1 Page)` with vertical page fill between 82.0% and 95.0%.
