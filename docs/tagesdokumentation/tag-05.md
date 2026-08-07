# Tagesdokumentation – Tag 5

**Datum:** 07.08.2026

## Tagesziel

Den lokalen ImmoFix-MVP abschließen, den vollständigen Benutzerablauf testen und das Projekt für den ersten vollständigen Commit im gemeinsamen Repository vorbereiten.

## Erledigt

- finale Projektvorgaben mit dem bestehenden Projekt abgeglichen
- öffentliche Reparaturmeldung und geschützten Verwaltungsbereich überprüft
- Login, Logout und Schutz der Admin-Routen getestet
- Demo-Daten für Immobilien, Wohnungen, Handwerker und Tickets vorbereitet
- lokalen Start mit Docker Compose erfolgreich durchgeführt
- PostgreSQL-, MongoDB-, API- und Frontend-Container geprüft
- README und technische Dokumentation vollständig auf Deutsch bereinigt
- Tagesdokumentation für Tag 1 bis Tag 5 vervollständigt
- `.gitignore` auf lokale Secrets, Build-Dateien und Systemdateien geprüft
- Projekt für den ersten vollständigen GitHub-Commit vorbereitet

## Getesteter Ablauf

1. Anwendung lokal mit Docker Compose starten.
2. Öffentliche Reparaturmeldung ohne Benutzerkonto absenden.
3. Admin-Bereich ohne Anmeldung aufrufen und zur Loginseite weitergeleitet werden.
4. Mit dem Administratorkonto anmelden.
5. Neues Ticket im Dashboard und in der Ticketliste prüfen.
6. Priorität, Status und zuständigen Handwerker bearbeiten.
7. Aktivitätsverlauf und interne Notizen kontrollieren.
8. Abmelden und erneuten Zugriff auf den Admin-Bereich prüfen.

## Ergebnis

Der lokale Fullstack-MVP ist funktionsfähig und erfüllt die Pflichtanforderungen aus der Projektvorgabe: React, React Router, Fetch API, FastAPI, produktive Datenbankanbindung, Auth Basics, Docker Compose, Git-Projektstruktur und deutsche Dokumentation.

Das Projekt ist für den ersten vollständigen Commit und den Upload in das zentrale Repository vorbereitet.

## Sprint-1-Review

### Erreicht

- vollständiger lokaler Fullstack-Ablauf
- öffentliche und interne Benutzeroberfläche
- PostgreSQL und MongoDB mit klar getrennten Aufgaben
- Authentifizierung und geschützte Verwaltungsfunktionen
- Docker-basiertes lokales Setup
- deutsche README-, Architektur-, API- und Tagesdokumentation

### Gut gelaufen

- die Projektidee ließ sich sinnvoll an die offiziellen Anforderungen anpassen
- die Trennung zwischen öffentlicher Meldung und interner Verwaltung verbessert die Nutzerführung
- Docker Compose ermöglicht einen reproduzierbaren Start aller Services

### Herausforderungen

- mehrere lokale Projektversionen führten zeitweise zu Verwechslungen beim Docker-Build
- lokale PostgreSQL-Portkonflikte mussten analysiert werden
- die Authentifizierung musste nachträglich sauber in Frontend und Backend integriert werden

### Erkenntnisse für Sprint 2

- ab jetzt nur noch mit einer eindeutigen Projektversion und dem Git-Repository arbeiten
- Änderungen regelmäßig und nachvollziehbar committen
- vor neuen Funktionen zuerst den vollständigen Demo-Ablauf testen
- AWS-Deployment erst beginnen, nachdem die lokale Version stabil bleibt

## Nächste Schritte ab Montag

- Repository und Commit-Verlauf weiterpflegen
- AWS-Architektur final planen
- optionales Deployment mit EC2 und RDS umsetzen
- Security Groups und Umgebungsvariablen dokumentieren
- Präsentationsfolien und Live-Demo vorbereiten
- Sprint-2-Review und Lessons Learned erstellen
