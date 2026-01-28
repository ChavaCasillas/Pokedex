# Copilot Instructions for Pokedex

## Project Overview
Pokedex is an early-stage Python learning project that consumes the PokeAPI to build a searchable Pokedex application. The project uses modern Python tooling and follows best practices for structure and code quality.

## Architecture & Design

### Current State
- **Early development**: Project is in tooling/setup phase. The `src/` directory is empty; implementation hasn't begun.
- **Tech Stack**: Python 3.10+, PokeAPI (HTTP), Pytest for testing, Ruff for linting
- **No existing architecture patterns yet** - this is a blank slate for building the application

### Key Design Principles (from README)
- Learning-focused: Demonstrate proper project structure, virtual environments, and software architecture
- API consumption: Will integrate with PokeAPI; design should support clean API abstraction
- Testable by design: Code should be structured to enable unit testing with Pytest

## Development Workflow

### Environment Setup
```bash
# Python 3.10+ required per pyproject.toml
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate      # Windows
```

### Code Quality Tools
- **Ruff** (linter): Configured with 88-char line length, Python 3.10 target (see `pyproject.toml`)
- **Pytest**: Tests live in `tests/` directory; smoke test at `test_smoke.py` verifies pytest works

### Testing
- Run all tests: `pytest tests/` or use Makefile (currently empty—update this as you build)
- Test discovery: Pytest finds files matching `test_*.py` pattern in `tests/` directory
- Add tests for each API integration point and business logic module

## Conventions to Follow

### Python Structure
- Place implementation code in `src/` (currently empty)
- Keep API communication logic separate from business logic (recommend `src/api/` for PokeAPI calls, `src/models/` for data classes)
- Use type hints for better IDE support and documentation

### Code Patterns
- Follow PEP 8 via Ruff; 88-char line limit is non-negotiable
- Use descriptive module and function names reflecting PokeAPI domain (e.g., `fetch_pokemon()`, `PokemonData`)
- Handle API errors gracefully; design for network failures

### Dependencies
- Add dependencies to `pyproject.toml` under `dependencies` (not yet present—add as needed)
- Likely needed: `requests` (or `httpx`) for PokeAPI, `pydantic` for data validation

## Next Steps for AI Agents
1. Create `src/api/pokeapi_client.py` for PokeAPI communication
2. Add data models in `src/models/pokemon.py` 
3. Write integration tests before implementing complex features
4. Update Makefile with common commands: `make test`, `make lint`, `make run`
5. Implement core Pokedex search functionality

## Key Files
- [pyproject.toml](pyproject.toml): Project metadata, Ruff config, Pytest config
- [README.md](README.md): Project purpose and tech stack overview
- [tests/test_smoke.py](tests/test_smoke.py): Baseline test proving pytest works
