lint:
	mypy .
	ruff check .

format:
	ruff check --fix-only .
	black .

test:
	pytest --cov=leak_snek
