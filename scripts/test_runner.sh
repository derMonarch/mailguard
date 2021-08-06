#!/bin/sh

cd ..
tox
tox -e flake8
tox -e bandit
tox -e vulture
tox -e isort
tox -e black