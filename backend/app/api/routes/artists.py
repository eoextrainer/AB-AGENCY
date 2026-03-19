from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_staff
from app.db import get_db
from app.models import Artist, User
from app.schemas import ArtistCreate, ArtistRead

router = APIRouter()


@router.get("", response_model=list[ArtistRead])
def list_artists(
    db: Session = Depends(get_db),
    discipline: str | None = Query(default=None),
    mood: str | None = Query(default=None),
    featured: bool | None = Query(default=None),
) -> list[Artist]:
    query = select(Artist)
    if discipline:
        query = query.where(Artist.discipline == discipline)
    if mood:
        query = query.where(Artist.mood == mood)
    if featured is not None:
        query = query.where(Artist.featured == featured)
    return list(db.scalars(query.order_by(Artist.name)).all())


@router.get("/{slug}", response_model=ArtistRead)
def get_artist(slug: str, db: Session = Depends(get_db)) -> Artist:
    artist = db.scalar(select(Artist).where(Artist.slug == slug))
    if artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return artist


@router.post("", response_model=ArtistRead)
def create_artist(payload: ArtistCreate, db: Session = Depends(get_db), _: User = Depends(require_staff)) -> Artist:
    existing = db.scalar(select(Artist).where(Artist.slug == payload.slug))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Artist slug already exists")
    artist = Artist(**payload.model_dump())
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist
