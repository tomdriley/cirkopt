# Cirkopt Python

## Setup

```
pipenv install --dev
```

## Running linter

```
pipenv run pylint src/ tests/ --rcfile=.pylintrc
```

## Running all tests

```
pipenv run python -m unittest discover
```