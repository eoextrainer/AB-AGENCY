from datetime import datetime, timezone
from enum import StrEnum

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def enum_values(enum_cls) -> list[str]:
    return [member.value for member in enum_cls]


class UserRole(StrEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    CLIENT = "client"


class InquiryStatus(StrEnum):
    NEW = "new"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    BOOKED = "booked"
    CLOSED = "closed"


class Artist(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    headline: Mapped[str] = mapped_column(String(255))
    discipline: Mapped[str] = mapped_column(String(100), index=True)
    group_size: Mapped[str] = mapped_column(String(50), index=True)
    mood: Mapped[str] = mapped_column(String(100), index=True)
    venue_type: Mapped[str] = mapped_column(String(100), index=True)
    technical_requirements: Mapped[dict] = mapped_column(JSON, default=dict)
    bio: Mapped[str] = mapped_column(Text)
    years_experience: Mapped[int] = mapped_column(Integer, default=0)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_new: Mapped[bool] = mapped_column(Boolean, default=False)
    location: Mapped[str] = mapped_column(String(150), default="London")
    travel_ready: Mapped[bool] = mapped_column(Boolean, default=True)
    portrait_image_url: Mapped[str | None] = mapped_column(String(500))
    spoken_languages: Mapped[list[str]] = mapped_column(JSON, default=list)
    performance_resume: Mapped[list[dict]] = mapped_column(JSON, default=list)
    hero_video_url: Mapped[str | None] = mapped_column(String(500))
    teaser_video_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    media_assets: Mapped[list["MediaAsset"]] = relationship(back_populates="artist", cascade="all, delete-orphan")
    testimonials: Mapped[list["Testimonial"]] = relationship(back_populates="artist", cascade="all, delete-orphan")
    user: Mapped["User | None"] = relationship(back_populates="artist", uselist=False)


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    artist_id: Mapped[int | None] = mapped_column(ForeignKey("artists.id", ondelete="CASCADE"))
    asset_type: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(500))
    thumbnail_url: Mapped[str | None] = mapped_column(String(500))
    alt_text: Mapped[str | None] = mapped_column(String(255))
    asset_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    artist: Mapped[Artist | None] = relationship(back_populates="media_assets")


class Testimonial(Base):
    __tablename__ = "testimonials"

    id: Mapped[int] = mapped_column(primary_key=True)
    artist_id: Mapped[int | None] = mapped_column(ForeignKey("artists.id", ondelete="SET NULL"))
    client_name: Mapped[str] = mapped_column(String(200))
    client_type: Mapped[str] = mapped_column(String(100))
    quote: Mapped[str] = mapped_column(Text)
    event_name: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    artist: Mapped[Artist | None] = relationship(back_populates="testimonials")


class Inquiry(Base):
    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(200))
    contact_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(255), index=True)
    phone: Mapped[str | None] = mapped_column(String(50))
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    event_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    location: Mapped[str] = mapped_column(String(200))
    venue_type: Mapped[str | None] = mapped_column(String(100))
    ceiling_height_meters: Mapped[int | None] = mapped_column(Integer)
    budget_min: Mapped[float | None] = mapped_column(Numeric(10, 2))
    budget_max: Mapped[float | None] = mapped_column(Numeric(10, 2))
    preferred_disciplines: Mapped[list[str]] = mapped_column(JSON, default=list)
    preferred_artist_slugs: Mapped[list[str]] = mapped_column(JSON, default=list)
    message: Mapped[str] = mapped_column(Text)
    lead_score: Mapped[int] = mapped_column(Integer, default=0)
    source: Mapped[str] = mapped_column(String(100), default="website")
    status: Mapped[InquiryStatus] = mapped_column(Enum(InquiryStatus, values_callable=enum_values), default=InquiryStatus.NEW)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200))
    hashed_password: Mapped[str] = mapped_column(String(255))
    artist_id: Mapped[int | None] = mapped_column(ForeignKey("artists.id", ondelete="SET NULL"), unique=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, values_callable=enum_values), default=UserRole.VIEWER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    artist: Mapped[Artist | None] = relationship(back_populates="user")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    inquiry_id: Mapped[int | None] = mapped_column(ForeignKey("inquiries.id", ondelete="SET NULL"))
    artist_id: Mapped[int | None] = mapped_column(ForeignKey("artists.id", ondelete="SET NULL"))
    booking_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(100), default="tentative")
    fee_amount: Mapped[float | None] = mapped_column(Numeric(10, 2))
    deposit_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_url: Mapped[str | None] = mapped_column(String(500))
    production_notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"

    id: Mapped[int] = mapped_column(primary_key=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id", ondelete="CASCADE"), index=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(50), default="available")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class CaseStudy(Base):
    __tablename__ = "case_studies"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    event_context: Mapped[str] = mapped_column(String(150))
    challenge: Mapped[str] = mapped_column(Text)
    solution: Mapped[str] = mapped_column(Text)
    client_name: Mapped[str | None] = mapped_column(String(200))
    hero_image_url: Mapped[str | None] = mapped_column(String(500))
    video_url: Mapped[str | None] = mapped_column(String(500))
    featured_artist_slugs: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class ServicePage(Base):
    __tablename__ = "service_pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_email: Mapped[str | None] = mapped_column(String(255))
    action: Mapped[str] = mapped_column(String(100))
    entity_type: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[str] = mapped_column(String(100))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
