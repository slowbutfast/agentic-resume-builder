#!/usr/bin/env python3
"""
JSON Schema Linter & Character Density Diagnostics for Resume Bank.
Validates data/resume_bank.json against data/resume_bank.schema.json and checks bullet character length heuristics.
"""
import json
import os
import sys
import jsonschema

# Base directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "resume_bank.json")
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "resume_bank.schema.json")

# Character count heuristics for 2-line edge-to-edge bullets (11pt font, 1.0\textwidth)
TARGET_MIN_CHARS = 175
TARGET_MAX_CHARS = 230

def check_bullet_character_diagnostics(data, quiet=False):
    warnings = []
    
    sections = [
        ("Experience", data.get("experience_bank", {})),
        ("Project", data.get("project_bank", {}))
    ]

    for sec_name, bank in sections:
        for entry_key, entry_val in bank.items():
            for b in entry_val.get("bullets", []):
                b_id = b.get("id", "unknown")
                text = b.get("text", "")
                c_len = len(text)
                target_lines = b.get("target_line_count", 2)

                if target_lines == 2 and c_len > TARGET_MAX_CHARS:
                    warnings.append(
                        f"  ⚠️  [{sec_name}:{entry_key}:{b_id}] {c_len} chars (> {TARGET_MAX_CHARS} max target). Potential Line 3 overflow."
                    )
                elif target_lines == 2 and c_len < TARGET_MIN_CHARS:
                    warnings.append(
                        f"  ⚠️  [{sec_name}:{entry_key}:{b_id}] {c_len} chars (< {TARGET_MIN_CHARS} min target). Potential Line 2 right-margin underflow."
                    )

    if warnings and not quiet:
        print("\n--- Bullet Character Density Diagnostics (2-Line Target: 210-225 chars) ---")
        for w in warnings:
            print(w)
        print("----------------------------------------------------------------------------")

def lint_resume_bank(data_path=DATA_PATH, schema_path=SCHEMA_PATH, quiet=False):
    if not os.path.exists(data_path):
        print(f"❌ Schema Lint Error: Data file '{data_path}' not found.", file=sys.stderr)
        return False

    if not os.path.exists(schema_path):
        print(f"❌ Schema Lint Error: Schema file '{schema_path}' not found.", file=sys.stderr)
        return False

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Schema Lint Error: Invalid JSON syntax in '{data_path}': {e}", file=sys.stderr)
        return False

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Schema Lint Error: Invalid JSON syntax in '{schema_path}': {e}", file=sys.stderr)
        return False

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if errors:
        print(f"❌ Schema Validation Failed for '{data_path}' ({len(errors)} error(s) found):\n", file=sys.stderr)
        for idx, err in enumerate(errors, 1):
            path_str = " -> ".join([str(p) for p in err.absolute_path]) or "root"
            print(f"  {idx}. [{path_str}]: {err.message}", file=sys.stderr)
        return False

    if not quiet:
        rel_data = os.path.relpath(data_path, BASE_DIR)
        rel_schema = os.path.relpath(schema_path, BASE_DIR)
        print(f"✅ Schema Lint PASSED: '{rel_data}' conforms perfectly to '{rel_schema}'.")
        check_bullet_character_diagnostics(data, quiet=quiet)

    return True

if __name__ == "__main__":
    success = lint_resume_bank()
    if not success:
        sys.exit(1)
