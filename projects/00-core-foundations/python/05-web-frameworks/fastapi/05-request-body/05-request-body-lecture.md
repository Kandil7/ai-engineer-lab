# Lecture 05: Request Body

## Topic Overview

When clients send data to your API (creating or updating resources), they send it in the request body. FastAPI uses Pydantic models to define, validate, and parse request bodies automatically. This lecture covers simple and complex request bodies, nested models, partial updates, multiple body parameters, and field-level validation with examples.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define Pydantic models for request body validation
2. Use `Field()` for field-level validation and documentation
3. Create nested Pydantic models for complex data structures
4. Handle full updates (PUT) and partial updates (PATCH)
5. Use `model_dump(exclude_unset=True)` for partial updates
6. Receive list request bodies
7. Add field examples for better Swagger documentation
8. Distinguish between request models and response models

---

## Key Concepts

### 1. Pydantic Models for Request Bodies

When a function parameter is a Pydantic model, FastAPI reads the request body as JSON and validates it.

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    bio: str | None = None
    is_active: bool = True


@app.post("/users/", status_code=201)
def create_user(user: UserCreate):
    # 'user' is automatically validated and parsed from JSON
    return {"id": 1, **user.model_dump()}
```

### 2. Field-Level Validation with Field()

`Field()` provides constraints and metadata for individual model fields:

```python
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., description="Email address")
    age: int = Field(..., ge=0, le=150, description="User's age")
    bio: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
```

**Common Field constraints:**

| Constraint | Description |
|-----------|-------------|
| `...` | Required field (no default) |
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `gt` | Greater than (exclusive) |
| `ge` | Greater than or equal |
| `lt` | Less than (exclusive) |
| `le` | Less than or equal |
| `pattern` | Regex pattern |
| `description` | Description in docs |

### 3. Nested Pydantic Models

Models can contain other models for complex, hierarchical data:

```python
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


class OrderItem(BaseModel):
    product_name: str
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., gt=0)


class Order(BaseModel):
    customer_name: str
    items: list[OrderItem]
    shipping_address: Address
    notes: str | None = None
```

**Nested JSON example:**
```json
{
    "customer_name": "Bob",
    "items": [
        {"product_name": "Keyboard", "quantity": 2, "unit_price": 79.99}
    ],
    "shipping_address": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62701"
    }
}
```

### 4. PUT vs PATCH (Full vs Partial Update)

```python
# PUT = full replacement (all fields required)
@app.put("/users/{user_id}")
def full_update(user_id: int, user: UserCreate):
    # Client must send ALL fields
    users_db[user_id] = user.model_dump()
    return users_db[user_id]


# PATCH = partial update (only changed fields)
@app.patch("/users/{user_id}")
def partial_update(user_id: int, user: UserUpdate):
    # Client sends only fields to change
    update_data = user.model_dump(exclude_unset=True)
    users_db[user_id].update(update_data)
    return users_db[user_id]
```

### 5. model_dump(exclude_unset=True)

This method returns only fields that were explicitly set in the request, ignoring defaults:

```python
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None


@app.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    update_data = user.model_dump(exclude_unset=True)
    # If only name was sent: {"name": "New Name"}
    # Defaults (None) are excluded
    users_db[user_id].update(update_data)
    return users_db[user_id]
```

### 6. List Request Bodies

Receive a list of items as the request body:

```python
@app.post("/batch-create")
def batch_create(users: list[UserCreate]):
    """Receive a list of users as JSON array."""
    created = []
    for user in users:
        user_dict = user.model_dump()
        user_dict["id"] = len(created) + 1
        created.append(user_dict)
    return {"created_count": len(created), "users": created}
```

### 7. Field Examples for Swagger

Add example values that appear in Swagger UI:

```python
class ProductCreate(BaseModel):
    name: str = Field(..., examples=["Wireless Mouse"])
    description: str = Field(default="", examples=["Ergonomic wireless mouse"])
    price: float = Field(..., gt=0, examples=[29.99])
    tags: list[str] = Field(default=[], examples=[["electronics", "peripherals"]])
```

### 8. Separate Request and Response Models

Always define separate models for input and output:

```python
class UserIn(BaseModel):
    """What the client sends."""

    name: str
    email: str
    password: str  # Sensitive — should NOT be in response


class UserOut(BaseModel):
    """What the client receives."""

    id: int
    name: str
    email: str


@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn):
    # password is received but NOT sent back
    ...
```

---

## Code Examples

### Example 1: Complete User CRUD

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., description="User's email")
    age: int = Field(..., ge=0, le=150)
    bio: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    email: str | None = None
    age: int | None = Field(default=None, ge=0, le=150)
    bio: str | None = None


users_db: dict[int, dict] = {}
next_id = 1


@app.post("/users/", status_code=201)
def create_user(user: UserCreate):
    global next_id
    user_dict = user.model_dump()
    user_dict["id"] = next_id
    user_dict["created_at"] = datetime.now().isoformat()
    users_db[next_id] = user_dict
    next_id += 1
    return user_dict


@app.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.model_dump(exclude_unset=True)
    users_db[user_id].update(update_data)
    return users_db[user_id]
```

### Example 2: Nested Order Model

```python
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


class OrderItem(BaseModel):
    product_name: str
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., gt=0)


class Order(BaseModel):
    customer_name: str
    items: list[OrderItem]
    shipping_address: Address
    notes: str | None = None


@app.post("/orders/")
def create_order(order: Order):
    total = sum(item.quantity * item.unit_price for item in order.items)
    return {
        "id": 1,
        "customer": order.customer_name,
        "total": round(total, 2),
        "items": [item.model_dump() for item in order.items],
    }
```

### Example 3: Batch Create

```python
@app.post("/batch-create")
def batch_create(users: list[UserCreate]):
    created = []
    for user in users:
        user_dict = user.model_dump()
        user_dict["id"] = len(created) + 1
        created.append(user_dict)
    return {"created_count": len(created), "users": created}


# Request body: JSON array
# [{"name": "Alice", "email": "a@test.com", "age": 30},
#  {"name": "Bob", "email": "b@test.com", "age": 25}]
```

---

## Common Mistakes to Avoid

### Mistake 1: Sending password in response
```python
# Wrong: Password leaks in response
@app.post("/users/")
def create_user(user: UserCreate):
    return user.model_dump()  # Includes password!


# Fix: Use response_model to filter
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate):
    return user.model_dump()  # Password excluded
```

### Mistake 2: Confusing PUT and PATCH
```python
# PUT: All fields required (full replacement)
@app.put("/users/{user_id}")
def update(user_id: int, user: UserCreate): ...  # Client must send ALL fields


# PATCH: Only changed fields (partial update)
@app.patch("/users/{user_id}")
def patch(user_id: int, user: UserUpdate):
    update_data = user.model_dump(exclude_unset=True)
    ...
```

### Mistake 3: Not using Field() for validation
```python
# Wrong: No constraints on age
class User(BaseModel):
    age: int  # Could be -1000!


# Fix: Use Field() constraints
class User(BaseModel):
    age: int = Field(..., ge=0, le=150)
```

### Mistake 4: Forgetting to handle nested validation
```python
# If OrderItem.quantity is negative, the entire Order validation fails
# FastAPI validates the entire nested structure automatically
class Order(BaseModel):
    items: list[OrderItem]  # Each OrderItem is validated


# Ensure nested models have their own validation
class OrderItem(BaseModel):
    quantity: int = Field(..., ge=1)  # Validated!
```

---

## Best Practices

1. **Always define separate models** for request input vs response output
2. **Use `Field()` constraints** — never trust client input
3. **Use `response_model`** to filter sensitive fields from responses
4. **Use `exclude_unset=True`** for PATCH operations
5. **Add `description`** to Field() for better Swagger docs
6. **Add `examples`** to Field() for interactive documentation
7. **Handle nested models** with their own validation
8. **Return 201** for successful creation, **200** for updates

---

## Practice Exercises

### Exercise 1: Product API
Create a Product model with: name (required), price (required, >0), description (optional), category (required), in_stock (default True), tags (list, default []).

### Exercise 2: Blog Post
Create a BlogPost model with: title (required), content (required, min 10 chars), author (required), tags (list), published (default False).

### Exercise 3: Nested Model
Create a Comment model with: author (UserCreate), text (required), likes (int, default 0).

### Exercise 4: Partial Update
Implement PATCH endpoint for updating only provided fields.

### Exercise 5: Batch Operation
Create endpoint that accepts a list of items and processes them.

---

## Summary

| Concept | Description |
|---------|-------------|
| Pydantic model | Defines request body structure with validation |
| `Field()` | Field-level validation and documentation |
| Nested models | Complex hierarchical data structures |
| PUT | Full replacement (all fields required) |
| PATCH | Partial update (only changed fields) |
| `exclude_unset=True` | Only include explicitly set fields |
| `response_model` | Filter output fields |
| `examples` | Swagger UI example values |

Request bodies are where FastAPI's Pydantic integration truly shines — automatic validation, serialization, and documentation with minimal code.

---

## Quick Reference

```python
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., description="Email address")
    age: int = Field(..., ge=0, le=150)
    bio: str | None = Field(default=None, max_length=500)


@app.post("/users/", status_code=201)
def create_user(user: UserCreate):
    return user.model_dump()


@app.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    update_data = user.model_dump(exclude_unset=True)
    users_db[user_id].update(update_data)
    return users_db[user_id]
```
