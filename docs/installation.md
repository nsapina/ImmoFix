# Installation und Testablauf

## Schnellstart

```bash
cp .env.example .env
bash scripts/check-project.sh
docker compose up -d --build
docker compose exec api python -m app.seed
```

## Erwarteter Containerstatus

```bash
docker compose ps
```

`postgres`, `mongo` und `api` sollen `healthy` sein. `frontend` soll `running` sein.

## Testablauf

1. `http://localhost:8080/login` öffnen.
2. Mit den Daten aus `.env` anmelden.
3. Unter **Wohnungen** eine Immobilie und eine Wohnung anlegen oder Demo-Daten verwenden.
4. Über das Logo zur öffentlichen Meldeseite wechseln.
5. Reparaturmeldung absenden.
6. Ticketnummer notieren.
7. Erneut anmelden und das Ticket öffnen.
8. Priorität, Status und Handwerker ändern.
9. Interne Notiz hinzufügen.
10. Activity Timeline prüfen.

## Fehlerdiagnose

```bash
docker compose logs api --tail=150
docker compose logs frontend --tail=100
docker compose logs postgres --tail=100
docker compose logs mongo --tail=100
```

Bei einer Änderung an Abhängigkeiten oder Dockerfiles:

```bash
docker compose up -d --build
```

Bei einer reinen Neustart-Anforderung:

```bash
docker compose up -d
```
