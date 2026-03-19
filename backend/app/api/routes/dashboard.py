from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import require_staff
from app.db import get_db
from app.models import Artist, AvailabilitySlot, Booking, Inquiry, InquiryStatus, User
from app.schemas import AdminOverview, AvailabilitySlotRead, BookingRead, DashboardStats, InquiryRead

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


@router.get("/overview", response_model=AdminOverview)
def admin_overview(db: Session = Depends(get_db), _: User = Depends(require_staff)) -> AdminOverview:
    stats = dashboard_stats(db=db, _=_)
    inquiries = list(db.scalars(select(Inquiry).order_by(Inquiry.created_at.desc())).all())
    bookings = list(db.scalars(select(Booking).order_by(Booking.created_at.desc())).all())
    availability = list(db.scalars(select(AvailabilitySlot).order_by(AvailabilitySlot.start_date.asc())).all())
    return AdminOverview(
        stats=stats,
        inquiries=[InquiryRead.model_validate(inquiry) for inquiry in inquiries],
        bookings=[BookingRead.model_validate(booking) for booking in bookings],
        availability=[AvailabilitySlotRead.model_validate(slot) for slot in availability],
    )
