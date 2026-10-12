from unittest.mock import patch

from app.services.ai_service import AIResult


def _project(client, headers):
    res = client.post("/projects", json={"title": "AI"}, headers=headers)
    assert res.status_code == 201
    return res.get_json()


def _chat(client, headers, project_id, message="hello", **extra):
    return client.post(
        f"/projects/{project_id}/ai/chat",
        json={"message": message, **extra},
        headers=headers,
    )


def test_chat_saves_history(client, auth_headers):
    p = _project(client, auth_headers)
    with patch("app.routes.ai.generate", return_value=AIResult("Hi there", True)):
        res = _chat(client, auth_headers, p["id"])
    assert res.status_code == 200
    body = res.get_json()
    assert body["reply"]["content"] == "Hi there"

    cid = body["conversation"]["id"]
    msgs = client.get(
        f"/projects/{p['id']}/ai/conversations/{cid}/messages", headers=auth_headers
    ).get_json()
    assert [m["role"] for m in msgs] == ["user", "assistant"]


def test_failed_generation_is_not_saved(client, auth_headers):
    p = _project(client, auth_headers)
    with patch(
        "app.routes.ai.generate", return_value=AIResult("The AI service is down", False)
    ):
        res = _chat(client, auth_headers, p["id"])
    assert res.status_code == 503
    assert res.get_json()["error"] == "The AI service is down"

    convos = client.get(
        f"/projects/{p['id']}/ai/conversations", headers=auth_headers
    ).get_json()
    assert convos == []


def test_rate_limit_per_minute(client, app, auth_headers):
    app.config["AI_RATE_LIMIT_PER_MINUTE"] = 2
    p = _project(client, auth_headers)
    with patch("app.routes.ai.generate", return_value=AIResult("ok", True)):
        assert _chat(client, auth_headers, p["id"]).status_code == 200
        assert _chat(client, auth_headers, p["id"]).status_code == 200
        third = _chat(client, auth_headers, p["id"])
    assert third.status_code == 429


def test_non_member_cannot_use_ai(client, auth_headers, second_user_headers):
    p = _project(client, auth_headers)
    res = _chat(client, second_user_headers, p["id"])
    assert res.status_code == 403


def test_overlong_message_rejected(client, auth_headers):
    p = _project(client, auth_headers)
    res = _chat(client, auth_headers, p["id"], message="x" * 4001)
    assert res.status_code == 422
