# Bullet Density Trade-Offs & Portfolio Layout Guidelines

This document outlines the comparative trade-offs between bullet point density strategies when tailoring resumes for different software engineering job listings.

---

## 🎯 Core Layout Strategies

### Strategy 1: Depth-First (3 Bullets per Project | 3 Projects Total)
- **Structure**: 2 Experience Entries (5 bullets) + 3 Project Entries (9 bullets) = **14 Bullets Total**
- **Vertical Page Fill**: **~90.1%** (1 Page)
- **3-Act Engineering Narrative**:
  1. *Act 1 (High-Level Purpose)*: System purpose, business/user problem solved, plain-English overview.
  2. *Act 2 (Deep Backend/Data Engineering)*: Data models, ORM/query optimization, caching layers, state machines, or algorithmic complexity.
  3. *Act 3 (AI Agent & FastMCP Integration)*: Specialized tooling, vector RAG embeddings, or LLM agent tool calling endpoints.
- **Best For**: Specialized engineering roles (AI/ML Engineer, Systems Engineer, Infrastructure / Backend Specialist).

---

### Strategy 2: Breadth-First (2 Bullets per Project | 4 Projects Total)
- **Structure**: 2 Experience Entries (4 bullets) + 4 Project Entries (8 bullets) = **12 Bullets Total**
- **Vertical Page Fill**: **~86.5%** (1 Page)
- **Compact Narrative**: Combines backend optimization and agent integration into a single compressed line.
- **Header Margin Overhead**: 4 project headers (`\resumeSubheading`) consume ~140pt of vertical padding (~35pt per header title).
- **Best For**: Generalist Full-Stack roles or early-stage startup applications where recruiters prioritize broad tech stack exposure over single-project depth.

> [!WARNING]
> **4 Projects with 3 Bullets Overflow Warning**:
> Including 4 projects with 3 bullets each yields 12 project bullets + 4 project headers (792pt vertical height), causing a **2-page overflow** (`91.7% Page 2`). If you feature 4 projects on a single page, each project must strictly use **2 bullets**.

---

### Strategy 3: Hybrid Tiered Model (Recommended)
- **Concept**:
  - **Flagship Systems** (`open-dungeon`, `tennis-betting`, `env_science_lab`): Assign **3 bullets** to demonstrate complete end-to-end architectural mastery (SQLite/Vector RAG + FastMCP + SSE streaming).
  - **Focused Utility Projects** (`kalshi-mcp`, `attention-max`, `caas_care_lab`): Assign **2 bullets** (Plain English Purpose + Core Metric/Pipeline).
- **Best For**: Dynamic role-based tailoring per job description.

---

## 📊 Comparative Trade-Off Matrix

| Factor | 3 Bullets / Project (3 Projects) | 2 Bullets / Project (4 Projects) | Hybrid Tiered Model |
| :--- | :--- | :--- | :--- |
| **Portfolio Breadth** | Displays 3 projects + 2 research experiences. | Displays 4 projects + 2 research experiences. | Displays 3–4 projects with clear focus hierarchy. |
| **Technical Depth** | **High**: Complete 3-act architectural narrative. | **Moderate**: Combines pipeline mechanisms into 1 line. | **High on Flagships, Focused on Secondary**. |
| **Header Vertical Overhead** | **Lower**: 3 headers consume ~105pt vertical padding. | **Higher**: 4 headers consume ~140pt vertical padding. | **Flexible**: Fits cleanly within 1-page budget (88%–90% fill). |
| **Recruiter Skim Experience** | Deep architectural hooks for technical interviewers. | Quick visual scanning across 4 distinct tech stacks. | Clear visual anchor pointing recruiters to flagships first. |
| **Target Role** | AI/ML, Backend, Infrastructure, Systems. | Generalist Full-Stack, Early-Stage Startups. | Role-tailored application profiles. |

---

## 🛠️ CLI Quick Commands for Role Tailoring

```bash
# 1. View summary tree of all entries and bullet IDs
python3 build_resume.py --summary (or -s)

# 2. Add a new tailored role profile
python3 build_resume.py --add-role --key backend_eng --title "Backend Engineer" --out backend_resume --experiences env_science_lab,caas_care_lab --projects smart_cache,distributed_kv

# 3. Edit bullet text deterministically
python3 build_resume.py --edit-bullet env_geo_pipeline --text "Engineered a Python geospatial processing package..."

# 4. Compile targeted PDF role and verify 1-page budget
python3 build_resume.py --role backend_eng
python3 build_resume.py --lint
```
