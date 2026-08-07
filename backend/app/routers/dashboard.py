from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import require_admin
from app.services import ticket_query, ticket_response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(require_admin)])


@router.get("", response_model=schemas.DashboardResponse)
def dashboard(db: Session = Depends(get_db)):
    open_statuses = ["new", "assigned", "in_progress", "waiting"]
    open_tickets = db.scalar(select(func.count(models.Ticket.id)).where(models.Ticket.status.in_(open_statuses))) or 0
    urgent_tickets = db.scalar(
        select(func.count(models.Ticket.id)).where(
            models.Ticket.priority == "urgent", models.Ticket.status.in_(open_statuses)
        )
    ) or 0
    unassigned_tickets = db.scalar(
        select(func.count(models.Ticket.id)).where(
            models.Ticket.contractor_id.is_(None), models.Ticket.status.in_(open_statuses)
        )
    ) or 0
    resolved_tickets = db.scalar(
        select(func.count(models.Ticket.id)).where(models.Ticket.status.in_(["resolved", "closed"]))
    ) or 0
    recent = db.scalars(ticket_query().order_by(models.Ticket.updated_at.desc()).limit(5)).unique().all()
    return {
        "open_tickets": open_tickets,
        "urgent_tickets": urgent_tickets,
        "unassigned_tickets": unassigned_tickets,
        "resolved_tickets": resolved_tickets,
        "recent_tickets": [ticket_response(ticket) for ticket in recent],
    }
