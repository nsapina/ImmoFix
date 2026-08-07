from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.mongo import list_events, log_event
from app.security import require_admin
from app.services import get_ticket_or_404

router = APIRouter(
    prefix="/tickets/{ticket_id}/events",
    tags=["Ticket-Aktivitäten"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=list[schemas.TicketEventResponse])
def get_events(ticket_id: int, db: Session = Depends(get_db)):
    get_ticket_or_404(db, ticket_id)
    return list_events(ticket_id)


@router.post("", response_model=schemas.TicketEventResponse, status_code=status.HTTP_201_CREATED)
def add_note(
    ticket_id: int,
    payload: schemas.TicketEventCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    get_ticket_or_404(db, ticket_id)
    event_id = log_event(ticket_id, "note_added", current_user.full_name, {"message": payload.message})
    ticket_events = list_events(ticket_id)
    if event_id:
        return next(event for event in ticket_events if event["id"] == event_id)
    return {
        "id": "not-persisted",
        "ticket_id": ticket_id,
        "event_type": "note_not_persisted",
        "actor": current_user.full_name,
        "data": {"message": payload.message},
        "created_at": datetime.now(timezone.utc),
    }
