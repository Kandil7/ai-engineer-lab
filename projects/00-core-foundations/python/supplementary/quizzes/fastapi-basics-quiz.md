# FastAPI Basics Quiz

## Topic Overview
FastAPI is a modern, high-performance Python web framework for building APIs. It leverages Python's type hints for automatic validation, documentation, and serialization. This quiz covers the fundamentals including route handling, request/response models, dependency injection, and async patterns.

**Difficulty:** Beginner to Intermediate
**Questions:** 20
**Time:** ~25 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What is FastAPI primarily designed for?**

A) Building desktop applications
B) Building high-performance REST APIs
C) Machine learning model training
D) Database administration

**Correct Answer:** B
**Explanation:** FastAPI is specifically designed for building high-performance REST APIs with automatic OpenAPI documentation, validation, and serialization.

---

### Question 2 [Easy]
**Which decorator is used to create a GET endpoint in FastAPI?**

A) `@app.post()`
B) `@app.get()`
C) `@app.route()`
D) `@app.handle()`

**Correct Answer:** B
**Explanation:** `@app.get()` creates a GET endpoint. FastAPI provides specific decorators for each HTTP method: `get()`, `post()`, `put()`, `patch()`, `delete()`.

---

### Question 3 [Easy]
**What Python feature does FastAPI heavily leverage for automatic validation?**

A) Decorators only
B) Type hints
C) Global variables
D) Metaclasses

**Correct Answer:** B
**Explanation:** FastAPI uses Python type hints extensively. You define function parameters with types, and FastAPI automatically validates incoming data against those types.

---

### Question 4 [Medium]
**How do you define a request body model in FastAPI?**

A) Using a regular Python class inheriting from `dict`
B) Using a Pydantic `BaseModel`
C) Using a dataclass with `@dataclass`
D) Using a TypedDict

**Correct Answer:** B
**Explanation:** FastAPI uses Pydantic's `BaseModel` for request body validation. Pydantic models provide automatic validation, serialization, and documentation generation.

```python
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False
```

---

### Question 5 [Medium]
**What is the purpose of `Depends` in FastAPI?**

A) To add middleware to requests
B) To define reusable logic for dependency injection
C) To create background tasks
D) To configure CORS

**Correct Answer:** B
**Explanation:** `Depends` is used for dependency injection. It allows you to declare dependencies that FastAPI will automatically resolve and inject into your endpoint functions.

---

### Question 6 [Medium]
**Which of the following correctly defines a path parameter?**

A) `@app.get("/items/{item_id}")`
B) `@app.get("/items?<item_id>")`
C) `@app.get("/items/:item_id")`
D) `@app.get("/items/{item_id}?")`

**Correct Answer:** A
**Explanation:** FastAPI uses curly braces `{}` for path parameters. The parameter is extracted from the URL path and can be typed: `def read_item(item_id: int):`

---

### Question 7 [Easy]
**How do you install FastAPI?**

A) `pip install fastapi`
B) `npm install fastapi`
C) `apt install fastapi`
D) `conda install fastapi`

**Correct Answer:** A
**Explanation:** FastAPI is a Python package installed via pip. You typically also install an ASGI server like `uvicorn` with `pip install uvicorn[standard]`.

---

### Question 8 [Medium]
**What does `response_model` do in an endpoint decorator?**

A) Defines the database schema for responses
B) Validates and serializes the return value against the model
C) Sets the HTTP response code
D) Configures caching headers

**Correct Answer:** B
**Explanation:** `response_model` validates and serializes the endpoint's return value. It filters out extra fields and ensures the response matches the defined schema in the OpenAPI docs.

---

### Question 9 [Medium]
**How do you run a FastAPI application with uvicorn?**

A) `python app.py`
B) `uvicorn main:app --reload`
C) `fastapi run app.py`
D) `node app.js`

**Correct Answer:** B
**Explanation:** `uvicorn main:app --reload` runs the ASGI server. `main` is the Python file, `app` is the FastAPI instance, and `--reload` enables auto-reload during development.

---

### Question 10 [Hard]
**What is the difference between `async def` and `def` for endpoint functions in FastAPI?**

A) No difference; both are treated identically
B) `async def` runs in a threadpool, `def` runs directly
C) `def` runs in a threadpool, `async def` runs in the event loop
D) `async def` is required for all endpoints

**Correct Answer:** C
**Explanation:** When you define an endpoint with `async def`, it runs directly in the event loop. With `def`, FastAPI automatically runs it in a threadpool to avoid blocking the event loop. Use `async def` only if you actually use `await` inside.

---

### Question 11 [Easy]
**What is the default port when running uvicorn without specifying one?**

A) 80
B) 3000
C) 5000
D) 8000

**Correct Answer:** D
**Explanation:** Uvicorn defaults to port 8000. You can specify a different port with `uvicorn main:app --port 8080`.

---

### Question 12 [Hard]
**Which of the following is the correct way to handle file uploads?**

A) Using `UploadFile` type hint with `File()`
B) Using `bytes` type hint with `File()`
C) Using `str` type hint with `File()`
D) Using `list` type hint with `File()`

**Correct Answer:** A
**Explanation:** `UploadFile` provides a file-like interface with `.read()`, `.write()`, `.filename`, and `.content_type`. Using `bytes` with `File()` loads the entire file into memory, while `UploadFile` uses a temporary file for large uploads.

```python
from fastapi import File, UploadFile


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename}
```

---

### Question 13 [Medium]
**What does `status_code=201` in a decorator do?**

A) Returns a 201 status code on success
B) Validates the response status is 201
C) Raises an error if status is not 201
D) Logs the status code

**Correct Answer:** A
**Explanation:** `status_code=201` sets the HTTP response status code to 201 Created when the endpoint successfully processes the request.

---

### Question 14 [Easy]
**How do you access query parameters in FastAPI?**

A) They are passed as a dictionary
B) They are declared as function parameters
C) You must use `request.query_params`
D) Query parameters are not supported

**Correct Answer:** B
**Explanation:** Query parameters are declared as function parameters with default values. FastAPI automatically parses them from the URL query string.

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

---

### Question 15 [Hard]
**What is the purpose of `APIRouter` in FastAPI?**

A) To route requests to different HTTP methods
B) To organize endpoints into separate modules
C) To add authentication middleware
D) To configure database connections

**Correct Answer:** B
**Explanation:** `APIRouter` allows you to split your application into separate files/modules. You create routers with `APIRouter()`, define endpoints on them, and include them in the main app with `app.include_router()`.

---

### Question 16 [Medium]
**How do you raise an HTTP exception in FastAPI?**

A) `raise HTTPException(status_code=404, detail="Not found")`
B) `return error(404, "Not found")`
C) `response(404)`
D) `abort(404)`

**Correct Answer:** A
**Explanation:** `HTTPException` from `fastapi` is the standard way to raise HTTP errors. It stops request processing and returns the specified status code and detail message.

---

### Question 17 [Easy]
**What is the automatic interactive documentation URL for a FastAPI app?**

A) `/api/docs`
B) `/swagger-ui`
C) `/docs`
D) All of the above

**Correct Answer:** C
**Explanation:** FastAPI serves only `/docs` (Swagger UI) and `/redoc` (ReDoc) by default. `/api/docs` and `/swagger-ui` are not served unless you explicitly reconfigure the docs URLs.

---

### Question 18 [Hard]
**Which middleware handles CORS in FastAPI?**

A) `CORSMiddleware`
B) `SecurityMiddleware`
C) `SessionMiddleware`
D) `CacheMiddleware`

**Correct Answer:** A
**Explanation:** `CORSMiddleware` handles Cross-Origin Resource Sharing. You configure it with allowed origins, methods, and headers, then add it to the app with `app.add_middleware()`.

---

### Question 19 [Medium]
**How do you define a Pydantic model for query parameter validation?**

A) Using `Query()` parameters directly
B) Using `Depends()` with a Pydantic model
C) Both A and B
D) Query parameters cannot use Pydantic models

**Correct Answer:** C
**Explanation:** You can use `Query()` for individual parameters or `Depends()` with a Pydantic model to group and validate multiple query parameters together.

---

### Question 20 [Hard]
**What is the purpose of `BackgroundTasks` in FastAPI?**

A) To schedule cron jobs
B) To run code after the response has been sent
C) To parallelize endpoint execution
D) To manage database connections

**Correct Answer:** B
**Explanation:** `BackgroundTasks` lets you run functions after the response is sent to the client. Useful for sending emails, logging, or any post-response work that shouldn't delay the response.

```python
from fastapi import BackgroundTasks


def send_email(email: str, message: str):
    # Send email logic here
    pass


@app.post("/send-notification/")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "Hello!")
    return {"message": "Notification sent in background"}
```

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | B |
| 2 | B |
| 3 | B |
| 4 | B |
| 5 | B |
| 6 | A |
| 7 | A |
| 8 | B |
| 9 | B |
| 10 | C |
| 11 | D |
| 12 | A |
| 13 | A |
| 14 | B |
| 15 | B |
| 16 | A |
| 17 | D |
| 18 | A |
| 19 | C |
| 20 | B |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered FastAPI basics! |
| 14-17 | Proficient - Solid understanding, review advanced topics |
| 10-13 | Developing - Good foundation, practice more |
| 6-9 | Beginner - Review the fundamentals |
| 0-5 | Novice - Start with FastAPI documentation |

---

*Quiz created for AI Engineer Lab - Python Foundations*
