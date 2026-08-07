# Technische Validierung

Für die finale Version wurden folgende Prüfungen durchgeführt:

- Python-Syntaxprüfung aller Backend-, Alembic- und Testdateien
- Alembic-Migration `0001` gegen eine neue Testdatenbank
- vier automatisierte Backend-Tests erfolgreich
- Passwort-Hashing und Passwortprüfung mit Argon2
- JWT-Erzeugung
- öffentliche Immobilien- und Wohnungsabfrage
- öffentliche Ticketanlage
- Zugriff auf Dashboard ohne Token ergibt HTTP 401
- Login mit Admin-Benutzer
- `/api/auth/me` mit Bearer Token
- geschütztes Dashboard mit Bearer Token
- geschützte Ticketabfrage und Ticketänderung
- interne Notiz über geschützten Endpunkt
- YAML-Parsing aller Compose-Dateien
- JSON-Parsing von `package.json`
- JSX-/JavaScript-Parsing aller Frontend-Quelldateien
- Prüfung aller relativen Frontend-Imports
- Prüfung auf veraltete kroatische Hilfstexte im Repository

Der API-Smoke-Test wurde mit SQLite als isolierter Testdatenbank ausgeführt. Die produktive lokale Konfiguration verwendet PostgreSQL über Docker Compose.

Ein vollständiger Docker-Build konnte in der Erstellungsumgebung nicht ausgeführt werden, da dort kein Docker-Daemon verfügbar ist und das interne npm-Registry `@vitejs/plugin-react` nicht bereitstellt. Der finale End-to-End-Test auf dem eigenen Rechner lautet:

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec api python -m app.seed
docker compose ps
```
