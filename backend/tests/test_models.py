from sqlalchemy import inspect

from app.models import Artist, MediaAsset


def test_artist_model_persists_seed_data(db_session):
    artist = db_session.query(Artist).filter(Artist.slug == "ambre-acrobatique").one()

    assert artist.featured is True
    assert artist.travel_ready is True
    assert artist.media_assets


def test_media_asset_uses_asset_metadata_column():
    mapper = inspect(MediaAsset)

    assert "asset_metadata" in mapper.columns
    assert "metadata" not in mapper.columns