#!/usr/bin/env bash
set -euo pipefail

required=(
  "compose.yaml"
  ".env.example"
  "backend/Dockerfile"
  "backend/requirements.txt"
  "backend/app/main.py"
  "backend/app/security.py"
  "backend/app/routers/auth.py"
  "backend/app/routers/public.py"
  "backend/alembic/versions/0001_initial.py"
  "frontend/Dockerfile"
  "frontend/package.json"
  "frontend/nginx.conf"
  "frontend/src/App.jsx"
  "frontend/src/auth/AuthContext.jsx"
  "frontend/src/pages/LoginPage.jsx"
  "frontend/src/pages/LandingPage.jsx"
)

missing=0
for file in "${required[@]}"; do
  if [[ ! -s "$file" ]]; then
    echo "FEHLT ODER IST LEER: $file"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "Das Projekt wurde nicht vollständig entpackt. Docker nicht starten."
  exit 1
fi

docker compose config >/dev/null
printf 'Projektstruktur und compose.yaml sind gültig.
'
