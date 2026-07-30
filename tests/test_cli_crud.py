#!/usr/bin/env python3
"""
Automated CLI CRUD & Inspection Test Suite for build_resume.py.
Validates flags: --summary, --role, Role CRUD, Entry CRUD, and Bullet CRUD.
"""
import os
import sys
import json
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_SCRIPT = os.path.join(BASE_DIR, "build_resume.py")
DATA_BANK = os.path.join(BASE_DIR, "data", "resume_bank.json")
BACKUP_BANK = os.path.join(BASE_DIR, "data", "resume_bank.json.bak")

def setup_backup():
    if os.path.exists(DATA_BANK):
        shutil.copyfile(DATA_BANK, BACKUP_BANK)

def restore_backup():
    if os.path.exists(BACKUP_BANK):
        shutil.copyfile(BACKUP_BANK, DATA_BANK)
        os.remove(BACKUP_BANK)

def run_cmd(args):
    cmd = [sys.executable, BUILD_SCRIPT] + args
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=BASE_DIR)
    return res.returncode, res.stdout, res.stderr

def test_help():
    print("Testing --help...")
    code, out, err = run_cmd(["--help"])
    assert code == 0, f"--help failed: {err}"
    assert "--summary" in out or "-s" in out, "--summary missing in --help"
    assert "--role" in out, "--role missing in --help"
    print("  ✅ --help passed")

def test_summary():
    print("Testing --summary...")
    code, out, err = run_cmd(["--summary"])
    assert code == 0, f"--summary failed: {err}"
    assert "experience_bank" in out.lower() or "experience" in out.lower(), "--summary output missing experiences"
    assert "project_bank" in out.lower() or "project" in out.lower(), "--summary output missing projects"
    print("  ✅ --summary passed")

def test_role_crud_and_single_build():
    print("Testing Role CRUD & --role build...")
    # 1. Add role
    code, out, err = run_cmd([
        "--add-role", "--key", "test_role",
        "--title", "Test Engineer Role",
        "--out", "test_resume",
        "--experiences", "env_science_lab",
        "--projects", "caas_care_lab"
    ])
    assert code == 0, f"--add-role failed: {err} {out}"

    # 2. Build single role
    code, out, err = run_cmd(["--role", "test_role"])
    assert code == 0, f"--role build failed: {err} {out}"

    # 3. Delete role
    code, out, err = run_cmd(["--delete-role", "test_role"])
    assert code == 0, f"--delete-role failed: {err} {out}"
    print("  ✅ Role CRUD & --role build passed")

def test_entry_and_bullet_crud():
    print("Testing Entry & Bullet CRUD...")
    # 1. Add project entry
    code, out, err = run_cmd([
        "--add-project", "--key", "test_p",
        "--name", "Test Project",
        "--tech", "Python, Docker",
        "--dates", "2026"
    ])
    assert code == 0, f"--add-project failed: {err} {out}"

    # 2. Add bullet
    code, out, err = run_cmd([
        "--add-bullet", "test_p",
        "--id", "test_b1",
        "--text", "Initial test bullet point text describing system capabilities."
    ])
    assert code == 0, f"--add-bullet failed: {err} {out}"

    # 3. Edit bullet
    code, out, err = run_cmd([
        "--edit-bullet", "test_b1",
        "--text", "Updated test bullet point text describing enhanced capabilities."
    ])
    assert code == 0, f"--edit-bullet failed: {err} {out}"

    # 4. Delete bullet
    code, out, err = run_cmd(["--delete-bullet", "test_b1"])
    assert code == 0, f"--delete-bullet failed: {err} {out}"

    # 5. Delete entry
    code, out, err = run_cmd(["--delete-entry", "test_p"])
    assert code == 0, f"--delete-entry failed: {err} {out}"
    print("  ✅ Entry & Bullet CRUD passed")

def main():
    setup_backup()
    try:
        test_help()
        test_summary()
        test_role_crud_and_single_build()
        test_entry_and_bullet_crud()
        print("\n🎉 ALL CLI CRUD TESTS PASSED!")
    finally:
        restore_backup()

if __name__ == "__main__":
    main()
