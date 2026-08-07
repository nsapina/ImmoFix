from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.mongo import delete_events, log_event
from app.security import require_admin
from app.services import (
    get_apartment_or_404,
    get_contractor_or_404,
    get_ticket_or_404,
    ticket_query,
    ticket_response,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets – Verwaltung"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=list[schemas.TicketResponse])
def list_tickets(
    status_filter: schemas.TicketStatus | None = Query(default=None, alias="status"),
    priority: schemas.Priority | None = None,
    apartment_id: int | None = None,
    property_id: int | None = None,
    contractor_id: int | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    query = ticket_query().order_by(models.Ticket.created_at.desc())
    if status_filter:
        query = query.where(models.Ticket.status == status_filter.value)
    if priority:
        query = query.where(models.Ticket.priority == priority.value)
    if apartment_id:
        query = query.where(models.Ticket.apartment_id == apartment_id)
    if property_id:
        query = query.join(models.Ticket.apartment).where(models.Apartment.property_id == property_id)
    if contractor_id:
        query = query.where(models.Ticket.contractor_id == contractor_id)
    if search:
        pattern = f"%{search.strip()}%"
        query = query.where(
            or_(
                models.Ticket.title.ilike(pattern),
                models.Ticket.description.ilike(pattern),
                models.Ticket.reported_by.ilike(pattern),
            )
        )
    return [ticket_response(ticket) for ticket in db.scalars(query).unique().all()]


@router.get("/{ticket_id}", response_model=schemas.TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return ticket_response(get_ticket_or_404(db, ticket_id))


@router.patch("/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket(
    ticket_id: int,
    payload: schemas.TicketUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    ticket = get_ticket_or_404(db, ticket_id)
    data = payload.model_dump(exclude_unset=True)

    if "apartment_id" in data:
        get_apartment_or_404(db, data["apartment_id"])
    if "contractor_id" in data and data["contractor_id"] is not None:
        get_contractor_or_404(db, data["contractor_id"])

    changes = {}
    for key, value in data.items():
        if isinstance(value, (schemas.Priority, schemas.TicketStatus)):
            value = value.value
        if key == "reporter_email" and value is not None:
            value = str(value)
        old_value = getattr(ticket, key)
        if old_value != value:
            changes[key] = {"from": old_value, "to": value}
            setattr(ticket, key, value)

    if "contractor_id" in changes and ticket.contractor_id is not None and "status" not in changes and ticket.status == "new":
        changes["status"] = {"from": "new", "to": "assigned"}
        ticket.status = "assigned"

    if "status" in changes:
        if ticket.status in {"resolved", "closed"} and ticket.resolved_at is None:
            ticket.resolved_at = datetime.now(timezone.utc)
        elif ticket.status not in {"resolved", "closed"}:
            ticket.resolved_at = None

    if changes:
        ticket.updated_at = datetime.now(timezone.utc)
        db.commit()
        ticket = get_ticket_or_404(db, ticket_id)
        log_event(ticket.id, "ticket_updated", current_user.full_name, {"changes": changes})
    return ticket_response(ticket)


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = get_ticket_or_404(db, ticket_id)
    db.delete(ticket)
    db.commit()
    delete_events(ticket_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
