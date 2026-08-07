# Präsentationsleitfaden

Empfohlene Dauer: 10–15 Minuten.

## 1. Problem und Idee

Reparaturanfragen kommen über Telefon oder Nachrichten und sind schwer nachzuverfolgen. ImmoFix bündelt alle Meldungen in einem System.

## 2. Architektur

React und nginx kommunizieren per Fetch API mit FastAPI. PostgreSQL speichert strukturierte Geschäftsdaten, MongoDB den Aktivitätsverlauf.

## 3. Live-Demo

1. Öffentliche Reparaturmeldung absenden.
2. Ticketnummer zeigen.
3. Admin-Login durchführen.
4. Neues Ticket im Dashboard öffnen.
5. Handwerker zuweisen und Status ändern.
6. Interne Notiz und Timeline zeigen.

## 4. Authentifizierung

Passwort-Hashing, JWT, React ProtectedRoute und geschützte FastAPI-Endpunkte kurz erklären.

## 5. Herausforderungen

- Trennung zwischen öffentlicher und interner Oberfläche
- sinnvolle Aufteilung auf PostgreSQL und MongoDB
- Docker-Abhängigkeiten und Healthchecks
- konsistente Authentifizierung zwischen Frontend und Backend

## 6. Lessons Learned

- zuerst MVP festlegen
- öffentliche und interne Daten sauber trennen
- Backend-Schutz ist wichtiger als nur versteckte Frontend-Routen
- kleine, testbare Schritte reduzieren Integrationsfehler
