# Lecture 04: Query Parameters

## Topic Overview

Query parameters are key-value pairs that appear after the `?` in a URL. They are used for filtering, sorting, pagination, and search operations. Unlike path parameters, query parameters are typically optional and come after the URL path. FastAPI handles them automatically by matching function parameter names to query parameter names, with full validation support through the `Query()` function.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define query parameters as function arguments with default values
2. Distinguish required vs optional query parameters
3. Use the `Query()` function for advanced validation and documentation
4. Handle boolean, list, and optional query parameters
5. Implement pagination, filtering, and search patterns
6. Use parameter aliases for query parameters
7. Apply min/max length and value constraints
8. Build complex multi-filter search endpoints

---

## Key Concepts

### 1. Basic Query Parameters

Query parameters are defined as function parameters with default values. If a parameter has a default, it's optional; if it doesn't, it's required.

```python
@app.get("/search")
def search_items(q: str = "", page: int = 1, per_page: int = 10):
    """
    All parameters have defaults → all optional.
    /search?q=phone&page=2&per_page=5
    """
    return {"query": q, "page": page, "per_page": per_page}
```

**Rules:**
- Parameters NOT in the path → treated as query parameters
- Has default value → optional
- No default value → required

### 2. Required vs Optional Query Parameters

```python
# Optional (has default)
@app.get("/users/")
def list_users(limit: int = 10):
    return {"limit": limit}


# Required (no default)
@app.get("/filter")
def filter_users(department: str):
    # /filter?department=Engineering ← required!
    return {"department": department}
```

### 3. The Query() Function

`Query()` provides validation, documentation, and constraint options:

```python
from fastapi import Query


@app.get("/users/")
def list_users(
    skip: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max items to return"),
    sort_by: str = Query(default="name", description="Field to sort by"),
):
    return {"skip": skip, "limit": limit, "sort_by": sort_by}
```

**Common Query() parameters:**

| Parameter | Description |
|-----------|-------------|
| `default` | Default value (use `...` for required) |
| `description` | Description in Swagger docs |
| `ge` | Greater than or equal |
| `gt` | Greater than (exclusive) |
| `le` | Less than or equal |
| `lt` | Less than (exclusive) |
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `alias` | Alternative parameter name |
| `deprecated` | Mark as deprecated in docs |

### 4. Boolean Query Parameters

FastAPI automatically converts string values to booleans:

```python
@app.get("/active-users")
def get_active_users(active: bool = True):
    """Boolean params: /active-users?active=false"""
    filtered = [u for u in USERS if u["active"] == active]
    return {"active": active, "count": len(filtered)}


# True values: "true", "1", "yes"
# False values: "false", "0", "no"
```

### 5. List Query Parameters

Receive multiple values for the same parameter:

```python
@app.get("/multi-filter")
def multi_filter(
    departments: list[str] = Query(default=[], description="Filter by departments"),
):
    """
    /multi-filter?departments=Engineering&departments=Sales
    departments = ["Engineering", "Sales"]
    """
    return {"departments": departments}
```

**Multiple values syntax:**
- Repeat the parameter: `?dept=A&dept=B`
- Bracket notation: `?dept[]=A&dept[]=B`

### 6. Optional Parameters

Use `None` as default for truly optional parameters:

```python
@app.get("/products/")
def list_products(
    product_name: str | None = Query(default=None, alias="name"),
    min_price: float = Query(default=0.0, ge=0),
    max_price: float = Query(default=10000.0, le=100000),
):
    """
    /products/?name=laptop&min_price=500
    product_name can be None if not provided
    """
    return {"name": product_name, "min_price": min_price}
```

### 7. Parameter Aliases

Use a different name in the URL than the function parameter:

```python
@app.get("/products/")
def list_products(
    product_name: str | None = Query(default=None, alias="name"),
):
    """
    URL uses ?name=phone
    Function uses product_name
    """
    return {"product_name": product_name}


# GET /products/?name=phone
# product_name = "phone"
```

### 8. Pagination Pattern

The most common query parameter pattern:

```python
@app.get("/users/")
def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    return {
        "skip": skip,
        "limit": limit,
        "results": USERS[skip : skip + limit],
    }


# GET /users/?skip=0&limit=10  → first 10 users
# GET /users/?skip=10&limit=10 → users 11-20
```

---

## Code Examples

### Example 1: Search with Pagination

```python
from fastapi import FastAPI, Query

app = FastAPI()

USERS = [
    {"id": 1, "name": "Alice", "age": 30, "department": "Engineering"},
    {"id": 2, "name": "Bob", "age": 25, "department": "Marketing"},
    {"id": 3, "name": "Charlie", "age": 35, "department": "Engineering"},
]


@app.get("/search")
def search_items(q: str = "", page: int = 1, per_page: int = 10):
    results = [u for u in USERS if q.lower() in u["name"].lower()] if q else USERS
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "query": q,
        "page": page,
        "per_page": per_page,
        "total": len(results),
        "results": results[start:end],
    }


# GET /search?q=alice        → Alice
# GET /search?page=1&per_page=2  → first 2 users
```

### Example 2: Multi-Filter Endpoint

```python
@app.get("/users/filter")
def filter_users(
    department: str | None = Query(default=None),
    min_age: int = Query(default=0, ge=0),
    max_age: int = Query(default=100, le=150),
    active_only: bool = Query(default=False),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=50),
):
    results = USERS
    if department:
        results = [u for u in results if u["department"] == department]
    results = [u for u in results if min_age <= u["age"] <= max_age]
    if active_only:
        results = [u for u in results if u["active"]]

    total = len(results)
    start = (page - 1) * page_size
    paginated = results[start : start + page_size]

    return {
        "filters": {"department": department, "age_range": [min_age, max_age]},
        "pagination": {"page": page, "total": total},
        "results": paginated,
    }


# GET /users/filter?department=Engineering&min_age=25&page=1
```

### Example 3: Validation with Query()

```python
@app.get("/items/")
def list_items(
    q: str = Query(default="", min_length=0, max_length=50),
    category: str | None = Query(default=None),
    min_price: float = Query(default=0.0, ge=0),
    max_price: float = Query(default=10000.0, le=100000),
    tags: list[str] = Query(default=[]),
):
    return {"filters": {"q": q, "category": category, "tags": tags}}


# GET /items/?q=phone&tags=new&tags=sale
```

---

## Common Mistakes to Avoid

### Mistake 1: Confusing path and query parameters
```python
# Wrong: This is a path parameter (no default, in URL)
@app.get("/items/{item_id}")
def get_item(item_id: int): ...


# This is a query parameter (has default, not in URL)
@app.get("/items/")
def list_items(limit: int = 10): ...
```

### Mistake 2: Forgetting required parameters have no default
```python
# Wrong: department is required but looks optional
@app.get("/filter")
def filter_users(department: str):  # No default = required
    ...


# Fix: Add default if you want it optional
@app.get("/filter")
def filter_users(department: str | None = None):  # Optional
    ...
```

### Mistake 3: Not using Query() for validation
```python
# Wrong: No validation on limit
@app.get("/items/")
def list_items(limit: int = 10):
    return {"limit": limit}


# Fix: Add validation constraints
@app.get("/items/")
def list_items(limit: int = Query(default=10, ge=1, le=100)):
    return {"limit": limit}
```

### Mistake 4: Boolean parameter confusion
```python
# Wrong: "false" string is truthy in Python
@app.get("/active")
def get_active(active: bool = True):
    return {"active": active}


# GET /active?active=false → active = False (FastAPI handles this)

# But be careful with manual checks
if request.query.get("active"):  # "false" is truthy!
    ...
```

---

## Best Practices

1. **Always use `Query()`** for validation constraints and documentation
2. **Provide sensible defaults** for pagination and filter parameters
3. **Use `description`** in Query() for better Swagger docs
4. **Use `ge=0`** for skip/offset parameters to prevent negative values
5. **Use `le`** for limit/page_size to prevent excessive data loads
6. **Use `alias`** when the URL parameter name differs from the function name
7. **Use `None` as default** for truly optional parameters
8. **Use list types** for parameters that accept multiple values

---

## Practice Exercises

### Exercise 1: Product Search
Create `GET /products/` with query params: `q` (search), `min_price`, `max_price`, `category`, `in_stock` (bool).

### Exercise 2: User List
Create `GET /users/` with: `department`, `min_age`, `max_age`, `active` (bool), `sort_by`, `order` (asc/desc).

### Exercise 3: Pagination
Create a paginated list endpoint with `page`, `page_size`, and return metadata: `total`, `total_pages`, `has_next`.

### Exercise 4: Multi-Select Filter
Create `GET /items/` accepting multiple tag values: `?tags=electronics&tags=sale`.

### Exercise 5: Advanced Search
Combine search, filters, sorting, and pagination in a single endpoint.

---

## Summary

| Concept | Description |
|---------|-------------|
| Default values | Make query parameters optional |
| `Query()` | Validation, documentation, and constraints |
| Boolean params | Automatic string→bool conversion |
| List params | Multiple values for one parameter |
| Aliases | Different URL name vs function name |
| Required params | No default = must be provided |
| Pagination | `skip`/`limit` or `page`/`page_size` |
| Filtering | `department`, `category`, `tags` params |

Query parameters are the workhorse of API filtering, searching, and pagination. Master the `Query()` function and you can build any data retrieval pattern.

---

## Quick Reference

```python
from fastapi import FastAPI, Query

app = FastAPI()


# Basic
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10): ...


# With validation
@app.get("/items/")
def list_items(
    q: str = Query(default="", min_length=0, max_length=50),
    category: str | None = Query(default=None, description="Filter by category"),
    min_price: float = Query(default=0.0, ge=0),
    max_price: float = Query(default=10000.0, le=100000),
    tags: list[str] = Query(default=[]),
    active: bool = Query(default=True),
): ...
```
