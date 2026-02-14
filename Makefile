lint:
	ruff check .

format:
	ruff format .

test:
	pytest -q

check: format lint test
