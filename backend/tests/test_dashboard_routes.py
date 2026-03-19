def test_dashboard_stats_aggregates_database_state(client, auth_headers, sample_inquiry):
    response = client.get("/api/dashboard/stats", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["total_artists"] >= 2
    assert body["open_inquiries"] >= 1
    assert body["average_lead_score"] >= 0