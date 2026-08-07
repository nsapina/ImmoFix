#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo ".env wurde aus .env.example erstellt."
fi

bash scripts/check-project.sh
docker compose up -d --build

for _ in $(seq 1 30); do
  if docker compose exec -T api python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

docker compose exec -T api python -m app.seed

echo
echo "ImmoFix läuft:"
echo "Öffentlich: http://localhost:8080"
echo "Login:      http://localhost:8080/login"
echo "Admin:      http://localhost:8080/admin"
echo "Swagger:    http://localhost:8000/docs"
