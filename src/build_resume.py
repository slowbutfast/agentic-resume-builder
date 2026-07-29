#!/usr/bin/env python3
"""
Resume Builder CLI & Data Bank Utility Helper.
Provides CLI flags for compiling resumes, validating JSON schema, inspecting schema cheat-sheets, and listing variants.
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
    print("  7. configurations    : { <variant_key>: { output_filename, title, experiences: [...], projects: [...] } }\n")
    print("📌 BULLET ITEM OBJECT STRUCTURE:")
    print("  {")
    print('    "id": "unique_bullet_id",')
    print('    "text": "Full high-density bullet description (approx 220-245 chars for 2 full lines)",')
    print('    "target_line_count": 2,')
    print('    "verification_status": "verified_full_width" | "pending_verification"')
    print("  }\n")
    print("💡 MODIFICATION TIPS:")
    print("  - To add a project: Add key to project_bank, then reference key in configurations[variant]['projects'].")
    print("  - To add an experience: Add key to experience_bank, then reference key in configurations[variant]['experiences'].")
    print("  - Run 'python3 build_resume.py --lint' to validate your edits instantly.")
    print("==================================================")

def list_configurations():
    if not os.path.exists(BANK_PATH):
        print(f"Error: Data file '{BANK_PATH}' not found.", file=sys.stderr)
        return

    with open(BANK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("==================================================")
    print("ACTIVE RESUME VARIANTS & PROJECT SELECTIONS")
    print("==================================================")
    for cfg_key, cfg in data.get("configurations", {}).items():
        print(f"\n🔹 Variant Key: {cfg_key}")
        print(f"   Title          : {cfg['title']}")
        print(f"   Output PDF     : build/pdf/{cfg['output_filename']}.pdf")
        print(f"   Experiences    : {', '.join(cfg.get('experiences', []))}")
        print(f"   Projects       : {', '.join(cfg.get('projects', []))}")
    print("\n==================================================")

def main_cli():
    parser = argparse.ArgumentParser(
        description="Resume Builder CLI & Data Bank Helper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 build_resume.py              # Build all resume PDF variants & PNG previews
  python3 build_resume.py --lint       # Validate data/resume_bank.json against schema
  python3 build_resume.py --schema     # Show JSON Schema cheat-sheet & bullet structure rules
  python3 build_resume.py --list       # List all active resume configurations & selected projects
"""
    )
    parser.add_argument("--lint", action="store_true", help="Run JSON Schema validation on data/resume_bank.json")
    parser.add_argument("--schema", action="store_true", help="Print human-readable JSON Schema cheat-sheet for modifying the data bank")
    parser.add_argument("--list", action="store_true", help="List active resume variants, selected experiences, and projects")

    args = parser.parse_args()

    if args.lint:
        success = lint_resume_bank(quiet=False)
        sys.exit(0 if success else 1)
    elif args.schema:
        print_schema_cheatsheet()
        sys.exit(0)
    elif args.list:
        list_configurations()
        sys.exit(0)
    else:
        run_build()

if __name__ == "__main__":
    main_cli()
