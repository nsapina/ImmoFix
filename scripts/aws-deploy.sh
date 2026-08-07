#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f .env.aws ]]; then
  echo ".env.aws fehlt. Zuerst .env.aws.example kopieren und ausfüllen."
  exit 1
fi

docker compose --env-file .env.aws -f compose.aws.yaml up -d --build
docker compose --env-file .env.aws -f compose.aws.yaml ps
