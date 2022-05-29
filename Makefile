.PHONY: test coverage-badge coverage

test:
	pytest src

coverage-badge:
	coverage run --source=src -m pytest
	coverage xml
	genbadge coverage -i coverage.xml -o .github/coverage.svg

coverage:
	coverage run --source=src -m pytest
	coverage html
	open htmlcov/index.html