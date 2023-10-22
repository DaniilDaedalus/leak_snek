lint:
	mypy .
	ruff check .
	black --check .

format:
	ruff check --fix-only .
	black .

test:
	pytest --cov=leak_snek
