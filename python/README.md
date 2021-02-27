# Cirkopt Python

## Setup

```
pipenv install --dev
```

## Running linter

```
pipenv run pylint src/ tests/ scripts/ --rcfile=.pylintrc
pipenv run mypy src/ tests/ scripts/
```

## Running all tests

```
pipenv run python -m unittest discover
```