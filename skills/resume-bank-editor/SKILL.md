---
name: resume-bank-editor
description: Autonomous job-tailoring and bank CRUD optimization loop for agentic resume editing.
---

# Resume Bank Editor Skill

This skill provides step-by-step instructions for AI agents operating on `data/resume_bank.json` to tailor resumes for specific job descriptions, modify entries/bullets via CLI CRUD flags, lint schema rules, build PDFs, and optimize visual page budget metrics.

## Autonomous Optimization Loop

1. **Inspect Bank Summary**:
   Run `--summary` to inspect active roles (`configurations`), experience entries, project entries, and bullet IDs with character counts and verification statuses:
   ```bash
   python3 build_resume.py --summary
   ```

2. **Tailor or Add a Role Configuration**:
   Create a dedicated role target for a specific job posting or update an existing role:
   ```bash
   # Add a new role selecting target experiences and projects
   python3 build_resume.py --add-role --key backend_eng --title "Backend Engineer" --out backend_resume --experiences env_science_lab,caas_care_lab --projects smart_cache,distributed_kv

   # Or edit selected items for an existing role
   python3 build_resume.py --edit-role swe --projects smart_cache,env_science_lab
   ```

3. **Audit Bullet Character Density**:
   Run schema linting to check character count warnings (target ~220–245 characters per bullet for 2 full lines):
   ```bash
   python3 build_resume.py --lint
   ```

4. **Execute Precise Deterministic Edits**:
   Use CLI CRUD flags to add, edit, or delete entries and bullets without raw JSON formatting risks:
   ```bash
   # Add a new bullet to an experience or project entry
   python3 build_resume.py --add-bullet smart_cache --id cache_perf --text "Engineered an in-memory caching engine reducing latency by 93% across zonal grid datasets."

   # Edit an existing bullet text by ID
   python3 build_resume.py --edit-bullet env_geo_pipeline --text "Engineered a Python geospatial processing package using GeoPandas, Shapely, and Rasterio with UTM 60S projections to render interactive H3 maps."

   # Delete a bullet by ID
   python3 build_resume.py --delete-bullet cache_perf
   ```

5. **Build Target PDF & Verify Page Budget**:
   Compile PDF for the specific role profile:
   ```bash
   python3 build_resume.py --role backend_eng
   ```
   - Verify stdout output reports `PASSED (1 Page)` and vertical page fill between 82.0% and 95.0%.
   - If `OVERFLOW` occurs: trim 3–5 words from longer bullets using `--edit-bullet`.
   - If `UNDERFLOW` occurs: expand bullets or select an extra project in `--edit-role`.
