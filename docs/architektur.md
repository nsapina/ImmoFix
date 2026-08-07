# Architektur

## Systemüberblick

ImmoFix besteht aus vier zentralen Komponenten:

1. **React-Frontend** für öffentliche Meldungen und interne Verwaltung.
2. **FastAPI-Backend** für REST-Endpunkte, Validierung und Geschäftslogik.
3. **PostgreSQL** für Benutzer, Immobilien, Wohnungen, Handwerker und Tickets.
4. **MongoDB** für flexible Ticket-Ereignisse und interne Notizen.

## Datenfluss

### Öffentliche Reparaturmeldung

```text
Bewohner -> React Landingpage -> POST /api/public/tickets
         -> FastAPI -> PostgreSQL Ticket
                    -> MongoDB Ereignis ticket_created
```

### Verwaltung

```text
Administrator -> Login -> JWT
Administrator -> /admin -> Authorization Bearer JWT
              -> FastAPI -> PostgreSQL / MongoDB
```

## Begründung der Datenbanken

PostgreSQL speichert strukturierte Daten mit klaren Beziehungen. Ein Ticket gehört zu einer Wohnung, eine Wohnung zu einer Immobilie und ein Ticket kann einem Handwerker zugeordnet werden.

MongoDB speichert Ereignisse mit flexibel unterschiedlichen Inhalten, beispielsweise Statusänderungen, Notizen oder Handwerkerzuweisungen. Die Kombination zeigt Polyglot Persistence, ohne die Daten künstlich auf zwei Systeme zu verteilen.

## Sicherheitsgrenze

Die öffentliche API bietet nur die Daten, die für eine Reparaturmeldung notwendig sind. Kontaktdaten anderer Wohnungen, Ticketlisten, Handwerker und interne Notizen sind ausschließlich über geschützte Endpunkte erreichbar.
