# Changelog

## 2.0.0 – Finale Kursversion

- öffentliche Reparaturmeldung und internen Verwaltungsbereich getrennt
- öffentliche API unter `/api/public/*` eingeführt
- Admin-Benutzermodell in PostgreSQL ergänzt
- Argon2-Passwort-Hashing implementiert
- JWT-Login und Benutzerprüfung ergänzt
- React AuthContext, ProtectedRoute und Loginseite erstellt
- sämtliche Verwaltungsendpunkte im Backend geschützt
- Logout und automatische Behandlung abgelaufener Sitzungen ergänzt
- Kategorien aus dem vereinfachten Ticket-Flow entfernt
- deutsche README-, API-, Architektur-, Sprint- und Tagesdokumentation erstellt
- Authentifizierungs- und Schema-Tests ergänzt

## 2.0.1 – Sprint-1-Abschluss

- Tagesdokumentation für Tag 5 ergänzt
- Sprint-1-Review dokumentiert
- Sprint-2-Plan auf Stabilisierung und AWS ausgerichtet
- Repository für den ersten vollständigen Commit vorbereitet

## 2.1.0 – AWS-EC2-Deployment und Abgabestand

- Tagesdokumentation für Tag 6 bis Tag 9 ergänzt
- Sprint-2-Review dokumentiert
- AWS-EC2-Deployment erfolgreich durchgeführt
- Docker Engine und Docker Compose auf EC2 eingesetzt
- Frontend auf HTTP-Port 80 bereitgestellt
- PostgreSQL, MongoDB, FastAPI und Frontend als Docker-Services auf EC2 betrieben
- `.env.aws.example` an den tatsächlich verwendeten EC2-Stand angepasst
- AWS-Dokumentation auf EC2 ohne RDS korrigiert
- README auf den Abgabestand vom 14.08.2026 aktualisiert
- nicht umgesetzte Punkte wie RDS, HTTPS und fertige Präsentationsdatei transparent dokumentiert
