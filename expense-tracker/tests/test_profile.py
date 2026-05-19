def test_profile_redirects_when_not_logged_in(client):
    response = client.get("/profile", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_profile_renders_when_logged_in(client):
    client.post("/login", data={"email": "user@test.com", "password": "password123"})
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Test User" in response.data
    assert b"user@test.com" in response.data


def test_profile_shows_member_since(client):
    client.post("/login", data={"email": "user@test.com", "password": "password123"})
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Member since" in response.data


def test_profile_contains_logout_link(client):
    client.post("/login", data={"email": "user@test.com", "password": "password123"})
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"/logout" in response.data
