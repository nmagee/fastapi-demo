# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Local (pipenv)
```bash
pipenv shell
pipenv install -r requirements.txt
fastapi run app/main.py          # dev server on port 8000
```

### Docker Compose (preferred)
```bash
docker compose build
docker compose up -d             # API on :8000, MongoDB on :27017
docker compose logs -f api       # tail logs
```

### Sample Data
```bash
python insert-one.py             # insert a single person record
python insert-many.py            # insert 10 sample student records
```

No linting or test framework is configured in this project.

## Architecture

Single-file FastAPI app (`app/main.py`) backed by MongoDB via PyMongo.

**Data model**: People records with `name`, `email`, and MongoDB `_id` (ObjectId). No Pydantic models — request bodies are parsed manually via `await request.json()`.

**MongoDB connection**: Established at module load time using env vars `MONGO_URI`, `MONGO_USERNAME`, `MONGO_PASSWORD`. Database: `nem2p`, collection: `people`.

**Routes**:
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Health check |
| GET | `/people` | List all people |
| POST | `/people` | Create a person (`{name, email}`) |
| GET | `/people/delete/{person_id}` | Delete by ObjectId |

CORS is configured permissively (`allow_origins=["*"]`).

## CI/CD

Two GitHub Actions workflows in `.github/workflows/` (note: `.zaml` extension, not `.yml`):
- `test-container.zaml` — builds image, tests `/` and `/docs` endpoints on every push
- `build.zaml` — builds multi-platform image (`linux/amd64`, `linux/arm64`) and pushes to GHCR after tests pass

## Docker

Production container runs `fastapi run` with 4 workers on port 80, mapped to host port 8000. Base image: `python:3.11-alpine3.20`.

The `docker-compose.yml` wires the API to MongoDB with credentials `admin/password` and a persistent volume `mongodb_data`.
