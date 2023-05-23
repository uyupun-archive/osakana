#!/bin/bash

set -e

STAGED_FILES=$(git diff --cached --name-only)

if echo "$STAGED_FILES" | grep -q "^server/"; then
    cd server
    pipenv run flake8 .
    pipenv run black --check .
    pipenv run isort --check-only .
fi


exit 0
