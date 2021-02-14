# Cirkopt Python

## Setup

```
pipenv install --dev
```

## Running linter

```
pipenv run pylint src/ tests/ --rcfile=.pylintrc
pipenv run mypy src/ tests/
```

## Running all tests

```
pipenv run python -m unittest discover
```