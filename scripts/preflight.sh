#!/usr/bin/env bash
# Run before releasing: full backend tests + production frontend build.
set -e
cd "$(dirname "$0")/.."

echo "== Backend tests"
( cd backend && python -m pytest )

echo "== Frontend production build"
( cd frontend && npm ci && npm run build )

echo "== All checks passed"
