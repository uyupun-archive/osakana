#!/bin/bash

set -e

cd server
pipenv run flake8 .
pipenv run black --check .
pipenv run isort --check-only .

exit 0
