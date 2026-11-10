# Glossary: Lecture 05 — Request Body

Alphabetical reference of all key terms from the Request Body lecture.

---

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| BaseModel | Pydantic base class for defining structured data with validation |
| Batch operation | Processing multiple items in a single request |
| Content-Type | HTTP header indicating the media type of the request body |
| Exclude defaults | Omit fields with default values from output |
| Exclude None | Omit fields set to None from output |
| Exclude unset | Omit fields not explicitly provided in the request |
| Field() | Function for adding validation constraints to model fields |
| Full update | PUT operation where all fields are required |
| JSON body | Request body data in JSON format |
| model_dump() | Pydantic method to convert a model to a Python dictionary |
| Nested model | A Pydantic model that contains other Pydantic models |
| Partial update | PATCH operation where only changed fields are sent |
| PATCH | HTTP method for partial resource updates |
| PUT | HTTP method for full resource replacement |
| Pydantic | Python library for data validation using type hints |
| Request body | Data sent from client to server in the HTTP body |
| Response model | Pydantic model that defines the shape of API responses |
| Validation | Checking that data matches expected types and constraints |

---

## Detailed Term Definitions

### BaseModel

**Definition:** The base class from Pydantic that you inherit from to define structured data models. It provides automatic validation, serialization, and OpenAPI schema generation.

**Example:**
```python
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., description="User's email")
    age: int = Field(..., ge=0, le=150)
    bio: str | None = Field(default=None)
    is_active: bool = Field(default=True)


# Automatic validation:
user = UserCreate(name="Alice", email="alice@test.com", age=30)  # OK
user = UserCreate(name="", email="bad", age=-5)  # ValidationError
```

**Key methods:**
- `model_dump()` — Convert to dict
- `model_dump(exclude_unset=True)` — Only explicitly set fields
- `model_dump(exclude_none=True)` — Exclude None values
- `model_dump(exclude_defaults=True)` — Exclude default values
- `model_validate(dict)` — Create from dict
- `model_validate_json(json_str)` — Create from JSON string

**Related terms:** Field, Validation, Serialization, JSON

---

### Batch Operation

**Definition:** An API operation that processes multiple items in a single request, reducing round-trips. Typically receives a JSON array as the request body.

**Example:**
```python
@app.post("/batch-create")
def batch_create(users: list[UserCreate]):
    created = []
    for user in users:
        user_dict = user.model_dump()
        user_dict["id"] = len(created) + 1
        created.append(user_dict)
    return {"created_count": len(created), "users": created}


# Request body (JSON array):
# [
#   {"name": "Alice", "email": "a@test.com", "age": 30},
#   {"name": "Bob", "email": "b@test.com", "age": 25}
# ]
```

**Related terms:** Request Body, List, CRUD

---

### Content-Type

**Definition:** An HTTP header that indicates the media type of the request body. For JSON request bodies, the Content-Type is `application/json`.

**Common values:**

| Content-Type | Description |
|-------------|-------------|
| `application/json` | JSON data |
| `application/x-www-form-urlencoded` | HTML form data |
| `multipart/form-data` | File uploads |
| `text/plain` | Plain text |

**Example:**
```bash
# JSON request body
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@test.com", "age": 30}'
```

**Related terms:** Request Body, JSON, Form Data

---

### Exclude Defaults

**Definition:** A `model_dump()` option that omits fields whose values match their default values. Useful for returning only explicitly set fields.

**Example:**
```python
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    tags: list[str] = []


item = Item(name="Widget", price=9.99)
# in_stock and tags use defaults

print(item.model_dump(exclude_defaults=True))
# {'name': 'Widget', 'price': 9.99}
# in_stock and tags excluded because they match defaults
```

**Related terms:** model_dump(), Exclude None, Exclude Unset

---

### Exclude None

**Definition:** A `model_dump()` option that omits fields with `None` values from the output.

**Example:**
```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


item = Item(name="Widget", price=9.99)
print(item.model_dump(exclude_none=True))
# {'name': 'Widget', 'price': 9.99}
# description and tax excluded because they're None
```

**Related terms:** model_dump(), Exclude Defaults, Exclude Unset

---

### Exclude Unset

**Definition:** A `model_dump()` option that omits fields that were not explicitly provided in the request. Only fields that were actually sent are included. Essential for PATCH operations.

**Example:**
```python
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None


# Client sends only: {"name": "New Name"}
user = UserUpdate(name="New Name")
print(user.model_dump(exclude_unset=True))
# {'name': 'New Name'}
# email and age excluded because they weren't sent
```

**Related terms:** model_dump(), PATCH, Partial Update

---

### Field()

**Definition:** A Pydantic function for adding validation constraints, descriptions, and metadata to individual model fields.

**Example:**
```python
from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product name",
        examples=["Wireless Mouse"],
    )
    price: float = Field(
        ...,
        gt=0,
        description="Price in USD",
        examples=[29.99],
    )
    tags: list[str] = Field(
        default=[],
        description="Product tags",
        examples=[["electronics", "sale"]],
    )
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `...` | — | Required field marker |
| `default` | any | Default value |
| `description` | str | Description for docs |
| `min_length` | int | Minimum string length |
| `max_length` | int | Maximum string length |
| `gt` | int/float | Greater than (exclusive) |
| `ge` | int/float | Greater than or equal |
| `lt` | int/float | Less than (exclusive) |
| `le` | int/float | Less than or equal |
| `pattern` | str | Regex pattern |
| `examples` | list | Example values for docs |

**Related terms:** BaseModel, Validation, Constraint

---

### Full Update (PUT)

**Definition:** A complete resource replacement where the client sends ALL fields. The entire resource is replaced with the new data.

**Example:**
```python
@app.put("/users/{user_id}")
def full_update_user(user_id: int, user: UserCreate):
    """All fields required — full replacement."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = user.model_dump()
    user_dict["id"] = user_id
    users_db[user_id] = user_dict
    return users_db[user_id]


# Client must send: {"name": "...", "email": "...", "age": ..., "bio": "...", "is_active": ...}
```

**Related terms:** PATCH, Partial Update, PUT

---

### JSON Body

**Definition:** Data sent from the client to the server in the HTTP request body, formatted as JSON. FastAPI automatically reads and parses JSON bodies when a Pydantic model is used as a parameter.

**Example:**
```python
@app.post("/users/")
def create_user(user: UserCreate):
    return user.model_dump()


# Client sends:
# POST /users/
# Content-Type: application/json
#
# {
#   "name": "Alice",
#   "email": "alice@test.com",
#   "age": 30
# }
```

**Related terms:** Request Body, Content-Type, Pydantic

---

### model_dump()

**Definition:** A Pydantic BaseModel method that converts a model instance to a Python dictionary. Essential for manipulating data before storing or returning it.

**Example:**
```python
class User(BaseModel):
    name: str
    email: str
    password: str


user = User(name="Alice", email="alice@test.com", password="secret")

# Full dict
print(user.model_dump())
# {'name': 'Alice', 'email': 'alice@test.com', 'password': 'secret'}

# Exclude specific fields
print(user.model_dump(exclude={"password"}))
# {'name': 'Alice', 'email': 'alice@test.com'}

# Only explicitly set fields
print(user.model_dump(exclude_unset=True))
# {'name': 'Alice', 'email': 'alice@test.com', 'password': 'secret'}
```

**Variants:**
- `model_dump()` — Full dict
- `model_dump(exclude={"field"})` — Exclude specific fields
- `model_dump(exclude_unset=True)` — Only explicitly set
- `model_dump(exclude_none=True)` — No None values
- `model_dump(exclude_defaults=True)` — No default values

**Related terms:** BaseModel, Serialization, Dictionary

---

### Nested Model

**Definition:** A Pydantic model that contains other Pydantic models as fields, allowing you to define complex, hierarchical data structures with full validation at every level.

**Example:**
```python
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class Order(BaseModel):
    customer_name: str
    items: list[OrderItem]
    shipping_address: Address  # Nested model


# JSON:
# {
#   "customer_name": "Bob",
#   "items": [...],
#   "shipping_address": {
#     "street": "123 Main St",
#     "city": "Springfield",
#     "state": "IL",
#     "zip_code": "62701"
#   }
# }
```

**Related terms:** BaseModel, Complex Data, Validation

---

### Partial Update (PATCH)

**Definition:** An update operation where only changed fields are sent. Unset fields retain their previous values.

**Example:**
```python
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None


@app.patch("/users/{user_id}")
def partial_update(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.model_dump(exclude_unset=True)
    users_db[user_id].update(update_data)
    return users_db[user_id]


# Client sends only: {"email": "new@test.com"}
# Only email is updated; name and age remain unchanged
```

**Related terms:** PUT, Full Update, Exclude Unset

---

### PATCH

**Definition:** An HTTP method used for partial updates to a resource. Only the fields included in the request body are modified.

**Example:**
```python
@app.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    update_data = user.model_dump(exclude_unset=True)
    users_db[user_id].update(update_data)
    return users_db[user_id]


# curl -X PATCH http://localhost:8000/users/1 \
#   -H "Content-Type: application/json" \
#   -d '{"bio": "Updated bio"}'
```

**Related terms:** PUT, Partial Update, HTTP Method

---

### PUT

**Definition:** An HTTP method used for full resource replacement. The client sends ALL fields, and the entire resource is replaced.

**Example:**
```python
@app.put("/users/{user_id}")
def full_update(user_id: int, user: UserCreate):
    user_dict = user.model_dump()
    user_dict["id"] = user_id
    users_db[user_id] = user_dict
    return users_db[user_id]


# curl -X PUT http://localhost:8000/users/1 \
#   -H "Content-Type: application/json" \
#   -d '{"name": "Alice", "email": "alice@new.com", "age": 31, "bio": "Hi!"}'
```

**Related terms:** PATCH, Full Update, HTTP Method

---

### Pydantic

**Definition:** A Python library for data validation and settings management using Python type hints. FastAPI uses Pydantic for request body validation, response serialization, and OpenAPI schema generation.

**Example:**
```python
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr  # Requires pydantic[email]
    age: int = Field(..., ge=0, le=150)


# Validates:
# - name is a non-empty string
# - email is a valid email format
# - age is 0-150
```

**Related terms:** BaseModel, Field, Validation, Type Hints

---

### Request Body

**Definition:** Data sent from the client to the server in the HTTP request body, typically as JSON. FastAPI reads and validates request bodies using Pydantic models.

**Example:**
```python
class ItemCreate(BaseModel):
    name: str
    price: float


@app.post("/items/")
def create_item(item: ItemCreate):
    # 'item' is the parsed and validated request body
    return {"id": 1, **item.model_dump()}


# Client sends:
# POST /items/
# Content-Type: application/json
# {"name": "Widget", "price": 9.99}
```

**Related terms:** JSON, Content-Type, Pydantic, Body

---

### Response Model

**Definition:** A Pydantic model that defines the shape and constraints of API response data. Used with the `response_model` parameter in path operation decorators to filter and validate output.

**Example:**
```python
class UserIn(BaseModel):
    name: str
    email: str
    password: str  # Should NOT be in response


class UserOut(BaseModel):
    id: int
    name: str
    email: str  # No password!


@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn):
    return {"id": 1, **user.model_dump()}
    # Password is filtered out automatically
```

**Related terms:** Request Body, Pydantic, Filtering

---

### Validation

**Definition:** The automatic process of checking that input data matches expected types, ranges, and constraints. FastAPI performs validation using type hints and Pydantic models, returning 422 errors for invalid data.

**Two levels for request bodies:**
1. **Type validation**: Automatic from type hints
2. **Constraint validation**: From Field() constraints

**Example:**
```python
class User(BaseModel):
    name: str  # Must be string
    age: int = Field(ge=0)  # Must be int >= 0


# Valid: {"name": "Alice", "age": 30}
# Invalid: {"name": 123, "age": -5} → 422
```

**Related terms:** Type Hints, Field(), Pydantic, HTTPException

---

## Request Body Patterns

### Pattern: Create Resource
```python
@app.post("/items/", status_code=201)
def create_item(item: ItemCreate):
    return item.model_dump()
```

### Pattern: Full Update
```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    items_db[item_id] = item.model_dump()
    return items_db[item_id]
```

### Pattern: Partial Update
```python
@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: ItemUpdate):
    update = item.model_dump(exclude_unset=True)
    items_db[item_id].update(update)
    return items_db[item_id]
```

### Pattern: Batch Create
```python
@app.post("/items/batch")
def batch_create(items: list[ItemCreate]):
    return {"created": len(items)}
```

### Pattern: Nested Data
```python
@app.post("/orders/")
def create_order(order: Order):
    total = sum(i.quantity * i.unit_price for i in order.items)
    return {"total": total}
```

---

*End of Glossary — Lecture 05: Request Body*
