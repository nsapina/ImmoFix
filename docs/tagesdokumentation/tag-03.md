# Tagesdokumentation – Tag 3

**Datum:** 05.08.2026

## Tagesziel

Ein lokal ausführbares Fullstack-Grundsystem erstellen.

## Erledigt

- Backend- und Frontend-Struktur erstellt
- Dockerfiles und Docker Compose eingerichtet
- PostgreSQL-Modelle und Alembic-Migration implementiert
- MongoDB-Aktivitätsverlauf angebunden
- öffentliche Reparaturmeldung entwickelt
- Admin-Dashboard, Ticketliste und Detailansicht erstellt
- Immobilien-, Wohnungs- und Handwerkerverwaltung ergänzt
- nginx als Reverse Proxy konfiguriert

## Ergebnis

Der zentrale Ablauf von der öffentlichen Meldung bis zur internen Ticketbearbeitung funktioniert lokal.

## Blocker / Lösung

Lokale Portkonflikte mit PostgreSQL wurden vermieden, indem die Datenbank nicht auf Port 5432 des Hostsystems veröffentlicht wird.
