def _create_project(client, headers, title="P1"):
    res = client.post("/projects", json={"title": title}, headers=headers)
    assert res.status_code == 201
    return res.get_json()


def test_non_member_cannot_read_project(client, auth_headers, second_user_headers):
    project = _create_project(client, auth_headers)
    res = client.get(f"/projects/{project['id']}", headers=second_user_headers)
    assert res.status_code == 403


def test_member_can_read_after_invite(client, auth_headers, second_user_headers):
    project = _create_project(client, auth_headers)
    invite = client.post(
        f"/projects/{project['id']}/members",
        json={"email": "other@example.com", "role": "member"},
        headers=auth_headers,
    )
    assert invite.status_code == 201
    res = client.get(f"/projects/{project['id']}", headers=second_user_headers)
    assert res.status_code == 200
    assert res.get_json()["title"] == "P1"


def test_non_owner_cannot_delete(client, auth_headers, second_user_headers):
    project = _create_project(client, auth_headers)
    client.post(
        f"/projects/{project['id']}/members",
        json={"email": "other@example.com"},
        headers=auth_headers,
    )
    res = client.delete(f"/projects/{project['id']}", headers=second_user_headers)
    assert res.status_code == 403
