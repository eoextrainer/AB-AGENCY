from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import require_staff
from app.db import get_db
from app.models import Artist, Inquiry, InquiryStatus, User
from app.schemas import DashboardStats

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
def dashboard_stats(db: Session = Depends(get_db), _: User = Depends(require_staff)) -> DashboardStats:
    total_artists = db.scalar(select(func.count()).select_from(Artist)) or 0
    featured_artists = db.scalar(select(func.count()).select_from(Artist).where(Artist.featured.is_(True))) or 0
    open_inquiries = db.scalar(select(func.count()).select_from(Inquiry).where(Inquiry.status.in_([InquiryStatus.NEW, InquiryStatus.QUALIFIED, InquiryStatus.PROPOSAL]))) or 0
    booked_inquiries = db.scalar(select(func.count()).select_from(Inquiry).where(Inquiry.status == InquiryStatus.BOOKED)) or 0
    average_lead_score = db.scalar(select(func.coalesce(func.avg(Inquiry.lead_score), 0))) or 0
    return DashboardStats(
        total_artists=total_artists,
        featured_artists=featured_artists,
        open_inquiries=open_inquiries,
        booked_inquiries=booked_inquiries,
        average_lead_score=float(average_lead_score),
    )
