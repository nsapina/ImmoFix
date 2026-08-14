# Tagesdokumentation – Tag 7

**Datum:** 11.08.2026

## Tagesziel

Den lokalen Projektstand stabilisieren und die technischen Voraussetzungen für ein reproduzierbares AWS-Deployment vorbereiten.

## Erledigt

- lokalen Start mit Docker Compose überprüft
- Zusammenspiel von Frontend, nginx und FastAPI kontrolliert
- PostgreSQL- und MongoDB-Verbindungen über den Health Check geprüft
- Login, Logout und Schutz der Admin-Routen erneut getestet
- Environment-Konfiguration auf Trennung zwischen lokalen und späteren AWS-Werten geprüft
- `.env`, `.env.aws` und sensible Zugangsdaten als nicht zu commitierende Dateien festgelegt
- benötigte AWS-Komponenten auf EC2, Docker und Security Groups reduziert

## Getesteter Ablauf

1. Anwendung lokal starten.
2. öffentliche Reparaturmeldung öffnen.
3. Admin-Bereich ohne Login aufrufen.
4. mit Administratorkonto anmelden.
5. Ticketdaten im Verwaltungsbereich prüfen.
6. Health Check für die Datenbanken kontrollieren.

## Ergebnis

Der lokale MVP blieb stabil. Dadurch konnte das AWS-Deployment vorbereitet werden, ohne gleichzeitig neue Fachfunktionen einzubauen.

## Nächste Schritte

- AWS-spezifische Compose-Konfiguration prüfen
- `.env.aws.example` für den tatsächlichen Deployment-Stand vorbereiten
- EC2-Instanz einrichten
