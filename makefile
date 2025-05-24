make ruff:
	uv run ruff check --fix src
	uv run ruff format src
