from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class Priority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


class TicketStatus(str, Enum):
    new = "new"
    assigned = "assigned"
    in_progress = "in_progress"
    waiting = "waiting"
    resolved = "resolved"
    closed = "closed"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_admin: bool
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PropertyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    address: str = Field(min_length=3, max_length=200)
    city: str = Field(min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)


class PropertyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    address: str | None = Field(default=None, min_length=3, max_length=200)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)


class PropertyResponse(PropertyCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PublicPropertyResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str
    model_config = ConfigDict(from_attributes=True)


class ApartmentCreate(BaseModel):
    property_id: int
    apartment_number: str = Field(min_length=1, max_length=30)
    floor: str | None = Field(default=None, max_length=30)
    contact_name: str | None = Field(default=None, max_length=120)
    contact_phone: str | None = Field(default=None, max_length=50)
    contact_email: EmailStr | None = None
    notes: str | None = None
    active: bool = True


class ApartmentUpdate(BaseModel):
    property_id: int | None = None
    apartment_number: str | None = Field(default=None, min_length=1, max_length=30)
    floor: str | None = Field(default=None, max_length=30)
    contact_name: str | None = Field(default=None, max_length=120)
    contact_phone: str | None = Field(default=None, max_length=50)
    contact_email: EmailStr | None = None
    notes: str | None = None
    active: bool | None = None


class ApartmentResponse(ApartmentCreate):
    id: int
    property_name: str
    property_address: str
    created_at: datetime


class PublicApartmentResponse(BaseModel):
    id: int
    property_id: int
    apartment_number: str
    floor: str | None
    model_config = ConfigDict(from_attributes=True)


class ContractorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    company: str | None = Field(default=None, max_length=120)
    phone: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = None
    specialization: str = Field(min_length=2, max_length=100)
    active: bool = True


class ContractorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    company: str | None = Field(default=None, max_length=120)
    phone: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = None
    specialization: str | None = Field(default=None, min_length=2, max_length=100)
    active: bool | None = None


class ContractorResponse(ContractorCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TicketCreate(BaseModel):
    """Öffentliche Reparaturmeldung. Verwaltungsfelder werden später gesetzt."""

    apartment_id: int
    description: str = Field(min_length=5, max_length=5000)
    reported_by: str = Field(min_length=2, max_length=120)
    reporter_phone: str | None = Field(default=None, max_length=50)
    reporter_email: EmailStr | None = None
    is_emergency: bool = False

    @model_validator(mode="after")
    def validate_contact(self):
        if not (self.reporter_phone and self.reporter_phone.strip()) and not self.reporter_email:
            raise ValueError("Bitte geben Sie eine Telefonnummer oder E-Mail-Adresse an")
        return self


class TicketUpdate(BaseModel):
    apartment_id: int | None = None
    contractor_id: int | None = None
    title: str | None = Field(default=None, min_length=3, max_length=180)
    description: str | None = Field(default=None, min_length=5, max_length=5000)
    priority: Priority | None = None
    status: TicketStatus | None = None
    reported_by: str | None = Field(default=None, min_length=2, max_length=120)
    reporter_phone: str | None = Field(default=None, max_length=50)
    reporter_email: EmailStr | None = None


class TicketResponse(BaseModel):
    id: int
    ticket_number: str
    apartment_id: int
    apartment_label: str
    property_name: str
    property_address: str
    contractor_id: int | None
    contractor_name: str | None
    title: str
    description: str
    priority: Priority
    status: TicketStatus
    reported_by: str
    reporter_phone: str | None
    reporter_email: str | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None


class TicketEventCreate(BaseModel):
    message: str = Field(min_length=2, max_length=2000)


class TicketEventResponse(BaseModel):
    id: str
    ticket_id: int
    event_type: str
    actor: str
    data: dict
    created_at: datetime


class DashboardResponse(BaseModel):
    open_tickets: int
    urgent_tickets: int
    unassigned_tickets: int
    resolved_tickets: int
    recent_tickets: list[TicketResponse]
