#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

bash scripts/check-project.sh
docker compose up -d --build
docker compose ps

echo
echo "Optional Demo-Daten anlegen:"
echo "docker compose exec api python -m app.seed"
echo "Anwendung: http://localhost:8080"
