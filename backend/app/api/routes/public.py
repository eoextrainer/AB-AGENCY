from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Artist, ServicePage
from app.schemas import PublicHomepage

router = APIRouter()


@router.get("/homepage", response_model=PublicHomepage)
def homepage(db: Session = Depends(get_db)) -> PublicHomepage:
    featured_artists = list(db.scalars(select(Artist).where(Artist.featured.is_(True)).limit(6)).all())
    services = [service.title for service in db.scalars(select(ServicePage).limit(4)).all()]
    return PublicHomepage(
        hero_title="Gravity-defying performance for the world’s most exacting events.",
        hero_subtitle="AB Agency pairs cinematic performance design with production precision for festivals, galas, and luxury celebrations.",
        featured_artists=featured_artists,
        trust_markers=["Risk-assessed productions", "International touring support", "Luxury and festival expertise"],
        featured_services=services,
    )
