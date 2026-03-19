from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_staff
from app.db import get_db
from app.models import AvailabilitySlot, User
from app.schemas import AvailabilitySlotCreate, AvailabilitySlotRead

router = APIRouter()


@router.get("", response_model=list[AvailabilitySlotRead])
def list_availability(
    db: Session = Depends(get_db),
    artist_id: int | None = Query(default=None),
    _: User = Depends(require_staff),
) -> list[AvailabilitySlot]:
    query = select(AvailabilitySlot).order_by(AvailabilitySlot.start_date.asc())
    if artist_id is not None:
        query = query.where(AvailabilitySlot.artist_id == artist_id)
    return list(db.scalars(query).all())


@router.post("", response_model=AvailabilitySlotRead, status_code=status.HTTP_201_CREATED)
def create_availability(payload: AvailabilitySlotCreate, db: Session = Depends(get_db), _: User = Depends(require_staff)) -> AvailabilitySlot:
    slot = AvailabilitySlot(**payload.model_dump())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


@router.get("/{slot_id}", response_model=AvailabilitySlotRead)
def get_availability(slot_id: int, db: Session = Depends(get_db), _: User = Depends(require_staff)) -> AvailabilitySlot:
    slot = db.scalar(select(AvailabilitySlot).where(AvailabilitySlot.id == slot_id))
    if slot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Availability slot not found")
    return slot