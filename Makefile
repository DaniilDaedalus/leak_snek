lint:
	mypy .
	ruff check .
	black --check .

format:
	ruff check --fix-only .
	black .

test:
	poetry run pytest --cov=leak_snek --cov-report=term-missing

lint-ci:
	poetry run mypy .
	poetry run ruff check .
	poetry run black --check .

coverage.json:
	poetry run pytest --cov=leak_snek --cov-report=json

test-ci: coverage.json

badges-ci: coverage.json
	mkdir -p badges && \
  poetry run python -m pybadges --left-text=coverage --right-text=$$(jq -j .totals.percent_covered_display coverage.json)% --right-color='#4dc71f' > badges/coverage.svg
