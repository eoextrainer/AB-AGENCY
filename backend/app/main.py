from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, select

from app.api.router import api_router
from app.core.config import settings
from app.core.security import get_password_hash
from app.db import SessionLocal, init_database
from app.models import Artist, MediaAsset, ServicePage, User, UserRole


SEEDED_ARTISTS = [
    {
        "slug": "luna-silk-duo",
        "name": "Luna Silk Duo",
        "headline": "Un duo de soie aerienne aux lignes sculpturales pour les galas, les musees et les lancements d'exception.",
        "discipline": "Danse aerienne",
        "group_size": "Duo",
        "mood": "Ethere",
        "venue_type": "Gala",
        "technical_requirements": {"rigging": True, "min_ceiling_height_m": 8, "power": "1x 13A"},
        "bio": "Luna Silk Duo developpe des tableaux suspendus a forte presence visuelle, pensés pour les diners de prestige et les moments de revelation scenographique.",
        "years_experience": 10,
        "featured": True,
        "is_new": True,
        "location": "Londres",
        "travel_ready": True,
        "portrait_image_url": "https://images.unsplash.com/photo-1515169067868-5387ec356754?auto=format&fit=crop&w=900&q=80",
        "spoken_languages": ["Anglais", "Francais"],
        "performance_resume": [
            {"period": "2025", "production": "Halo Dinner", "venue": "Somerset House", "role": "Duo aerien"},
            {"period": "2024", "production": "Museum by Night", "venue": "V&A Museum", "role": "Installation vivante"},
        ],
        "hero_video_url": "https://cdn.coverr.co/videos/coverr-aerial-silks-1578393576073?download=1080p",
        "teaser_video_url": "https://cdn.coverr.co/videos/coverr-swinging-from-aerial-silk-1572458909737?download=1080p",
        "media_assets": [
            {"asset_type": "image", "title": "Duo suspendu", "url": "https://images.unsplash.com/photo-1515169067868-5387ec356754?auto=format&fit=crop&w=1200&q=80", "thumbnail_url": "https://images.unsplash.com/photo-1515169067868-5387ec356754?auto=format&fit=crop&w=600&q=80", "alt_text": "Luna Silk Duo en suspension"},
            {"asset_type": "video", "title": "Extrait duo", "url": "https://cdn.coverr.co/videos/coverr-aerial-silks-1578393576073?download=1080p", "thumbnail_url": "https://images.unsplash.com/photo-1515169067868-5387ec356754?auto=format&fit=crop&w=600&q=80", "alt_text": "Video de Luna Silk Duo"},
        ],
    },
    {
        "slug": "volt-cyr",
        "name": "Volt Cyr",
        "headline": "Un numero de roue Cyr affute, veloce et couture pour les marques, les festivals et les scenes urbaines premium.",
        "discipline": "Performance au sol",
        "group_size": "Solo",
        "mood": "Dramatique",
        "venue_type": "Festival",
        "technical_requirements": {"rigging": False, "floor": "Plateau lisse et stable", "power": "Aucune"},
        "bio": "Volt Cyr livre une ecriture physique nerveuse et maitrisée, ideale pour les ouvertures spectaculaires et les respirations visuelles a haute energie.",
        "years_experience": 12,
        "featured": True,
        "is_new": False,
        "location": "Bruxelles",
        "travel_ready": True,
        "portrait_image_url": "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=900&q=80",
        "spoken_languages": ["Anglais", "Francais"],
        "performance_resume": [
            {"period": "2025", "production": "Velocity", "venue": "DockX Brussels", "role": "Solo Cyr"},
            {"period": "2024", "production": "Brand Pulse", "venue": "Tour & Taxis", "role": "Ouverture de scene"},
        ],
        "hero_video_url": "https://cdn.coverr.co/videos/coverr-female-dancer-performing-1560260224327?download=1080p",
        "teaser_video_url": "https://cdn.coverr.co/videos/coverr-ballerina-warming-up-1562833129043?download=1080p",
        "media_assets": [
            {"asset_type": "image", "title": "Portrait cyr", "url": "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=1200&q=80", "thumbnail_url": "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=600&q=80", "alt_text": "Volt Cyr en scene"},
            {"asset_type": "video", "title": "Extrait roue Cyr", "url": "https://cdn.coverr.co/videos/coverr-female-dancer-performing-1560260224327?download=1080p", "thumbnail_url": "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=600&q=80", "alt_text": "Video de Volt Cyr"},
        ],
    },
    {
        "slug": "ambre-acrobatique",
        "name": "Ambre Lenoir",
        "headline": "Une signature de danse acrobatique sculptée pour les galas de marque et les scènes immersives.",
        "discipline": "Danse acrobatique",
        "group_size": "Solo",
        "mood": "Sophistique",
        "venue_type": "Gala",
        "technical_requirements": {"floor": "Surface de danse amortie", "power": "1x 13A", "rigging": False},
        "bio": "Ambre compose des performances au sol à forte intensité visuelle, entre lignes contemporaines, portés explosifs et musicalité éditoriale.",
        "years_experience": 11,
        "featured": True,
        "is_new": True,
        "location": "Paris",
        "travel_ready": True,
        "portrait_image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80",
        "spoken_languages": ["Francais", "Anglais"],
        "performance_resume": [
            {"period": "2025", "production": "Nocturne Couture", "venue": "Grand Palais Ephemere", "role": "Solo d'ouverture"},
            {"period": "2024", "production": "Maison Lumiere", "venue": "Hotel Salomon de Rothschild", "role": "Performance signature"},
            {"period": "2023", "production": "Pulse Residency", "venue": "La Seine Musicale", "role": "Artiste residente"},
        ],
        "hero_video_url": "https://cdn.coverr.co/videos/coverr-ballerina-warming-up-1562833129043?download=1080p",
        "teaser_video_url": "https://cdn.coverr.co/videos/coverr-contemporary-dance-performance-1562833133577?download=1080p",
        "media_assets": [
            {"asset_type": "image", "title": "Portrait editorial", "url": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=1200&q=80", "thumbnail_url": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=600&q=80", "alt_text": "Portrait d'Ambre Lenoir en posture choregraphique"},
            {"asset_type": "image", "title": "Scene gala", "url": "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=1200&q=80", "thumbnail_url": "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=600&q=80", "alt_text": "Ambre Lenoir sur une scene de gala"},
            {"asset_type": "video", "title": "Showreel", "url": "https://cdn.coverr.co/videos/coverr-female-dancer-performing-1560260224327?download=1080p", "thumbnail_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?auto=format&fit=crop&w=600&q=80", "alt_text": "Apercu video d'Ambre Lenoir"},
        ],
    },
    {
        "slug": "celeste-aerienne",
        "name": "Celeste Moreau",
        "headline": "Une danse aerienne fluide pour les salles monumentales, les dines de prestige et les lancements immersifs.",
        "discipline": "Danse aerienne",
        "group_size": "Solo",
        "mood": "Ethere",
        "venue_type": "Hotel ballroom",
        "technical_requirements": {"rigging": True, "min_ceiling_height_m": 8, "power": "1x 13A"},
        "bio": "Celeste melange suspension, souplesse et lenteur dramatique dans des tableaux aeriens conçus pour les architectures spectaculaires.",
        "years_experience": 9,
        "featured": True,
        "is_new": False,
        "location": "Lyon",
        "travel_ready": True,
        "portrait_image_url": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=900&q=80",
        "spoken_languages": ["Francais", "Anglais", "Espagnol"],
        "performance_resume": [
            {"period": "2025", "production": "Constellation Bleue", "venue": "Opera de Lyon", "role": "Solo aerien"},
            {"period": "2024", "production": "Le Bal Suspendu", "venue": "InterContinental Marseille", "role": "Performance de diner"},
            {"period": "2023", "production": "Aura", "venue": "Musee des Confluences", "role": "Creation immersive"},
        ],
        "hero_video_url": "https://cdn.coverr.co/videos/coverr-gymnast-training-in-studio-1579988943555?download=1080p",
        "teaser_video_url": "https://cdn.coverr.co/videos/coverr-swinging-from-aerial-silk-1572458909737?download=1080p",
        "media_assets": [
            {"asset_type": "image", "title": "Portrait en hauteur", "url": "https://images.unsplash.com/photo-1521334884684-d80222895322?auto=format&fit=crop&w=1200&q=80", "thumbnail_url": "https://images.unsplash.com/photo-1521334884684-d80222895322?auto=format&fit=crop&w=600&q=80", "alt_text": "Celeste Moreau en suspension"},
            {"asset_type": "image", "title": "Rubans aeriens", "url": "https://images.unsplash.com/photo-1515169067868-5387ec356754?auto=format&fit=crop&w=1200&q=80", "thumbnail_url": "https://images.unsplash.com/photo-1515169067868-5387ec356754?auto=format&fit=crop&w=600&q=80", "alt_text": "Danse aerienne en rubans"},
            {"asset_type": "video", "title": "Extrait suspendu", "url": "https://cdn.coverr.co/videos/coverr-aerial-silks-1578393576073?download=1080p", "thumbnail_url": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=600&q=80", "alt_text": "Video de Celeste Moreau en danse aerienne"},
        ],
    },
    {
        "slug": "santiago-salsa",
        "name": "Santiago Rivera",
        "headline": "Une salsa scénique brillante pour les soirees festives, les marques premium et les publics participatifs.",
        "discipline": "Danse salsa",
        "group_size": "Solo",
        "mood": "Festif",
        "venue_type": "Festival",
        "technical_requirements": {"floor": "Parquet ou plateau lisse", "power": "Playback stereo", "rigging": False},
        "bio": "Santiago fait monter l'energie avec une salsa virtuose, des interactions public mesurées et une elegance scénique taillée pour les grands temps forts.",
        "years_experience": 14,
        "featured": True,
        "is_new": False,
        "location": "Bordeaux",
        "travel_ready": True,
        "portrait_image_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=900&q=80",
        "spoken_languages": ["Espagnol", "Francais", "Anglais"],
        "performance_resume": [
            {"period": "2025", "production": "Soleil Latino", "venue": "Palais de la Bourse", "role": "Finale salsa"},
            {"period": "2024", "production": "Nuit Havana Club", "venue": "Les Bassins des Lumieres", "role": "Performance immersive"},
            {"period": "2023", "production": "Ritmo Vivo", "venue": "Casino Barriere", "role": "Tete d'affiche"},
        ],
        "hero_video_url": "https://cdn.coverr.co/videos/coverr-couple-dancing-1594311604990?download=1080p",
        "teaser_video_url": "https://cdn.coverr.co/videos/coverr-dance-1574888719139?download=1080p",
        "media_assets": [
            {"asset_type": "image", "title": "Portrait scene", "url": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=1200&q=80", "thumbnail_url": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=600&q=80", "alt_text": "Portrait de Santiago Rivera"},
            {"asset_type": "image", "title": "Soiree salsa", "url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=80", "thumbnail_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80", "alt_text": "Santiago Rivera en performance salsa"},
            {"asset_type": "video", "title": "Showreel salsa", "url": "https://cdn.coverr.co/videos/coverr-dancing-people-1571753457233?download=1080p", "thumbnail_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80", "alt_text": "Video salsa de Santiago Rivera"},
        ],
    },
]

SEEDED_USERS = [
    {"username": settings.first_superuser_username, "email": settings.first_superuser_email, "full_name": "AB Agency Admin", "password": settings.first_superuser_password, "role": UserRole.ADMIN, "artist_slug": None},
    {"username": "ambre", "email": "ambre@ab-agency.com", "full_name": "Ambre Lenoir", "password": "pass123", "role": UserRole.CLIENT, "artist_slug": "ambre-acrobatique"},
    {"username": "celeste", "email": "celeste@ab-agency.com", "full_name": "Celeste Moreau", "password": "pass123", "role": UserRole.CLIENT, "artist_slug": "celeste-aerienne"},
    {"username": "santiago", "email": "santiago@ab-agency.com", "full_name": "Santiago Rivera", "password": "pass123", "role": UserRole.CLIENT, "artist_slug": "santiago-salsa"},
]

SEEDED_SERVICES = [
    {"slug": "representation", "title": "Representation artistique", "summary": "Une selection de talents de haut niveau pour les evenements decisifs.", "body": "AB Agency represente des artistes d'exception en aerien, acrobatique et performance immersive."},
    {"slug": "production-support", "title": "Pilotage de production", "summary": "Planification technique et coordination d'exploitation.", "body": "Nous transformons une ambition artistique en dispositif fiable, securise et executable."},
    {"slug": "creative-consulting", "title": "Conseil creatif", "summary": "Conception de moments spectaculaires et memorables.", "body": "Nous aidons les clients a construire des concepts de performance sur mesure avec une vision claire de la production."},
]


def upsert_artist(db, payload: dict) -> Artist:
    artist = db.scalar(select(Artist).where(Artist.slug == payload["slug"]))
    artist_fields = {key: value for key, value in payload.items() if key != "media_assets"}
    if artist is None:
        artist = Artist(**artist_fields)
        db.add(artist)
        db.flush()
    else:
        for key, value in artist_fields.items():
            setattr(artist, key, value)

    artist.media_assets.clear()
    for asset in payload.get("media_assets", []):
        artist.media_assets.append(MediaAsset(**asset))
    return artist


def upsert_user(db, payload: dict, artists_by_slug: dict[str, Artist]) -> User:
    user = db.scalar(select(User).where(or_(User.username == payload["username"], User.email == payload["email"])))
    artist = artists_by_slug.get(payload["artist_slug"]) if payload.get("artist_slug") else None
    if user is None:
        user = User(
            username=payload["username"],
            email=payload["email"],
            full_name=payload["full_name"],
            hashed_password=get_password_hash(payload["password"]),
            role=payload["role"],
            is_active=True,
            artist_id=artist.id if artist else None,
        )
        db.add(user)
        return user

    user.username = payload["username"]
    user.email = payload["email"]
    user.full_name = payload["full_name"]
    user.hashed_password = get_password_hash(payload["password"])
    user.role = payload["role"]
    user.is_active = True
    user.artist_id = artist.id if artist else None
    return user


def upsert_service_page(db, payload: dict) -> ServicePage:
    page = db.scalar(select(ServicePage).where(ServicePage.slug == payload["slug"]))
    if page is None:
        page = ServicePage(**payload)
        db.add(page)
        return page

    page.title = payload["title"]
    page.summary = payload["summary"]
    page.body = payload["body"]
    return page


def seed_database(db) -> None:
    artists_by_slug = {}
    for artist_payload in SEEDED_ARTISTS:
        artist = upsert_artist(db, artist_payload)
        artists_by_slug[artist.slug] = artist

    for service_payload in SEEDED_SERVICES:
        upsert_service_page(db, service_payload)

    db.flush()

    for user_payload in SEEDED_USERS:
        upsert_user(db, user_payload, artists_by_slug)

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
