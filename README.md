# EstimateAI Backend

AI-powered construction takeoff and PDF estimation platform.

## Project Structure

```
estimate_ai_backend/
├── app/
│   ├── main.py
│   ├── core/           # config, database, security, logging, dependencies, constants
│   ├── shared/         # exceptions, response, pagination, enums
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic DTOs
│   ├── repositories/   # Data access layer
│   ├── services/       # Business logic
│   ├── api/v1/         # HTTP routers
│   ├── modules/        # PDF engine, viewer, AI, OCR, BOQ, jobs, etc.
│   ├── utils/          # File, image, PDF helpers
│   └── middleware/     # Logging, exception handlers
├── storage/            # original, thumbnails, previews, exports, temp
├── uploads/
├── tests/
├── alembic/
└── logs/
```

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

API: http://localhost:8000/docs

```bash
uvicorn app.main:app --reload
pytest -v
```

## API Routes (v1)

| Router | Prefix |
|--------|--------|
| auth_router | `/api/v1/auth` |
| user_router | `/api/v1/users` |
| project_router | `/api/v1/projects` |
| drawing_router | `/api/v1/drawings` |
| annotation_router | `/api/v1/annotations` |
| measurement_router | `/api/v1/measurements` |
| takeoff_router | `/api/v1/takeoffs` |
| ai_router | `/api/v1/ai` |
