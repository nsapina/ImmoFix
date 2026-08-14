# AWS-EC2-Deployment

## Ziel

ImmoFix wurde für die Projektabgabe auf einer AWS-EC2-Instanz bereitgestellt. Der Deployment-Stand verwendet Docker Compose und führt alle vier Services auf derselben EC2-Instanz aus:

- nginx / React als öffentliches Frontend
- FastAPI als Backend
- PostgreSQL für strukturierte Geschäftsdaten
- MongoDB für Ticket-Ereignisse

AWS RDS wurde nicht umgesetzt.

## Zielarchitektur der Abgabe

```text
Internet
   |
   | HTTP 80
   v
AWS EC2 (Ubuntu)
   |
   +-- frontend
   |     nginx + React
   |
   +-- api
   |     FastAPI
   |
   +-- postgres
   |     PostgreSQL 16
   |
   +-- mongo
         MongoDB 7
```

Die Services kommunizieren intern über das von Docker Compose erzeugte Netzwerk.

## Voraussetzungen

Auf der EC2-Instanz wurden benötigt:

- Ubuntu
- Git
- Docker Engine
- Docker Compose Plugin
- Zugriff auf das GitHub-Repository

## Security Group

Für den Abgabestand gelten folgende Regeln:

| Port | Zweck | Zugriff |
|---|---|---|
| 22 | SSH | nur eigene IP-Adresse |
| 80 | HTTP / Frontend | öffentlich |
| 5432 | PostgreSQL | nicht öffentlich |
| 27017 | MongoDB | nicht öffentlich |
| 8000 | FastAPI | nicht als öffentliche Security-Group-Regel freigeben |

Hinweis: Durch die Basisdatei `compose.yaml` kann der API-Port im aktuellen Compose-Merge auf dem EC2-Host veröffentlicht werden. Entscheidend für den Abgabestand ist, dass Port `8000` nicht in der AWS Security Group für das Internet geöffnet wird. Für ein produktives Hardening sollte das Host-Publishing von Port `8000` vollständig entfernt werden.

## Repository auf EC2 laden

```bash
git clone https://github.com/nsapina/ImmoFix
cd ImmoFix
```

## AWS-Environment-Datei

Die Vorlage wird kopiert:

```bash
cp .env.aws.example .env.aws
```

Anschließend werden alle Platzhalter ersetzt.

Wichtige Variablen sind:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `MONGO_USER`
- `MONGO_PASSWORD`
- `MONGO_DB`
- `APP_ENV=production`
- `CORS_ORIGINS`
- `WEB_PORT=80`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `JWT_SECRET`

Ein zufälliger JWT-Secret kann beispielsweise so erzeugt werden:

```bash
openssl rand -hex 32
```

`.env.aws` ist in `.gitignore` eingetragen und darf nicht committed werden.

## Warum zwei Compose-Dateien verwendet werden

Die Datei `compose.yaml` enthält die gemeinsame Basis mit PostgreSQL, MongoDB, API und Frontend.

Die Datei `compose.aws.yaml` ergänzt beziehungsweise überschreibt AWS-spezifische Einstellungen, zum Beispiel:

- `restart: unless-stopped`
- Frontend-Port `80:80`
- AWS-spezifische Environment-Datei
- Produktions-Healthchecks

Der AWS-Stack wird deshalb nicht nur mit `compose.aws.yaml`, sondern mit beiden Dateien gestartet.

## Konfiguration vor dem Start prüfen

```bash
docker compose \
  --env-file .env.aws \
  -f compose.yaml \
  -f compose.aws.yaml \
  config
```

Diese Prüfung ist wichtig, weil Docker Compose beide Dateien zu einer endgültigen Konfiguration zusammenführt.

## Deployment starten

```bash
docker compose \
  --env-file .env.aws \
  -f compose.yaml \
  -f compose.aws.yaml \
  up -d --build
```

## Status prüfen

```bash
docker compose \
  --env-file .env.aws \
  -f compose.yaml \
  -f compose.aws.yaml \
  ps
```

Beim erfolgreichen Deployment liefen folgende Services:

- `immofix_aws-postgres-1` – healthy
- `immofix_aws-mongo-1` – healthy
- `immofix_aws-api-1` – healthy
- `immofix_aws-frontend-1` – running, Port `80`

## Health Check

Direkt auf der EC2-Instanz:

```bash
curl http://localhost:8000/api/health
```

Über nginx:

```bash
curl http://localhost/api/health
```

## Demo-Daten

Optional können Testdaten angelegt werden:

```bash
docker compose \
  --env-file .env.aws \
  -f compose.yaml \
  -f compose.aws.yaml \
  exec api python -m app.seed
```

## Anwendung öffnen

Die Anwendung wird über die öffentliche IPv4-Adresse der EC2-Instanz geöffnet:

```text
http://EC2_PUBLIC_IP
```

Login:

```text
http://EC2_PUBLIC_IP/login
```

Die konkrete IP-Adresse wird nicht dauerhaft in der Dokumentation gespeichert, da sie sich bei einer EC2-Instanz ohne Elastic IP nach einem Stop/Start ändern kann.

## Durchgeführter Test

Nach dem Deployment wurde geprüft:

1. öffentliche Landingpage wird über Port 80 geladen
2. Reparaturmeldung kann erstellt werden
3. `/admin` leitet ohne Sitzung zur Loginseite weiter
4. Admin-Login funktioniert
5. Tickets werden im Verwaltungsbereich angezeigt
6. PostgreSQL und MongoDB sind über den Health Check erreichbar
7. alle Docker-Services laufen stabil

## Aufgetretene Probleme und Lösungen

### `.env.aws` fehlte

`compose.aws.yaml` erwartet eine Datei `.env.aws`. Zunächst war nur `.env` vorhanden. Die AWS-Datei wurde anschließend separat angelegt.

### Unterschiedliche Environment-Strukturen

Für den finalen EC2-Stand werden die Variablen aus `.env.aws.example` verwendet. Die Verbindungsstrings für PostgreSQL und MongoDB werden von der Basis-Konfiguration aus diesen Werten zusammengesetzt.

### YAML-Datei versehentlich dupliziert

Beim manuellen Bearbeiten von `compose.aws.yaml` entstand zeitweise ein zweiter `services:`-Block. Die Datei wurde mit Git auf den Repository-Stand zurückgesetzt und anschließend erneut validiert.

### Compose-Merge verstehen

Für das funktionierende Deployment werden `compose.yaml` und `compose.aws.yaml` gemeinsam verwendet. Dadurch bleibt der PostgreSQL-Service aus der Basisdatei Bestandteil des AWS-Stacks.

## Nicht umgesetzt

Folgende Punkte waren für den Kurs-MVP nicht erforderlich beziehungsweise wurden bis zur Abgabe nicht umgesetzt:

- AWS RDS
- eigene Domain
- HTTPS/TLS
- Application Load Balancer
- automatische CI/CD-Pipeline
- Hochverfügbarkeit oder mehrere EC2-Instanzen

## Mögliche Weiterentwicklung

Für einen produktionsnäheren Betrieb wären folgende Schritte sinnvoll:

1. PostgreSQL auf ein privates AWS RDS migrieren.
2. Port `8000` auch auf Docker-Ebene nicht mehr an den Host veröffentlichen.
3. Domain und HTTPS einrichten.
4. Secrets über einen AWS-Dienst statt über eine lokale `.env.aws` verwalten.
5. Backups und Monitoring ergänzen.
