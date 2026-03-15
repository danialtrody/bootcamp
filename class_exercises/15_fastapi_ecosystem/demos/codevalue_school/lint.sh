#!/bin/bash

echo "Running flake8 with \"wemake-python-styleguide (WPS)\" plugin"
./venv/bin/flake8 . --select=WPS

echo "Running mypy"
./venv/bin/mypy --exclude-gitignore . 