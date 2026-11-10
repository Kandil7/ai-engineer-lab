# Glossary: Lecture 08 — File Upload

Alphabetical reference of all key terms from the File Upload lecture.

---

## Quick Reference Table

| Term | One-Line Definition |
|------|---------------------|
| Binary data | Raw file data (images, PDFs, etc.) |
| Bytes parameter | Using `bytes = File(...)` to receive raw file content |
| Chunk | A piece of data read from a file during streaming |
| Content type | MIME type indicating the file format |
| File hash | Cryptographic fingerprint for file integrity |
| File() | FastAPI function for declaring file parameters |
| File-like object | Python object with read/write methods |
| MIME type | Standard identifier for file formats |
| Path traversal | Security vulnerability from unsanitized filenames |
| Sanitize | Clean filenames to prevent security issues |
| SpooledTemporaryFile | Python's file-like object for temporary storage |
| Streaming | Reading file data in chunks instead of all at once |
| Upload directory | Folder where uploaded files are stored |
| UploadFile | FastAPI's file upload handler class |
| Validation | Checking file type and size before processing |

---

## Detailed Term Definitions

### Binary Data

**Definition:** Raw file data that is not text. Images, PDFs, executables, and archives are all binary files. Binary data must be handled differently from text — it's read as `bytes` objects.

**Example:**
```python
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()  # Returns bytes
    # content is binary data
    return {"size": len(content), "type": type(content).__name__}
```

**Related terms:** Bytes, UploadFile, Content Type

---

### Bytes Parameter

**Definition:** An alternative to `UploadFile` where the entire file is loaded into memory as a `bytes` object. Simpler but not suitable for large files.

**Example:**
```python
from fastapi import File


@app.post("/upload-raw/")
async def upload_raw(file: bytes = File(...)):
    # Entire file in memory as bytes
    return {"size": len(file), "type": "bytes"}


# vs UploadFile (recommended)
@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()  # Also bytes, but with streaming support
    return {"size": len(content)}
```

**When to use:**
- `bytes`: Small files (< 1MB), simple processing
- `UploadFile`: Large files, need metadata, streaming

**Related terms:** UploadFile, File(), Binary Data

---

### Chunk

**Definition:** A piece of data read from a file during streaming processing. Instead of loading the entire file into memory, you process it piece by piece.

**Example:**
```python
@app.post("/upload/large/")
async def upload_large(file: UploadFile = File(...)):
    chunk_size = 1024 * 1024  # 1MB chunks
    total_size = 0
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        while chunk := await file.read(chunk_size):
            f.write(chunk)
            total_size += len(chunk)

    return {"filename": file.filename, "total_size": total_size}
```

**Common chunk sizes:**

| Size | Use Case |
|------|----------|
| 8KB | Small files |
| 64KB | Medium files |
| 1MB | Large files |
| 8MB | Very large files |

**Related terms:** Streaming, Memory, UploadFile

---

### Content Type

**Definition:** A MIME (Multipurpose Internet Mail Extensions) type that identifies the format of a file. FastAPI provides this as `file.content_type` for uploaded files.

**Common content types:**

| MIME Type | File Format |
|-----------|-------------|
| `image/jpeg` | JPEG images |
| `image/png` | PNG images |
| `image/gif` | GIF images |
| `image/webp` | WebP images |
| `application/pdf` | PDF documents |
| `text/plain` | Plain text |
| `application/json` | JSON files |
| `application/zip` | ZIP archives |
| `video/mp4` | MP4 videos |

**Example:**
```python
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }
```

**Related terms:** MIME Type, Validation, File Format

---

### File Hash

**Definition:** A cryptographic fingerprint calculated from file content. Used to verify file integrity — if the hash matches, the file hasn't been corrupted or tampered with.

**Example:**
```python
import hashlib


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    md5 = hashlib.md5(content).hexdigest()
    sha256 = hashlib.sha256(content).hexdigest()
    return {
        "filename": file.filename,
        "md5": md5,
        "sha256": sha256,
        "size": len(content),
    }
```

**Hash algorithms:**

| Algorithm | Speed | Security | Use Case |
|-----------|-------|----------|----------|
| MD5 | Fast | Weak | Checksums (not security) |
| SHA-1 | Fast | Weak | Legacy systems |
| SHA-256 | Medium | Strong | Security, verification |

**Related terms:** Integrity, Checksum, Security

---

### File() Function

**Definition:** A FastAPI function that declares a parameter as a file upload. Works with `UploadFile` (recommended) or `bytes`.

**Example:**
```python
from fastapi import File, UploadFile


# With UploadFile (recommended)
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {"size": len(content)}


# With bytes (simple but loads all into memory)
@app.post("/upload-raw/")
async def upload_raw(file: bytes = File(...)):
    return {"size": len(file)}


# With description
@app.post("/upload/")
async def upload(
    file: UploadFile = File(..., description="File to upload"),
):
    return {"filename": file.filename}
```

**Related terms:** UploadFile, Form Data, Multipart

---

### File-like Object

**Definition:** A Python object that provides the same interface as a file (read, write, seek, close methods) without being an actual file on disk. `UploadFile.file` is a `SpooledTemporaryFile`.

**Example:**
```python
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    # file is a file-like object
    content = await file.read()  # Read
    await file.seek(0)  # Seek to beginning
    content2 = await file.read()  # Read again
    await file.close()  # Close
    return {"size": len(content)}
```

**Methods:**
- `await file.read()` — Read content
- `await file.read(n)` — Read n bytes
- `await file.write(data)` — Write data
- `await file.seek(offset)` — Move to position
- `await file.close()` — Close file

**Related terms:** UploadFile, SpooledTemporaryFile, IO

---

### MIME Type

**Definition:** Multipurpose Internet Mail Extensions — a standard that identifies file formats on the internet. Used in HTTP headers and file uploads to indicate what type of data is being transmitted.

**Example:**
```python
# Checking MIME type
@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    # file.content_type is the MIME type
    if file.content_type == "image/jpeg":
        return {"format": "JPEG"}
    elif file.content_type == "image/png":
        return {"format": "PNG"}
    else:
        raise HTTPException(400, "Not an image")
```

**Related terms:** Content Type, File Format, Validation

---

### Path Traversal

**Definition:** A security vulnerability where an attacker uses `../` in a filename to access files outside the intended directory. Always sanitize filenames before using them in file paths.

**Example:**
```python
import re
import os

# DANGEROUS: Direct use of filename
file_path = os.path.join(UPLOAD_DIR, file.filename)
# If filename = "../../../etc/passwd", this accesses system files!


# SAFE: Sanitize filename
def sanitize_filename(name: str) -> str:
    # Remove path components
    name = os.path.basename(name)
    # Remove special characters
    name = re.sub(r"[^\w\-_\. ]", "", name)
    # Limit length
    name = name[:255]
    return name


safe_name = sanitize_filename(file.filename)
file_path = os.path.join(UPLOAD_DIR, safe_name)
```

**Related terms:** Security, Sanitize, Filename

---

### Sanitize

**Definition:** The process of cleaning user-provided data (especially filenames) to prevent security issues like path traversal, injection attacks, and filesystem errors.

**Example:**
```python
import re
import uuid


def sanitize_filename(filename: str) -> str:
    """Clean filename for safe storage."""
    # Get extension
    ext = os.path.splitext(filename)[1].lower()
    # Clean name
    name = os.path.splitext(filename)[0]
    name = re.sub(r"[^\w\-]", "", name)  # Keep only word chars
    name = name[:100]  # Limit length
    # Use UUID to prevent overwrites
    return f"{uuid.uuid4().hex}_{name}{ext}"


# "My Photo!.jpg" → "a1b2c3d4_MyPhoto.jpg"
```

**Related terms:** Security, Path Traversal, Filename

---

### SpooledTemporaryFile

**Definition:** A Python file-like object that stores data in memory up to a size threshold, then automatically spools to disk. Used by FastAPI's `UploadFile` to handle files efficiently.

**Example:**
```python
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    # file.file is a SpooledTemporaryFile
    # Small files stay in memory
    # Large files automatically go to disk
    content = await file.read()
    return {"size": len(content)}
```

**Benefits:**
- Small files: Fast (in memory)
- Large files: Memory-efficient (spools to disk)
- Automatic cleanup

**Related terms:** UploadFile, File-like Object, Memory

---

### Streaming

**Definition:** Processing file data piece by piece (in chunks) instead of loading the entire file into memory. Essential for handling large files efficiently.

**Example:**
```python
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

    return {"total_size": total_size, "md5": md5.hexdigest()}
```

**vs Loading entirely:**
```python
# Loading (bad for large files)
content = await file.read()  # 1GB file = 1GB in memory!

# Streaming (good for large files)
while chunk := await file.read(1024 * 1024):
    process(chunk)  # Only 1MB in memory at a time
```

**Related terms:** Chunk, Memory, UploadFile

---

### Upload Directory

**Definition:** The folder where uploaded files are saved on the server. Should be configured, monitored, and secured appropriately.

**Example:**
```python
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return {"saved_to": file_path}
```

**Best practices:**
- Create directory at startup
- Store outside web root
- Organize by date or category
- Set appropriate permissions
- Implement cleanup policies

**Related terms:** File Path, Storage, Organization

---

### UploadFile

**Definition:** FastAPI's file upload handler class. Provides file-like interface with metadata (filename, content_type) and async methods for reading/writing.

**Example:**
```python
from fastapi import UploadFile, File


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    return {
        "filename": file.filename,  # Original filename
        "content_type": file.content_type,  # MIME type
        "file": type(file.file).__name__,  # SpooledTemporaryFile
    }
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `filename` | str | Original filename |
| `content_type` | str | MIME type |
| `file` | SpooledTemporaryFile | File-like object |

**Methods:**

| Method | Description |
|--------|-------------|
| `await read()` | Read entire file |
| `await read(n)` | Read n bytes |
| `await write(data)` | Write data |
| `await seek(offset)` | Move to position |
| `await close()` | Close file |

**Related terms:** File(), Upload, MIME Type

---

### Validation

**Definition:** The process of checking uploaded files against constraints like allowed types, maximum sizes, and filename patterns before processing.

**Example:**
```python
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB


@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    # Type validation
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Invalid type: {file.content_type}")

    # Size validation
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, "File too large (max 5MB)")

    # Filename validation
    if not file.filename:
        raise HTTPException(400, "No filename")

    return {"filename": file.filename, "size": len(content)}
```

**Validation types:**
1. **Type**: MIME type checking
2. **Size**: Maximum file size
3. **Filename**: Sanitization and uniqueness
4. **Content**: Magic bytes checking (advanced)

**Related terms:** File(), MIME Type, Security

---

## File Upload Patterns

### Pattern: Basic Upload
```python
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}
```

### Pattern: Type Validation
```python
@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(400, "Invalid file type")
    ...
```

### Pattern: Size Validation
```python
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large")
    ...
```

### Pattern: Streaming
```python
@app.post("/upload/large/")
async def upload_large(file: UploadFile = File(...)):
    with open(path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)
    ...
```

### Pattern: Multiple Files
```python
@app.post("/upload/multiple/")
async def upload_multiple(files: list[UploadFile] = File(...)):
    return {"count": len(files)}
```

### Pattern: File + Metadata
```python
@app.post("/upload/document/")
async def upload_document(
    file: UploadFile = File(...),
    category: str = "general",
    description: str = "",
): ...
```

---

*End of Glossary — Lecture 08: File Upload*
