def test_list_artists_returns_seeded_artists(client):
    response = client.get("/api/artists")

    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_get_artist_by_slug(client):
    response = client.get("/api/artists/ambre-acrobatique")

    assert response.status_code == 200
    assert response.json()["name"] == "Ambre Lenoir"
    assert response.json()["media_assets"]


def test_get_my_artist_profile_returns_linked_artist(client):
    login = client.post("/api/auth/login", json={"username": "celeste", "password": "pass123"})
    token = login.json()["access_token"]

    response = client.get("/api/artists/me/profile", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["user"]["username"] == "celeste"
    assert response.json()["artist"]["slug"] == "celeste-aerienne"


def test_create_artist_requires_staff(client, auth_headers):
    response = client.post(
        "/api/artists",
        headers=auth_headers,
        json={
            "slug": "sky-arc",
            "name": "Sky Arc",
            "headline": "Contemporary aerial harness trio.",
            "discipline": "Aerial",
            "group_size": "Trio",
            "mood": "Romantic",
            "venue_type": "Theater",
            "technical_requirements": {"rigging": True},
            "bio": "A suspended trio for immersive gala reveals.",
            "years_experience": 6,
            "featured": False,
            "is_new": True,
            "location": "Paris",
            "travel_ready": True,
            "portrait_image_url": None,
            "spoken_languages": ["Francais"],
            "performance_resume": [],
            "hero_video_url": None,
            "teaser_video_url": None
        },
    )

    assert response.status_code == 200
    assert response.json()["slug"] == "sky-arc"