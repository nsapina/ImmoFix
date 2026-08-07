$ErrorActionPreference = "Stop"

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host ".env wurde aus .env.example erstellt."
}

$required = @(
    "compose.yaml",
    "backend/Dockerfile",
    "backend/app/main.py",
    "backend/app/security.py",
    "backend/alembic/versions/0001_initial.py",
    "frontend/Dockerfile",
    "frontend/src/App.jsx",
    "frontend/src/pages/LoginPage.jsx"
)

foreach ($file in $required) {
    if (-not (Test-Path $file)) {
        throw "Projektdatei fehlt: $file"
    }
}

docker compose config | Out-Null
docker compose up -d --build

for ($i = 0; $i -lt 30; $i++) {
    docker compose exec -T api python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" 2>$null
    if ($LASTEXITCODE -eq 0) { break }
    Start-Sleep -Seconds 2
}

docker compose exec -T api python -m app.seed

Write-Host ""
Write-Host "ImmoFix läuft:"
Write-Host "Öffentlich: http://localhost:8080"
Write-Host "Login:      http://localhost:8080/login"
Write-Host "Admin:      http://localhost:8080/admin"
Write-Host "Swagger:    http://localhost:8000/docs"
