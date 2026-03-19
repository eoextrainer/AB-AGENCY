def test_public_homepage_returns_featured_content(client, service_titles):
    response = client.get("/api/public/homepage")

    assert response.status_code == 200
    body = response.json()
    assert body["hero_title"]
    assert body["featured_artists"]
    assert set(body["featured_services"]).issubset(set(service_titles))