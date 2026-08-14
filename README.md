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
- PostgreSQL für strukturierte Geschäftsdaten
- MongoDB für Ticket-Ereignisse
- Docker Compose für lokale Entwicklung und AWS-Deployment
- Deployment auf einer AWS-EC2-Instanz

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
| Deployment | AWS EC2 mit Docker Compose |

## Architektur

### Lokal

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

### AWS-Abgabestand

```text
Internet
   |
   | HTTP 80
   v
AWS EC2
   |
   +-- nginx / React
   |
   +-- FastAPI
   |
   +-- PostgreSQL-Container
   |
   +-- MongoDB-Container
```

Für die Projektabgabe laufen Frontend, Backend, PostgreSQL und MongoDB gemeinsam als Docker-Services auf einer EC2-Instanz. AWS RDS wurde nicht umgesetzt.

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
├── compose.dev.yaml
├── compose.aws.yaml
├── .env.example
├── .env.aws.example
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

## AWS-Deployment auf EC2

Für die Abgabe wurde ImmoFix erfolgreich auf einer Ubuntu-EC2-Instanz bereitgestellt.

### Environment-Datei

```bash
cp .env.aws.example .env.aws
```

Alle Platzhalter in `.env.aws` müssen vor dem Start ersetzt werden. Die Datei `.env.aws` wird über `.gitignore` ausgeschlossen und darf keine echten Zugangsdaten im Repository enthalten.

### Deployment starten

Die AWS-Konfiguration wird mit der Basis-Compose-Datei kombiniert:

```bash
docker compose \
  --env-file .env.aws \
  -f compose.yaml \
  -f compose.aws.yaml \
  up -d --build
```

Status prüfen:

```bash
docker compose \
  --env-file .env.aws \
  -f compose.yaml \
  -f compose.aws.yaml \
  ps
```

Beim getesteten Deployment liefen die Services `postgres`, `mongo`, `api` und `frontend`; die Datenbank- und API-Healthchecks waren erfolgreich. Das Frontend wird über Port `80` der EC2-Instanz ausgeliefert.

Ausführliche Beschreibung: [docs/aws-deployment.md](docs/aws-deployment.md)

## Wichtige Docker-Befehle

```bash
# Status lokal
docker compose ps

# Logs lokal
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
- [Sprintplanung und Reviews](docs/sprints.md)
- [Präsentationsleitfaden](docs/praesentation.md)
- [AWS-EC2-Deployment](docs/aws-deployment.md)

### Tagesdokumentation

- [Tag 1 – Projektidee und MVP](docs/tagesdokumentation/tag-01.md)
- [Tag 2 – Architektur und Sprintplanung](docs/tagesdokumentation/tag-02.md)
- [Tag 3 – Fullstack-Grundsystem](docs/tagesdokumentation/tag-03.md)
- [Tag 4 – Login und Projektdokumentation](docs/tagesdokumentation/tag-04.md)
- [Tag 5 – Lokaler MVP, Sprint-1-Review und Git-Vorbereitung](docs/tagesdokumentation/tag-05.md)
- [Tag 6 – Sprint-2-Planung und Projektprüfung](docs/tagesdokumentation/tag-06.md)
- [Tag 7 – Stabilisierung und Deployment-Vorbereitung](docs/tagesdokumentation/tag-07.md)
- [Tag 8 – AWS-Konfiguration und Abgabevorbereitung](docs/tagesdokumentation/tag-08.md)
- [Tag 9 – AWS-EC2-Deployment und Sprint-2-Review](docs/tagesdokumentation/tag-09.md)

## Team und Rollen

Das Projekt wurde als Einzelprojekt umgesetzt. Daher wurden alle technischen und organisatorischen Aufgaben von einer Person übernommen.

| Teammitglied | Rolle / Verantwortungsbereich |
|---|---|
| Nikola Sapina | Fullstack-Entwicklung, Datenbanken, Authentifizierung, Docker, AWS-Deployment, Dokumentation und Tests |

## Git-Workflow

Vor jedem Commit wird geprüft, dass keine lokalen Secrets oder Schlüssel übertragen werden:

```bash
git status
git check-ignore .env
git check-ignore .env.aws
git status --short
```

Nicht in das Repository gehören insbesondere `.env`, `.env.aws`, private Schlüssel, Tokens oder AWS-Zugangsdaten.

Änderungen werden anschließend committed und gepusht:

```bash
git add .
git commit -m "docs: finalize project documentation and AWS EC2 deployment"
git push
```

## Projektstatus

**Stand: 14.08.2026**

Der lokale Fullstack-MVP ist vollständig umgesetzt und getestet. Die Anwendung umfasst React, React Router, Fetch API, FastAPI, PostgreSQL, MongoDB, Auth Basics, Alembic, Docker Compose und deutsche Projektdokumentation.

Zusätzlich wurde ImmoFix erfolgreich auf einer AWS-EC2-Instanz mit Docker Compose bereitgestellt. React/nginx, FastAPI, PostgreSQL und MongoDB laufen als Docker-Services auf der EC2-Instanz. Das Frontend ist über HTTP-Port `80` erreichbar.

AWS RDS wurde im Rahmen der Projektabgabe nicht umgesetzt. Eine fertige Präsentationsdatei ist nicht Bestandteil dieses Repository-Stands; `docs/praesentation.md` enthält lediglich einen Leitfaden für eine mögliche Vorstellung des Projekts.
