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
        hero_title="Des performances vertigineuses pour les événements les plus exigeants.",
        hero_subtitle="AB Agency unit une mise en scène cinématographique à une précision de production pensée pour les festivals, les galas et les célébrations de prestige.",
        featured_artists=featured_artists,
        trust_markers=["Productions évaluées et sécurisées", "Accompagnement pour tournées internationales", "Maîtrise des univers luxe et festival"],
        featured_services=services,
    )
