from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_staff
from app.db import get_db
from app.models import Booking, User
from app.schemas import BookingCreate, BookingRead

router = APIRouter()


@router.get("", response_model=list[BookingRead])
def list_bookings(db: Session = Depends(get_db), _: User = Depends(require_staff)) -> list[Booking]:
    return list(db.scalars(select(Booking).order_by(Booking.created_at.desc())).all())


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db), _: User = Depends(require_staff)) -> Booking:
    booking = Booking(**payload.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/{booking_id}", response_model=BookingRead)
def get_booking(booking_id: int, db: Session = Depends(get_db), _: User = Depends(require_staff)) -> Booking:
    booking = db.scalar(select(Booking).where(Booking.id == booking_id))
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking