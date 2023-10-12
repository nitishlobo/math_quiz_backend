# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# MAKEFILE
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# General variables
PYTHON = python3
VENV_DIR = .venv

.PHONY: help clean clean-build clean-pyc clean-test test install-lint update-lint lint

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean                      to clean build, test, coverage, python artifacts and AWS outputs"
	@echo "  clean-build                to clean python build artifacts"
	@echo "  clean-pyc                  to clean python file artifacts"
	@echo "  clean-test                 to clean python test and coverage artifacts"
	@echo "  test                       to run unit tests"
	@echo "  install-lint               to install python linting tools"
	@echo "  update-lint                to update python linting tools"
	@echo "  lint                       to run autopep8, ruff, black and other linting tools on staged files"
	@echo "  lint-all                   to run autopep8, ruff, black and other linting tools on the entire repo"
	@echo "  run		                to run the FastAPI app locally"

# Remove all build, test, coverage and python artifacts.
clean: clean-build clean-pyc clean-lint clean-test

# Set up the git hook scripts
install-lint:
	pip install pre-commit
	pre-commit install

# Update version numbers of each pre-commit hook
update-lint:
	pre-commit autoupdate

# Run pre-commit hooks on all files in repo
# Note: you can run a specific pre-commit by doing:
# `pre-commit run black`
# Note: if you want to run ruff (isort module) manually:
# `ruff check --select I .`
# See docs/fond-dev-guide/content/lint for more.
lint:
	pre-commit run

lint-all:
	pre-commit run -a

run:
	uvicorn main:main_app --reload

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
