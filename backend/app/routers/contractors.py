from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import require_admin
from app.services import get_contractor_or_404

router = APIRouter(prefix="/contractors", tags=["Handwerker"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[schemas.ContractorResponse])
def list_contractors(active: bool | None = None, db: Session = Depends(get_db)):
    query = select(models.Contractor).order_by(models.Contractor.name)
    if active is not None:
        query = query.where(models.Contractor.active == active)
    return db.scalars(query).all()


@router.post("", response_model=schemas.ContractorResponse, status_code=status.HTTP_201_CREATED)
def create_contractor(payload: schemas.ContractorCreate, db: Session = Depends(get_db)):
    item = models.Contractor(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{contractor_id}", response_model=schemas.ContractorResponse)
def update_contractor(contractor_id: int, payload: schemas.ContractorUpdate, db: Session = Depends(get_db)):
    item = get_contractor_or_404(db, contractor_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{contractor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contractor(contractor_id: int, db: Session = Depends(get_db)):
    item = get_contractor_or_404(db, contractor_id)
    if item.tickets:
        raise HTTPException(status_code=409, detail="Handwerker ist Tickets zugeordnet und kann nicht gelöscht werden")
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
