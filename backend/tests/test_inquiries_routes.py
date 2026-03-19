from app.api.routes.inquiries import score_lead
from app.schemas import InquiryCreate


def test_score_lead_rewards_high_value_requests():
    payload = InquiryCreate(
        company_name="Acme",
        contact_name="Jordan",
        email="jordan@example.com",
        event_type="festival",
        location="London",
        venue_type="indoor",
        ceiling_height_meters=9,
        budget_max=15000,
        preferred_artist_slugs=["luna-silk-duo"],
        message="Need a hero act",
    )

    assert score_lead(payload) == 100


def test_create_inquiry_persists_request(client):
    response = client.post(
        "/api/inquiries",
        json={
            "company_name": "Acme Events",
            "contact_name": "Jordan Vale",
            "email": "jordan@example.com",
            "event_type": "festival",
            "event_date": "2026-07-12T18:00:00",
            "location": "London",
            "venue_type": "indoor",
            "budget_min": 6000,
            "budget_max": 12000,
            "preferred_disciplines": ["Aerial", "Duo"],
            "preferred_artist_slugs": ["luna-silk-duo"],
            "message": "Looking for a headline act"
        },
    )

    assert response.status_code == 200
    assert response.json()["lead_score"] >= 80
    assert response.json()["budget_min"] == "6000.00"
    assert response.json()["preferred_disciplines"] == ["Aerial", "Duo"]


def test_list_inquiries_requires_staff(client, auth_headers, sample_inquiry):
    response = client.get("/api/inquiries", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()[0]["company_name"]