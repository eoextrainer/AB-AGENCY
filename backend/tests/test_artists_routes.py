def test_list_artists_returns_seeded_artists(client):
    response = client.get("/api/artists")

    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_artist_by_slug(client):
    response = client.get("/api/artists/luna-silk-duo")

    assert response.status_code == 200
    assert response.json()["name"] == "Luna Silk Duo"


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
            "featured": False,
            "is_new": True,
            "location": "Paris",
            "travel_ready": True,
            "hero_video_url": None,
            "teaser_video_url": None
        },
    )

    assert response.status_code == 200
    assert response.json()["slug"] == "sky-arc"