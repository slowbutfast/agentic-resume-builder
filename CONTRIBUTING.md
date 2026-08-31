# Contributing to agentic-resume-builder

Thanks for taking a look. This is a young project and the surface area is small, so almost any contribution is useful — bug reports included.

## Getting set up

```bash
git clone https://github.com/slowbutfast/agentic-resume-builder.git
cd agentic-resume-builder
pip install -r requirements.txt
```

You'll also need `pdflatex` and `pdftoppm` on your `PATH` — see [Prerequisites](README.md#prerequisites) in the README.

Verify your checkout works before changing anything:

```bash
python3 build_resume.py --summary   # should print the role/entry tree
python3 build_resume.py --lint      # should pass schema validation
python3 tests/test_cli_crud.py      # CLI CRUD regression suite
```

## Where things live

- `src/build_resume.py` — CLI argument parsing and all CRUD operations on the data bank
- `src/generate_resumes.py` — TeX assembly, `pdflatex` compilation, PNG preview rendering
- `src/lint_schema.py` — JSON Schema validation plus bullet character-density diagnostics
- `data/resume_bank.schema.json` — the formal contract for the data bank; update this if you add fields
- `skills/` — agent skill definitions, one directory per skill
- `templates/main.tex` — the LaTeX baseline

## Guidelines

**Don't commit personal data.** `data/resume_bank.json` is git-ignored and never tracked — it's your private working copy, created from `data/resume_bank.example.json`. If you're changing the sample data itself, edit `resume_bank.example.json` (anonymized, `ALEX R. RIVERA`) and keep your real bank out of the diff.

**Keep the CLI deterministic.** The whole point of the CLI flags is that an agent can call them and get a predictable result. Avoid interactive prompts or anything that requires a human at the keyboard mid-command.

**Schema changes need a migration note.** If you change `resume_bank.schema.json`, say in the PR description what existing banks need to do to stay valid.

**Run the tests.** `python3 tests/test_cli_crud.py` exercises the CRUD paths. If you add a flag, add a case.

## Opening a PR

Branch off `main`, keep the change focused, and describe what you changed and why. If it's a behavior change, paste the before/after CLI output or a preview PNG — this project is visual and that makes review much faster.

For larger ideas, open an issue first so we can talk through the approach before you spend time on it. Issues tagged `good first issue` are scoped small on purpose.
