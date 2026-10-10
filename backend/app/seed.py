import click

from app.extensions import db
from app.models import User, Project, ProjectMember, Note, Task, Persona

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


def register_cli(app):
    @app.cli.command("seed")
    def seed():
        """Seed AI personas and a demo account."""
        for p in PERSONAS:
            if not Persona.query.filter_by(name=p["name"]).first():
                db.session.add(Persona(**p))

        if not User.query.filter_by(email="demo@bigtree.ai").first():
            user = User(name="Demo User", email="demo@bigtree.ai")
            user.set_password("Demo1234!")
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
        click.echo("Seeded personas and demo data (demo@bigtree.ai / Demo1234!).")
