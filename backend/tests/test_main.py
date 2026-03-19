from fastapi.testclient import TestClient

from app.main import create_application


def test_health_endpoint_returns_ok(db_session):
    app = create_application(testing=True)

    from app.api.deps import get_db

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}