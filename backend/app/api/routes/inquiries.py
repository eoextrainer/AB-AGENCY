from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import require_staff
from app.db import get_db
from app.models import Inquiry, User
from app.schemas import InquiryCreate, InquiryRead

router = APIRouter()


def score_lead(payload: InquiryCreate) -> int:
    score = 25
    high_value_types = {"corporate gala", "festival", "luxury wedding", "brand launch"}
    if payload.event_type.lower() in high_value_types:
        score += 20
    if payload.budget_max and payload.budget_max >= 10000:
        score += 25
    if payload.ceiling_height_meters and payload.ceiling_height_meters >= 8:
        score += 10
    if payload.preferred_artist_slugs:
        score += 10
    if payload.venue_type and payload.venue_type.lower() in {"indoor", "theater", "hotel ballroom"}:
        score += 10
    return min(score, 100)


@router.post("", response_model=InquiryRead)
def create_inquiry(payload: InquiryCreate, db: Session = Depends(get_db)) -> Inquiry:
    inquiry = Inquiry(**payload.model_dump(), lead_score=score_lead(payload))
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry


@router.get("", response_model=list[InquiryRead])
def list_inquiries(db: Session = Depends(get_db), _: User = Depends(require_staff)) -> list[Inquiry]:
    return list(db.scalars(select(Inquiry).order_by(Inquiry.created_at.desc())).all())


@router.get("/summary/count")
def inquiry_summary(db: Session = Depends(get_db), _: User = Depends(require_staff)) -> dict:
    total = db.scalar(select(func.count()).select_from(Inquiry)) or 0
    return {"total": total}
