"""Gemini-backed AI co-pilot service.

Public API used by routes:
  - build_project_context(project) -> str
  - generate(history, persona_prompt, context) -> AIResult
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

from flask import current_app

log = logging.getLogger(__name__)

MAX_HISTORY = 20
MAX_HISTORY_CHARS = 12000
MAX_CONTEXT_CHARS = 12000
MAX_NOTE_CHARS = 4000

DEFAULT_SYSTEM = (
    "You are a helpful, concise creative co-pilot. "
    "Give clear, concrete suggestions and keep answers focused."
)

BASE_RULES = (
    "You are the AI co-pilot inside Bigtree.ai, a creative collaboration workspace. "
    "Use the project context below when it is relevant. If the answer is not in the "
    "context, say so rather than inventing details about the project."
)


@dataclass(frozen=True)
class AIResult:
    """ok=False means the provider failed or is not configured — do not save as a reply."""

    text: str
    ok: bool = True


def _note_sort_key(note):
    ts = getattr(note, "updated_at", None) or getattr(note, "created_at", None)
    if isinstance(ts, datetime):
        return ts
    return datetime.min


def build_project_context(project) -> str:
    parts = [f"Project title: {project.title}"]
    if getattr(project, "description", None):
        parts.append(f"Project description: {project.description}")

    used = sum(len(p) for p in parts)

    notes = list(getattr(project, "notes", []) or [])
    # Newest first so the most relevant material fits in the budget.
    notes.sort(key=_note_sort_key, reverse=True)

    for note in notes:
        body = note.body or ""
        if len(body) > MAX_NOTE_CHARS:
            body = body[:MAX_NOTE_CHARS] + "\n[truncated]"
        chunk = f"\n## Note: {note.title}\n{body}"
        if used + len(chunk) > MAX_CONTEXT_CHARS:
            # Try a shorter truncated form of this note so it is not dropped entirely.
            room = MAX_CONTEXT_CHARS - used - len(f"\n## Note: {note.title}\n") - len("\n[truncated]")
            if room > 200:
                body = (note.body or "")[:room] + "\n[truncated]"
                chunk = f"\n## Note: {note.title}\n{body}"
                parts.append(chunk)
                used += len(chunk)
            break
        parts.append(chunk)
        used += len(chunk)

    files = getattr(project, "files", []) or []
    if files:
        names = ", ".join(f.filename for f in files[:30])
        file_line = f"\nFiles in this project: {names}"
        if used + len(file_line) <= MAX_CONTEXT_CHARS + 300:
            parts.append(file_line)

    return "\n".join(parts)


def _trim_history(history):
    """Keep the latest turns within count/char budgets; history must start with user."""
    if not history:
        return []

    # Drop leading assistant turns so the prompt starts with a user message.
    start = 0
    for i, (role, _) in enumerate(history):
        if role == "user":
            start = i
            break
    else:
        return []

    trimmed = list(history[start:])

    # Prefer the newest messages within MAX_HISTORY.
    if len(trimmed) > MAX_HISTORY:
        trimmed = trimmed[-MAX_HISTORY:]
        # Ensure we still start on a user turn after slicing.
        for i, (role, _) in enumerate(trimmed):
            if role == "user":
                trimmed = trimmed[i:]
                break

    # Enforce character budget from the end (keep latest).
    total = 0
    kept = []
    for role, text in reversed(trimmed):
        total += len(text)
        if total > MAX_HISTORY_CHARS and kept:
            break
        kept.append((role, text))
    kept.reverse()

    # Final guard: start with user.
    for i, (role, _) in enumerate(kept):
        if role == "user":
            return kept[i:]
    return []


def generate(history, persona_prompt, context) -> AIResult:
    """history: list of (role, text) with role 'user' or 'assistant'."""
    api_key = (current_app.config.get("GEMINI_API_KEY") or "").strip()
    if not api_key:
        return AIResult(
            "The AI co-pilot isn't configured yet. Add GEMINI_API_KEY to your "
            ".env file and restart the server.",
            ok=False,
        )

    system = "\n\n".join(
        [
            persona_prompt or DEFAULT_SYSTEM,
            BASE_RULES,
            "Project context:\n" + (context or ""),
        ]
    )
    history = _trim_history(history)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        contents = [
            types.Content(
                role="user" if role == "user" else "model",
                parts=[types.Part.from_text(text=text)],
            )
            for role, text in history
        ]
        response = client.models.generate_content(
            model=current_app.config.get("GEMINI_MODEL", "gemini-3.8-flash"),
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system),
        )
        text = (getattr(response, "text", None) or "").strip()
        if not text:
            return AIResult(
                "I couldn't generate a response. Try rephrasing your message.",
                ok=False,
            )
        return AIResult(text, ok=True)
    except Exception:
        log.exception("AI generation failed")
        return AIResult(
            "Something went wrong while contacting the AI service. Please try again.",
            ok=False,
        )


def generate_reply(history, persona_prompt, context) -> str:
    """Backward-compatible helper used by older unit tests."""
    return generate(history, persona_prompt, context).text
