cat > README.md << 'EOF'
# BigTree.ai

Creative collaboration workspace: projects, real-time team chat, and a project-aware AI co-pilot.

## Stack

| Layer     | Tech                                      |
|-----------|-------------------------------------------|
| Frontend  | React (Vite), Redux Toolkit, React Router |
| Backend   | Flask, SQLAlchemy, Flask-JWT-Extended, SocketIO |
| Database  | PostgreSQL (or SQLite for local dev)      |
| AI        | Google Gemini                             |

## Quick start

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then set GEMINI_API_KEY (and optional DATABASE_URL)