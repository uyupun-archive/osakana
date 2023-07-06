#!/bin/bash

set -e

STAGED_FILES=$(git diff --cached --name-only)

if echo "$STAGED_FILES" | grep -q "\.py$"; then
    cd server
    poetry run flake8 .
    poetry run black --check .
    poetry run isort --check-only .
    npm run pyright .
    cd - > /dev/null
fi

if echo "$STAGED_FILES" | grep -q -E "\.(ts|js|jsx|tsx)$"; then
    cd dashboard
    npm run lint:eslint
    cd - > /dev/null
fi

if echo "$STAGED_FILES" | grep -q "dashboard/.*"; then
    cd dashboard
    npm run lint:prettier
    cd - > /dev/null
fi

exit 0
