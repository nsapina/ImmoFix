from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.database import get_db
from app.security import require_admin
from app.services import apartment_response, get_apartment_or_404, get_property_or_404

router = APIRouter(prefix="/apartments", tags=["Wohnungen"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[schemas.ApartmentResponse])
def list_apartments(active: bool | None = None, db: Session = Depends(get_db)):
    query = select(models.Apartment).options(joinedload(models.Apartment.property)).order_by(models.Apartment.id)
    if active is not None:
        query = query.where(models.Apartment.active == active)
    return [apartment_response(item) for item in db.scalars(query).all()]


@router.post("", response_model=schemas.ApartmentResponse, status_code=status.HTTP_201_CREATED)
def create_apartment(payload: schemas.ApartmentCreate, db: Session = Depends(get_db)):
    get_property_or_404(db, payload.property_id)
    item = models.Apartment(**payload.model_dump())
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Wohnungsnummer existiert in dieser Immobilie bereits")
    item = db.scalar(select(models.Apartment).options(joinedload(models.Apartment.property)).where(models.Apartment.id == item.id))
    return apartment_response(item)


@router.patch("/{apartment_id}", response_model=schemas.ApartmentResponse)
def update_apartment(apartment_id: int, payload: schemas.ApartmentUpdate, db: Session = Depends(get_db)):
    item = get_apartment_or_404(db, apartment_id)
    data = payload.model_dump(exclude_unset=True)
    if "property_id" in data:
        get_property_or_404(db, data["property_id"])
    for key, value in data.items():
        setattr(item, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Wohnungsnummer existiert in dieser Immobilie bereits")
    item = db.scalar(select(models.Apartment).options(joinedload(models.Apartment.property)).where(models.Apartment.id == apartment_id))
    return apartment_response(item)


@router.delete("/{apartment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_apartment(apartment_id: int, db: Session = Depends(get_db)):
    item = get_apartment_or_404(db, apartment_id)
    if item.tickets:
        raise HTTPException(status_code=409, detail="Wohnung besitzt Tickets und kann nicht gelöscht werden")
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
