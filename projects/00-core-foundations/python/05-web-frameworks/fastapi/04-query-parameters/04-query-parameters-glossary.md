# Glossary: Lecture 04 — Query Parameters

Alphabetical reference of all key terms from the Query Parameters lecture.

---

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| Alias | An alternative name for a query parameter in the URL |
| Boolean parameter | A query parameter that accepts true/false values |
| Default value | A fallback value when the parameter is not provided |
| Filter | Narrowing results based on parameter values |
| List parameter | A query parameter that accepts multiple values |
| Offset | Number of items to skip (used in pagination) |
| Optional parameter | A parameter that may or may not be provided |
| Page size | Number of items per page (limit) |
| Pagination | Returning data in chunks |
| Query() | FastAPI function for validating and documenting query params |
| Query parameter | A key-value pair after the ? in a URL |
| Required parameter | A parameter that must be provided |
| Search | Finding results matching a text query |
| Skip | Alias for offset — items to skip before returning results |
| Sort | Ordering results by a field and direction |
| Validation | Checking that data matches expected types and constraints |

---

## Detailed Term Definitions

### Alias

**Definition:** An alternative name for a query parameter that appears in the URL. The function parameter name differs from the URL parameter name, providing flexibility in API design.

**Example:**
```python
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/products/")
def list_products(
    product_name: str | None = Query(default=None, alias="name"),
):
    return {"product_name": product_name}


# URL: /products/?name=phone
# Function receives: product_name = "phone"
```

**Related terms:** Query Parameter, Query(), Documentation

---

### Boolean Parameter

**Definition:** A query parameter that accepts boolean (true/false) values. FastAPI automatically converts string representations to Python booleans.

**Accepted true values:** `"true"`, `"1"`, `"yes"`
**Accepted false values:** `"false"`, `"0"`, `"no"`

**Example:**
```python
@app.get("/active-users")
def get_active_users(active: bool = True):
    filtered = [u for u in USERS if u["active"] == active]
    return {"active": active, "count": len(filtered)}


# GET /active-users?active=true  → active = True
# GET /active-users?active=false → active = False
# GET /active-users              → active = True (default)
```

**Related terms:** Query Parameter, Type Conversion, Default Value

---

### Default Value

**Definition:** A value assigned to a function parameter that is used when the caller does not provide that argument. In FastAPI, parameters with defaults become optional query parameters.

**Example:**
```python
# With default → optional
@app.get("/items/")
def list_items(limit: int = 10):
    return {"limit": limit}


# Without default → required
@app.get("/filter")
def filter_items(category: str):
    return {"category": category}


# None default → optional (can be None)
@app.get("/search")
def search(q: str | None = None):
    return {"query": q}
```

**Related terms:** Optional Parameter, Required Parameter, Query Parameter

---

### Filter

**Definition:** A query parameter that narrows down results based on specific criteria. Common filter patterns include text search, category selection, price range, and boolean flags.

**Example:**
```python
@app.get("/users/")
def list_users(
    department: str | None = Query(default=None),
    min_age: int = Query(default=0, ge=0),
    max_age: int = Query(default=100, le=150),
    active_only: bool = Query(default=False),
):
    results = USERS
    if department:
        results = [u for u in results if u["department"] == department]
    results = [u for u in results if min_age <= u["age"] <= max_age]
    if active_only:
        results = [u for u in results if u["active"]]
    return {"count": len(results), "results": results}


# GET /users/?department=Engineering&min_age=25&active_only=true
```

**Related terms:** Query Parameter, Search, Pagination

---

### List Parameter

**Definition:** A query parameter that can accept multiple values. The same parameter name is repeated in the URL, and FastAPI collects them into a Python list.

**Example:**
```python
@app.get("/multi-filter")
def multi_filter(
    departments: list[str] = Query(default=[], description="Filter by departments"),
):
    return {"departments": departments}


# GET /multi-filter?departments=Engineering&departments=Sales
# departments = ["Engineering", "Sales"]
```

**Multiple value syntax:**
- Repeat parameter: `?dept=A&dept=B`
- Comma-separated (requires custom parsing): `?dept=A,B`

**Related terms:** Query Parameter, Filter, Array

---

### Offset

**Definition:** The number of items to skip before returning results. Used in pagination to move between pages. Often called `skip` in FastAPI.

**Example:**
```python
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    return items_db[skip : skip + limit]


# GET /items/?skip=0&limit=10   → items 1-10
# GET /items/?skip=10&limit=10  → items 11-20
# GET /items/?skip=20&limit=10  → items 21-30
```

**Related terms:** Pagination, Limit, Page Size

---

### Optional Parameter

**Definition:** A query parameter that may or may not be provided by the client. In FastAPI, parameters with default values (including `None`) are optional.

**Example:**
```python
@app.get("/users/")
def list_users(
    department: str | None = Query(default=None),  # Optional
    min_age: int = Query(default=0),  # Optional (has default)
    active: bool = Query(default=True),  # Optional (has default)
):
    return {"department": department, "min_age": min_age}


# All of these are valid:
# GET /users/
# GET /users/?department=Engineering
# GET /users/?department=Engineering&min_age=25
# GET /users/?active=false
```

**Related terms:** Default Value, Required Parameter, Query Parameter

---

### Page Size

**Definition:** The maximum number of items to return per page in a paginated response. Also called `limit` or `per_page`.

**Example:**
```python
@app.get("/users/")
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
):
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "page": page,
        "page_size": page_size,
        "results": USERS[start:end],
    }


# GET /users/?page=1&page_size=10  → items 1-10
# GET /users/?page=2&page_size=10  → items 11-20
```

**Related terms:** Pagination, Offset, Limit

---

### Pagination

**Definition:** The practice of dividing large result sets into smaller chunks (pages). Two common patterns: offset-based (skip/limit) and page-based (page/page_size).

**Offset-based pattern:**
```python
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    return items_db[skip : skip + limit]
```

**Page-based pattern with metadata:**
```python
@app.get("/items/")
def list_items(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
):
    total = len(items_db)
    start = (page - 1) * page_size
    end = start + page_size
    total_pages = (total + page_size - 1) // page_size

    return {
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
        },
        "results": items_db[start:end],
    }
```

**Related terms:** Skip, Limit, Page Size, Offset

---

### Query() Function

**Definition:** A FastAPI function that provides validation, documentation, and constraint options for query parameters. Replaces bare parameter definitions for more control.

**Example:**
```python
from fastapi import Query


@app.get("/items/")
def list_items(
    q: str = Query(
        default="",
        min_length=0,
        max_length=50,
        description="Search term",
    ),
    category: str | None = Query(
        default=None,
        description="Filter by category",
    ),
    min_price: float = Query(
        default=0.0,
        ge=0,
        description="Minimum price",
    ),
):
    return {"q": q, "category": category, "min_price": min_price}
```

**Parameters:**

| Parameter | Description |
|-----------|-------------|
| `default` | Default value (use `...` for required) |
| `description` | Description text in Swagger docs |
| `alias` | Alternative URL parameter name |
| `ge` | Greater than or equal |
| `gt` | Greater than (exclusive) |
| `le` | Less than or equal |
| `lt` | Less than (exclusive) |
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `deprecated` | Mark as deprecated in docs |
| `examples` | Example values for documentation |

**Related terms:** Path(), Validation, Documentation

---

### Query Parameter

**Definition:** A key-value pair appended to the URL after the `?` character. Multiple query parameters are separated by `&`. FastAPI infers them from function parameters that are NOT path parameters and do NOT have Pydantic model types.

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
- Always strings in the URL (FastAPI converts types)

**Related terms:** Path Parameter, URL, Query(), Validation

---

### Required Parameter

**Definition:** A query parameter that MUST be provided by the client. If not provided, FastAPI returns a 422 validation error. Defined by having no default value.

**Example:**
```python
@app.get("/filter")
def filter_users(department: str):
    """department is required — no default value"""
    return {"department": department}


# GET /filter?department=Engineering → 200 OK
# GET /filter                        → 422 Validation Error
```

**Related terms:** Default Value, Optional Parameter, Validation Error

---

### Search

**Definition:** Finding results that match a text query. Typically implemented as a `q` or `search` query parameter that filters results based on partial string matching.

**Example:**
```python
@app.get("/users/search")
def search_users(
    q: str = Query(default="", min_length=0, max_length=50),
    department: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=50),
):
    results = USERS
    if q:
        results = [u for u in results if q.lower() in u["name"].lower()]
    if department:
        results = [u for u in results if u["department"] == department]

    total = len(results)
    start = (page - 1) * page_size
    paginated = results[start : start + page_size]

    return {
        "query": q,
        "total": total,
        "results": paginated,
    }


# GET /users/search?q=alice&department=Engineering&page=1
```

**Related terms:** Filter, Query Parameter, Pagination

---

### Skip

**Definition:** The number of items to skip before returning results in a paginated response. Synonymous with `offset`. Used in offset-based pagination.

**Example:**
```python
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    return items_db[skip : skip + limit]


# GET /items/?skip=0   → first 10 items
# GET /items/?skip=10  → skip first 10, return next 10
```

**Related terms:** Offset, Pagination, Limit

---

### Sort

**Definition:** The process of ordering query results by a specific field and direction (ascending or descending). Implemented via `sort_by` and `order` query parameters.

**Example:**
```python
@app.get("/users/")
def list_users(
    sort_by: str = Query(default="name", description="Field to sort by"),
    order: str = Query(default="asc", description="Sort order: asc or desc"),
):
    sorted_users = sorted(
        USERS,
        key=lambda u: u.get(sort_by, ""),
        reverse=(order == "desc"),
    )
    return {"sort_by": sort_by, "order": order, "results": sorted_users}


# GET /users/?sort_by=age&order=desc
```

**Related terms:** Query Parameter, Order, Filter

---

### Validation

**Definition:** The process of checking that input data matches expected types, ranges, and constraints. For query parameters, validation is performed using type hints and the `Query()` function.

**Two levels:**
1. **Type validation**: Automatic from type hints
   ```python
   def list_items(limit: int = 10):
       # limit must be an integer
   ```

2. **Constraint validation**: From `Query()` function
   ```python
   def list_items(limit: int = Query(default=10, ge=1, le=100)):
       # limit must be 1-100
   ```

**Related terms:** Type Hints, Query(), Constraints, HTTPException

---

## Query Parameter Patterns

### Pattern: Basic Pagination
```python
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10): ...
```

### Pattern: Search
```python
@app.get("/search")
def search(q: str = "", page: int = 1): ...
```

### Pattern: Filter
```python
@app.get("/users/")
def list_users(department: str | None = None, active: bool = True): ...
```

### Pattern: Sort
```python
@app.get("/items/")
def list_items(sort_by: str = "name", order: str = "asc"): ...
```

### Pattern: Complex Filter
```python
@app.get("/items/")
def list_items(
    q: str = "",
    category: str | None = None,
    min_price: float = 0.0,
    max_price: float = 10000.0,
    tags: list[str] = [],
    page: int = 1,
    page_size: int = 10,
): ...
```

---

*End of Glossary — Lecture 04: Query Parameters*
