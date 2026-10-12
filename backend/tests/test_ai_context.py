from datetime import datetime, timedelta
from types import SimpleNamespace as NS

from app.services import ai_service


def _note(title, body, minutes_ago):
    t = datetime(2026, 1, 1) - timedelta(minutes=minutes_ago)
    return NS(title=title, body=body, updated_at=t, created_at=t)


def _project(notes, files=()):
    return NS(
        title="Demo",
        description="Desc",
        notes=list(notes),
        files=[NS(filename=f) for f in files],
    )


def test_newest_notes_come_first():
    ctx = ai_service.build_project_context(
        _project([_note("Oldest note", "a", 60), _note("Newest note", "b", 1)])
    )
    assert ctx.index("Newest note") < ctx.index("Oldest note")


def test_big_note_is_truncated_not_dropped():
    ctx = ai_service.build_project_context(
        _project([_note("Big", "x" * 10000, 1), _note("Small", "tiny", 2)])
    )
    assert "[truncated]" in ctx
    assert "tiny" in ctx


def test_context_stays_within_budget():
    notes = [_note(f"N{i}", "y" * 5000, i) for i in range(10)]
    ctx = ai_service.build_project_context(_project(notes, files=["a.txt"]))
    assert len(ctx) <= ai_service.MAX_CONTEXT_CHARS + 300


def test_history_starts_with_user_and_keeps_latest():
    hist = [("assistant", "x"), ("user", "a"), ("assistant", "b"), ("user", "c")]
    out = ai_service._trim_history(hist)
    assert out[0][0] == "user"
    assert out[-1] == ("user", "c")


def test_history_respects_limits():
    hist = [("user" if i % 2 else "assistant", "y" * 1000) for i in range(40)]
    out = ai_service._trim_history(hist)
    assert len(out) <= ai_service.MAX_HISTORY
    assert sum(len(t) for _, t in out) <= ai_service.MAX_HISTORY_CHARS
    assert out[0][0] == "user"
