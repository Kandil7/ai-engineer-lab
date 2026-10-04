# FastAPI Advanced Quiz

## Topic Overview
This quiz covers advanced FastAPI concepts including middleware, authentication, WebSockets, database integration, testing, and production deployment patterns. These topics are essential for building robust, scalable API applications.

**Difficulty:** Intermediate to Advanced
**Questions:** 20
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Medium]
**What is the purpose of middleware in FastAPI?**

A) To handle database connections
B) To process requests and responses before/after they reach the endpoint
C) To define API routes
D) To manage application state

**Correct Answer:** B
**Explanation:** Middleware intercepts every request and response, allowing you to add functionality like logging, authentication, CORS, compression, and error handling globally.

---

### Question 2 [Medium]
**How do you create custom middleware in FastAPI?**

A) By decorating a function with `@middleware`
B) By creating a class that implements `__call__` or using `@app.middleware("http")`
C) By inheriting from `BaseMiddleware`
D) By using `app.use()`

**Correct Answer:** B
**Explanation:** You can create middleware as a class with `__call__` or as a simple function decorated with `@app.middleware("http")`. Both approaches receive the request and call `call_next()`.

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

---

### Question 3 [Hard]
**Which dependency injection pattern allows sharing a database session across multiple endpoints?**

A) Using a module-level variable
B) Using a generator dependency with `yield`
C) Using global state
D) Using environment variables

**Correct Answer:** B
**Explanation:** Generator dependencies with `yield` are perfect for database sessions. The code before `yield` runs during setup (creating the session), and the code after `yield` runs during cleanup (closing the session).

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### Question 4 [Medium]
**How do you implement JWT authentication in FastAPI?**

A) Using built-in `@app.auth()` decorator
B) Using `HTTPBearer` with PyJWT or python-jose library
C) FastAPI has built-in JWT support
D) Using cookies only

**Correct Answer:** B
**Explanation:** FastAPI doesn't have built-in JWT. You typically use `HTTPBearer` or `OAuth2PasswordBearer` as a dependency with a library like `python-jose` or `PyJWT` to encode/decode tokens.

---

### Question 5 [Hard]
**What is the correct way to handle WebSocket connections?**

A) Using `@app.websocket("/ws")` decorator
B) Using `@app.get("/ws")` decorator
C) Using HTTP long-polling
D) WebSockets are not supported

**Correct Answer:** A
**Explanation:** FastAPI supports WebSockets natively with the `@app.websocket()` decorator. The endpoint function receives a `WebSocket` object and can use `await ws.accept()`, `await ws.send_text()`, and `await ws.receive_text()`.

---

### Question 6 [Medium]
**What is the purpose of `OAuth2PasswordBearer` in FastAPI?**

A) To encrypt passwords
B) To extract and validate Bearer tokens from the Authorization header
C) To hash passwords
D) To create OAuth2 applications

**Correct Answer:** B
**Explanation:** `OAuth2PasswordBearer` is a dependency that extracts the Bearer token from the Authorization header and makes it available for validation. It doesn't validate the token itself - you handle that logic.

---

### Question 7 [Hard]
**How do you test a FastAPI application?**

A) Using `TestClient` from `fastapi.testclient`
B) Using `requests` library against a running server
C) Using `httpx.AsyncClient` for async testing
D) Both A and C

**Correct Answer:** D
**Explanation:** `TestClient` (from Starlette) works for synchronous testing, while `httpx.AsyncClient` with `ASGITransport` works for async testing. Both are standard approaches in FastAPI.

```python
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

# Sync testing
client = TestClient(app)
response = client.get("/items/")

# Async testing
async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
    response = await ac.get("/items/")
```

---

### Question 8 [Medium]
**What does `app.include_router()` do?**

A) Adds middleware to the application
B) Mounts a sub-application at a specific path
C) Includes an APIRouter to add its endpoints to the main app
D) Configures database routing

**Correct Answer:** C
**Explanation:** `app.include_router()` integrates an `APIRouter` instance, adding all its defined endpoints to the main application. You can optionally prefix all routes with a path.

---

### Question 9 [Hard]
**How do you implement rate limiting in FastAPI?**

A) Using `@app.rate_limit()` decorator
B) Using middleware with a token bucket or sliding window algorithm
C) FastAPI has built-in rate limiting
D) Rate limiting is not possible

**Correct Answer:** B
**Explanation:** FastAPI doesn't have built-in rate limiting. You implement it via middleware or dependencies, typically using algorithms like token bucket, sliding window, or fixed window with Redis or in-memory storage.

---

### Question 10 [Medium]
**What is the purpose of `lifespan` in FastAPI?**

A) To limit application uptime
B) To handle startup and shutdown events
C) To set request timeout
D) To configure session duration

**Correct Answer:** B
**Explanation:** The `lifespan` context manager handles application startup and shutdown events. It replaced the older `@app.on_event("startup")` and `@app.on_event("shutdown")` decorators.

```python
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await connect_to_database()
    yield
    # Shutdown code
    await close_database_connection()


app = FastAPI(lifespan=lifespan)
```

---

### Question 11 [Hard]
**How do you implement background tasks that persist across application restarts?**

A) Using `BackgroundTasks`
B) Using Celery with Redis/RabbitMQ
C) Using threading
D) Using `time.sleep()`

**Correct Answer:** B
**Explanation:** `BackgroundTasks` only works during the request lifecycle. For persistent background tasks, use Celery, ARQ, or Dramatiq with a message broker like Redis or RabbitMQ.

---

### Question 12 [Medium]
**What is the purpose of `status` module in FastAPI?**

A) To check server health
B) To provide HTTP status code constants
C) To monitor application performance
D) To handle database status

**Correct Answer:** B
**Explanation:** The `status` module provides constants for HTTP status codes (e.g., `status.HTTP_200_OK`, `status.HTTP_404_NOT_FOUND`), making code more readable and maintainable.

---

### Question 13 [Hard]
**How do you handle multiple dependencies with the same parameter name?**

A) FastAPI automatically resolves naming conflicts
B) Use `alias` parameter in `Depends()`
C) You cannot have dependencies with same parameter names
D) Rename the function parameters

**Correct Answer:** B
**Explanation:** When multiple dependencies use the same parameter name, use `Depends(..., alias="custom_name")` or override the parameter in the endpoint function signature.

---

### Question 14 [Medium]
**What is the purpose of `Depends(use_cache=True)`?**

A) Caches the dependency result per request
B) Caches the dependency result globally
C) Disables the dependency
D) Caches HTTP responses

**Correct Answer:** A
**Explanation:** When `use_cache=True` (the default), if multiple places request the same dependency, FastAPI executes it only once per request and shares the result. Set to `False` to execute it multiple times.

---

### Question 15 [Hard]
**How do you implement WebSocket authentication?**

A) WebSocket connections don't support authentication
B) Pass the token as a query parameter or in the connection headers
C) Only use HTTP authentication
D) Use cookies exclusively

**Correct Answer:** B
**Explanation:** WebSocket connections can authenticate via query parameters (e.g., `ws://host/ws?token=xxx`) or headers. You validate the token in the endpoint or a dependency before accepting the connection.

---

### Question 16 [Medium]
**What is the `response_class` parameter used for in endpoints?**

A) To define the HTTP response class
B) To specify the response media type (JSON, HTML, etc.)
C) To configure CORS
D) To set response headers

**Correct Answer:** B
**Explanation:** `response_class` determines the content type. Use `JSONResponse` for JSON, `HTMLResponse` for HTML, `PlainTextResponse` for plain text, etc. It affects both the serialization and the OpenAPI documentation.

---

### Question 17 [Hard]
**How do you implement API versioning in FastAPI?**

A) Using URL path prefixes with multiple routers
B) Using header-based versioning
C) Using query parameter versioning
D) All of the above

**Correct Answer:** D
**Explanation:** FastAPI supports multiple versioning strategies. The most common is URL path prefixing with routers (`/api/v1/`, `/api/v2/`), but header-based and query parameter versioning are also implementable.

---

### Question 18 [Medium]
**What is the purpose of `PydanticSettings` in FastAPI?**

A) To configure Pydantic validation
B) To manage application settings from environment variables
C) To define API schemas
D) To handle database settings

**Correct Answer:** B
**Explanation:** `PydanticSettings` loads configuration from environment variables, `.env` files, or other sources, providing type-safe settings management for your FastAPI application.

---

### Question 19 [Hard]
**How do you implement streaming responses in FastAPI?**

A) Using `StreamingResponse` with a generator
B) Using `FileResponse`
C) Using `JSONResponse` with chunked encoding
D) Streaming is not supported

**Correct Answer:** A
**Explanation:** `StreamingResponse` accepts an async generator that yields chunks. This is useful for streaming large files, SSE (Server-Sent Events), or chunked data.

```python
from fastapi.responses import StreamingResponse


async def generate():
    for i in range(100):
        yield f"data: {i}\n\n"


@app.get("/stream")
async def stream():
    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

### Question 20 [Hard]
**What is the recommended way to structure a large FastAPI application?**

A) Put all endpoints in one file
B) Use `APIRouter` to split endpoints by feature, with separate routers, schemas, and services
C) Use multiple `FastAPI()` instances
D) Use Flask patterns

**Correct Answer:** B
**Explanation:** A scalable FastAPI project uses `APIRouter` to organize endpoints by feature (users, items, orders), with separate modules for schemas, models, services, and dependencies. This promotes maintainability and testability.

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | B |
| 2 | B |
| 3 | B |
| 4 | B |
| 5 | A |
| 6 | B |
| 7 | D |
| 8 | C |
| 9 | B |
| 10 | B |
| 11 | B |
| 12 | B |
| 13 | B |
| 14 | A |
| 15 | B |
| 16 | B |
| 17 | D |
| 18 | B |
| 19 | A |
| 20 | B |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered advanced FastAPI! |
| 14-17 | Proficient - Strong understanding, ready for production |
| 10-13 | Developing - Good foundation, practice advanced patterns |
| 6-9 | Beginner - Review basics first |
| 0-5 | Novice - Start with FastAPI basics quiz |

---

*Quiz created for AI Engineer Lab - Python Foundations*
