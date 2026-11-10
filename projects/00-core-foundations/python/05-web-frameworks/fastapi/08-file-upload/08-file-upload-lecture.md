# Lecture 08: File Upload

## Topic Overview

File uploads are essential for applications that handle images, documents, videos, or any binary data. FastAPI provides `UploadFile` and `File()` for handling multipart form uploads with streaming support, MIME type validation, and memory-efficient processing. This lecture covers single and multiple file uploads, type validation, size limits, streaming large files, and organizing uploaded files.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `UploadFile` and `File()` for file uploads
2. Handle single and multiple file uploads
3. Validate file types (MIME types) and sizes
4. Stream large files without loading into memory
5. Save files to disk with proper naming
6. Combine file uploads with form data
7. List and manage uploaded files
8. Calculate file hashes (MD5) for integrity

---

## Key Concepts

### 1. UploadFile Class

`UploadFile` is a file-like object that FastAPI provides for handling uploaded files:

```python
from fastapi import UploadFile, File


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()  # Read entire file
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
    }
```

**UploadFile attributes:**

| Attribute | Description |
|-----------|-------------|
| `filename` | Original filename from the client |
| `content_type` | MIME type (e.g., "image/jpeg") |
| `file` | SpooledTemporaryFile (file-like object) |

**UploadFile methods:**

| Method | Description |
|--------|-------------|
| `await file.read()` | Read entire file content |
| `await file.read(size)` | Read specified number of bytes |
| `await file.write(data)` | Write data to the file |
| `await file.seek(offset)` | Move to position in file |
| `await file.close()` | Close the file |

### 2. File() Function

`File()` is used to declare a file parameter. It works with `UploadFile` for file objects or `bytes` for raw file content.

```python
from fastapi import File, UploadFile


# Using UploadFile (recommended)
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {"size": len(content)}


# Using bytes (loads entire file into memory)
@app.post("/upload-raw/")
async def upload_raw(file: bytes = File(...)):
    return {"size": len(file)}
```

**When to use which:**
- `UploadFile`: Better for large files, provides metadata, streaming
- `bytes`: Simpler for small files, but loads everything into memory

### 3. MIME Type Validation

Validate file types using the `content_type` attribute:

```python
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {ALLOWED_TYPES}",
        )
    content = await file.read()
    # Process image...
    return {"filename": file.filename, "content_type": file.content_type}
```

### 4. File Size Validation

Check file size before processing:

```python
@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    max_size = 5 * 1024 * 1024  # 5MB
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="File too large. Max 5MB.")
    # Process file...
```

### 5. Multiple File Upload

Upload multiple files at once:

```python
@app.post("/upload/multiple/")
async def upload_multiple(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        results.append(
            {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
            }
        )
    return {"total_files": len(results), "files": results}
```

### 6. Streaming Large Files

Process large files in chunks to avoid memory issues:

```python
import hashlib


@app.post("/upload/large/")
async def upload_large(file: UploadFile = File(...)):
    chunk_size = 1024 * 1024  # 1MB chunks
    total_size = 0
    md5_hash = hashlib.md5()
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        while chunk := await file.read(chunk_size):
            f.write(chunk)
            md5_hash.update(chunk)
            total_size += len(chunk)

    return {
        "filename": file.filename,
        "total_size": total_size,
        "md5": md5_hash.hexdigest(),
    }
```

### 7. File + Form Data Combination

Combine file upload with form fields:

```python
@app.post("/upload/document/")
async def upload_document(
    file: UploadFile = File(...),
    category: str = "general",
    description: str = "",
):
    content = await file.read()
    category_dir = os.path.join(UPLOAD_DIR, category)
    os.makedirs(category_dir, exist_ok=True)

    file_path = os.path.join(category_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": file.filename,
        "category": category,
        "description": description,
        "size": len(content),
    }
```

### 8. File Hashing (MD5)

Calculate file hash for integrity verification:

```python
import hashlib


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    md5 = hashlib.md5(content).hexdigest()
    return {
        "filename": file.filename,
        "md5": md5,
        "size": len(content),
    }
```

---

## Code Examples

### Example 1: Basic File Upload

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
import os

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
    }
```

### Example 2: Image Upload with Validation

```python
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB


@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid type: {file.content_type}. Allowed: {ALLOWED_TYPES}",
        )

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 5MB.")

    file_path = os.path.join(UPLOAD_DIR, f"image_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(content)

    return {"filename": file.filename, "size": len(content)}
```

### Example 3: Multiple File Upload

```python
@app.post("/upload/multiple/")
async def upload_multiple(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
        results.append(
            {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
            }
        )
    return {"total_files": len(results), "files": results}
```

### Example 4: Streaming Large Files

```python
import hashlib


@app.post("/upload/large/")
async def upload_large(file: UploadFile = File(...)):
    chunk_size = 1024 * 1024  # 1MB
    total_size = 0
    md5 = hashlib.md5()
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        while chunk := await file.read(chunk_size):
            f.write(chunk)
            md5.update(chunk)
            total_size += len(chunk)

    return {
        "filename": file.filename,
        "total_size": total_size,
        "total_size_human": f"{total_size / (1024 * 1024):.2f} MB",
        "md5": md5.hexdigest(),
    }
```

### Example 5: File + Metadata

```python
@app.post("/upload/document/")
async def upload_document(
    file: UploadFile = File(...),
    category: str = "general",
    description: str = "",
):
    content = await file.read()
    category_dir = os.path.join(UPLOAD_DIR, category)
    os.makedirs(category_dir, exist_ok=True)
    file_path = os.path.join(category_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return {"filename": file.filename, "category": category, "size": len(content)}
```

---

## Common Mistakes to Avoid

### Mistake 1: Not using `async` for file operations
```python
# Wrong: Synchronous file read (blocks event loop)
@app.post("/upload/")
def upload(file: UploadFile = File(...)):
    content = file.read()  # Blocking!
    return {"size": len(content)}


# Fix: Use async
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()  # Non-blocking
    return {"size": len(content)}
```

### Mistake 2: Loading large files entirely into memory
```python
# Wrong: Loads entire file into memory
content = await file.read()  # 100MB file = 100MB in memory!

# Fix: Stream in chunks for large files
while chunk := await file.read(1024 * 1024):
    f.write(chunk)
```

### Mistake 3: Not validating file types
```python
# Wrong: Accepts any file type
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    # Could be an executable!
    content = await file.read()


# Fix: Validate content_type
ALLOWED = {"image/jpeg", "image/png"}
if file.content_type not in ALLOWED:
    raise HTTPException(status_code=400, detail="Invalid file type")
```

### Mistake 4: Using filename directly without sanitization
```python
# Wrong: Path traversal vulnerability
file_path = os.path.join(UPLOAD_DIR, file.filename)
# If filename = "../../../etc/passwd", dangerous!

# Fix: Sanitize filename
import re

safe_name = re.sub(r"[^\w\-_\. ]", "", file.filename)
file_path = os.path.join(UPLOAD_DIR, safe_name)
```

---

## Best Practices

1. **Always use `async`** for file upload endpoints
2. **Stream large files** in chunks to avoid memory issues
3. **Validate file types** using MIME type checking
4. **Validate file sizes** before processing
5. **Sanitize filenames** to prevent path traversal
6. **Use unique filenames** (timestamps, UUIDs) to avoid overwrites
7. **Calculate file hashes** for integrity verification
8. **Organize uploads** into subdirectories by category
9. **Set upload limits** at the server/proxy level
10. **Store uploads outside** the web root directory

---

## Practice Exercises

### Exercise 1: Basic Upload
Create a single file upload endpoint that saves to disk and returns filename, size, and content type.

### Exercise 2: Image Upload
Create an image upload endpoint with MIME type validation (JPEG, PNG, GIF only) and 5MB size limit.

### Exercise 3: Multiple Upload
Create an endpoint that accepts up to 5 files and returns metadata for each.

### Exercise 4: Large File
Create a streaming file upload endpoint that processes files in 1MB chunks and calculates MD5.

### Exercise 5: Document Manager
Create a document upload endpoint with category, description, and organized storage by category.

---

## Summary

| Concept | Description |
|---------|-------------|
| `UploadFile` | File-like object with metadata |
| `File()` | Declares a file parameter |
| `await file.read()` | Read file content |
| `file.content_type` | MIME type of the file |
| `file.filename` | Original filename |
| Streaming | Process large files in chunks |
| MIME validation | Check file type before processing |
| MD5 hash | Verify file integrity |

File uploads are essential for many applications. FastAPI's `UploadFile` provides a clean, async, memory-efficient way to handle them.

---

## Quick Reference

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
import os

app = FastAPI()


# Single upload
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}


# Multiple upload
@app.post("/upload/multiple/")
async def upload_multiple(files: list[UploadFile] = File(...)):
    return {"count": len(files)}


# With validation
@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(400, "Invalid file type")
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large")
    return {"filename": file.filename}
```
