import pytest
from pydantic import ValidationError

from app.schemas import TicketCreate


def test_public_ticket_create_defaults():
    ticket = TicketCreate(
        apartment_id=1,
        description="Die Heizung bleibt kalt.",
        reported_by="Test Person",
        reporter_phone="+49 170 1234567",
    )
    assert ticket.is_emergency is False


def test_public_ticket_requires_contact():
    with pytest.raises(ValidationError):
        TicketCreate(
            apartment_id=1,
            description="Die Heizung bleibt kalt.",
            reported_by="Test Person",
        )
