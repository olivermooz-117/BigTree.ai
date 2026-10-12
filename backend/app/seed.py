import os

import click

from app.config import is_production
from app.extensions import db
from app.models import User, Project, ProjectMember, Note, Task, Persona

DEMO_EMAIL = "demo@bigtree.ai"
DEV_DEMO_PASSWORD = "Demo1234!"

PERSONAS = [
    dict(
        name="Co-pilot",
        description="Balanced, helpful creative partner",
        system_prompt=(
            "You are a friendly, practical creative co-pilot. Give clear, concrete "
            "suggestions and keep answers focused."
        ),
        is_default=True,
    ),
    dict(
        name="Editor",
        description="Tightens and improves your writing",
        system_prompt=(
            "You are a sharp, supportive editor. Improve clarity, structure and tone. "
            "Point out what to cut, and show a revised version when helpful."
        ),
    ),
    dict(
        name="Hype Coach",
        description="High-energy motivation and ideas",
        system_prompt=(
            "You are an upbeat hype coach for creatives. Be energetic and encouraging, "
            "and always end with one concrete next action."
        ),
    ),
    dict(
        name="Strict Critic",
        description="Honest, direct feedback",
        system_prompt=(
            "You are a strict but fair critic. Give honest, specific feedback on "
            "weaknesses first, then strengths. No flattery."
        ),
    ),
]


def _seed_personas():
    created = 0
    for p in PERSONAS:
        if not Persona.query.filter_by(name=p["name"]).first():
            db.session.add(Persona(**p))
            created += 1
    db.session.commit()
    return created


def _demo_password():
    configured = os.getenv("DEMO_PASSWORD", "").strip()
    if is_production():
        allowed = os.getenv("ALLOW_DEMO_SEED", "").strip().lower() in ("1", "true", "yes")
        if not allowed:
            raise click.ClickException(
                "Demo seeding is disabled in production. Set ALLOW_DEMO_SEED=true "
                "and DEMO_PASSWORD to enable it deliberately."
            )
        if len(configured) < 12:
            raise click.ClickException(
                "Set DEMO_PASSWORD (12+ characters) to seed the demo account in production."
            )
        return configured
    return configured or DEV_DEMO_PASSWORD


def register_cli(app):
    @app.cli.command("seed")
    def seed():
        """Seed the AI personas the app needs to run (safe in production)."""
        created = _seed_personas()
        click.echo(f"Seeded {created} new persona(s).")

    @app.cli.command("seed-demo")
    def seed_demo():
        """Seed a demo account and sample project (opt-in; blocked in production)."""
        password = _demo_password()
        _seed_personas()

        if User.query.filter_by(email=DEMO_EMAIL).first():
            click.echo("Demo account already exists; nothing to do.")
            return

        user = User(name="Demo User", email=DEMO_EMAIL)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        project = Project(
            title="Album Launch Plan",
            description="Planning the release of a debut EP.",
            owner_id=user.id,
        )
        project.members.append(ProjectMember(user_id=user.id, role="owner"))
        db.session.add(project)
        db.session.flush()

        db.session.add_all(
            [
                Note(
                    project_id=project.id,
                    author_id=user.id,
                    title="Release vision",
                    body=(
                        "Five-track EP, warm analog sound, release in spring. "
                        "Single drops three weeks before the full EP."
                    ),
                ),
                Task(project_id=project.id, title="Book mastering session"),
                Task(
                    project_id=project.id,
                    title="Design cover art brief",
                    status="doing",
                ),
            ]
        )
        db.session.commit()
        if is_production():
            click.echo(f"Seeded demo account {DEMO_EMAIL}.")
        else:
            click.echo(f"Seeded demo account ({DEMO_EMAIL} / {password}).")
