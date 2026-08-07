import argparse

from sqlalchemy import func, select

from app import models
from app.config import settings
from app.database import SessionLocal
from app.mongo import log_event
from app.security import hash_password


def ensure_admin(db) -> models.User:
    admin = db.scalar(select(models.User).where(func.lower(models.User.email) == settings.admin_email.lower()))
    if admin is not None:
        print(f"Admin-Konto bereits vorhanden: {admin.email}")
        return admin

    admin = models.User(
        email=settings.admin_email.lower(),
        full_name=settings.admin_name,
        password_hash=hash_password(settings.admin_password),
        is_active=True,
        is_admin=True,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"Admin-Konto angelegt: {admin.email}")
    return admin


def ensure_demo_data(db) -> None:
    if db.scalar(select(models.Property.id).limit(1)):
        print("Demo-Daten übersprungen: Immobilien sind bereits vorhanden.")
        return

    property_1 = models.Property(name="Sonnenhof", address="Sonnenstraße 12", city="Berlin", postal_code="10115")
    property_2 = models.Property(name="Parkresidenz", address="Parkweg 8", city="Berlin", postal_code="10243")
    db.add_all([property_1, property_2])
    db.flush()

    apartments = [
        models.Apartment(property_id=property_1.id, apartment_number="4B", floor="4", contact_name="Anna Becker", contact_phone="+49 170 1111111", contact_email="anna@example.com"),
        models.Apartment(property_id=property_1.id, apartment_number="2A", floor="2", contact_name="Markus Klein", contact_phone="+49 170 2222222"),
        models.Apartment(property_id=property_2.id, apartment_number="EG-1", floor="EG", contact_name="Leyla Demir", contact_phone="+49 170 3333333"),
    ]
    contractors = [
        models.Contractor(name="Ivan Horvat", company="Horvat Sanitär", phone="+49 30 555100", email="ivan@example.com", specialization="Sanitär"),
        models.Contractor(name="Mia Schneider", company="Elektro Schneider", phone="+49 30 555200", email="mia@example.com", specialization="Elektrik"),
    ]
    db.add_all(apartments + contractors)
    db.flush()

    tickets = [
        models.Ticket(
            apartment_id=apartments[0].id,
            contractor_id=contractors[0].id,
            title="Wasser unter der Spüle",
            description="Unter der Küchenspüle tritt Wasser aus. Das Ventil wurde vorläufig geschlossen.",
            priority="urgent",
            status="assigned",
            reported_by="Anna Becker",
            reporter_phone="+49 170 1111111",
        ),
        models.Ticket(
            apartment_id=apartments[1].id,
            title="Steckdose ohne Strom",
            description="Die Steckdose im Schlafzimmer funktioniert nicht mehr.",
            priority="normal",
            status="new",
            reported_by="Markus Klein",
            reporter_phone="+49 170 2222222",
        ),
    ]
    db.add_all(tickets)
    db.commit()

    for ticket in tickets:
        log_event(ticket.id, "ticket_created", ticket.reported_by, {"title": ticket.title})
    log_event(tickets[0].id, "contractor_assigned", settings.admin_name, {"contractor": contractors[0].name})
    print("Demo-Daten wurden erfolgreich angelegt.")


def run_seed(admin_only: bool = False) -> None:
    db = SessionLocal()
    try:
        ensure_admin(db)
        if not admin_only:
            ensure_demo_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ImmoFix-Startdaten anlegen")
    parser.add_argument("--admin-only", action="store_true", help="Nur das Admin-Konto anlegen")
    args = parser.parse_args()
    run_seed(admin_only=args.admin_only)
