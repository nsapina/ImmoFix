# Tagesdokumentation – Tag 9

**Datum:** 13.08.2026

## Tagesziel

ImmoFix auf AWS EC2 deployen, den vollständigen Docker-Stack prüfen und Sprint 2 abschließen.

## Erledigt

- AWS-EC2-Instanz mit Ubuntu gestartet
- SSH-Zugriff mit Key Pair eingerichtet
- Git auf der EC2-Instanz geprüft
- Docker Engine und Docker Compose Plugin installiert
- Docker mit `hello-world` getestet
- eigenes Benutzerkonto zur Docker-Gruppe hinzugefügt
- GitHub-Repository auf die EC2-Instanz geklont
- separate `.env.aws` angelegt und AWS-Werte konfiguriert
- `compose.yaml` und `compose.aws.yaml` gemeinsam verwendet
- Compose-Konfiguration validiert
- alle Docker-Images auf EC2 gebaut
- PostgreSQL-, MongoDB-, API- und Frontend-Service gestartet
- Healthchecks kontrolliert
- Frontend über HTTP-Port 80 veröffentlicht

## Erfolgreicher Container-Status

Beim abschließenden Test liefen:

- `immofix_aws-postgres-1` – healthy
- `immofix_aws-mongo-1` – healthy
- `immofix_aws-api-1` – healthy
- `immofix_aws-frontend-1` – running

Das Frontend war über Port `80` der öffentlichen EC2-Adresse erreichbar.

## Aufgetretene Probleme

### Fehlende `.env.aws`

Beim ersten Start meldete Docker Compose, dass `.env.aws` nicht vorhanden war. Die Datei wurde anschließend separat angelegt und mit den benötigten Produktionswerten befüllt.

### Unterschied zwischen lokaler und AWS-Environment-Datei

Die lokalen Werte aus `.env` sollten nicht unverändert für AWS verwendet werden. Für den Server wurde deshalb eine eigene `.env.aws` verwendet.

### YAML-Fehler durch doppelten `services:`-Block

Beim manuellen Bearbeiten von `compose.aws.yaml` wurde der Inhalt versehentlich dupliziert. Docker Compose meldete einen bereits definierten Mapping-Key. Die Datei wurde anschließend mit Git auf den gültigen Repository-Stand zurückgesetzt.

### Compose-Merge

Es wurde geklärt, dass `compose.yaml` und `compose.aws.yaml` gemeinsam geladen werden. Dadurch bleibt der PostgreSQL-Service aus der Basis-Konfiguration auch im AWS-Stack erhalten.

## Ergebnis

Das AWS-EC2-Deployment wurde erfolgreich abgeschlossen. ImmoFix läuft auf der EC2-Instanz mit React/nginx, FastAPI, PostgreSQL und MongoDB als Docker-Services.

AWS RDS wurde nicht umgesetzt. Für die Projektabgabe war ein stabiler und nachvollziehbarer EC2-Deployment-Stand wichtiger als eine zusätzliche Datenbankmigration kurz vor Abschluss.

## Sprint-2-Review

### Erreicht

- AWS EC2 eingerichtet
- Docker-basierter Fullstack-Deployment erfolgreich
- Frontend über Port 80 erreichbar
- PostgreSQL und MongoDB healthy
- FastAPI healthy
- Secrets außerhalb des Git-Repositorys gehalten
- AWS-Deployment dokumentiert

### Nicht umgesetzt

- AWS RDS
- Domain und HTTPS
- fertige Präsentationsdatei

### Wichtigste Erkenntnis

Die bereits lokal funktionierende Docker-Architektur konnte mit relativ wenigen Infrastrukturänderungen auf EC2 übertragen werden. Die größten Fehlerquellen lagen nicht in der Fachlogik, sondern in Environment-Dateien, Compose-Merge-Regeln und YAML-Konfiguration.
