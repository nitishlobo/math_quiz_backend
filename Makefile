# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# MAKEFILE
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# General variables
PYTHON = python3
VENV_DIR = .venv
PYTEST_CMD = python -m pytest -vv -rfEsP --maxfail=1 --tb=long --color=yes --code-highlight=yes
PYTEST_CMD_WITH_THREADING = $(PYTEST_CMD) -n 5

.PHONY: help clean clean-build clean-pyc clean-test test install-lint update-lint lint

help:
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "RUN"
	@echo "  run                        run the FastAPI app locally"
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "TEST"
	@echo "  test                       run unit tests"
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "LINT"
	@echo "  install-lint               install python linting tools"
	@echo "  update-lint                update python linting tools"
	@echo "  lint                       run autopep8, ruff, black and other linting tools on staged files"
	@echo "  lint-all                   run autopep8, ruff, black and other linting tools on the entire repo"
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "CLEAN"
	@echo "  clean                      clean build, test, coverage, python artifacts and AWS outputs"
	@echo "  clean-build                clean python build artifacts"
	@echo "  clean-pyc                  clean python file artifacts"
	@echo "  clean-lint                 clean python file artifacts"
	@echo "  clean-test                 clean python test and coverage artifacts"
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "DATABASE"
	@echo "  db-current-rev             display the current alembic revision of the database"
	@echo "  db-upgrade-all             upgrade the database with all the available alembic revisions"
	@echo "  db-downgrade-all           downgrade the database with all the available alembic revisions"
	@echo "  db-migrate msg='example'   take all python sqlalchemy models and autogenerates migration files"
	@echo "      msg                        description of what is being migrated (will be in file name and docstring)"
	@echo "  db-upgrade rev='ae1'       upgrade the database to a specific revision number"
	@echo "      rev                        partial/complete revision id of the alembic file or relative integer"
	@echo "  db-downgrade rev='ae1'     upgrade the database to a specific revision number"
	@echo "      rev                        partial/complete revision id of the alembic file or relative integer"

run:
	uvicorn main:main_app --reload

test:
	pytest

# Remove all build, test, coverage and python artifacts.
clean: clean-build clean-pyc clean-lint clean-test

# Set up the git hook scripts
install-lint:
	pip install pre-commit
	pre-commit install

# Update version numbers of each pre-commit hook
update-lint:
	pre-commit autoupdate

# Run pre-commit hooks on staged files
# Note: you can run a specific pre-commit by doing:
# `pre-commit run black`
# Note: if you want to run ruff (isort module) manually:
# `ruff check --select I .`
# See docs/fond-dev-guide/content/lint for more.
lint:
	pre-commit run

# Run pre-commit hooks on entire repo
lint-all:
	pre-commit run -a

# -------------------------------------------------------------------------------------------------
# Database commands
# -------------------------------------------------------------------------------------------------
db-current-rev:
	cd v1 && alembic current

db-history:
	cd v1 && alembic history

# Usage example:
# make db-migrate msg="create user table"
db-migrate:
	cd v1 && alembic revision --autogenerate -m "$(msg)"

db-upgrade-all:
	cd v1 && alembic upgrade head

# Usage example:
# make db-upgrade rev="ae1" (upgrade to specific version)
# make db-upgrade rev="+3" (upgrade relative to current version)
db-upgrade:
	cd v1 && alembic upgrade "$(rev)"

db-downgrade-all:
	cd v1 && alembic downgrade base

# Usage example:
# make db-downgrade rev="ae1" (downgrade to specific version)
# make db-downgrade rev="-3" (downgrade relative to current version)
db-downgrade:
	cd v1 && alembic downgrade "$(rev)"

# -------------------------------------------------------------------------------------------------
# OS specific commands - please uncomment the relevant section depending on your OS
# -------------------------------------------------------------------------------------------------
# Windows

# Remove build artifacts
clean-build:
	for /d /r %%p in (.eggs, *.egg-info, *.egg) do  @if exist "%%p" rmdir /s /q "%%p"

# Remove lint artifacts
clean-lint:
	for /d /r %%p in (.ruff_cache, .mypy_cache) do  @if exist "%%p" rmdir /s /q "%%p"

# Remove Python file artifacts
clean-pyc:
	for /d /r %%p in (__pycache__) do  @if exist "%%p" rmdir /s /q "%%p"
	for /d /r %%p in (*.pyc, *.pyo, *~) do  @if exist "%%p" del /s /f /q "%%p"

# Remove test and coverage artifacts
clean-test:
	for /d /r %%p in (.pytest_cache) do  @if exist "%%p" rmdir /s /q "%%p"

# -------------------------------------------------------------------------------------------------
# MacOS / Linux

# # Remove build artifacts
# clean-build:
# 	find . -name '.eggs' -exec rm -fr {} +
# 	find . -name '*.egg-info' -exec rm -fr {} +
# 	find . -name '*.egg' -exec rm -f {} +

# # Remove Python file artifacts
# clean-pyc:
# 	find . -name '*.pyc' -exec rm -f {} +
# 	find . -name '*.pyo' -exec rm -f {} +
# 	find . -name '*~' -exec rm -f {} +
# 	find . -name '__pycache__' -exec rm -fr {} +

# # Remove lint artifacts
# clean-lint:
# 	find . -name '.ruff_cache' -exec rm -fr {} +
# 	find . -name '.mypy_cache' -exec rm -fr {} +

# # Remove test and coverage artifacts
# clean-test:
# 	find . -name '.pytest_cache' -exec rm -fr {} +
