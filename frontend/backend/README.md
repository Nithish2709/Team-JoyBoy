# PDS Sentinel AI - FastAPI Backend Scaffold

This repository contains the backend scaffolding for the **PDS Sentinel AI – Multi-Agent Intelligent Public Distribution Monitoring Platform** built using FastAPI, PostgreSQL, and Redis.

## Technical Specifications
- **Python**: 3.12+
- **Database**: PostgreSQL (SQLAlchemy 2.0 Asynchronous Client Engine with `asyncpg`)
- **Cache/Broker**: Redis (Asynchronous Pool Client)
- **Migrations**: Alembic Async
- **Containerization**: Docker & Docker Compose
- **Logging**: Centrally managed structured console and file outputs via Loguru.

---

## Folder Layout (Clean Architecture)
```
app/
 ├── api/           # Presentation Layer: versioned routers & endpoints
 ├── core/          # System utilities: config loaded via Pydantic settings & logs
 ├── config/        # Environment settings & parameters
 ├── db/            # Database configurations & client pool mappings
 ├── middleware/    # App middlewares: custom request timers & telemetry logs
 ├── models/        # Enterprise database mapping ORM entities (SQLAlchemy)
 ├── repositories/  # Abstracted queries and database CRUD helpers
 ├── schemas/       # Request and response data validators (Pydantic v2)
 ├── services/      # Core business rule transaction controllers
 ├── agents/        # Intelligent LLM/agent setups
 ├── workflows/     # Graph task structures (LangGraph)
 ├── state/         # Agent runtime shared context maps
 ├── utils/         # Base helpers & mathematical algorithms
 └── workers/       # Celery offline queue systems
```

---

## Setup & Execution

### 1. Environment Configurations
Copy `.env.example` to `.env` and adjust the variables:
```bash
cp .env.example .env
```

### 2. Run Native (Local Environment)

Install dependencies:
```bash
pip install -r requirements.txt
```

Launch the uvicorn development server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Swagger Docs API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc API**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. Run Containerized (Docker Compose)

Launch PostgreSQL, Redis, and Backend containers:
```bash
docker compose up -d --build
```

Monitor server logs:
```bash
docker compose logs -f backend
```

---

## Health Check Routes
- **General server status**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
- **PostgreSQL connectivity check**: [http://localhost:8000/api/v1/health/database](http://localhost:8000/api/v1/health/database)
- **Redis server ping validation**: [http://localhost:8000/api/v1/health/redis](http://localhost:8000/api/v1/health/redis)

---

## Testing

Execute async test cases locally via `pytest`:
```bash
pytest tests/
```
