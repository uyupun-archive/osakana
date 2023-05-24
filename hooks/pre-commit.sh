#!/bin/bash

set -e

STAGED_FILES=$(git diff --cached --name-only)

if echo "$STAGED_FILES" | grep -q "^server/"; then
    cd server
    poetry run flake8 .
    poetry run black --check .
    poetry run isort --check-only .
fi


exit 0
