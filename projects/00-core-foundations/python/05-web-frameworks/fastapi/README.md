# FastAPI Tutorial — GeeksforGeeks Series

25 complete, working FastAPI exercise scripts covering the full framework from basics to production patterns.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] httpx jinja2 aiofiles sqlalchemy pydantic[email]

# Run any script
uvicorn 01-introduction:app --reload
```

## Exercises

| # | File | Topic | Description |
|---|------|-------|-------------|
| 01 | `01-introduction.py` | Introduction | FastAPI basics, path operations, JSON responses |
| 02 | `02-getting-started.py` | Getting Started | CRUD operations, Pydantic models, status codes |
| 03 | `03-path-parameters.py` | Path Parameters | Type conversion, enums, Path() validation, UUIDs |
| 04 | `04-query-parameters.py` | Query Parameters | Defaults, validation, pagination, filtering |
| 05 | `05-request-body.py` | Request Body | Pydantic models, nested models, partial updates |
| 06 | `06-response-model.py` | Response Models | Filtering, exclude_unset, exclude_none, security |
| 07 | `07-form-data.py` | Form Data | HTML forms, Form() fields, validation |
| 08 | `08-file-upload.py` | File Upload | UploadFile, multiple files, streaming, validation |
| 09 | `09-dependency-injection.py` | Dependency Injection | Depends(), class deps, yield deps, overrides |
| 10 | `10-middleware.py` | Middleware | Request ID, timing, logging, CORS, security headers |
| 11 | `11-background-tasks.py` | Background Tasks | BackgroundTasks, email simulation, async jobs |
| 12 | `12-security.py` | Security | Password hashing, API keys, OAuth2 basics |
| 13 | `13-jwt-auth.py` | JWT Authentication | Access/refresh tokens, token rotation, blacklisting |
| 14 | `14-oauth2.py` | OAuth2 | Password grant, authorization code flow, scopes |
| 15 | `15-websockets.py` | WebSockets | Echo, chat rooms, DMs, connection management |
| 16 | `16-templates.py` | Templates | Jinja2 rendering, dynamic pages, server-side HTML |
| 17 | `17-static-files.py` | Static Files | Mount directories, FileResponse, streaming |
| 18 | `18-database.py` | Database | SQLAlchemy CRUD, sessions, SQLite |
| 19 | `19-orm.py` | ORM Relationships | One-to-many, JOINs, aggregations, complex queries |
| 20 | `20-testing.py` | Testing | TestClient, parameterized tests, dependency overrides |
| 21 | `21-async.py` | Async/Await | Concurrency, asyncio.gather, async HTTP, streaming |
| 22 | `22-cors.py` | CORS | CORSMiddleware, preflight, dynamic CORS |
| 23 | `23-exception-handling.py` | Exception Handling | Custom exceptions, handlers, error responses |
| 24 | `24-api-router.py` | APIRouter | Modular routing, tags, router-level dependencies |
| 25 | `25-events.py` | Lifespan Events | Startup/shutdown, resource management, app state |

## How to Use

Each file is self-contained. Run any exercise independently:

```bash
# Example: Run the JWT authentication exercise
uvicorn 13-jwt-auth:app --reload

# Open interactive docs
# http://127.0.0.1:8000/docs
```

Every file includes curl commands in comments at the bottom for testing from the terminal.

## Testing

```bash
# Run the testing exercise
pytest 20-testing.py -v

# Run smoke tests directly
python 20-testing.py
```

## Key Concepts Covered

- **Pydantic**: Data validation and serialization
- **Path Operations**: GET, POST, PUT, PATCH, DELETE
- **Dependency Injection**: Reusable logic, auth, DB sessions
- **Middleware**: Request/response processing pipeline
- **Async**: Non-blocking I/O, concurrency patterns
- **Security**: JWT, OAuth2, password hashing
- **Database**: SQLAlchemy ORM, relationships, queries
- **WebSockets**: Real-time communication
- **Testing**: TestClient, fixtures, dependency overrides

## Beyond the 25 core scripts

Topics 26–52 live in their own directories (`NN-topic-name/`), each with a
lecture, glossary, and runnable demo (`python NN-topic.py --verify`). The
first topic with a full 3-tier challenge set (per
[`../../PRACTICE_SPEC.md`](../../PRACTICE_SPEC.md)) is:

- **36 — Streaming and SSE** → [`challenges/36-streaming-and-sse/`](challenges/36-streaming-and-sse/README.md)
  (Bronze/Silver/Gold + quiz) and a DevMate bridge task in
  [`36-streaming-and-sse/devmate-task.md`](36-streaming-and-sse/devmate-task.md).
