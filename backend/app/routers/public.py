from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.mongo import log_event
from app.services import get_apartment_or_404, get_ticket_or_404, ticket_response

router = APIRouter(prefix="/public", tags=["Öffentliche Meldung"])


def make_title(description: str) -> str:
    compact = " ".join(description.split())
    if len(compact) <= 78:
        return compact
    return f"{compact[:75].rstrip()}…"


@router.get("/properties", response_model=list[schemas.PublicPropertyResponse])
def list_public_properties(db: Session = Depends(get_db)):
    return db.scalars(select(models.Property).order_by(models.Property.name)).all()


@router.get("/apartments", response_model=list[schemas.PublicApartmentResponse])
def list_public_apartments(
    property_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(models.Apartment).where(models.Apartment.active.is_(True)).order_by(models.Apartment.apartment_number)
    if property_id is not None:
        query = query.where(models.Apartment.property_id == property_id)
    return db.scalars(query).all()


@router.post("/tickets", response_model=schemas.TicketResponse, status_code=status.HTTP_201_CREATED)
def create_public_ticket(payload: schemas.TicketCreate, db: Session = Depends(get_db)):
    apartment = get_apartment_or_404(db, payload.apartment_id)
    if not apartment.active:
        raise HTTPException(status_code=409, detail="Diese Wohnung ist nicht aktiv")

    ticket = models.Ticket(
        apartment_id=payload.apartment_id,
        title=make_title(payload.description),
        description=payload.description.strip(),
        priority="urgent" if payload.is_emergency else "normal",
        status="new",
        reported_by=payload.reported_by.strip(),
        reporter_phone=payload.reporter_phone.strip() if payload.reporter_phone else None,
        reporter_email=str(payload.reporter_email) if payload.reporter_email else None,
    )
    db.add(ticket)
    db.commit()
    ticket = get_ticket_or_404(db, ticket.id)
    log_event(
        ticket.id,
        "ticket_created",
        payload.reported_by.strip(),
        {"title": ticket.title, "emergency": payload.is_emergency},
    )
    return ticket_response(ticket)
