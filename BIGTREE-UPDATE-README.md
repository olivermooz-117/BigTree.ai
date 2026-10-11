# BigTree.ai professional landing page update

This patch refreshes the public landing page, global design system, SEO metadata and backend CORS defaults.

## Files included

- `frontend/src/pages/Landing.jsx` — new responsive marketing page with product mockup, features, how-it-works section and calls to action.
- `frontend/src/index.css` — cohesive dark evergreen/lime design system and responsive styles. This replaces the existing stylesheet; review app-specific components after applying.
- `frontend/index.html` — SEO and social preview metadata.
- `backend/app/__init__.py` — restricts CORS and Socket.IO origins to configured origins.
- `backend/.env.example` — documents the new CORS setting and safer environment setup.

## Apply from the repository root

Unzip this archive into your existing repository folder and allow it to overwrite the listed files. Or use the terminal commands below after placing this ZIP in the repository root:

```bash
unzip -o bigtree-professional-update.zip -d .
```

Then configure `backend/.env` with `CORS_ORIGINS` set to the exact frontend origin(s). For local development:

```env
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

For production, use the deployed frontend URL(s), with no trailing slash. Do not deploy the example secrets; generate independent strong random values for `SECRET_KEY` and `JWT_SECRET_KEY`.

## Verify

Frontend:

```bash
cd frontend
npm ci
npm run build
```

Backend (from repository root, using your virtual environment):

```bash
cd backend
pytest
```

Start the backend and frontend using your existing project instructions.

## Important notes

- The landing page uses the existing `/register` and `/login` routes and does not require a new frontend dependency.
- The dashboard preview is illustrative UI, not a live dashboard embedded in the landing page.
- Google Fonts are loaded from Google Fonts when network access is available; fallback fonts are included.
- Before production deployment, confirm the exact deployed frontend origin is present in `CORS_ORIGINS`, test Socket.IO from that origin, and review file upload/storage, database migrations, logging and error handling.
- This patch does not claim that all backend features have been tested or that production deployment is complete.
