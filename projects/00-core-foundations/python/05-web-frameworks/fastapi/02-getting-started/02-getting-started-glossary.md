# Glossary: Lecture 02 — Getting Started with FastAPI

Alphabetical reference of all key terms from the Getting Started with FastAPI lecture.

---

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| BaseModel | Pydantic base class for defining data models with validation |
| CRUD | Create, Read, Update, Delete — standard database operations |
| Default value | A fallback value used when a parameter is not provided |
| Field | A single attribute/property in a Pydantic model |
| HTTPException | Exception class for returning HTTP error responses |
| In-memory store | Data held in Python lists/dicts instead of a database |
| model_dump() | Pydantic method to convert a model to a Python dictionary |
| Optional | A field that may or may not be present in the data |
| Pagination | Returning data in chunks (skip/limit pattern) |
| Path parameter | A variable part of the URL path |
| Query parameter | A key-value pair after the ? in a URL |
| Request body | Data sent from client to server in the HTTP body |
| Response | Data sent from server back to the client |
| Status code | A three-digit number indicating the result of an HTTP request |
| Type hint | Python annotation specifying the expected type of a value |
| Validation | Checking that data matches expected types and constraints |

---

## Detailed Term Definitions

### BaseModel (Pydantic)

**Definition:** The base class from Pydantic that you inherit from to define structured data models. Pydantic uses these models for automatic validation, serialization, and documentation.

**Example:**
```python
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    tags: list[str] = []


# Usage
item = Item(name="Laptop", price=999.99)
print(item.model_dump())
# {'name': 'Laptop', 'price': 999.99, 'description': None, 'tags': []}
```

**Key methods:**
- `model_dump()` — Convert to dictionary
- `model_dump_json()` — Convert to JSON string
- `model_validate()` — Validate from dict
- `model_validate_json()` — Validate from JSON string

**Related terms:** Validation, Field, Serialization, Type Hints

---

### CRUD

**Definition:** An acronym for the four basic operations of persistent storage: Create, Read, Update, Delete. Most APIs implement these four operations.

| Operation | HTTP Method | Typical Path | Description |
|-----------|------------|--------------|-------------|
| Create | POST | `/items/` | Add a new resource |
| Read (one) | GET | `/items/{id}` | Retrieve a specific resource |
| Read (list) | GET | `/items/` | Retrieve multiple resources |
| Update | PUT | `/items/{id}` | Replace a resource entirely |
| Partial Update | PATCH | `/items/{id}` | Update specific fields |
| Delete | DELETE | `/items/{id}` | Remove a resource |

**Example:**
```python
@app.post("/items/", status_code=201)      # Create
@app.get("/items/{item_id}")               # Read one
@app.get("/items/")                        # Read list
@app.put("/items/{item_id}")               # Update
@app.delete("/items/{item_id}")            # Delete
```

**Related terms:** HTTP Method, REST, Endpoint

---

### Default Value

**Definition:** A value assigned to a function parameter that is used when the caller does not provide that argument. In FastAPI, parameters with defaults become optional query parameters.

**Example:**
```python
# Both skip and limit are optional
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# Request: GET /items/         → skip=0, limit=10
# Request: GET /items/?skip=5  → skip=5, limit=10
```

**Related terms:** Query Parameter, Optional, Required Parameter

---

### Field

**Definition:** A single attribute in a Pydantic model, defined with a type annotation and optional validation constraints.

**Example:**
```python
from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: str | None = Field(default=None, max_length=500)
    tags: list[str] = Field(default=[])
```

**Common Field constraints:**

| Constraint | Description |
|-----------|-------------|
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `gt` | Greater than (exclusive) |
| `ge` | Greater than or equal |
| `lt` | Less than (exclusive) |
| `le` | Less than or equal |
| `pattern` | Regex pattern for strings |

**Related terms:** BaseModel, Validation, Constraint

---

### HTTPException

**Definition:** A special exception class in FastAPI that, when raised, automatically generates an HTTP error response with the specified status code and detail message.

**Example:**
```python
from fastapi import HTTPException


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return items[item_id]
```

**Parameters:**
- `status_code` (required): HTTP status code (e.g., 404, 400, 500)
- `detail` (required): Error message returned to the client
- `headers` (optional): Additional response headers

**Related terms:** Status Code, Error Handling, Validation Error

---

### In-Memory Store

**Definition:** A data storage approach where all data lives in Python variables (lists, dicts) in the server's memory. Data is lost when the server restarts. Useful for learning and prototyping.

**Example:**
```python
# List-based store
items_db: list[dict] = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Phone", "price": 699.99},
]

# Dict-based store (faster lookups)
users_db: dict[int, dict] = {}
next_id = 1


@app.post("/users/")
def create_user(user: User):
    global next_id
    user_dict = user.model_dump()
    user_dict["id"] = next_id
    users_db[next_id] = user_dict
    next_id += 1
    return user_dict
```

**Related terms:** Database, Persistence, Prototyping

---

### model_dump()

**Definition:** A Pydantic BaseModel method that converts a model instance to a Python dictionary. This is essential for manipulating data, adding extra fields, or storing in a database.

**Example:**
```python
class Item(BaseModel):
    name: str
    price: float


@app.post("/items/")
def create_item(item: Item):
    item_dict = item.model_dump()  # {'name': 'Widget', 'price': 9.99}
    item_dict["id"] = 1  # Add extra field
    item_dict["created_at"] = "2024-01-01"
    return item_dict


# Variants:
item.model_dump()  # Full dict
item.model_dump(exclude_unset=True)  # Only fields that were set
item.model_dump(exclude_none=True)  # Exclude None values
item.model_dump(include={"name"})  # Only specified fields
```

**Related terms:** BaseModel, Serialization, Dictionary

---

### Optional

**Definition:** A type annotation indicating that a value may be `None` (absent). In Python 3.10+, use `str | None`. In older versions, use `Optional[str]`.

**Example:**
```python
# Python 3.10+ syntax
class User(BaseModel):
    name: str
    bio: str | None = None  # Optional with default


# Python 3.9 and earlier
from typing import Optional


class User(BaseModel):
    name: str
    bio: Optional[str] = None


# As a FastAPI query parameter
@app.get("/users/")
def list_users(department: str | None = None):
    if department:
        return {"department": department}
    return {"department": "all"}
```

**Related terms:** Default Value, None, Nullable

---

### Pagination

**Definition:** The practice of returning a subset of results from a large dataset. Typically uses `skip` (offset) and `limit` (page size) parameters.

**Example:**
```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    """
    Pagination pattern:
    /items/?skip=0&limit=10  → items 1-10
    /items/?skip=10&limit=10 → items 11-20
    /items/?skip=0&limit=25  → items 1-25
    """
    return items_db[skip : skip + limit]
```

**Alternative pattern (page-based):**
```python
@app.get("/items/")
def read_items(page: int = 1, page_size: int = 10):
    start = (page - 1) * page_size
    end = start + page_size
    return items_db[start:end]
```

**Related terms:** Skip, Limit, Offset, Page Size

---

### Path Parameter

**Definition:** A variable segment embedded in the URL path, defined using curly braces `{}` in the route decorator and as a typed function parameter.

**Example:**
```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


# URL: /items/42 → item_id = 42 (auto-converted to int)
# URL: /items/abc → 422 Validation Error (not an integer)
```

**Characteristics:**
- Always required (no default value)
- Part of the URL path
- Supports types: `int`, `str`, `float`, `UUID`, `Path` types

**Related terms:** Query Parameter, URL, Type Hints

---

### Query Parameter

**Definition:** A key-value pair appended to the URL after the `?` character. Multiple query parameters are separated by `&`. FastAPI infers them from function parameters that are NOT path parameters.

**Example:**
```python
@app.get("/search")
def search(q: str = "", page: int = 1, per_page: int = 10):
    return {"query": q, "page": page, "per_page": per_page}


# URL: /search?q=phone&page=2&per_page=5
# q="phone", page=2, per_page=5
```

**Characteristics:**
- Optional if they have default values
- Required if they have no default value
- Support validation via `Query()` function

**Related terms:** Path Parameter, URL, Query

---

### Request Body

**Definition:** Data sent from the client to the server in the HTTP request body, typically as JSON. FastAPI reads and validates request bodies using Pydantic models.

**Example:**
```python
class UserCreate(BaseModel):
    name: str
    email: str
    age: int


@app.post("/users/", status_code=201)
def create_user(user: UserCreate):
    # 'user' is the parsed and validated request body
    return {"id": 1, **user.model_dump()}


# Client sends:
# POST /users/
# Content-Type: application/json
# {"name": "Alice", "email": "alice@test.com", "age": 30}
```

**Related terms:** Pydantic, JSON, Content-Type, Body

---

### Response

**Definition:** The data sent from the server back to the client after processing a request. FastAPI automatically serializes Python dicts, lists, and Pydantic models to JSON.

**Example:**
```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": "Widget"}


# Response headers:
# Content-Type: application/json
# Body: {"item_id": 1, "name": "Widget"}
```

**Related terms:** JSON, Status Code, Content-Type

---

### Status Code

**Definition:** A three-digit number in an HTTP response that indicates the result of the request. FastAPI defaults to 200 but allows custom codes.

**Common status codes:**

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful request |
| 201 | Created | Resource successfully created |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid client input |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Not permitted |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server failure |

**Example:**
```python
@app.post("/items/", status_code=201)
def create_item(item: Item):
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    items.pop(item_id)
```

**Related terms:** HTTP, Response, HTTPException

---

### Type Hints

**Definition:** Python annotations that specify the expected type of a variable, parameter, or return value. FastAPI uses these for validation, documentation, and serialization.

**Example:**
```python
# Parameter type hints
@app.get("/items/{item_id}")
def read_item(item_id: int): ...  # item_id must be int


# Return type hints
@app.get("/items/")
def list_items() -> list[dict]: ...  # Returns a list of dicts


# Variable type hints
name: str = "Alice"
age: int = 30
```

**Supported types in FastAPI:**
- Primitives: `int`, `str`, `float`, `bool`
- Complex: `list[str]`, `dict[str, int]`, `tuple[int, int]`
- Optional: `str | None`
- Pydantic models: `Item`, `User`
- Standard library: `UUID`, `datetime`, `Decimal`

**Related terms:** Validation, Pydantic, Autocompletion

---

### Validation

**Definition:** The automatic process of checking that input data matches expected types, ranges, and constraints. FastAPI performs validation using type hints and Pydantic models, returning 422 errors for invalid data.

**Example:**
```python
class Item(BaseModel):
    name: str  # Must be a string
    price: float  # Must be a float
    quantity: int  # Must be an integer


# Valid request:
# {"name": "Widget", "price": 9.99, "quantity": 5} → 200 OK

# Invalid request:
# {"name": 123, "price": "free", "quantity": -1} → 422 Validation Error
```

**Related terms:** Type Hints, Pydantic, HTTPException

---

## Pydantic Field Constraints Quick Reference

| Constraint | Type | Description |
|-----------|------|-------------|
| `min_length` | str | Minimum string length |
| `max_length` | str | Maximum string length |
| `gt` | int/float | Greater than (exclusive) |
| `ge` | int/float | Greater than or equal |
| `lt` | int/float | Less than (exclusive) |
| `le` | int/float | Less than or equal |
| `pattern` | str | Regex pattern |
| `enum` | Enum | One of allowed values |

---

*End of Glossary — Lecture 02: Getting Started with FastAPI*
