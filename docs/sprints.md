# Sprintplanung und Reviews

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
- Änderungen nachvollziehbar über Git verwalten
- lokale Stabilität vor dem AWS-Deployment prüfen
- Deployment-Schritte dokumentieren

## Sprint 2 – Stabilisierung und AWS-Deployment

**Zeitraum:** 10.08.2026–13.08.2026  
**Sprintziel:** Den lokalen MVP stabilisieren, die Deployment-Konfiguration vorbereiten und die Anwendung auf AWS EC2 bereitstellen.

### Umgesetzte Inhalte

- bestehende Fullstack-Funktionen erneut geprüft
- Docker- und Environment-Konfiguration für AWS vorbereitet
- separate `.env.aws` für Server-Secrets verwendet
- AWS-EC2-Instanz eingerichtet
- Git, Docker Engine und Docker Compose Plugin auf EC2 eingerichtet
- Repository auf EC2 geklont
- AWS-Konfiguration mit `compose.yaml` und `compose.aws.yaml` validiert
- React/nginx auf Port 80 bereitgestellt
- FastAPI, PostgreSQL und MongoDB als Docker-Services gestartet
- Docker-Healthchecks geprüft
- End-to-End-Ablauf auf der EC2-Instanz getestet
- AWS-Deployment dokumentiert

### Nicht umgesetzt

- AWS RDS
- Domain und HTTPS
- fertige Präsentationsdatei

Die Präsentation war bis zum Repository-Abgabestand noch nicht ausgearbeitet. Im Repository befindet sich lediglich ein Präsentationsleitfaden.

## Sprint-2-Review – 13.08.2026

### Ergebnis

Das wichtigste Sprintziel wurde erreicht: ImmoFix läuft zusätzlich zur lokalen Umgebung auf einer AWS-EC2-Instanz.

Die finale AWS-Architektur der Abgabe besteht aus vier Docker-Services auf einer EC2-Instanz:

- frontend / nginx
- FastAPI
- PostgreSQL
- MongoDB

Das Frontend ist über HTTP-Port 80 erreichbar. PostgreSQL und MongoDB werden nicht direkt über die AWS Security Group veröffentlicht.

### Gut gelaufen

- der lokale Docker-Stack ließ sich auf die EC2-Umgebung übertragen
- Healthchecks halfen bei der Kontrolle der Service-Abhängigkeiten
- GitHub wurde als zentrale Projektquelle verwendet
- Frontend und API konnten ohne Änderung des React-Fetch-Konzepts über nginx betrieben werden

### Herausforderungen

- `.env.aws` musste getrennt von der lokalen `.env` behandelt werden
- die Funktionsweise des Compose-Merges zwischen `compose.yaml` und `compose.aws.yaml` musste nachvollzogen werden
- beim Bearbeiten der YAML-Datei entstand kurzzeitig ein doppelter `services:`-Block
- unterschiedliche lokale Projektstände hatten zuvor zu Verwechslungen geführt

### Lessons Learned

- Deployment-Konfigurationen sollten vor dem Start mit `docker compose ... config` validiert werden
- Secrets gehören nicht in Git
- ein funktionierender lokaler Docker-Stack vereinfacht ein EC2-Deployment deutlich
- zunächst einen einfachen, funktionierenden Cloud-Stand herstellen und zusätzliche Dienste wie RDS erst danach integrieren
- dokumentiert werden sollte nur, was tatsächlich umgesetzt und getestet wurde

## Definition of Done

Eine Funktion beziehungsweise ein Deployment-Schritt gilt als fertig, wenn:

- er reproduzierbar ausgeführt werden kann,
- Frontend und Backend miteinander kommunizieren,
- erforderliche Datenbanken erreichbar sind,
- Fehler über Logs oder Healthchecks nachvollziehbar sind,
- keine Zugangsdaten im Repository liegen,
- die Änderung getestet und dokumentiert wurde.
