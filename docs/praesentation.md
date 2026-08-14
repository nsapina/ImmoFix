# Präsentationsleitfaden

> Hinweis: Diese Datei ist ein Leitfaden für eine mögliche Projektvorstellung. Eine fertige Präsentationsdatei ist nicht Bestandteil des Repository-Abgabestands vom 14.08.2026.

Empfohlene Dauer: 10–15 Minuten.

## 1. Problem und Idee

Reparaturanfragen kommen häufig über Telefon, E-Mail oder einzelne Nachrichten und sind dadurch schwer nachzuverfolgen. ImmoFix bündelt Reparaturmeldungen in einem zentralen System.

## 2. Architektur

React wird über nginx ausgeliefert und kommuniziert per Fetch API mit FastAPI. PostgreSQL speichert strukturierte Geschäftsdaten, MongoDB den Aktivitätsverlauf der Tickets.

Für die Abgabe wurde die Anwendung zusätzlich auf AWS EC2 mit Docker Compose bereitgestellt. Auf der EC2-Instanz laufen Frontend, FastAPI, PostgreSQL und MongoDB als Docker-Services. AWS RDS wurde nicht umgesetzt.

## 3. Möglicher Live-Demo-Ablauf

1. öffentliche Reparaturmeldung absenden
2. erzeugte Ticketnummer zeigen
3. Admin-Login durchführen
4. neues Ticket im Dashboard öffnen
5. Handwerker zuweisen und Status ändern
6. interne Notiz und Timeline zeigen
7. AWS-Deployment beziehungsweise Docker-Service-Status kurz erklären

## 4. Authentifizierung

Kurz erläutern:

- Argon2-Passwort-Hashing
- JWT Bearer Token
- React `ProtectedRoute`
- zusätzlich geschützte FastAPI-Endpunkte

## 5. AWS-Deployment

Mögliche Punkte:

- Ubuntu-EC2-Instanz
- GitHub-Repository auf EC2 geklont
- Docker Engine und Docker Compose installiert
- separate `.env.aws` für Secrets
- `compose.yaml` und `compose.aws.yaml` gemeinsam verwendet
- Frontend über Port 80 erreichbar
- PostgreSQL und MongoDB als Container auf EC2
- kein RDS im finalen Abgabestand

## 6. Herausforderungen

- Trennung zwischen öffentlicher und interner Oberfläche
- sinnvolle Aufteilung auf PostgreSQL und MongoDB
- konsistente Authentifizierung zwischen Frontend und Backend
- Environment-Konfiguration für lokale Umgebung und AWS
- Docker-Compose-Merge und YAML-Validierung

## 7. Lessons Learned

- zuerst einen klaren MVP festlegen
- Backend-Endpunkte zusätzlich zum Frontend schützen
- Secrets niemals in Git speichern
- Deployment-Dateien vor dem Start mit `docker compose config` validieren
- zunächst einen stabilen Deployment-Stand herstellen und optionale Dienste wie RDS erst danach ergänzen
