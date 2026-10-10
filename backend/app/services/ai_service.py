import logging

from flask import current_app

log = logging.getLogger(__name__)

MAX_CONTEXT_CHARS = 12000
MAX_HISTORY = 20

DEFAULT_SYSTEM = (
    "You are a friendly, practical creative co-pilot. "
    "Give clear, concrete suggestions and keep answers focused."
)

BASE_RULES = (
    "You are the AI co-pilot inside Bigtree.ai, a creative collaboration workspace. "
    "Use the project context below when it is relevant. If the answer is not in the "
    "context, say so rather than inventing details about the project."
)


def build_project_context(project):
    parts = [f"Project title: {project.title}"]
    if project.description:
        parts.append(f"Project description: {project.description}")

    used = sum(len(p) for p in parts)
    for note in project.notes:
        chunk = f"\n## Note: {note.title}\n{note.body or ''}"
        if used + len(chunk) > MAX_CONTEXT_CHARS:
            break
        parts.append(chunk)
        used += len(chunk)

    if project.files:
        names = ", ".join(f.filename for f in project.files[:30])
        parts.append(f"\nFiles in this project: {names}")

    return "\n".join(parts)


def generate_reply(history, persona_prompt, context):
    """history: list of (role, text) tuples, role is 'user' or 'assistant'."""
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        return (
            "The AI co-pilot isn't configured yet. Add GEMINI_API_KEY to your "
            ".env file and restart the server."
        )

    system = "\n\n".join(
        [persona_prompt or DEFAULT_SYSTEM, BASE_RULES, "Project context:\n" + context]
    )

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        contents = [
            types.Content(
                role="user" if role == "user" else "model",
                parts=[types.Part.from_text(text=text)],
            )
            for role, text in history[-MAX_HISTORY:]
        ]
        response = client.models.generate_content(
            model=current_app.config.get("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system),
        )
        text = (response.text or "").strip()
        return text or "I couldn't generate a response. Try rephrasing your message."
    except Exception:
        log.exception("AI generation failed")
        return "Something went wrong while contacting the AI service. Please try again."
