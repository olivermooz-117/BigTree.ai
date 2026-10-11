def test_register_and_me(client):
    res = client.post(
        "/auth/register",
        json={"name": "Ada", "email": "ada@example.com", "password": "password123"},
    )
    assert res.status_code == 201
    data = res.get_json()
    assert "access_token" in data
    assert data["user"]["email"] == "ada@example.com"

    me = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {data['access_token']}"},
    )
    assert me.status_code == 200
    assert me.get_json()["name"] == "Ada"


def test_register_duplicate_email(client):
    payload = {"name": "A", "email": "dup@example.com", "password": "password123"}
    assert client.post("/auth/register", json=payload).status_code == 201
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 409


def test_login_ok_and_bad(client):
    client.post(
        "/auth/register",
        json={"name": "B", "email": "b@example.com", "password": "password123"},
    )
    ok = client.post(
        "/auth/login",
        json={"email": "b@example.com", "password": "password123"},
    )
    assert ok.status_code == 200
    bad = client.post(
        "/auth/login",
        json={"email": "b@example.com", "password": "wrongpass1"},
    )
    assert bad.status_code == 401


def test_me_requires_auth(client):
    res = client.get("/auth/me")
    assert res.status_code == 401
