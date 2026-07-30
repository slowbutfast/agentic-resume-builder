#!/usr/bin/env python3
"""
Resume Builder CLI & Data Bank Utility Helper.
Provides CLI flags for compiling resumes, validating JSON schema, inspecting bank summaries,
and performing CRUD operations on roles, entries, and bullet points.
"""
import argparse
import json
import os
import sys

# Ensure src/ is on sys.path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from lint_schema import lint_resume_bank
from generate_resumes import main as run_build, DATA_DIR

SCHEMA_PATH = os.path.join(DATA_DIR, "resume_bank.schema.json")
BANK_PATH = os.path.join(DATA_DIR, "resume_bank.json")

def load_bank_data():
    if not os.path.exists(BANK_PATH):
        print(f"❌ Error: Master data file '{BANK_PATH}' not found.", file=sys.stderr)
        sys.exit(1)
    try:
        with open(BANK_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading '{BANK_PATH}': {e}", file=sys.stderr)
        sys.exit(1)

def save_bank_data(data):
    # Save to disk first
    with open(BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Run lint validation
    if not lint_resume_bank(quiet=True):
        print("⚠️ Warning: Saved data bank has schema linting issues. Run 'python3 build_resume.py --lint' for details.")
    else:
        print("✅ Bank updated & schema verified successfully.")

def print_schema_cheatsheet():
    print("==================================================")
    print("RESUME BANK DATA SCHEMA CHEAT-SHEET")
    print("==================================================")
    print("Master Data File : data/resume_bank.json")
    print("Schema Definition: data/resume_bank.schema.json\n")
    print("📌 REQUIRED TOP-LEVEL KEYS:")
    print("  1. template_metadata : { template_source, document_class, font_size, paper_size, margins, max_page_budget, last_verified_timestamp }")
    print("  2. header            : { name, email, phone, linkedin, linkedin_url, github, github_url }")
    print("  3. education         : [ { institution, location, degree, dates, coursework }, ... ]")
    print("  4. experience_bank   : { <key>: { company, title, location, dates, bullets: [ bullet_item, ... ] } }")
    print("  5. project_bank      : { <key>: { name, tech_stack, dates, bullets: [ bullet_item, ... ] } }")
    print("  6. skills            : { languages, frameworks, tools, developer_ai, interests }")
    print("  7. configurations    : { <role_key>: { output_filename, title, experiences: [...], projects: [...] } }\n")
    print("📌 BULLET ITEM OBJECT STRUCTURE:")
    print("  {")
    print('    "id": "unique_bullet_id",')
    print('    "text": "Full high-density bullet description (approx 220-245 chars for 2 full lines)",')
    print('    "target_line_count": 2,')
    print('    "verification_status": "verified_full_width" | "pending_verification"')
    print("  }\n")
    print("==================================================")

def list_configurations():
    data = load_bank_data()
    print("==================================================")
    print("ACTIVE RESUME ROLES & PROJECT SELECTIONS")
    print("==================================================")
    for cfg_key, cfg in data.get("configurations", {}).items():
        print(f"\n🔹 Role Key       : {cfg_key}")
        print(f"   Title          : {cfg['title']}")
        print(f"   Output PDF     : build/pdf/{cfg['output_filename']}.pdf")
        print(f"   Experiences    : {', '.join(cfg.get('experiences', []))}")
        print(f"   Projects       : {', '.join(cfg.get('projects', []))}")
    print("\n==================================================")

def print_summary():
    data = load_bank_data()
    print("==================================================")
    print("RESUME BANK STRUCTURE & SLUG SUMMARY")
    print("==================================================")

    print("\n📌 ROLES (configurations):")
    for r_key, r_val in data.get("configurations", {}).items():
        exp_str = ", ".join(r_val.get("experiences", []))
        proj_str = ", ".join(r_val.get("projects", []))
        print(f"  • {r_key} (Title: \"{r_val.get('title')}\" | Out: {r_val.get('output_filename')}.pdf)")
        print(f"    - Experiences: [{exp_str}]")
        print(f"    - Projects: [{proj_str}]")

    print("\n🏢 EXPERIENCE BANK:")
    for e_key, e_val in data.get("experience_bank", {}).items():
        bullets = e_val.get("bullets", [])
        print(f"  📦 {e_key} - \"{e_val.get('title')}\" at {e_val.get('company')} ({len(bullets)} bullets)")
        for b in bullets:
            b_id = b.get("id", "unknown")
            b_len = len(b.get("text", ""))
            status = b.get("verification_status", "pending")
            lines = b.get("target_line_count", 2)
            print(f"    ├── bullet_id: {b_id} ({b_len} chars | target_lines: {lines} | status: {status})")

    print("\n💻 PROJECT BANK:")
    for p_key, p_val in data.get("project_bank", {}).items():
        bullets = p_val.get("bullets", [])
        print(f"  📦 {p_key} - \"{p_val.get('name')}\" [{p_val.get('tech_stack')}] ({len(bullets)} bullets)")
        for b in bullets:
            b_id = b.get("id", "unknown")
            b_len = len(b.get("text", ""))
            status = b.get("verification_status", "pending")
            lines = b.get("target_line_count", 2)
            print(f"    ├── bullet_id: {b_id} ({b_len} chars | target_lines: {lines} | status: {status})")
    print("\n==================================================")

# --- Role CRUD Operations ---

def add_role(key, title, out_filename, experiences_str, projects_str):
    data = load_bank_data()
    exps = [e.strip() for e in experiences_str.split(",") if e.strip()] if experiences_str else []
    projs = [p.strip() for p in projects_str.split(",") if p.strip()] if projects_str else []
    
    if key in data.get("configurations", {}):
        print(f"❌ Error: Role key '{key}' already exists in configurations.", file=sys.stderr)
        sys.exit(1)

    data.setdefault("configurations", {})[key] = {
        "output_filename": out_filename,
        "title": title,
        "experiences": exps,
        "projects": projs
    }
    print(f"➕ Added role configuration '{key}'.")
    save_bank_data(data)

def edit_role(key, title=None, out_filename=None, experiences_str=None, projects_str=None):
    data = load_bank_data()
    configs = data.get("configurations", {})
    if key not in configs:
        print(f"❌ Error: Role key '{key}' not found in configurations.", file=sys.stderr)
        sys.exit(1)

    role = configs[key]
    if title is not None:
        role["title"] = title
    if out_filename is not None:
        role["output_filename"] = out_filename
    if experiences_str is not None:
        role["experiences"] = [e.strip() for e in experiences_str.split(",") if e.strip()]
    if projects_str is not None:
        role["projects"] = [p.strip() for p in projects_str.split(",") if p.strip()]

    print(f"✏️ Updated role configuration '{key}'.")
    save_bank_data(data)

def delete_role(key):
    data = load_bank_data()
    configs = data.get("configurations", {})
    if key not in configs:
        print(f"❌ Error: Role key '{key}' not found in configurations.", file=sys.stderr)
        sys.exit(1)

    del configs[key]
    print(f"🗑️ Deleted role configuration '{key}'.")
    save_bank_data(data)

# --- Entry CRUD Operations ---

def add_project(key, name, tech_stack, dates):
    data = load_bank_data()
    p_bank = data.setdefault("project_bank", {})
    if key in p_bank:
        print(f"❌ Error: Project key '{key}' already exists in project_bank.", file=sys.stderr)
        sys.exit(1)

    p_bank[key] = {
        "name": name,
        "tech_stack": tech_stack,
        "dates": dates,
        "bullets": []
    }
    print(f"➕ Added project entry '{key}'.")
    save_bank_data(data)

def add_experience(key, company, title, location, dates):
    data = load_bank_data()
    e_bank = data.setdefault("experience_bank", {})
    if key in e_bank:
        print(f"❌ Error: Experience key '{key}' already exists in experience_bank.", file=sys.stderr)
        sys.exit(1)

    e_bank[key] = {
        "company": company,
        "title": title,
        "location": location,
        "dates": dates,
        "bullets": []
    }
    print(f"➕ Added experience entry '{key}'.")
    save_bank_data(data)

def delete_entry(key):
    data = load_bank_data()
    found = False

    if key in data.get("experience_bank", {}):
        del data["experience_bank"][key]
        print(f"🗑️ Deleted experience entry '{key}'.")
        found = True
    elif key in data.get("project_bank", {}):
        del data["project_bank"][key]
        print(f"🗑️ Deleted project entry '{key}'.")
        found = True

    if not found:
        print(f"❌ Error: Entry key '{key}' not found in experience_bank or project_bank.", file=sys.stderr)
        sys.exit(1)

    # Check if referenced in any active roles
    for r_key, r_val in data.get("configurations", {}).items():
        if key in r_val.get("experiences", []):
            r_val["experiences"].remove(key)
        if key in r_val.get("projects", []):
            r_val["projects"].remove(key)

    save_bank_data(data)

# --- Bullet CRUD Operations ---

def find_parent_entry(data, parent_key):
    if parent_key in data.get("experience_bank", {}):
        return data["experience_bank"][parent_key]
    if parent_key in data.get("project_bank", {}):
        return data["project_bank"][parent_key]
    return None

def add_bullet(parent_key, bullet_id, text, target_line_count=2):
    data = load_bank_data()
    parent = find_parent_entry(data, parent_key)
    if not parent:
        print(f"❌ Error: Parent entry key '{parent_key}' not found in experience_bank or project_bank.", file=sys.stderr)
        sys.exit(1)

    # Check for duplicate bullet ID across bank
    for bank_name in ["experience_bank", "project_bank"]:
        for entry in data.get(bank_name, {}).values():
            for b in entry.get("bullets", []):
                if b.get("id") == bullet_id:
                    print(f"❌ Error: Bullet ID '{bullet_id}' already exists in bank.", file=sys.stderr)
                    sys.exit(1)

    new_bullet = {
        "id": bullet_id,
        "text": text,
        "target_line_count": target_line_count,
        "verification_status": "pending_verification"
    }
    parent.setdefault("bullets", []).append(new_bullet)
    print(f"➕ Added bullet '{bullet_id}' to '{parent_key}'.")
    save_bank_data(data)

def edit_bullet(bullet_id, text, target_line_count=None, status=None):
    data = load_bank_data()
    found_bullet = None

    for bank_name in ["experience_bank", "project_bank"]:
        for entry in data.get(bank_name, {}).values():
            for b in entry.get("bullets", []):
                if b.get("id") == bullet_id:
                    found_bullet = b
                    break
            if found_bullet:
                break
        if found_bullet:
            break

    if not found_bullet:
        print(f"❌ Error: Bullet ID '{bullet_id}' not found in data/resume_bank.json.", file=sys.stderr)
        sys.exit(1)

    found_bullet["text"] = text
    if target_line_count is not None:
        found_bullet["target_line_count"] = target_line_count
    if status is not None:
        found_bullet["verification_status"] = status

    print(f"✏️ Updated bullet '{bullet_id}' ({len(text)} chars).")
    save_bank_data(data)

def delete_bullet(bullet_id):
    data = load_bank_data()
    deleted = False

    for bank_name in ["experience_bank", "project_bank"]:
        for entry in data.get(bank_name, {}).values():
            bullets = entry.get("bullets", [])
            initial_count = len(bullets)
            entry["bullets"] = [b for b in bullets if b.get("id") != bullet_id]
            if len(entry["bullets"]) < initial_count:
                deleted = True
                break
        if deleted:
            break

    if not deleted:
        print(f"❌ Error: Bullet ID '{bullet_id}' not found in data/resume_bank.json.", file=sys.stderr)
        sys.exit(1)

    print(f"🗑️ Deleted bullet '{bullet_id}'.")
    save_bank_data(data)

# --- CLI Main Engine ---

def main_cli():
    parser = argparse.ArgumentParser(
        description="Resume Builder CLI, Inspection & Bank CRUD Helper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples & Agent Workflows:
  # 1. View bank overview tree of active roles, entry keys, and bullet IDs
  python3 build_resume.py --summary (or -s)

  # 2. Build a specific tailored role or all roles
  python3 build_resume.py --role swe
  python3 build_resume.py

  # 3. Add or edit a job-tailored role profile
  python3 build_resume.py --add-role --key backend_eng --title "Backend Engineer" --out backend_resume --experiences env_science_lab --projects smart_cache
  python3 build_resume.py --edit-role backend_eng --projects smart_cache,distributed_kv
  python3 build_resume.py --delete-role backend_eng

  # 4. Entry CRUD (Projects & Experiences)
  python3 build_resume.py --add-project --key smart_cache --name "Smart Cache Engine" --tech "Go, Redis" --dates "Jan 2026 – May 2026"
  python3 build_resume.py --add-experience --key startup_intern --company "Acme Corp" --title "SWE Intern" --location "Remote" --dates "Jun 2026"
  python3 build_resume.py --delete-entry smart_cache

  # 5. Bullet CRUD
  python3 build_resume.py --add-bullet smart_cache --id cache_perf --text "Engineered an in-memory cache..."
  python3 build_resume.py --edit-bullet cache_perf --text "Engineered an in-memory cache reducing query latencies by 93%..."
  python3 build_resume.py --delete-bullet cache_perf

  # 6. Schema Linting & Help
  python3 build_resume.py --lint
  python3 build_resume.py --schema
"""
    )

    # Inspection & Compilation Flags
    parser.add_argument("-s", "--summary", action="store_true", help="Print summary hierarchy of roles, entries, and bullet IDs with character counts")
    parser.add_argument("--role", type=str, help="Build only the specified tailored resume role configuration (e.g. --role swe)")
    parser.add_argument("--lint", action="store_true", help="Run JSON Schema validation and bullet density checks")
    parser.add_argument("--schema", action="store_true", help="Print human-readable JSON Schema cheat-sheet")
    parser.add_argument("--list", action="store_true", help="List active resume roles and selected experiences/projects")

    # Role CRUD Flags
    parser.add_argument("--add-role", action="store_true", help="Add a new job-tailored role configuration")
    parser.add_argument("--edit-role", type=str, metavar="KEY", help="Edit an existing job-tailored role configuration by key")
    parser.add_argument("--delete-role", type=str, metavar="KEY", help="Delete a role configuration by key")

    # Entry CRUD Flags
    parser.add_argument("--add-project", action="store_true", help="Add a new project entry to project_bank")
    parser.add_argument("--add-experience", action="store_true", help="Add a new experience entry to experience_bank")
    parser.add_argument("--delete-entry", type=str, metavar="KEY", help="Delete an experience or project entry by key")

    # Bullet CRUD Flags
    parser.add_argument("--add-bullet", type=str, metavar="PARENT_KEY", help="Add a new bullet to a target experience or project key")
    parser.add_argument("--edit-bullet", type=str, metavar="BULLET_ID", help="Edit an existing bullet by ID")
    parser.add_argument("--delete-bullet", type=str, metavar="BULLET_ID", help="Delete a bullet by ID")

    # Shared Optional Parameters
    parser.add_argument("--key", type=str, help="Target key for adding a role, project, or experience")
    parser.add_argument("--title", type=str, help="Title string for role or experience")
    parser.add_argument("--name", type=str, help="Name string for project entry")
    parser.add_argument("--out", type=str, help="Output PDF filename (without .pdf extension) for role configuration")
    parser.add_argument("--experiences", type=str, help="Comma-separated experience keys for role configuration")
    parser.add_argument("--projects", type=str, help="Comma-separated project keys for role configuration")
    parser.add_argument("--tech", type=str, help="Tech stack string for project entry")
    parser.add_argument("--company", type=str, help="Company name string for experience entry")
    parser.add_argument("--location", type=str, help="Location string for experience entry")
    parser.add_argument("--dates", type=str, help="Date range string (e.g. 'Jan 2026 – May 2026')")
    parser.add_argument("--id", type=str, help="Bullet ID for --add-bullet")
    parser.add_argument("--text", type=str, help="Bullet point text description")
    parser.add_argument("--line-count", type=int, default=2, help="Target line count for bullet (default: 2)")
    parser.add_argument("--status", type=str, help="Verification status for bullet ('verified_full_width' or 'pending_verification')")

    args = parser.parse_args()

    # Route execution logic
    if args.summary:
        print_summary()
        sys.exit(0)
    elif args.lint:
        success = lint_resume_bank(quiet=False)
        sys.exit(0 if success else 1)
    elif args.schema:
        print_schema_cheatsheet()
        sys.exit(0)
    elif args.list:
        list_configurations()
        sys.exit(0)
    elif args.add_role:
        if not args.key or not args.title or not args.out:
            print("❌ Error: --add-role requires --key, --title, and --out flags.", file=sys.stderr)
            sys.exit(1)
        add_role(args.key, args.title, args.out, args.experiences, args.projects)
        sys.exit(0)
    elif args.edit_role:
        edit_role(args.edit_role, args.title, args.out, args.experiences, args.projects)
        sys.exit(0)
    elif args.delete_role:
        delete_role(args.delete_role)
        sys.exit(0)
    elif args.add_project:
        if not args.key or not args.name or not args.tech or not args.dates:
            print("❌ Error: --add-project requires --key, --name, --tech, and --dates flags.", file=sys.stderr)
            sys.exit(1)
        add_project(args.key, args.name, args.tech, args.dates)
        sys.exit(0)
    elif args.add_experience:
        if not args.key or not args.company or not args.title or not args.location or not args.dates:
            print("❌ Error: --add-experience requires --key, --company, --title, --location, and --dates flags.", file=sys.stderr)
            sys.exit(1)
        add_experience(args.key, args.company, args.title, args.location, args.dates)
        sys.exit(0)
    elif args.delete_entry:
        delete_entry(args.delete_entry)
        sys.exit(0)
    elif args.add_bullet:
        if not args.id or not args.text:
            print("❌ Error: --add-bullet <PARENT_KEY> requires --id and --text flags.", file=sys.stderr)
            sys.exit(1)
        add_bullet(args.add_bullet, args.id, args.text, args.line_count)
        sys.exit(0)
    elif args.edit_bullet:
        if not args.text:
            print("❌ Error: --edit-bullet <BULLET_ID> requires --text flag.", file=sys.stderr)
            sys.exit(1)
        edit_bullet(args.edit_bullet, args.text, args.line_count, args.status)
        sys.exit(0)
    elif args.delete_bullet:
        delete_bullet(args.delete_bullet)
        sys.exit(0)
    else:
        # Default: build target role or all roles
        run_build(role_key=args.role)

if __name__ == "__main__":
    main_cli()
