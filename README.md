# Pokedex CLI

[![CI](https://github.com/ChavaCasillas/Pokedex/actions/workflows/ci.yml/badge.svg)](https://github.com/ChavaCasillas/Pokedex/actions/workflows/ci.yml)

A simple command-line Pokedex built in Python using the public PokeAPI.

---

## Purpose
This project is a learning exercise to practice:
- Python project structure (src/ layout)
- Virtual environments and editable installs
- Clean, layered architecture (CLI → Client → Models/Errors)
- API consumption with httpx
- Testing (pytest) and mocking
- Tooling: Ruff + Makefile + GitHub Actions

---

## What I learned (so far)
- How a CLI app is structured: `argparse` + subcommands + handlers
- Why `main(argv=None)` matters (testable CLI without touching `sys.argv`)
- Why stdout vs stderr matters (clean JSON output for piping)
- How to map internal exceptions to CLI exit codes
- How to isolate HTTP logic in a Client layer
- How to model API data using `dataclasses`
- How to write CLI tests with `pytest`:
  - `monkeypatch` to avoid real HTTP
  - `capsys` to capture stdout/stderr
  - validating JSON output with `json.loads`
- Why `pip install -e .` is useful (editable package linking)
- How `pyproject.toml` defines dependencies, scripts, and tool config
- How Makefile targets speed up common tasks (`make test`, `make cli_tests`)

---

## Features
- Fetch Pokémon by name or ID
- Human-readable output
- JSON output mode (`--json`)
- Structured error handling + exit codes
- Unit-tested CLI layer
- Linting with Ruff
- Makefile shortcuts

---

## Tech Stack
- Python 3.10+
- httpx
- pytest
- Ruff

---

## Installation (Development)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .