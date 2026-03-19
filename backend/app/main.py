from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api.router import api_router
from app.core.config import settings
from app.core.security import get_password_hash
from app.db import SessionLocal, init_database
from app.models import Artist, ServicePage, User, UserRole


def seed_database(db) -> None:
    if db.scalar(select(User.id).limit(1)) is None:
        db.add(
            User(
                email=settings.first_superuser_email,
                full_name="AB Agency Admin",
                hashed_password=get_password_hash(settings.first_superuser_password),
                role=UserRole.ADMIN,
            )
        )
    if db.scalar(select(Artist.id).limit(1)) is None:
        db.add_all(
            [
                Artist(
                    slug="luna-silk-duo",
                    name="Luna Silk Duo",
                    headline="A suspended duet of sculptural aerial silk and slow-burn theatricality.",
                    discipline="Aerial",
                    group_size="Duo",
                    mood="Ethereal",
                    venue_type="Corporate",
                    technical_requirements={"rigging": True, "min_ceiling_height_m": 8, "power": "1x 13A"},
                    bio="Aerial silk duet developed for luxury galas, museum commissions, and cinematic brand moments.",
                    featured=True,
                    is_new=True,
                    hero_video_url="https://cdn.example.com/videos/luna-hero.mp4",
                    teaser_video_url="https://cdn.example.com/videos/luna-teaser.mp4",
                ),
                Artist(
                    slug="volt-cyr",
                    name="Volt Cyr",
                    headline="A polished Cyr wheel act balancing velocity, control, and couture styling.",
                    discipline="Ground Performance",
                    group_size="Solo",
                    mood="Dramatic",
                    venue_type="Festival",
                    technical_requirements={"rigging": False, "floor": "Level performance surface", "power": "None"},
                    bio="High-impact solo Cyr wheel performance suited to brand launches and outdoor stages.",
                    featured=True,
                    is_new=False,
                    hero_video_url="https://cdn.example.com/videos/volt-hero.mp4",
                    teaser_video_url="https://cdn.example.com/videos/volt-teaser.mp4",
                ),
            ]
        )
    if db.scalar(select(ServicePage.id).limit(1)) is None:
        db.add_all(
            [
                ServicePage(slug="representation", title="Talent Representation", summary="Curated performance talent for high-stakes events.", body="AB Agency represents exceptional performance artists across aerial, acrobatic, and immersive disciplines."),
                ServicePage(slug="production-support", title="Production Support", summary="Technical planning and production coordination.", body="We translate artistic ambition into safe, executable production plans."),
                ServicePage(slug="creative-consulting", title="Creative Consulting", summary="Concept development for standout event moments.", body="We help clients shape custom performance concepts with operational clarity."),
            ]
        )
    db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    db = SessionLocal()
    try:
        seed_database(db)
        yield
    finally:
        db.close()


@asynccontextmanager
async def testing_lifespan(_: FastAPI):
    yield


def create_application(*, testing: bool = False) -> FastAPI:
    application = FastAPI(title=settings.app_name, lifespan=testing_lifespan if testing else lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router, prefix=settings.api_prefix)

    @application.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_application()
