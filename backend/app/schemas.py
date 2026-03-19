from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import InquiryStatus, UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.VIEWER


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime


class ArtistBase(BaseModel):
    slug: str
    name: str
    headline: str
    discipline: str
    group_size: str
    mood: str
    venue_type: str
    technical_requirements: dict = Field(default_factory=dict)
    bio: str
    featured: bool = False
    is_new: bool = False
    location: str = "London"
    travel_ready: bool = True
    hero_video_url: str | None = None
    teaser_video_url: str | None = None


class ArtistCreate(ArtistBase):
    pass


class ArtistRead(ArtistBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class InquiryCreate(BaseModel):
    company_name: str
    contact_name: str
    email: EmailStr
    phone: str | None = None
    event_type: str
    event_date: datetime | None = None
    location: str
    venue_type: str | None = None
    ceiling_height_meters: int | None = None
    budget_min: Decimal | None = None
    budget_max: Decimal | None = None
    preferred_disciplines: list[str] = Field(default_factory=list)
    preferred_artist_slugs: list[str] = Field(default_factory=list)
    message: str
    source: str = "website"


class InquiryRead(InquiryCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_score: int
    status: InquiryStatus
    created_at: datetime


class DashboardStats(BaseModel):
    total_artists: int
    featured_artists: int
    open_inquiries: int
    booked_inquiries: int
    average_lead_score: float


class BookingBase(BaseModel):
    inquiry_id: int | None = None
    artist_id: int | None = None
    booking_date: datetime | None = None
    status: str = "tentative"
    fee_amount: Decimal | None = None
    deposit_paid: bool = False
    contract_url: str | None = None
    production_notes: str | None = None


class BookingCreate(BookingBase):
    pass


class BookingRead(BookingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class AvailabilitySlotBase(BaseModel):
    artist_id: int
    start_date: datetime
    end_date: datetime
    status: str = "available"


class AvailabilitySlotCreate(AvailabilitySlotBase):
    pass


class AvailabilitySlotRead(AvailabilitySlotBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class PublicHomepage(BaseModel):
    hero_title: str
    hero_subtitle: str
    featured_artists: list[ArtistRead]
    trust_markers: list[str]
    featured_services: list[str]
