module_name = modelmind
.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: install
install:          ## Install the project in dev mode.
	poetry install
	pre-commit install --hook-type pre-commit --hook-type pre-push
# INSTALL NPM + firebase (functions)

.PHONY: format
format:           ## Format code using black & isort.
	poetry run ruff check $(module_name)/ --fix
	poetry run ruff format $(module_name)/
	tofu fmt -recursive infra/

.PHONY: lint
lint:             ## Run mypy linter.
	mypy --ignore-missing-imports $(module_name)/ --config-file mypy.ini


.PHONY: test
test: lint        ## Run tests and generate coverage report.
	poetry run pytest -v --cov-config .coveragerc --cov=$(module_name) -l --tb=short --maxfail=1 tests/
	coverage xml
	coverage html

.PHONY: watch
watch:            ## Run tests on every change.
	ls **/**.py | entr pytest --picked=first -s -vvv -l --tb=long --maxfail=1 tests/


.PHONY: export
poetry-export:          ## Export poetry requirements to requirements.txt.
	poetry export --without-hashes --without dev --without analytics -f requirements.txt -o requirements.txt


.PHONY: update
poetry-update:          ## Update poetry dependencies and export to requirements.txt.
	poetry update
	make poetry-export


.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
