def test_create_availability_slot(client, auth_headers):
    response = client.post(
        "/api/availability",
        headers=auth_headers,
        json={
            "artist_id": 1,
            "start_date": "2026-09-01T10:00:00",
            "end_date": "2026-09-03T23:00:00",
            "status": "limited"
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "limited"


def test_filter_availability_by_artist(client, auth_headers):
    client.post(
        "/api/availability",
        headers=auth_headers,
        json={
            "artist_id": 1,
            "start_date": "2026-09-01T10:00:00",
            "end_date": "2026-09-03T23:00:00",
            "status": "available"
        },
    )

    response = client.get("/api/availability?artist_id=1", headers=auth_headers)

    assert response.status_code == 200
    assert all(slot["artist_id"] == 1 for slot in response.json())