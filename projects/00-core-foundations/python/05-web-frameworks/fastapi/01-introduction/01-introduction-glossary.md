# Glossary: Lecture 01 — Introduction to FastAPI

Alphabetical reference of all key terms from the Introduction to FastAPI lecture.

---

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| API | Application Programming Interface — a contract for how software components communicate |
| ASGI | Asynchronous Server Gateway Interface — the standard for async Python web servers |
| Auto-documentation | Swagger UI and ReDoc generated automatically from your code |
| CORS | Cross-Origin Resource Sharing — controls which domains can access your API |
| Endpoint | A specific URL path where your API responds to requests |
| FastAPI | Modern Python web framework for building high-performance APIs |
| HTTP Method | GET, POST, PUT, PATCH, DELETE — verbs that define the action |
| JSON | JavaScript Object Notation — lightweight data interchange format |
| OpenAPI | Specification standard for describing REST APIs |
| Path Operation | A function that handles a specific HTTP method + URL path |
| Pydantic | Python library for data validation using type hints |
| ReDoc | Alternative API documentation viewer |
| Starlette | Lightweight ASGI framework that FastAPI is built on |
| Swagger UI | Interactive API documentation and testing tool |
| Type Hints | Python annotations that specify variable/parameter types |
| Uvicorn | Lightning-fast ASGI server for running FastAPI apps |
| Validation | Automatic checking that input data matches expected types |

---

## Detailed Term Definitions

### API (Application Programming Interface)

**Definition:** A set of rules and protocols that allows different software applications to communicate with each other. In the context of FastAPI, an API is a web service that accepts HTTP requests and returns HTTP responses.

**Example:**
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/users")  # This is an API endpoint
def get_users():
    return [{"id": 1, "name": "Alice"}]
```

**Related terms:** Endpoint, REST, HTTP Method, JSON

---

### ASGI (Asynchronous Server Gateway Interface)

**Definition:** A spiritual successor to WSGI (Web Server Gateway Interface) designed to support async Python web frameworks. ASGI enables non-blocking I/O operations, which is critical for handling many concurrent connections efficiently.

**Example:**
```bash
# Uvicorn is an ASGI server
uvicorn main:app --reload
```

**Related terms:** Uvicorn, Starlette, Async, WSGI

---

### Auto-Documentation

**Definition:** FastAPI automatically generates interactive API documentation from your code's type hints and docstrings. This includes Swagger UI at `/docs` and ReDoc at `/redoc`.

**Example:**
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Get a user by ID.

    This docstring appears in the Swagger UI!
    """
    return {"user_id": user_id}
```

**Related terms:** Swagger UI, ReDoc, OpenAPI, Docstrings

---

### CORS (Cross-Origin Resource Sharing)

**Definition:** A security mechanism that controls which domains are allowed to make requests to your API. By default, browsers block cross-origin requests. You configure CORS middleware to allow specific origins.

**Example:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Related terms:** Middleware, Security, Browser

---

### Endpoint

**Definition:** A specific URL path combined with an HTTP method that your API responds to. For example, `GET /users` is one endpoint and `POST /users` is a different endpoint on the same path.

**Example:**
```python
@app.get("/items/{item_id}")  # GET endpoint
def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/items")  # POST endpoint
def create_item():
    return {"status": "created"}
```

**Related terms:** Path Operation, URL, HTTP Method, Route

---

### FastAPI

**Definition:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. Created by Sebastián Ramírez (tiangolo). It is built on Starlette (web) and Pydantic (data).

**Key advantages:**
- Fast performance (on par with Node.js and Go)
- Fast to code (great developer experience)
- Fewer bugs (automatic validation)
- Intuitive (great editor support)
- Easy to learn and use
- Short (minimize code duplication)
- Robust (production-ready with auto docs)

**Example:**
```python
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Hello"}
```

**Related terms:** Starlette, Pydantic, Uvicorn, ASGI

---

### HTTP Method

**Definition:** The verb in an HTTP request that specifies the desired action. FastAPI provides decorators for all standard HTTP methods:

| Method | Decorator | Purpose |
|--------|-----------|---------|
| GET | `@app.get()` | Read/retrieve data |
| POST | `@app.post()` | Create new data |
| PUT | `@app.put()` | Full update of a resource |
| PATCH | `@app.patch()` | Partial update of a resource |
| DELETE | `@app.delete()` | Remove a resource |
| OPTIONS | `@app.options()` | Discover allowed methods |
| HEAD | `@app.head()` | Like GET but no body |

**Example:**
```python
@app.get("/items/{id}")
def read_item(id: int): ...


@app.post("/items")
def create_item(item: Item): ...


@app.put("/items/{id}")
def update_item(id: int, item: Item): ...


@app.delete("/items/{id}")
def delete_item(id: int): ...
```

**Related terms:** Endpoint, Path Operation, REST

---

### JSON (JavaScript Object Notation)

**Definition:** A lightweight, text-based data interchange format that is easy for humans to read and write and easy for machines to parse and generate. FastAPI automatically converts Python dicts and lists to JSON.

**Example:**
```python
# Python dict → JSON automatically
@app.get("/data")
def get_data():
    return {"name": "Alice", "age": 30, "hobbies": ["reading", "coding"]}


# Response body:
# {"name":"Alice","age":30,"hobbies":["reading","coding"]}
```

**Related terms:** Serialization, Response, Request Body

---

### Middleware

**Definition:** Software that sits between the client and the server, processing requests and responses. Middleware can add cross-cutting functionality like logging, authentication, CORS, and compression.

**Example:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)
```

**Related terms:** CORS, Request, Response, Security

---

### OpenAPI

**Definition:** A specification standard (formerly known as Swagger) for describing REST APIs. FastAPI generates an OpenAPI schema automatically from your code, which is used by Swagger UI, ReDoc, and other API clients.

**Example:**
```bash
# Access the raw OpenAPI JSON
curl http://127.0.0.1:8000/openapi.json
```

**Related terms:** Swagger UI, ReDoc, API Specification, JSON Schema

---

### Path Operation

**Definition:** A function in FastAPI that is decorated with an HTTP method decorator (`@app.get()`, `@app.post()`, etc.) and handles requests to a specific URL path. The term "path operation" comes from the OpenAPI specification.

**Example:**
```python
@app.get("/users/{user_id}")  # This is a path operation
def get_user(user_id: int):
    """Path operation function."""
    return {"user_id": user_id}
```

**Related terms:** Endpoint, Decorator, Route, HTTP Method

---

### Pydantic

**Definition:** A Python library for data validation and settings management using Python type hints. FastAPI uses Pydantic to validate request bodies, query parameters, and response data automatically.

**Example:**
```python
from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    email: str


@app.post("/users")
def create_user(user: User):
    # 'user' is automatically validated and parsed
    return {"name": user.name, "age": user.age}
```

**Related terms:** Validation, BaseModel, Type Hints, Serialization

---

### ReDoc

**Definition:** An alternative API documentation viewer generated automatically by FastAPI. It produces a three-panel documentation layout. Accessible at `/redoc` by default.

**Example:**
```bash
# Open ReDoc in browser
open http://127.0.0.1:8000/redoc
```

**Related terms:** Swagger UI, OpenAPI, Auto-Documentation

---

### Response

**Definition:** The data sent back from the server to the client after processing a request. In FastAPI, returning a Python dict, list, or Pydantic model automatically creates a JSON response with a 200 status code.

**Example:**
```python
from fastapi.responses import JSONResponse


@app.get("/response")
def get_response():
    return {"status": "ok"}  # Auto-converted to JSONResponse
```

**Related terms:** JSON, Status Code, Response Model

---

### Route

**Definition:** A mapping between a URL path (and HTTP method) and a handler function. When you use `@app.get("/path")`, you are registering a route.

**Example:**
```python
# Route registration
@app.get("/items")       # Route: GET /items → list_items
@app.post("/items")      # Route: POST /items → create_item
@app.get("/items/{id}")  # Route: GET /items/{id} → get_item
```

**Related terms:** Endpoint, Path Operation, URL

---

### Starlette

**Definition:** A lightweight ASGI framework/toolkit that provides the core web functionality FastAPI is built upon. Starlette handles routing, request/response objects, middleware, WebSocket support, and more.

**Example:**
```python
# FastAPI extends Starlette
from fastapi import FastAPI

app = FastAPI()
# app is a Starlette application
```

**Related terms:** ASGI, FastAPI, Middleware, Request

---

### Swagger UI

**Definition:** An interactive API documentation tool that provides a "Try it out" interface for testing endpoints directly in the browser. FastAPI generates it automatically at `/docs`.

**Example:**
```bash
# Open Swagger UI in browser
open http://127.0.0.1:8000/docs
```

**Features:**
- Lists all endpoints grouped by tags
- Shows request/response schemas
- Allows testing endpoints directly
- Displays authentication requirements

**Related terms:** ReDoc, OpenAPI, Auto-Documentation

---

### Type Hints

**Definition:** Python annotations that specify the expected type of a variable, parameter, or return value. FastAPI uses these for automatic validation, serialization, and documentation generation.

**Example:**
```python
# Type hints enable automatic validation
@app.get("/items/{item_id}")
def get_item(item_id: int):  # item_id must be an integer
    return {"item_id": item_id}


# Without type hints, no validation occurs
@app.get("/items/{item_id}")
def get_item_no_validation(item_id):  # No type = no validation
    return {"item_id": item_id}
```

**Related terms:** Validation, Pydantic, Type Safety

---

### Uvicorn

**Definition:** A lightning-fast ASGI web server for Python. It is used to run FastAPI applications in both development and production. Supports hot reloading, multi-worker deployment, and TLS.

**Example:**
```bash
# Development (with hot reload)
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With logging
uvicorn main:app --reload --log-level info
```

**Common options:**

| Option | Description |
|--------|-------------|
| `--reload` | Auto-restart on code changes |
| `--host` | Bind address (default: 127.0.0.1) |
| `--port` | Listen port (default: 8000) |
| `--workers` | Number of worker processes |
| `--log-level` | Logging level (debug, info, warning, error) |

**Related terms:** ASGI, Development Server, Production Deployment

---

### Validation

**Definition:** The process of checking that input data matches expected types, ranges, and constraints. FastAPI performs automatic validation using type hints and Pydantic models.

**Example:**
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    # If user_id is not an integer, FastAPI returns 422
    return {"user_id": user_id}


# Request: GET /users/abc → 422 Validation Error
# Request: GET /users/42 → 200 OK
```

**Related terms:** Type Hints, Pydantic, Error Handling

---

### WSGI (Web Server Gateway Interface)

**Definition:** The original standard for connecting Python web applications to web servers. WSGI is synchronous and does not support async operations. FastAPI uses ASGI instead, which is the async successor to WSGI.

**Example:**
```python
# WSGI (old standard, used by Flask/Django)
# Synchronous, one request at a time per thread

# ASGI (new standard, used by FastAPI)
# Asynchronous, handles many concurrent connections
```

**Related terms:** ASGI, Uvicorn, Starlette

---

## Glossary of HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid client input |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Authenticated but not allowed |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server-side failure |

---

## Glossary of Common Patterns

### Pattern: Basic Endpoint
```python
@app.get("/resource")
def list_resource():
    return {"data": []}
```

### Pattern: CRUD Operations
```python
@app.get("/items/{id}")      # Read
@app.post("/items")          # Create
@app.put("/items/{id}")      # Update
@app.delete("/items/{id}")   # Delete
```

### Pattern: Application Setup
```python
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="API", version="1.0.0")


@app.get("/")
def root():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

*End of Glossary — Lecture 01: Introduction to FastAPI*
