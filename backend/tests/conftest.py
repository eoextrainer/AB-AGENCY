import os
from collections.abc import Generator
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("DATABASE_URL", "sqlite://")

from app.api.deps import get_db
from app.core.security import get_password_hash
from app.db import Base
from app.main import create_application, seed_database
from app.models import Artist, Booking, Inquiry, InquiryStatus, ServicePage, User, UserRole


TEST_DATABASE_URL = "sqlite://"


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        seed_database(session)
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app = create_application(testing=True)

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session: Session) -> User:
    return db_session.query(User).filter(User.role == UserRole.ADMIN).one()


@pytest.fixture
def editor_user(db_session: Session) -> User:
    user = User(
        email="editor@ab-agency.com",
        full_name="AB Editor",
        hashed_password=get_password_hash("editor-pass"),
        role=UserRole.EDITOR,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def viewer_user(db_session: Session) -> User:
    user = User(
        email="viewer@ab-agency.com",
        full_name="AB Viewer",
        hashed_password=get_password_hash("viewer-pass"),
        role=UserRole.VIEWER,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@ab-agency.com", "password": "admin12345"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_inquiry(db_session: Session) -> Inquiry:
    inquiry = Inquiry(
        company_name="Acme Events",
        contact_name="Jordan Vale",
        email="jordan@example.com",
        event_type="festival",
        event_date=datetime(2026, 7, 12, 18, 0, 0),
        location="London",
        venue_type="indoor",
        budget_min=5000,
        budget_max=15000,
        preferred_disciplines=["Aerial"],
        preferred_artist_slugs=["luna-silk-duo"],
        message="Looking for a headline moment.",
        lead_score=85,
        status=InquiryStatus.QUALIFIED,
    )
    db_session.add(inquiry)
    db_session.commit()
    db_session.refresh(inquiry)
    return inquiry


@pytest.fixture
def sample_booking(db_session: Session, sample_inquiry: Inquiry) -> Booking:
    artist = db_session.query(Artist).filter(Artist.slug == "luna-silk-duo").one()
    booking = Booking(
        inquiry_id=sample_inquiry.id,
        artist_id=artist.id,
        booking_date=datetime(2026, 7, 12, 18, 0, 0),
        status="confirmed",
        fee_amount=12000,
        deposit_paid=True,
    )
    db_session.add(booking)
    db_session.commit()
    db_session.refresh(booking)
    return booking


@pytest.fixture
def service_titles(db_session: Session) -> list[str]:
    return [service.title for service in db_session.query(ServicePage).all()]