# Tagesdokumentation – Tag 8

**Datum:** 12.08.2026

## Tagesziel

Die AWS-Konfiguration für ImmoFix vorbereiten und den geplanten EC2-Deployment-Ablauf dokumentieren.

## Erledigt

- `compose.aws.yaml` als AWS-spezifische Ergänzung zur Basis-Konfiguration geprüft
- Frontend-Port für AWS auf HTTP-Port 80 vorgesehen
- `restart: unless-stopped` für Serverbetrieb berücksichtigt
- separate Datei `.env.aws` für Produktionswerte vorgesehen
- benötigte Environment-Variablen dokumentiert
- Security-Group-Konzept festgelegt:
  - SSH nur von der eigenen IP
  - HTTP Port 80 öffentlich
  - PostgreSQL und MongoDB nicht öffentlich
- GitHub-Repository als Quelle für das EC2-Deployment vorbereitet
- RDS bewusst zurückgestellt, um zunächst einen stabilen EC2-Docker-Stand zu erreichen

## Deployment-Konzept

Für die Abgabe soll die Basisdatei `compose.yaml` gemeinsam mit `compose.aws.yaml` verwendet werden. Dadurch bleiben PostgreSQL und MongoDB als Docker-Services erhalten, während die AWS-spezifischen Einstellungen ergänzt werden.

Geplanter Startbefehl:

```bash
docker compose \
  --env-file .env.aws \
  -f compose.yaml \
  -f compose.aws.yaml \
  up -d --build
```

## Ergebnis

Die Deployment-Struktur war vorbereitet. Noch war nicht das Ziel, RDS oder weitere AWS-Dienste zu integrieren, sondern den bereits funktionierenden Docker-Stack reproduzierbar auf EC2 auszuführen.

## Nächste Schritte

- EC2-Instanz per SSH einrichten
- Docker installieren
- Repository klonen
- `.env.aws` anlegen
- Compose-Konfiguration validieren und starten
