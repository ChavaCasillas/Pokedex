lint:
	ruff check .

format:
	ruff format .

test:
	pytest -v

check: format lint test
