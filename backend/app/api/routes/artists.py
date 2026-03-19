from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_user, require_staff
from app.db import get_db
from app.models import Artist, User
from app.schemas import ArtistCreate, ArtistPortal, ArtistRead, UserRead

router = APIRouter()


@router.get("", response_model=list[ArtistRead])
def list_artists(
    db: Session = Depends(get_db),
    discipline: str | None = Query(default=None),
    mood: str | None = Query(default=None),
    featured: bool | None = Query(default=None),
) -> list[Artist]:
    query = select(Artist).options(selectinload(Artist.media_assets))
    if discipline:
        query = query.where(Artist.discipline == discipline)
    if mood:
        query = query.where(Artist.mood == mood)
    if featured is not None:
        query = query.where(Artist.featured == featured)
    return list(db.scalars(query.order_by(Artist.name)).all())


@router.get("/me/profile", response_model=ArtistPortal)
def get_my_artist_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ArtistPortal:
    if current_user.artist_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No artist profile attached to this account")

    artist = db.scalar(select(Artist).options(selectinload(Artist.media_assets)).where(Artist.id == current_user.artist_id))
    if artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist profile not found")

    return ArtistPortal(user=UserRead.model_validate(current_user), artist=ArtistRead.model_validate(artist))


@router.get("/{slug}", response_model=ArtistRead)
def get_artist(slug: str, db: Session = Depends(get_db)) -> Artist:
    artist = db.scalar(select(Artist).options(selectinload(Artist.media_assets)).where(Artist.slug == slug))
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
