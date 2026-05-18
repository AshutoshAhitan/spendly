def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign in" in response.data


def test_login_valid_credentials_redirects_to_profile(client):
    response = client.post(
        "/login",
        data={"email": "user@test.com", "password": "password123"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/profile")


def test_login_sets_session_user_id(client):
    client.post(
        "/login",
        data={"email": "user@test.com", "password": "password123"},
    )
    with client.session_transaction() as sess:
        assert "user_id" in sess
        assert sess["user_name"] == "Test User"


def test_login_wrong_password_shows_error(client):
    response = client.post(
        "/login",
        data={"email": "user@test.com", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid email or password." in response.data


def test_login_unknown_email_shows_error(client):
    response = client.post(
        "/login",
        data={"email": "nobody@test.com", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid email or password." in response.data


def test_login_empty_email_shows_error(client):
    response = client.post(
        "/login",
        data={"email": "", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid email or password." in response.data


def test_login_empty_password_shows_error(client):
    response = client.post(
        "/login",
        data={"email": "user@test.com", "password": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid email or password." in response.data


def test_login_email_sticky_on_failure(client):
    response = client.post(
        "/login",
        data={"email": "user@test.com", "password": "wrongpass"},
        follow_redirects=True,
    )
    assert b"user@test.com" in response.data


def test_logout_clears_session_and_redirects(client):
    client.post(
        "/login",
        data={"email": "user@test.com", "password": "password123"},
    )
    with client.session_transaction() as sess:
        assert "user_id" in sess

    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_logout_without_login_still_redirects(client):
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
