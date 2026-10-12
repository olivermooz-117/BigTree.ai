from unittest.mock import patch, MagicMock

from app.services import ai_service


def test_generate_reply_without_api_key(app):
    with app.app_context():
        app.config["GEMINI_API_KEY"] = ""
        text = ai_service.generate_reply(
            [("user", "Hello")],
            "You are helpful.",
            "Project title: Demo",
        )
    assert "isn't configured" in text or "GEMINI_API_KEY" in text


def test_generate_reply_mocked(app):
    class FakeResp:
        text = "Mocked answer"

    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = FakeResp()

    with app.app_context():
        app.config["GEMINI_API_KEY"] = "fake-key-for-test"
        app.config["GEMINI_MODEL"] = "gemini-3.8-flash"
        with patch("google.genai.Client", return_value=fake_client):
            text = ai_service.generate_reply(
                [("user", "Hi")],
                "System",
                "Context",
            )
    assert text == "Mocked answer"
