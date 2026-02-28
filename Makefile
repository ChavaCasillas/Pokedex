.PHONY: help install test cli_tests lint format

help:
	@echo "Targets:"
	@echo "  install    Install package in editable mode"
	@echo "  test       Run full test suite"
	@echo "  cli_tests  Run CLI tests only"
	@echo "  error_tests Run error handling tests only"
	@echo "  pokeapi_tests Run PokeAPI tests only"
	@echo "  lint       Run ruff checks"
	@echo "  format     Format code with ruff"

install:
	pip install -e .

test:
	pytest -v

cli_tests:
	pytest -v tests/test_cli.py

error_tests:
	pytest -v tests/test_errors.py

pokeapi_tests:
	pytest -v tests/test_pokeapi.py

lint:
	ruff check .

format:
	ruff format .