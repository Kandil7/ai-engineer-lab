# Glossary: Lecture 07 — Form Data

Alphabetical reference of all key terms from the Form Data lecture.

---

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| Checkbox | HTML input type for boolean (on/off) selections |
| Content-Type | HTTP header indicating the media type of request data |
| Dropdown | HTML select element for choosing from predefined options |
| Form data | Data submitted via HTML forms (key-value pairs) |
| Form() | FastAPI function for declaring form data parameters |
| HTML form | An HTML element that collects user input for submission |
| HTMLResponse | FastAPI response class for serving HTML content |
| Multipart | Form encoding that supports file uploads |
| Textarea | HTML input for multi-line text |
| URL-encoded | Form encoding for text-only form data |
| Validation | Checking form data matches expected types and constraints |
| python-multipart | Python package required for form data handling |

---

## Detailed Term Definitions

### Checkbox

**Definition:** An HTML input element that allows users to select or deselect an option. In FastAPI, checkboxes are handled as boolean form fields.

**HTML:**
```html
<label>
    <input type="checkbox" name="subscribe" value="true">
    Subscribe to newsletter
</label>
```

**FastAPI:**
```python
@app.post("/feedback/")
def feedback(subscribe: bool = Form(default=False)):
    return {"subscribed": subscribe}
```

**Notes:**
- If checked, value is `"true"` → converted to `True`
- If unchecked, the field is not sent → uses default `False`

**Related terms:** Boolean, Form(), Default Value

---

### Content-Type

**Definition:** An HTTP header that specifies the media type of the request body. For form data, the Content-Type determines how the data is encoded.

**Form Content-Types:**

| Type | Description |
|------|-------------|
| `application/x-www-form-urlencoded` | Standard form submission (text only) |
| `multipart/form-data` | Form with file uploads |

**Example:**
```bash
# URL-encoded form data
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"

# Or just use -d (curl defaults to url-encoded)
curl -X POST http://localhost:8000/login/ \
  -d "username=admin&password=secret"
```

**Related terms:** Form Data, Multipart, URL-encoded

---

### Dropdown (Select)

**Definition:** An HTML `<select>` element that presents a list of predefined options for the user to choose one.

**HTML:**
```html
<select name="role">
    <option value="user">User</option>
    <option value="admin">Admin</option>
    <option value="moderator">Moderator</option>
</select>
```

**FastAPI:**
```python
@app.post("/register/")
def register(role: str = Form(default="user")):
    valid_roles = ["user", "admin", "moderator"]
    if role not in valid_roles:
        raise HTTPException(status_code=400, detail="Invalid role")
    return {"role": role}
```

**Related terms:** Form Data, Validation, Enum

---

### Form Data

**Definition:** Data submitted via HTML forms using either `application/x-www-form-urlencoded` or `multipart/form-data` encoding. Unlike JSON, form data is flat key-value pairs.

**Example:**
```python
@app.post("/contact/")
def contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    return {"name": name, "email": email, "message_length": len(message)}
```

**curl example:**
```bash
curl -X POST http://localhost:8000/contact/ \
  -d "name=Alice&email=alice@test.com&message=Hello+FastAPI"
```

**Characteristics:**
- Flat key-value pairs (no nesting)
- Values are always strings (FastAPI converts types)
- Supports file uploads with multipart encoding
- Native to HTML forms

**Related terms:** Form(), Content-Type, URL-encoded

---

### Form() Function

**Definition:** A FastAPI function that declares a parameter as form data. Required for all form fields in an endpoint.

**Example:**
```python
from fastapi import Form


# Required form field
@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


# Optional form field with default
@app.post("/contact/")
def contact(
    name: str = Form(...),
    subject: str = Form(default="General"),
):
    return {"name": name, "subject": subject}


# With validation constraints
@app.post("/register/")
def register(
    username: str = Form(..., min_length=3, max_length=20),
    password: str = Form(..., min_length=8),
):
    return {"username": username}
```

**Parameters:**

| Parameter | Description |
|-----------|-------------|
| `...` | Required field (no default) |
| `default` | Default value |
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `description` | Description for Swagger docs |

**Related terms:** Form Data, Validation, python-multipart

---

### HTML Form

**Definition:** An HTML `<form>` element that collects user input and submits it to a server. FastAPI can serve HTML forms and handle their submissions.

**Example:**
```python
from fastapi.responses import HTMLResponse


@app.get("/form", response_class=HTMLResponse)
def get_form():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Contact Form</title></head>
    <body>
        <h1>Contact Us</h1>
        <form action="/contact/" method="post">
            <label>Name: <input type="text" name="name" required></label><br><br>
            <label>Email: <input type="email" name="email" required></label><br><br>
            <label>Message:<br>
                <textarea name="message" required minlength="10"></textarea>
            </label><br><br>
            <label><input type="checkbox" name="subscribe" value="true">
                Subscribe</label><br><br>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """


@app.post("/contact/")
def contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    subscribe: bool = Form(default=False),
):
    return {"status": "received", "name": name}
```

**Related terms:** HTMLResponse, Form(), Method

---

### HTMLResponse

**Definition:** A FastAPI response class that sends HTML content to the client with the correct `Content-Type: text/html` header.

**Example:**
```python
from fastapi.responses import HTMLResponse


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head><title>My App</title></head>
    <body>
        <h1>Welcome to My FastAPI App</h1>
        <a href="/form">Go to Contact Form</a>
    </body>
    </html>
    """
```

**Related terms:** HTML Form, Response, Content-Type

---

### Multipart

**Definition:** A form encoding type (`multipart/form-data`) that supports both text fields and file uploads. Required when forms include `<input type="file">`.

**Example:**
```html
<!-- Multipart form with file upload -->
<form action="/upload/" method="post" enctype="multipart/form-data">
    <input type="text" name="description">
    <input type="file" name="file">
    <button type="submit">Upload</button>
</form>
```

**FastAPI:**
```python
from fastapi import Form, UploadFile, File


@app.post("/upload/")
async def upload(
    description: str = Form(...),
    file: UploadFile = File(...),
):
    return {"description": description, "filename": file.filename}
```

**curl example:**
```bash
curl -X POST http://localhost:8000/upload/ \
  -F "description=My document" \
  -F "file=@document.pdf"
```

**Related terms:** Form Data, UploadFile, File()

---

### Textarea

**Definition:** An HTML `<textarea>` element for multi-line text input. In FastAPI, textarea values are submitted as regular string form fields.

**HTML:**
```html
<label>Message:<br>
    <textarea name="message" rows="5" cols="40"
              required minlength="10" maxlength="500">
    </textarea>
</label>
```

**FastAPI:**
```python
@app.post("/contact/")
def contact(message: str = Form(..., min_length=10, max_length=500)):
    return {"message_length": len(message)}
```

**Related terms:** Form Data, Validation, Text Input

---

### URL-encoded

**Definition:** The default form encoding (`application/x-www-form-urlencoded`) where form data is sent as key-value pairs with special characters escaped. Suitable for text-only forms.

**Example:**
```bash
# URL-encoded form data
curl -X POST http://localhost:8000/login/ \
  -d "username=admin&password=secret"

# Multiple fields
curl -X POST http://localhost:8000/contact/ \
  -d "name=Alice+Smith&email=alice%40test.com&subject=Hello"
```

**Encoding rules:**
- Spaces → `+` or `%20`
- `@` → `%40`
- `&` → `%26` (within values)

**Related terms:** Multipart, Form Data, Content-Type

---

### Validation

**Definition:** The process of checking that form data matches expected types, lengths, and constraints. FastAPI performs validation automatically using `Form()` parameters.

**Example:**
```python
@app.post("/register/")
def register(
    username: str = Form(..., min_length=3, max_length=20),
    email: str = Form(...),
    password: str = Form(..., min_length=8),
    role: str = Form(default="user"),
):
    valid_roles = ["user", "admin", "moderator"]
    if role not in valid_roles:
        raise HTTPException(status_code=400, detail="Invalid role")
    return {"username": username}
```

**Validation levels:**
1. **Type validation**: Automatic (str, int, bool)
2. **Constraint validation**: min_length, max_length, ge, le
3. **Business validation**: Custom logic in the function body

**Related terms:** Form(), Constraints, HTTPException

---

### python-multipart

**Definition:** A Python package required by FastAPI to parse form data and file uploads. Must be installed separately from FastAPI.

**Installation:**
```bash
pip install python-multipart
```

**Why it's separate:**
- Not all FastAPI apps need form handling
- Reduces dependencies for JSON-only APIs
- Only imported when form data is used

**Common error without it:**
```
ImportError: 'python-multipart' must be installed to use form data
```

**Related terms:** Form Data, UploadFile, Dependencies

---

## Form Data Patterns

### Pattern: Login Form
```python
@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "secret":
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

### Pattern: Contact Form
```python
@app.post("/contact/")
def contact(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(default="General"),
    message: str = Form(..., min_length=10),
    subscribe: bool = Form(default=False),
): ...
```

### Pattern: Registration
```python
@app.post("/register/")
def register(
    username: str = Form(..., min_length=3, max_length=20),
    email: str = Form(...),
    password: str = Form(..., min_length=8),
    confirm_password: str = Form(...),
    role: str = Form(default="user"),
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")
    return {"username": username, "role": role}
```

### Pattern: Serve HTML Form
```python
@app.get("/form", response_class=HTMLResponse)
def get_form():
    return """
    <form action="/submit/" method="post">
        <input type="text" name="field" required>
        <button type="submit">Submit</button>
    </form>
    """
```

### Pattern: Feedback
```python
@app.post("/feedback/")
def feedback(
    rating: int = Form(..., ge=1, le=5),
    comment: str = Form(default=""),
    recommend: bool = Form(default=True),
): ...
```

---

*End of Glossary — Lecture 07: Form Data*
