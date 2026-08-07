from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import require_admin
from app.services import get_property_or_404

router = APIRouter(prefix="/properties", tags=["Immobilien"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[schemas.PropertyResponse])
def list_properties(db: Session = Depends(get_db)):
    return db.scalars(select(models.Property).order_by(models.Property.name)).all()


@router.post("", response_model=schemas.PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(payload: schemas.PropertyCreate, db: Session = Depends(get_db)):
    item = models.Property(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{property_id}", response_model=schemas.PropertyResponse)
def update_property(property_id: int, payload: schemas.PropertyUpdate, db: Session = Depends(get_db)):
    item = get_property_or_404(db, property_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    item = get_property_or_404(db, property_id)
    if item.apartments:
        raise HTTPException(status_code=409, detail="Immobilie enthält Wohnungen und kann nicht gelöscht werden")
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
