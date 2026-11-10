# Glossary: FastAPI Static Files

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Static Files | Unprocessed files served directly | CSS, JS, images |
| Mount | Attach directory to URL path | `app.mount("/static")` |
| StaticFiles | FastAPI/Starlette class for serving | `StaticFiles(directory)` |
| CSS | Cascading Style Sheets | `style.css` |
| JavaScript | Client-side scripting | `main.js` |
| Image | Visual media files | PNG, JPG, SVG |
| Font | Custom typeface files | WOFF2, TTF |
| Favicon | Website icon | `favicon.ico` |
| CDN | Content Delivery Network | jsDelivr, CloudFlare |
| Cache | Browser file storage | `Cache-Control` header |
| MIME Type | File format identifier | `text/css` |
| Directory Traversal | Security vulnerability | `../../etc/passwd` |
| Content-Type | Response header for file type | `application/javascript` |
| Minify | Compress code by removing whitespace | `style.min.css` |
| Gzip | File compression algorithm | `.gz` files |

---

## Terms - Alphabetical Order

### Assets

**Definition:** Static resources used by web applications (CSS, JS, images, fonts, etc.).

**Example:**
```
project/
├── static/
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── fonts/
```

```python
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
```

```html
<link rel="stylesheet" href="/assets/css/style.css">
<script src="/assets/js/main.js"></script>
```

**Related Terms:** Static Files, CSS, JavaScript

---

### Cache

**Definition:** Browser mechanism to store files locally, reducing server requests.

**Example:**
```python
from starlette.staticfiles import StaticFiles
from starlette.responses import Response


class CachedStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)

        # Set cache duration based on file type
        if path.endswith((".css", ".js", ".png", ".jpg")):
            response.headers["Cache-Control"] = "public, max-age=31536000"  # 1 year
        elif path.endswith(".html"):
            response.headers["Cache-Control"] = "no-cache"

        return response


app.mount("/static", CachedStaticFiles(directory="static"), name="static")
```

**HTML cache busting:**
```html
<!-- Version query string -->
<link rel="stylesheet" href="/static/css/style.css?v=1.2.3">
<script src="/static/js/main.js?v=1.2.3"></script>
```

**Related Terms:** Cache-Control, Browser Storage, Performance

---

### Cache-Control

**Definition:** HTTP header controlling browser caching behavior.

**Example:**
```python
# Different caching strategies
headers = {
    # Cache for 1 year (immutable assets)
    "Cache-Control": "public, max-age=31536000, immutable",
    # Cache for 1 hour
    "Cache-Control": "public, max-age=3600",
    # No caching
    "Cache-Control": "no-cache, no-store, must-revalidate",
    # Revalidate with server
    "Cache-Control": "private, must-revalidate",
}
```

| Directive | Meaning |
|-----------|---------|
| public | Can be cached by any cache |
| private | Only browser can cache |
| max-age=N | Cache for N seconds |
| no-cache | Must revalidate before use |
| no-store | Don't cache at all |
| immutable | Content never changes |

**Related Terms:** Headers, Performance, CDN

---

### CDN (Content Delivery Network)

**Definition:** Distributed servers that deliver static content based on user location.

**Example:**
```html
<!-- Bootstrap from CDN -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Font Awesome from CDN -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- jQuery from CDN -->
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
```

**Python with CDN:**
```python
CDN_BASE = "https://cdn.jsdelivr.net/npm"


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "bootstrap_css": f"{CDN_BASE}/bootstrap@5.3.0/dist/css/bootstrap.min.css",
            "bootstrap_js": f"{CDN_BASE}/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",
        },
    )
```

**Related Terms:** Performance, Distribution, Caching

---

### Compress

**Definition:** Reduce file size to improve transfer speed (gzip, brotli).

**Example:**
```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Enable Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
```

**Nginx configuration:**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
gzip_min_length 1000;
```

**Related Terms:** Gzip, Performance, File Size

---

### Content-Type

**Definition:** HTTP header indicating the media type of the response.

**Example:**
```python
from starlette.responses import FileResponse


@app.get("/files/{filename}")
async def serve_file(filename: str):
    file_path = f"static/{filename}"

    # Content-Type is auto-detected
    return FileResponse(file_path)


# Or set manually
from starlette.responses import Response


@app.get("/custom")
async def custom_content():
    content = b"<h1>Hello</h1>"
    return Response(content=content, media_type="text/html")
```

**Common MIME Types:**

| Extension | Content-Type |
|-----------|--------------|
| .css | text/css |
| .js | application/javascript |
| .json | application/json |
| .png | image/png |
| .jpg | image/jpeg |
| .svg | image/svg+xml |
| .woff2 | font/woff2 |
| .pdf | application/pdf |

**Related Terms:** MIME, Headers, Response

---

### Directory Traversal

**Definition:** Security vulnerability allowing access to files outside intended directory.

**Example:**
```python
# ❌ VULNERABLE - Path traversal possible
@app.get("/files/{filename}")
async def get_file(filename: str):
    # Attacker could use: ../../etc/passwd
    return FileResponse(f"static/{filename}")


# ✅ SECURE - Validate path
from pathlib import Path

STATIC_DIR = Path("static").resolve()


@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = (STATIC_DIR / filename).resolve()

    # Ensure path is within static directory
    if not str(file_path).startswith(str(STATIC_DIR)):
        raise HTTPException(403, "Forbidden")

    if not file_path.is_file():
        raise HTTPException(404, "Not found")

    return FileResponse(file_path)
```

**Related Terms:** Security, Path Validation, Vulnerability

---

### Favicon

**Definition:** Small icon displayed in browser tab, typically `favicon.ico`.

**Example:**
```python
from fastapi.staticfiles import StaticFiles

# Serve favicon
app.mount("/static", StaticFiles(directory="static"), name="static")
```

**HTML:**
```html
<!-- Standard favicon -->
<link rel="icon" href="/static/images/favicon.ico" type="image/x-icon">

<!-- PNG favicon (modern browsers) -->
<link rel="icon" type="image/png" sizes="32x32" href="/static/images/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/static/images/favicon-16x16.png">

<!-- Apple Touch Icon -->
<link rel="apple-touch-icon" sizes="180x180" href="/static/images/apple-touch-icon.png">
```

**Generate favicons:**
- [RealFaviconGenerator](https://realfavicongenerator.net/)
- [Favicon.io](https://favicon.io/)

**Related Terms:** Icons, Browser Tab, Assets

---

### Font

**Definition:** Custom typeface files for web typography.

**Example:**
```python
app.mount("/fonts", StaticFiles(directory="static/fonts"), name="fonts")
```

**CSS:**
```css
/* Modern font format */
@font-face {
    font-family: 'CustomFont';
    src: url('/fonts/custom.woff2') format('woff2'),
         url('/fonts/custom.woff') format('woff');
    font-weight: 400;
    font-style: normal;
    font-display: swap;  /* Improve loading */
}

/* Usage */
body {
    font-family: 'CustomFont', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

**Font formats:**

| Format | Support | Size |
|--------|---------|------|
| WOFF2 | Modern browsers | Smallest |
| WOFF | All browsers | Small |
| TTF | Legacy | Large |
| EOT | IE only | Large |

**Related Terms:** Typography, WOFF2, @font-face

---

### Gzip

**Definition:** Compression algorithm reducing file size for faster transfer.

**Example:**
```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Compress responses over 1KB
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**File sizes comparison:**
```
style.css      → style.css.gz      (70% smaller)
main.js        → main.js.gz        (65% smaller)
index.html     → index.html.gz     (60% smaller)
```

**Server configuration:**
```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml application/json application/javascript;
```

**Related Terms:** Compression, Performance, Bandwidth

---

### JavaScript

**Definition:** Client-side scripting language for web interactivity.

**Example:**
```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

**static/js/main.js:**
```javascript
// DOM manipulation
document.addEventListener('DOMContentLoaded', function() {
    // Initialize app
    console.log('App loaded');
});

// Event handling
document.querySelector('.btn').addEventListener('click', function() {
    alert('Clicked!');
});

// Fetch API
async function getData(url) {
    const response = await fetch(url);
    return await response.json();
}
```

**HTML:**
```html
<!-- At bottom of body for performance -->
<script src="/static/js/main.js"></script>

<!-- Async loading -->
<script src="/static/js/analytics.js" async></script>

<!-- Defer loading -->
<script src="/static/js/app.js" defer></script>
```

**Related Terms:** Client-Side, DOM, ES6

---

### Minify

**Definition:** Remove whitespace and comments from code to reduce file size.

**Example:**
```css
/* Before minification */
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
}

/* After minification */
body{margin:0;padding:0;font-family:Arial,sans-serif}
```

**Tools:**
- CSS: cssnano, clean-css
- JavaScript: Terser, UglifyJS
- HTML: html-minifier

**Versioning for cache busting:**
```html
<link rel="stylesheet" href="/static/css/style.min.css?v=1.0.0">
<script src="/static/js/main.min.js?v=1.0.0"></script>
```

**Related Terms:** Compression, Performance, File Size

---

### MIME Type

**Definition:** Standard identifier indicating file format (Multipurpose Internet Mail Extensions).

**Example:**
```python
from starlette.responses import FileResponse

# Auto-detected MIME types
return FileResponse("style.css")  # → text/css
return FileResponse("image.png")  # → image/png
return FileResponse("script.js")  # → application/javascript

# Custom MIME type
from starlette.responses import Response

Response(content=b"...", media_type="application/json")
Response(content=b"...", media_type="image/svg+xml")
```

**Common types:**

| Extension | MIME Type |
|-----------|-----------|
| .html | text/html |
| .css | text/css |
| .js | application/javascript |
| .json | application/json |
| .png | image/png |
| .jpg | image/jpeg |
| .svg | image/svg+xml |
| .woff2 | font/woff2 |

**Related Terms:** Content-Type, File Format

---

### Mount

**Definition:** FastAPI method to attach a directory or app to a URL path.

**Example:**
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Basic mount
app.mount("/static", StaticFiles(directory="static"), name="static")

# Multiple mounts
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/js", StaticFiles(directory="static/js"), name="js")
app.mount("/images", StaticFiles(directory="static/images"), name="images")

# Mount with HTML mode
app.mount("/docs", StaticFiles(directory="docs", html=True), name="docs")
```

**Related Terms:** Directory, URL Path, StaticFiles

---

### Static Files

**Definition:** Files served directly to clients without server-side processing.

**Example:**
```
static/
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   ├── logo.png
│   └── favicon.ico
└── fonts/
    └── custom.woff2
```

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

**Related Terms:** CSS, JavaScript, Images, Fonts

---

### StaticFiles

**Definition:** FastAPI/Starlette class for serving static files from a directory.

**Example:**
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Basic usage
app.mount("/static", StaticFiles(directory="static"), name="static")

# With HTML mode (serves index.html for directory)
app.mount("/public", StaticFiles(directory="public", html=True), name="public")

# Check if directory exists
from pathlib import Path

if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")
```

**Parameters:**

| Parameter | Description |
|-----------|-------------|
| directory | Path to static files |
| name | Name for reverse URL lookup |
| html | Serve index.html for directories |

**Related Terms:** Mount, Directory, Serving

---

### SVG (Scalable Vector Graphics)

**Definition:** XML-based vector image format, scalable without quality loss.

**Example:**
```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

**HTML:**
```html
<!-- Direct SVG -->
<img src="/static/images/icon.svg" alt="Icon" width="24" height="24">

<!-- Inline SVG -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path d="M12 2L2 22h20L12 2z"/>
</svg>

<!-- SVG as background -->
<div class="icon" style="background-image: url('/static/images/icon.svg')"></div>
```

**CSS:**
```css
.icon {
    width: 24px;
    height: 24px;
    background: url('/static/images/icon.svg') no-repeat center;
    background-size: contain;
}
```

**Related Terms:** Vector, Icons, Responsive

---

## Code Examples Collection

### Complete Static Files Setup

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# Configuration
STATIC_DIR = Path("static")
TEMPLATES_DIR = Path("templates")

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
```

**templates/base.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My App{% endblock %}</title>
    
    {# CSS #}
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
    
    {# Favicon #}
    <link rel="icon" href="/static/images/favicon.ico" type="image/x-icon">
    
    {% block head %}{% endblock %}
</head>
<body>
    {# Header #}
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <img src="/static/images/logo.png" alt="Logo" height="30">
                </a>
                <div class="navbar-nav">
                    <a class="nav-link" href="/">Home</a>
                    <a class="nav-link" href="/about">About</a>
                </div>
            </div>
        </nav>
    </header>
    
    {# Main Content #}
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>
    
    {# Footer #}
    <footer class="bg-dark text-white mt-5 py-3">
        <div class="container text-center">
            <p>&copy; 2024 My App</p>
        </div>
    </footer>
    
    {# Scripts #}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/main.js"></script>
    
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Optimized Static Files with Versioning

```python
import hashlib
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


def get_file_hash(filepath: str) -> str:
    """Generate short hash for cache busting"""
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


# Store file hashes
static_hashes = {}
for file in Path("static").rglob("*"):
    if file.is_file():
        static_hashes[str(file)] = get_file_hash(file)

app.mount("/static", StaticFiles(directory="static"), name="static")
```

**Template:**
```html
<link rel="stylesheet" href="/static/css/style.css?v={{ static_hashes['static/css/style.css'] }}">
<script src="/static/js/main.js?v={{ static_hashes['static/js/main.js'] }}"></script>
```

### Security - Path Validation

```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

STATIC_DIR = Path("static").resolve()


# Secure file serving
@app.get("/files/{file_path:path}")
async def serve_file(file_path: str):
    """Serve static files with path validation"""

    # Resolve full path
    full_path = (STATIC_DIR / file_path).resolve()

    # Security check 1: Ensure within static directory
    if not str(full_path).startswith(str(STATIC_DIR)):
        raise HTTPException(status_code=403, detail="Forbidden")

    # Security check 2: File must exist
    if not full_path.is_file():
        raise HTTPException(status_code=404, detail="Not found")

    # Security check 3: Check extension (optional)
    allowed_extensions = {".css", ".js", ".png", ".jpg", ".svg", ".woff2"}
    if full_path.suffix.lower() not in allowed_extensions:
        raise HTTPException(status_code=403, detail="File type not allowed")

    from starlette.responses import FileResponse

    return FileResponse(full_path)
```

---

## Quick Reference Card

### FastAPI Static Files API

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Basic mount
app.mount("/static", StaticFiles(directory="static"), name="static")

# With HTML mode
app.mount("/public", StaticFiles(directory="public", html=True), name="public")
```

### HTML Static File References

```html
{# CSS #}
<link rel="stylesheet" href="/static/css/style.css">

{# JavaScript #}
<script src="/static/js/main.js"></script>

{# Images #}
<img src="/static/images/photo.jpg" alt="Photo">

{# Favicon #}
<link rel="icon" href="/static/images/favicon.ico">

{# Fonts in CSS #}
@font-face {
    font-family: 'Custom';
    src: url('/static/fonts/custom.woff2');
}
```

### Cache Headers

```python
# 1 year (immutable assets)
"Cache-Control": "public, max-age=31536000, immutable"

# 1 hour
"Cache-Control": "public, max-age=3600"

# No cache
"Cache-Control": "no-cache, no-store, must-revalidate"
```

### Directory Structure

```
static/
├── css/
│   ├── style.css
│   └── bootstrap.min.css
├── js/
│   ├── main.js
│   └── app.js
├── images/
│   ├── logo.png
│   ├── favicon.ico
│   └── hero.jpg
└── fonts/
    ├── custom.woff2
    └── icons.ttf
```
