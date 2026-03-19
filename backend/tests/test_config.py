from app.core.config import Settings, get_settings, settings


def test_production_requires_non_default_seed_passwords():
    try:
        Settings(environment="production")
    except ValueError as exc:
        assert "FIRST_SUPERUSER_PASSWORD" in str(exc)
        assert "ARTIST_AMBRE_PASSWORD" in str(exc)
        return

    raise AssertionError("Production settings should reject default seeded passwords")


def test_production_accepts_custom_seed_passwords():
    configured_settings = Settings(
        environment="production",
        first_superuser_password="Admin!2026Secure",
        artist_ambre_password="Ambre!2026Secure",
        artist_celeste_password="Celeste!2026Secure",
        artist_santiago_password="Santiago!2026Secure",
    )

    assert configured_settings.environment == "production"


def test_get_settings_is_cached():
    assert get_settings() is get_settings()


def test_default_settings_values_are_exposed():
    assert settings.app_name == "AB Agency API"
    assert settings.api_prefix == "/api"
    assert settings.docs_enabled is True