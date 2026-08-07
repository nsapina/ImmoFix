from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app import models, schemas


def get_property_or_404(db: Session, property_id: int) -> models.Property:
    item = db.get(models.Property, property_id)
    if not item:
        raise HTTPException(status_code=404, detail="Immobilie nicht gefunden")
    return item


def get_apartment_or_404(db: Session, apartment_id: int) -> models.Apartment:
    item = db.get(models.Apartment, apartment_id)
    if not item:
        raise HTTPException(status_code=404, detail="Wohnung nicht gefunden")
    return item


def get_contractor_or_404(db: Session, contractor_id: int) -> models.Contractor:
    item = db.get(models.Contractor, contractor_id)
    if not item:
        raise HTTPException(status_code=404, detail="Handwerker nicht gefunden")
    return item


def ticket_query():
    return select(models.Ticket).options(
        joinedload(models.Ticket.apartment).joinedload(models.Apartment.property),
        joinedload(models.Ticket.contractor),
    )


def get_ticket_or_404(db: Session, ticket_id: int) -> models.Ticket:
    ticket = db.scalar(ticket_query().where(models.Ticket.id == ticket_id))
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket nicht gefunden")
    return ticket


def apartment_response(apartment: models.Apartment) -> schemas.ApartmentResponse:
    return schemas.ApartmentResponse(
        id=apartment.id,
        property_id=apartment.property_id,
        property_name=apartment.property.name,
        property_address=f"{apartment.property.address}, {apartment.property.city}",
        apartment_number=apartment.apartment_number,
        floor=apartment.floor,
        contact_name=apartment.contact_name,
        contact_phone=apartment.contact_phone,
        contact_email=apartment.contact_email,
        notes=apartment.notes,
        active=apartment.active,
        created_at=apartment.created_at,
    )


def ticket_number(ticket: models.Ticket) -> str:
    return f"IMF-{ticket.created_at.year}-{ticket.id:05d}"


def ticket_response(ticket: models.Ticket) -> schemas.TicketResponse:
    return schemas.TicketResponse(
        id=ticket.id,
        ticket_number=ticket_number(ticket),
        apartment_id=ticket.apartment_id,
        apartment_label=f"Whg. {ticket.apartment.apartment_number}",
        property_name=ticket.apartment.property.name,
        property_address=f"{ticket.apartment.property.address}, {ticket.apartment.property.city}",
        contractor_id=ticket.contractor_id,
        contractor_name=ticket.contractor.name if ticket.contractor else None,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        status=ticket.status,
        reported_by=ticket.reported_by,
        reporter_phone=ticket.reporter_phone,
        reporter_email=ticket.reporter_email,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        resolved_at=ticket.resolved_at,
    )
