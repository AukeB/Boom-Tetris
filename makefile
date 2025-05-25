ruff:
	uv run ruff check --fix src
	uv run ruff format src

clean:
	find . -type d -name '__pycache__' -exec rm -r {} + 2>/dev/null
	find . -type d -name '.ruff_cache' -exec rm -r {} + 2>/dev/null

git:
	git add *
	git commit -m Updated
	git push

all:
	make ruff
	make clean
	make git
