# API-Übersicht

Basis-URL lokal: `http://localhost:8000/api`

## Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@immofix.de","password":"ImmoFix2026!"}'
```

Die Antwort enthält `access_token`. Für geschützte Endpunkte:

```bash
TOKEN="HIER_TOKEN_EINFÜGEN"
curl http://localhost:8000/api/dashboard \
  -H "Authorization: Bearer $TOKEN"
```

## Öffentliche Endpunkte

```bash
curl http://localhost:8000/api/public/properties
curl "http://localhost:8000/api/public/apartments?property_id=1"
```

Ticket erstellen:

```bash
curl -X POST http://localhost:8000/api/public/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "apartment_id": 1,
    "description": "Unter der Küchenspüle tritt Wasser aus.",
    "reported_by": "Anna Becker",
    "reporter_phone": "+49 170 1111111",
    "reporter_email": null,
    "is_emergency": true
  }'
```

## Geschützte Endpunkte

```bash
curl http://localhost:8000/api/tickets -H "Authorization: Bearer $TOKEN"
curl http://localhost:8000/api/properties -H "Authorization: Bearer $TOKEN"
curl http://localhost:8000/api/apartments -H "Authorization: Bearer $TOKEN"
curl http://localhost:8000/api/contractors -H "Authorization: Bearer $TOKEN"
```

Ticket aktualisieren:

```bash
curl -X PATCH http://localhost:8000/api/tickets/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress","priority":"high","contractor_id":1}'
```

Interne Notiz:

```bash
curl -X POST http://localhost:8000/api/tickets/1/events \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Handwerker wurde telefonisch informiert."}'
```
