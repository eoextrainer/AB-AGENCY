# Runtime Notes

## Local services

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

## Commands

- Backend tests: `cd backend && .venv/bin/python -m pytest -q`
- Frontend tests: `cd frontend && npm test`
- Compose stack: `docker compose up --build`
- Local media optimization: `python scripts/media/optimize_media.py input.mov output-dir`