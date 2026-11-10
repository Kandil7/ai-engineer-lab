# Glossary: Lecture 03 — Path Parameters

Alphabetical reference of all key terms from the Path Parameters lecture.

---

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| `:path` | Path converter type that allows slashes in the parameter value |
| Enum | A class defining a fixed set of allowed values |
| HTTPException | Exception for returning HTTP error responses |
| Path() | FastAPI function for adding validation to path parameters |
| Path parameter | A variable segment embedded in the URL path |
| Type conversion | Automatic conversion from string to the declared Python type |
| Type hint | Python annotation specifying the expected type |
| UUID | Universally Unique Identifier — a 128-bit identifier |
| Validation | Checking data against types and constraints |
| `ge` | Greater than or equal — Path validation constraint |
| `gt` | Greater than — Path validation constraint |
| `le` | Less than or equal — Path validation constraint |
| `lt` | Less than — Path validation constraint |

---

## Detailed Term Definitions

### `:path` (Path Converter)

**Definition:** A special path parameter type that allows the captured value to include forward slashes `/`. Without `:path`, the parameter stops capturing at the first `/`.

**Example:**
```python
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}


# URL: /files/home/user/document.txt
# file_path = "home/user/document.txt"
# Without :path, file_path would only be "home"
```

**Related terms:** Path Parameter, URL, Static Path

---

### Enum (Enumeration)

**Definition:** A Python class that defines a set of named constant values. When used as a path parameter type, FastAPI constrains the parameter to only accept the enum's defined values. Inherits from `str` and `Enum` for JSON serialization.

**Example:**
```python
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"message": "Deep Learning FTW!"}
    elif model_name is ModelName.resnet:
        return {"message": "Residual Learning FTW!"}
    elif model_name is ModelName.lenet:
        return {"message": "LeNet is best!"}


# Valid: GET /models/alexnet → 200 OK
# Invalid: GET /models/vgg → 422 Validation Error
```

**Key points:**
- Always inherit from both `str` and `Enum` (e.g., `class Color(str, Enum)`)
- Use `is` for comparison (`model_name is ModelName.alexnet`)
- Swagger UI shows a dropdown of allowed values
- Invalid values automatically return 422

**Related terms:** Path Parameter, Validation, Allowed Values

---

### `ge` (Greater Than or Equal)

**Definition:** A validation constraint for numeric path parameters that specifies the minimum allowed value (inclusive). Part of the `Path()` function's validation options.

**Example:**
```python
from fastapi import Path


@app.get("/products/{product_id}")
def get_product(product_id: int = Path(..., ge=1)):
    return {"product_id": product_id}


# Valid: GET /products/1 → 200 OK
# Invalid: GET /products/0 → 422 (product_id must be >= 1)
# Invalid: GET /products/-5 → 422
```

**Related terms:** `gt`, `le`, `lt`, Path Validation

---

### `gt` (Greater Than)

**Definition:** A validation constraint for numeric path parameters that specifies the minimum allowed value (exclusive). The value must be strictly greater than the specified number.

**Example:**
```python
@app.get("/scores/{score}")
def get_score(score: int = Path(..., gt=0)):
    return {"score": score}


# Valid: GET /scores/1 → 200 OK
# Invalid: GET /scores/0 → 422 (score must be > 0)
```

**Related terms:** `ge`, `le`, `lt`, Path Validation

---

### HTTPException

**Definition:** A special exception class in FastAPI that generates an HTTP error response with a specific status code and detail message. Used for business logic validation that goes beyond type checking.

**Example:**
```python
from fastapi import HTTPException


@app.get("/categories/{category_name}")
def get_category(category_name: str):
    allowed = ["electronics", "books", "clothing"]
    if category_name.lower() not in allowed:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category_name}' not found. Allowed: {allowed}",
        )
    return {"category": category_name.lower()}


# GET /categories/electronics → 200 OK
# GET /categories/invalid → 404 Not Found
```

**Related terms:** Status Code, Error Handling, Validation

---

### `le` (Less Than or Equal)

**Definition:** A validation constraint for numeric path parameters that specifies the maximum allowed value (inclusive).

**Example:**
```python
@app.get("/products/{product_id}")
def get_product(product_id: int = Path(..., ge=1, le=1000)):
    return {"product_id": product_id}


# Valid: GET /products/500 → 200 OK
# Invalid: GET /products/1001 → 422 (must be <= 1000)
```

**Related terms:** `lt`, `ge`, `gt`, Path Validation

---

### `lt` (Less Than)

**Definition:** A validation constraint for numeric path parameters that specifies the maximum allowed value (exclusive). The value must be strictly less than the specified number.

**Example:**
```python
@app.get("/grades/{grade}")
def get_grade(grade: int = Path(..., gt=0, lt=101)):
    return {"grade": grade}


# Valid: GET /grades/85 → 200 OK
# Invalid: GET /grades/101 → 422 (must be < 101)
```

**Related terms:** `le`, `ge`, `gt`, Path Validation

---

### Path() Function

**Definition:** A FastAPI function that provides additional metadata and validation constraints for path parameters. It allows you to add titles, descriptions, and numeric/string constraints.

**Example:**
```python
from fastapi import Path


@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(
        ...,  # Required (no default)
        title="Item ID",  # Display name in docs
        description="The unique item ID",  # Description in docs
        ge=1,  # >= 1
        le=1000000,  # <= 1,000,000
    ),
):
    return {"item_id": item_id}
```

**Parameters:**

| Parameter | Description |
|-----------|-------------|
| `...` | Required parameter marker (no default) |
| `title` | Human-readable name in Swagger UI |
| `description` | Description text in Swagger UI |
| `ge` | Greater than or equal |
| `gt` | Greater than (exclusive) |
| `le` | Less than or equal |
| `lt` | Less than (exclusive) |
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `pattern` | Regex pattern for strings |
| `examples` | Example values for docs |

**Related terms:** Path Parameter, Validation, Constraints

---

### Path Parameter

**Definition:** A variable segment embedded directly in the URL path, defined using curly braces `{}` in the route decorator. Path parameters are always required and are used to identify specific resources.

**Example:**
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


# URL: /users/42
# user_id = 42 (converted to int)
```

**Characteristics:**
- Always required (no default values)
- Part of the URL path (not after `?`)
- Supports automatic type conversion
- Validates against the declared type
- Multiple path parameters can exist in one URL

**Related terms:** Query Parameter, URL, Type Hints

---

### Type Conversion

**Definition:** FastAPI's automatic process of converting the string value extracted from the URL path to the Python type declared in the function parameter's type hint.

**Example:**
```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    # URL: /items/42
    # FastAPI converts "42" (string) → 42 (int)
    return {"item_id": item_id}


@app.get("/orders/{order_id}")
def get_order(order_id: UUID):
    # URL: /orders/550e8400-e29b-41d4-a716-446655440000
    # FastAPI converts string → UUID object
    return {"order_id": order_id}
```

**Supported types:**

| Type | Example Input | Converted Value |
|------|--------------|-----------------|
| `int` | `"42"` | `42` |
| `float` | `"3.14"` | `3.14` |
| `str` | `"hello"` | `"hello"` |
| `bool` | `"true"` | `True` |
| `UUID` | `"550e8400-..."` | `UUID('550e8400-...')` |
| `Path` | `"a/b/c.txt"` | `"a/b/c.txt"` (with `:path`) |

**Related terms:** Type Hints, Validation, Path Parameter

---

### Type Hint

**Definition:** A Python annotation that specifies the expected type of a variable, parameter, or return value. In FastAPI path parameters, type hints enable automatic validation and documentation.

**Example:**
```python
# Type hint enables automatic validation
@app.get("/users/{user_id}")
def get_user(user_id: int):  # int is the type hint
    return {"user_id": user_id}


# Without type hint, no validation
@app.get("/users/{user_id}")
def get_user(user_id):  # No type = string, no validation
    return {"user_id": user_id}
```

**Related terms:** Validation, Type Conversion, Pydantic

---

### UUID (Universally Unique Identifier)

**Definition:** A 128-bit identifier that is unique across all space and time. FastAPI natively supports UUID type conversion for path parameters. Commonly used for database primary keys.

**Example:**
```python
from uuid import UUID


@app.get("/orders/{order_id}")
def get_order(order_id: UUID):
    return {"order_id": str(order_id), "status": "shipped"}


# URL: /orders/550e8400-e29b-41d4-a716-446655440000
# FastAPI converts string → UUID object
# Invalid UUID format → 422 Validation Error
```

**UUID format:** `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**Related terms:** Type Conversion, Path Parameter, Primary Key

---

### Validation

**Definition:** The process of checking that input data matches expected types, ranges, and constraints. FastAPI performs two levels of validation for path parameters: type validation (automatic) and constraint validation (via `Path()`).

**Two levels:**
1. **Type validation**: Automatic from type hints
   ```python
   @app.get("/items/{item_id}")
   def get_item(item_id: int):
       # "abc" → 422 (not an integer)
       # "42" → 42 (valid)
   ```

2. **Constraint validation**: From `Path()` function
   ```python
   @app.get("/items/{item_id}")
   def get_item(item_id: int = Path(..., ge=1, le=1000)):
       # 0 → 422 (must be >= 1)
       # 1001 → 422 (must be <= 1000)
   ```

**Related terms:** Type Hints, Path(), Constraints, HTTPException

---

## Path Parameter Patterns

### Pattern: Resource by ID
```python
@app.get("/users/{user_id}")
def get_user(user_id: int): ...


@app.get("/posts/{post_id}")
def get_post(post_id: int): ...
```

### Pattern: Nested Resources
```python
@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int): ...
```

### Pattern: Enum Constraint
```python
class Status(str, Enum):
    active = "active"
    inactive = "inactive"


@app.get("/users/{status}")
def list_users(status: Status): ...
```

### Pattern: Validated ID
```python
@app.get("/products/{product_id}")
def get_product(product_id: int = Path(..., ge=1, le=1000000)): ...
```

### Pattern: File Path
```python
@app.get("/files/{file_path:path}")
def read_file(file_path: str): ...
```

### Pattern: UUID Identifier
```python
from uuid import UUID


@app.get("/orders/{order_id}")
def get_order(order_id: UUID): ...
```

---

*End of Glossary — Lecture 03: Path Parameters*
