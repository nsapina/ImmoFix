# Sprintplanung

## Sprint 1 – Funktionsfähiger lokaler Fullstack-MVP

**Zeitraum:** 03.08.2026–07.08.2026  
**Sprintziel:** Reparaturmeldungen können öffentlich erstellt und intern in einem geschützten Verwaltungsbereich bearbeitet werden.

### Umgesetzte Inhalte

- Projektidee, MVP und Architektur festgelegt
- React-Routing und Seitenstruktur
- FastAPI-Backend und Pydantic-Validierung
- PostgreSQL-Modelle und Alembic-Migration
- MongoDB-Aktivitätsverlauf
- Dockerfiles und Docker Compose
- öffentliche Ticketmeldung
- Dashboard, Ticketverwaltung, Wohnungen und Handwerker
- Admin-Benutzer, Passwort-Hashing und JWT-Login
- Protected Routes und geschützte Backend-Endpunkte
- Tests, README und deutsche Projektdokumentation
- Vorbereitung des ersten vollständigen Repository-Commits

## Sprint-1-Review – 07.08.2026

Der lokale MVP ist funktionsfähig. Der vollständige Ablauf von der öffentlichen Reparaturmeldung bis zur internen Bearbeitung wurde getestet. Die Pflichttechnologien und Auth Basics sind integriert.

### Wichtigste Herausforderungen

- lokale Portkonflikte mit PostgreSQL
- Verwechslung verschiedener lokaler Projektstände
- nachträgliche Integration der Authentifizierung

### Konsequenzen für Sprint 2

- nur noch eine zentrale Repository-Version verwenden
- Änderungen regelmäßig committen und dokumentieren
- lokale Stabilität vor dem AWS-Deployment prüfen
- Live-Demo als festen End-to-End-Ablauf vorbereiten

## Sprint 2 – Deployment, Stabilisierung und Präsentation

**Zeitraum:** 10.08.2026–13.08.2026  
**Sprintziel:** Das Projekt wird stabilisiert, optional auf AWS bereitgestellt und für die Abschlusspräsentation vorbereitet.

### Geplante Aufgaben

- AWS-Architektur und Sicherheitskonzept finalisieren
- EC2-Instanz vorbereiten
- PostgreSQL optional über AWS RDS bereitstellen
- Docker-Compose-Deployment auf EC2 testen
- Umgebungsvariablen und Secrets sicher konfigurieren
- Security Groups und Netzwerkzugriff dokumentieren
- responsive Darstellung und Fehlermeldungen prüfen
- Demo-Daten und Live-Demo-Ablauf stabilisieren
- README und Tagesdokumentation fortführen
- Präsentation und Generalprobe vorbereiten
- Sprint-2-Review und Lessons Learned dokumentieren

## Definition of Done

Eine Funktion gilt als fertig, wenn:

- sie lokal über Docker Compose läuft,
- Frontend und Backend miteinander kommunizieren,
- Fehler verständlich angezeigt werden,
- keine Zugangsdaten im Repository liegen,
- die Änderung getestet, dokumentiert und committed wurde.
