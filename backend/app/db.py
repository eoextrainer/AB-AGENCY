from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _engine_kwargs(database_url: str) -> dict:
    kwargs = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    return kwargs


def create_db_engine(database_url: str | None = None):
    return create_engine(database_url or settings.database_url, **_engine_kwargs(database_url or settings.database_url))


def create_session_factory(bind_engine=None):
    engine_to_use = bind_engine or engine
    return sessionmaker(bind=engine_to_use, autocommit=False, autoflush=False, class_=Session)


engine = create_db_engine()
SessionLocal = create_session_factory(engine)


def init_database(bind_engine=None) -> None:
    Base.metadata.create_all(bind=bind_engine or engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
