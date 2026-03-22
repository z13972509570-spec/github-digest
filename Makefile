.PHONY: install test trending weekly

install:
	pip install -e .

test:
	python -m github_digest trending

weekly:
	python -m github_digest weekly

trending:
	python -m github_digest trending
