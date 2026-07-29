#!/usr/bin/env python3
"""
JSON Schema Linter for Resume Bank.
Validates data/resume_bank.json against data/resume_bank.schema.json.
"""
import json
import os
import sys
import jsonschema

# Base directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "resume_bank.json")
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "resume_bank.schema.json")

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
    return True

if __name__ == "__main__":
    success = lint_resume_bank()
    if not success:
        sys.exit(1)
