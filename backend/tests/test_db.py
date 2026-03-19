from sqlalchemy import inspect

from app.db import create_db_engine, create_session_factory


def test_create_db_engine_supports_sqlite():
    engine = create_db_engine("sqlite://")

    assert str(engine.url) == "sqlite://"


def test_create_session_factory_binds_to_engine(db_session):
    inspector = inspect(db_session.bind)

    assert "artists" in inspector.get_table_names()
    assert create_session_factory(db_session.bind) is not None