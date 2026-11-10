# Glossary: Lecture 06 — Response Model

Alphabetical reference of all key terms from the Response Model lecture.

---

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| BaseModel | Pydantic base class for defining data models with validation |
| Computed field | A field calculated or added in the path operation function |
| Exclude defaults | Omit fields matching their default values from output |
| Exclude None | Omit fields set to None from output |
| Exclude unset | Omit fields not explicitly provided in the request |
| Filtering | Controlling which fields appear in the API response |
| HATEOAS | Hypermedia links in responses for API discoverability |
| Password leak | Accidentally exposing sensitive data in API responses |
| Response model | Pydantic model defining the shape of API responses |
| Serialization | Converting Python objects to JSON |
| Swagger schema | OpenAPI schema generated from response models |
| UserIn | Pydantic model for incoming (request) data |
| UserOut | Pydantic model for outgoing (response) data |
| Validation | Checking data matches expected types and constraints |

---

## Detailed Term Definitions

### BaseModel

**Definition:** The base class from Pydantic that you inherit from to define structured data models. In the context of response models, it defines what fields are included in API responses.

**Example:**
```python
from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool


# This model defines the response shape
# Any extra fields from the data source are filtered out
```

**Related terms:** Response Model, Validation, Serialization

---

### Computed Field

**Definition:** A field that is calculated or added in the path operation function rather than stored in the database. Response models can include these computed fields.

**Example:**
```python
class UserOutWithMeta(BaseModel):
    id: int
    name: str
    email: str
    profile_url: str = ""  # Computed in the function


@app.get("/users/{user_id}/profile", response_model=UserOutWithMeta)
def get_user_profile(user_id: int):
    user = users_db[user_id].copy()
    user["profile_url"] = f"/users/{user_id}/profile"  # Computed
    return user


# Response includes the computed profile_url field
```

**Related terms:** Response Model, HATEOAS, Metadata

---

### Exclude Defaults

**Definition:** A `response_model` option that omits fields whose values match their default values from the API response.

**Example:**
```python
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True  # Default value
    tags: list[str] = []  # Default value


@app.post("/items/", response_model=Item, response_model_exclude_defaults=True)
def create_item(item: Item):
    return item


# Request: {"name": "Widget", "price": 9.99}
# Response: {"name": "Widget", "price": 9.99}
# in_stock and tags excluded because they match defaults
```

**Related terms:** Exclude Unset, Exclude None

---

### Exclude None

**Definition:** A `response_model` option that omits fields with `None` values from the API response. Useful for cleaning up optional fields.

**Example:**
```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/items/list", response_model=list[Item], response_model_exclude_none=True)
def list_items():
    return [
        Item(name="Laptop", description="A laptop", price=999.99, tax=89.99),
        Item(name="Phone", price=699.99),  # description=None, tax=None
    ]


# Response:
# [
#   {"name": "Laptop", "description": "A laptop", "price": 999.99, "tax": 89.99},
#   {"name": "Phone", "price": 699.99}
# ]
```

**Related terms:** Exclude Unset, Exclude Defaults

---

### Exclude Unset

**Definition:** A `response_model` option that omits fields that were not explicitly provided in the request body. Only fields that were actually sent appear in the response.

**Example:**
```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/", response_model=Item, response_model_exclude_unset=True)
def create_item(item: Item):
    return item


# Request: {"name": "Widget", "price": 9.99}
# Response: {"name": "Widget", "price": 9.99}
# description and tax omitted because they weren't sent
```

**Related terms:** Exclude None, Exclude Defaults, PATCH

---

### Filtering

**Definition:** The process of controlling which fields from internal data are included in API responses. Response models perform automatic field filtering.

**Example:**
```python
class UserDB(BaseModel):
    id: int
    name: str
    email: str
    password: str  # Sensitive — should NOT be in response
    internal_note: str  # Internal — should NOT be in response


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    # password and internal_note are filtered out


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    return users_db[user_id]  # All internal fields are filtered
```

**Related terms:** Response Model, Security, Data Protection

---

### HATEOAS (Hypermedia as the Engine of Application State)

**Definition:** A REST API design pattern where responses include hyperlinks to related resources, allowing clients to navigate the API dynamically.

**Example:**
```python
class UserOutWithLinks(BaseModel):
    id: int
    name: str
    email: str
    links: dict = {}


@app.get("/users/{user_id}", response_model=UserOutWithLinks)
def get_user(user_id: int):
    user = users_db[user_id].copy()
    user["links"] = {
        "self": f"/users/{user_id}",
        "orders": f"/users/{user_id}/orders",
        "profile": f"/users/{user_id}/profile",
    }
    return user
```

**Related terms:** Computed Field, API Design, REST

---

### Password Leak

**Definition:** An API security vulnerability where sensitive data like passwords, API keys, or tokens are accidentally included in API responses. This is one of the most common API security issues.

**Example:**
```python
# DANGEROUS: Password leaked in response
@app.post("/users/")
def create_user(user: UserIn):
    return user.model_dump()  # Includes password!


# SAFE: response_model filters password
@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn):
    user_dict = user.model_dump()
    user_dict["id"] = 1
    return user_dict  # Password filtered by response_model
```

**Prevention:**
1. Always use `response_model` to define response shape
2. Never return the full request model as response
3. Define UserOut without sensitive fields
4. Use `response_model_exclude={"password"}` for quick filtering

**Related terms:** Security, Response Model, Data Protection

---

### Response Model

**Definition:** A Pydantic model that defines the shape and constraints of API response data. Specified using the `response_model` parameter in path operation decorators.

**Example:**
```python
class UserOut(BaseModel):
    id: int
    name: str
    email: str


# Single response
@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    return users_db[user_id]


# List response
@app.get("/users/", response_model=list[UserOut])
def list_users():
    return list(users_db.values())


# With exclude options
@app.post("/items/", response_model=Item, response_model_exclude_unset=True)
def create_item(item: Item):
    return item
```

**Options:**

| Parameter | Description |
|-----------|-------------|
| `response_model` | The Pydantic model class |
| `response_model_exclude_unset` | Only explicitly set fields |
| `response_model_exclude_none` | Omit None values |
| `response_model_exclude_defaults` | Omit default values |
| `response_model_exclude` | Exclude specific fields |

**Related terms:** BaseModel, Filtering, OpenAPI, Security

---

### Serialization

**Definition:** The process of converting Python objects (Pydantic models, dicts, lists) into JSON format for HTTP responses. FastAPI handles serialization automatically.

**Example:**
```python
class Item(BaseModel):
    name: str
    price: float


@app.get("/item")
def get_item():
    item = Item(name="Widget", price=9.99)
    return item  # Automatically serialized to JSON
    # Response: {"name": "Widget", "price": 9.99}
```

**Related terms:** JSON, Response Model, model_dump()

---

### Swagger Schema

**Definition:** The OpenAPI schema generated by FastAPI from your response models. It defines the response format in Swagger UI and ReDoc, enabling client code generation.

**Example:**
```python
@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """Get a user by ID.

    The Swagger UI will show the UserOut schema
    as the response format.
    """
    return users_db[user_id]


# Swagger UI shows:
# Response: UserOut { id: integer, name: string, email: string }
```

**Related terms:** OpenAPI, Documentation, Response Model

---

### UserIn

**Definition:** A Pydantic model naming convention for models that define incoming request data (what the client sends). Often contains sensitive fields like passwords.

**Example:**
```python
class UserIn(BaseModel):
    """What the client sends."""

    name: str
    email: str
    password: str  # Only in request, not in response
    age: int


@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn):
    # 'user' is a UserIn instance
    # But response is filtered to UserOut
    return {"id": 1, **user.model_dump()}
```

**Related terms:** UserOut, Request Body, Response Model

---

### UserOut

**Definition:** A Pydantic model naming convention for models that define outgoing response data (what the client receives). Excludes sensitive fields.

**Example:**
```python
class UserOut(BaseModel):
    """What the client receives — no password."""

    id: int
    name: str
    email: str
    is_active: bool
    created_at: str


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    return users_db[user_id]
```

**Related terms:** UserIn, Response Model, Filtering

---

### Validation

**Definition:** The process of checking that data matches expected types and constraints. Response models validate the response data before sending it to the client.

**Example:**
```python
class UserOut(BaseModel):
    id: int
    name: str
    email: str


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = users_db[user_id]
    # If user has extra fields → filtered by response_model
    # If user is missing fields → validation error
    return user
```

**Two types:**
1. **Request validation**: Checking incoming data
2. **Response validation**: Checking outgoing data (from response_model)

**Related terms:** Response Model, Type Hints, Pydantic

---

## Response Model Options

| Option | Effect | Use Case |
|--------|--------|----------|
| `response_model=X` | Filter to model fields | Default, always use |
| `response_model_exclude_unset=True` | Only explicitly set fields | PATCH endpoints |
| `response_model_exclude_none=True` | Omit None values | Clean optional fields |
| `response_model_exclude_defaults=True` | Omit defaults | Minimal responses |
| `response_model_exclude={"field"}` | Exclude specific fields | Quick filtering |

---

## Response Model Patterns

### Pattern: Basic Response Model
```python
@app.get("/users/{id}", response_model=UserOut)
def get_user(id: int): ...
```

### Pattern: List Response
```python
@app.get("/users/", response_model=list[UserOut])
def list_users(): ...
```

### Pattern: Create with Filtered Response
```python
@app.post("/users/", response_model=UserOut, status_code=201)
def create_user(user: UserIn): ...
```

### Pattern: Exclude Unset (PATCH)
```python
@app.patch("/users/{id}", response_model=UserOut, response_model_exclude_unset=True)
def update_user(id: int, user: UserUpdate): ...
```

### Pattern: Computed Fields
```python
class UserOutWithLinks(BaseModel):
    id: int
    name: str
    links: dict = {}


@app.get("/users/{id}", response_model=UserOutWithLinks)
def get_user(id: int):
    user = db[id].copy()
    user["links"] = {"self": f"/users/{id}"}
    return user
```

---

*End of Glossary — Lecture 06: Response Model*
