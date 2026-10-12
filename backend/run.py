from app import create_app
from app.config import is_production
from app.extensions import socketio

app = create_app()

if __name__ == "__main__":
    # Local development server only. In production use gunicorn (see Procfile).
    socketio.run(app, debug=not is_production(), port=5000)
