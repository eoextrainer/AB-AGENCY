def test_create_booking_requires_staff_and_returns_record(client, auth_headers, sample_inquiry):
    response = client.post(
        "/api/bookings",
        headers=auth_headers,
        json={
            "inquiry_id": sample_inquiry.id,
            "artist_id": 1,
            "booking_date": "2026-07-12T18:00:00",
            "status": "confirmed",
            "fee_amount": 12000,
            "deposit_paid": True,
            "contract_url": "https://example.com/contracts/1",
            "production_notes": "Requires in-house rigger"
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "confirmed"


def test_list_bookings_returns_existing_records(client, auth_headers, sample_booking):
    response = client.get("/api/bookings", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == sample_booking.id