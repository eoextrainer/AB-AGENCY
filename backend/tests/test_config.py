from app.core.config import get_settings, settings


def test_get_settings_is_cached():
    assert get_settings() is get_settings()


def test_default_settings_values_are_exposed():
    assert settings.app_name == "AB Agency API"
    assert settings.api_prefix == "/api"
    assert settings.docs_enabled is True