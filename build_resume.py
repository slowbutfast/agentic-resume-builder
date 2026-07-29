#!/usr/bin/env python3
"""
Root entry point wrapper for resume build pipeline & CLI helper.
Executes src/build_resume.py.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.insert(0, SRC_DIR)

from build_resume import main_cli

if __name__ == "__main__":
    main_cli()
