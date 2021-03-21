#!/usr/bin/env bash

python -m unittest discover && pylint src/ tests/ scripts/ --rcfile=.pylintrc && mypy src/ tests/ scripts/