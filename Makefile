lint:
	ruff .
	mypy .

format:
	ruff --fix .
