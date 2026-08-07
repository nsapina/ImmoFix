# ImmoFix

ImmoFix ist eine Fullstack-Webanwendung zur zentralen Verwaltung von Reparatur- und Wartungsanfragen für Mietwohnungen. Bewohner melden ein Problem über eine öffentliche Landingpage. Autorisierte Mitarbeiter bearbeiten die Anfrage anschließend in einem geschützten Verwaltungsbereich.

## Kernfunktionen

- öffentliche Reparaturmeldung ohne Registrierung
- Auswahl von Immobilie und Wohnung
- Kontaktangaben, Problembeschreibung und Notfall-Option
- automatische Ticketnummer nach dem Absenden
- Admin-Login mit Passwort-Hashing und JWT
- geschützte React-Routen und geschützte FastAPI-Endpunkte
- Dashboard mit offenen, dringenden und nicht zugewiesenen Tickets
- Ticketfilter, Statusänderung, Priorität und Handwerkerzuweisung
- Verwaltung von Immobilien, Wohnungen und Handwerkern
- Aktivitätsverlauf und interne Notizen
- PostgreSQL für Geschäftsdaten
- MongoDB für Ticket-Ereignisse
- Docker Compose für das lokale Setup

## Technologien

| Bereich | Technologie |
|---|---|
| Frontend | React, Vite, React Router, Fetch API |
| Backend | FastAPI, Pydantic, SQLAlchemy |
| Relationale Datenbank | PostgreSQL |
| Ereignisdaten | MongoDB |
| Migrationen | Alembic |
| Authentifizierung | Argon2-Passwort-Hashing, JWT Bearer Token |
| Infrastruktur | Docker, Docker Compose, nginx |
| Optionales Deployment | AWS EC2 und AWS RDS |

## Architektur

```text
Browser
   |
   v
nginx / React
   |
   +-- /api/public/* ----> FastAPI ----> PostgreSQL
   |                         |
   +-- /api/auth/* ----------+----> users
   |                         |
   +-- /api/* + JWT ---------+----> MongoDB ticket_events
```

Die öffentliche Meldeseite verwendet ausschließlich `/api/public/*`. Alle Verwaltungsendpunkte benötigen einen gültigen Bearer Token.

## Projektstruktur

```text
ImmoFix/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── security.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── seed.py
│   ├── alembic/
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── auth/
│   │   ├── components/
│   │   └── pages/
│   ├── nginx.conf
│   └── Dockerfile
├── docs/
├── scripts/
├── compose.yaml
├── .env.example
└── README.md
```

## Lokale Installation mit Docker

### Voraussetzungen

- Docker Desktop oder Docker Engine
- Docker Compose v2
- freie Ports `8080` und `8000`

### 1. Environment-Datei anlegen

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 2. Projekt prüfen

```bash
bash scripts/check-project.sh
```

### 3. Anwendung starten

```bash
docker compose up -d --build
```

Beim Start werden die Alembic-Migrationen ausgeführt und das Administratorkonto aus `.env` angelegt.

### 4. Demo-Daten anlegen

```bash
docker compose exec api python -m app.seed
```

### 5. Anwendung öffnen

- öffentliche Meldeseite: http://localhost:8080
- Login: http://localhost:8080/login
- Verwaltung: http://localhost:8080/admin
- Swagger: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

### Lokale Anmeldedaten

Die Standardwerte kommen aus `.env.example`:

```text
E-Mail:  admin@immofix.de
Passwort: ImmoFix2026!
```

Vor einem öffentlichen Deployment müssen Passwort und `JWT_SECRET` geändert werden.

## Wichtige Docker-Befehle

```bash
# Status
docker compose ps

# Logs
docker compose logs -f

# Tests
docker compose exec api pytest -q

# Stoppen, Daten behalten
docker compose down

# Vollständiger Reset inklusive Daten
docker compose down -v --remove-orphans
```

## API-Übersicht

### Öffentlich

| Methode | Route | Funktion |
|---|---|---|
| GET | `/api/public/properties` | Immobilien für die Meldeseite |
| GET | `/api/public/apartments?property_id=1` | aktive Wohnungen |
| POST | `/api/public/tickets` | Reparaturmeldung erstellen |
| POST | `/api/auth/login` | Admin anmelden |
| GET | `/api/health` | Datenbankstatus prüfen |

### Mit Bearer Token

| Methode | Route | Funktion |
|---|---|---|
| GET | `/api/auth/me` | angemeldeten Benutzer abrufen |
| GET | `/api/dashboard` | Dashboard-Kennzahlen |
| GET/PATCH/DELETE | `/api/tickets/...` | Tickets verwalten |
| GET/POST/PATCH/DELETE | `/api/properties/...` | Immobilien verwalten |
| GET/POST/PATCH/DELETE | `/api/apartments/...` | Wohnungen verwalten |
| GET/POST/PATCH/DELETE | `/api/contractors/...` | Handwerker verwalten |
| GET/POST | `/api/tickets/{id}/events` | Aktivitäten und Notizen |

Ausführliche Beispiele: [docs/api-uebersicht.md](docs/api-uebersicht.md)

## Authentifizierung

1. Das Backend legt beim ersten Start einen Admin-Benutzer in PostgreSQL an.
2. Das Passwort wird nicht im Klartext gespeichert, sondern mit Argon2 gehasht.
3. Nach erfolgreichem Login gibt FastAPI ein zeitlich begrenztes JWT zurück.
4. Das Frontend speichert den Token für den Kurs-MVP lokal und sendet ihn als `Authorization: Bearer ...`.
5. React schützt `/admin` mit einer `ProtectedRoute`.
6. FastAPI prüft den Token zusätzlich auf jedem Verwaltungsendpunkt.

## Dokumentation

- [Architektur](docs/architektur.md)
- [API-Übersicht](docs/api-uebersicht.md)
- [Installation und Testablauf](docs/installation.md)
- [Sprintplanung](docs/sprints.md)
- [Präsentationsleitfaden](docs/praesentation.md)
- [AWS-Deployment](docs/aws-deployment.md)

### Tagesdokumentation

- [Tag 1 – Projektidee und MVP](docs/tagesdokumentation/tag-01.md)
- [Tag 2 – Architektur und Sprintplanung](docs/tagesdokumentation/tag-02.md)
- [Tag 3 – Fullstack-Grundsystem](docs/tagesdokumentation/tag-03.md)
- [Tag 4 – Login und Projektdokumentation](docs/tagesdokumentation/tag-04.md)
- [Tag 5 – Lokaler MVP, Sprint-1-Review und Git-Vorbereitung](docs/tagesdokumentation/tag-05.md)
- [Vorlage für weitere Tage](docs/tagesdokumentation/vorlage.md)

## Team und Rollen

Vor der Abgabe ergänzen:

| Teammitglied | Rolle / Verantwortungsbereich |
|---|---|
| `[Name]` | `[z. B. Backend, Authentifizierung]` |
| `[Name]` | `[z. B. Frontend, UX]` |
| `[Name]` | `[z. B. Docker, Dokumentation, Tests]` |

## Git-Workflow

### Erster vollständiger Repository-Upload

```bash
git init
git branch -M main
git status
git check-ignore .env
git add .
git status --short
git commit -m "feat: complete local ImmoFix fullstack MVP"
gh repo create ImmoFix --private --source=. --remote=origin --push
```

Vor dem Commit muss geprüft werden, dass `.env`, Passwörter, Tokens und AWS-Zugangsdaten nicht in der Staging Area erscheinen.

### Weitere Änderungen

```bash
git status
git add .
git commit -m "docs: update daily project documentation"
git push
```

Commit-Nachrichten sollen konkrete Änderungen beschreiben.

## Projektstatus

**Stand: 07.08.2026**

Der lokale MVP enthält alle Pflichtbereiche: React, FastAPI, Fetch API, React Router, PostgreSQL, MongoDB, Auth Basics, Docker Compose, Migrationen und deutsche Projektdokumentation. Der vollständige lokale Ablauf wurde getestet und das Projekt ist für den ersten vollständigen Repository-Commit vorbereitet.

Ab dem 10.08.2026 liegt der Schwerpunkt auf dem optionalen AWS-Deployment, der Stabilisierung des Demo-Ablaufs und der Vorbereitung der Abschlusspräsentation.
