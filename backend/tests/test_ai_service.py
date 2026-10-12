from unittest.mock import MagicMock, patch

from app.services import ai_service
from app.services.ai_service import AIResult


def test_generate_reply_without_api_key(app):
    with app.app_context():
        app.config["GEMINI_API_KEY"] = ""
        result = ai_service.generate(
            [("user", "Hello")],
            "You are helpful.",
            "Project title: Demo",
        )
    assert isinstance(result, AIResult)
    assert result.ok is False
    assert "isn't configured" in result.text or "GEMINI_API_KEY" in result.text


def test_generate_reply_mocked(app):
    class FakeResp:
        text = "Mocked answer"

    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = FakeResp()

    with app.app_context():
        app.config["GEMINI_API_KEY"] = "fake-key-for-test"
        app.config["GEMINI_MODEL"] = "gemini-3.8-flash"
        with patch("google.genai.Client", return_value=fake_client):
            result = ai_service.generate(
                [("user", "Hi")],
                "System",
                "Context",
            )
    assert result.ok is True
    assert result.text == "Mocked answer"
