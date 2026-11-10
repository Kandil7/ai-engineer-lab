# Glossary: Logging

## Quick Reference Table

| Term | Definition | Key Methods | Purpose |
|------|------------|-------------|---------|
| Logger | Interface for logging | `debug()`, `info()`, `warning()` | Create log messages |
| Handler | Directs log output | `StreamHandler()`, `FileHandler()` | Route logs |
| Formatter | Formats log messages | `Formatter(fmt, datefmt)` | Format output |
| Filter | Filters log messages | `Filter(name)` | Control which logs pass |
| Level | Message severity | DEBUG, INFO, WARNING, ERROR, CRITICAL | Classify importance |
| Propagation | Pass logs to parent | `propagation = True/False` | Hierarchical logging |
| basicConfig | Quick setup | `logging.basicConfig()` | Initial configuration |
| NullHandler | Disable logging | `NullHandler()` | Library logging |

---

## Alphabetical Definitions

### basicConfig

**Definition**: A function that configures the root logger with a default handler and formatter. Should be called once at application startup.

**Example**:
```python
import logging

# Basic configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="app.log",
    filemode="w",
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

**Related Terms**: configuration, handler, formatter

**Parameters**:
- `level`: Minimum level to handle
- `format`: Log message format
- `datefmt`: Date format string
- `filename`: Log to file
- `filemode`: File open mode ('w' or 'a')

---

### CRITICAL

**Definition**: The highest logging level (50), indicating a severe problem that may prevent the program from continuing.

**Example**:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.critical("Database connection lost")
logger.critical("Out of memory - cannot continue")
```

**Related Terms**: ERROR, WARNING, level hierarchy

---

### DEBUG

**Definition**: The lowest logging level (10), used for detailed diagnostic information useful during development.

**Example**:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Variable x = %s", x)
logger.debug("Entering function %s", function_name)
logger.debug("Query: %s", query)
```

**Related Terms**: INFO, WARNING, level hierarchy

---

### ERROR

**Definition**: A logging level (40) indicating a serious problem that prevents a function from performing its task.

**Example**:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    result = 1 / 0
except Exception as e:
    logger.error("Failed to calculate: %s", e)
    logger.error("Failed to calculate", exc_info=True)  # With traceback
```

**Related Terms**: CRITICAL, WARNING, exception logging

---

### exception

**Definition**: A logging method that logs at ERROR level with traceback information. Equivalent to `error(msg, exc_info=True)`.

**Example**:
```python
import logging

logger = logging.getLogger(__name__)


def risky_operation():
    try:
        result = 1 / 0
    except Exception:
        logger.exception("Error in risky_operation")
        raise


try:
    risky_operation()
except Exception:
    pass
```

**Related Terms**: error, exc_info, traceback

---

### Filter

**Definition**: An object that determines which log records are passed to handlers. Can be applied to loggers or handlers.

**Example**:
```python
import logging


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.addFilter(InfoFilter())

logger.addHandler(handler)

logger.debug("This won't appear")  # Filtered out
logger.info("This will appear")  # Passes filter
logger.warning("This won't appear")  # Filtered out
```

**Related Terms**: handler, logger, level

---

### Formatter

**Definition**: An object that formats log records into strings. Defines the output format of log messages.

**Example**:
```python
import logging

logger = logging.getLogger("myapp")

# Simple formatter
simple = logging.Formatter("%(levelname)s: %(message)s")

# Detailed formatter
detailed = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

handler = logging.StreamHandler()
handler.setFormatter(detailed)
logger.addHandler(handler)

logger.info("Formatted message")
```

**Related Terms**: handler, format string, asctime

**Format Variables**:

| Variable | Description |
|----------|-------------|
| `%(asctime)s` | Time of log message |
| `%(name)s` | Logger name |
| `%(levelname)s` | Log level name |
| `%(message)s` | Log message |
| `%(funcName)s` | Function name |
| `%(lineno)d` | Line number |

---

### Handler

**Definition**: An object that directs log records to appropriate destinations (console, file, network, etc.).

**Example**:
```python
import logging

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# Console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

# File handler
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logger.addHandler(console)
logger.addHandler(file_handler)

logger.info("Goes to both console and file")
logger.debug("Goes to file only")
```

**Related Terms**: StreamHandler, FileHandler, formatter

**Common Handlers**:
- `StreamHandler`: Output to streams (stdout/stderr)
- `FileHandler`: Output to files
- `RotatingFileHandler`: Rotate files by size
- `TimedRotatingFileHandler`: Rotate files by time
- `SocketHandler`: Send to network

---

### INFO

**Definition**: A logging level (20) used for confirmation that things are working as expected.

**Example**:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Application started")
logger.info("User %s logged in", username)
logger.info("Processing completed successfully")
```

**Related Terms**: DEBUG, WARNING, level hierarchy

---

### NullHandler

**Definition**: A handler that does nothing. Used in libraries to prevent "No handlers could be found" warnings.

**Example**:
```python
import logging

# In a library
logger = logging.getLogger("mylib")
logger.addHandler(logging.NullHandler())

# Library code
logger.debug("This won't cause warnings")
```

**Related Terms**: handler, library logging

---

### logger

**Definition**: The main interface for logging. Loggers are named and form a hierarchy. They create log records and pass them to handlers.

**Example**:
```python
import logging

# Get logger by name
logger = logging.getLogger("myapp.database")
logger.setLevel(logging.DEBUG)

# Configure
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(name)s - %(message)s"))
logger.addHandler(handler)

# Log messages
logger.info("Connected to database")
logger.debug("Executing query: %s", query)
```

**Related Terms**: handler, level, hierarchy

**Hierarchy**:
```
root
└── myapp
    └── myapp.database
    └── myapp.api
```

---

### level

**Definition**: A numeric value indicating the severity of a log message. Only messages at or above the handler's level are processed.

**Example**:
```python
import logging

# Level hierarchy
# CRITICAL = 50
# ERROR    = 40
# WARNING  = 30
# INFO     = 20
# DEBUG    = 10

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

logger.debug("Not shown")  # Below WARNING
logger.info("Not shown")  # Below WARNING
logger.warning("Shown")  # At WARNING
logger.error("Shown")  # Above WARNING
```

**Related Terms**: DEBUG, INFO, WARNING, ERROR, CRITICAL

---

### propagation

**Definition**: A boolean attribute that determines whether log records are passed to parent loggers. Default is True.

**Example**:
```python
import logging

# Parent logger
parent = logging.getLogger("app")
parent.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
parent.addHandler(handler)

# Child logger
child = logging.getLogger("app.child")

# With propagation (default)
child.info("Child message")  # Also goes to parent handler

# Without propagation
child.propagation = False
child.info("Child message only")  # Only goes to child's handlers
```

**Related Terms**: logger hierarchy, parent logger

---

### WARNING

**Definition**: A logging level (30) used for events that might cause problems in the future.

**Example**:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.warning("Disk space running low: %s%%", space)
logger.warning("Deprecated function used: %s", function_name)
logger.warning("Configuration not found, using defaults")
```

**Related Terms**: INFO, ERROR, level hierarchy

---

## Concept Relationships

```
Logging Module
├── Components
│   ├── Logger (create messages)
│   ├── Handler (route messages)
│   ├── Formatter (format messages)
│   └── Filter (filter messages)
│
├── Levels
│   ├── DEBUG (10) - Diagnostic
│   ├── INFO (20) - Confirmation
│   ├── WARNING (30) - Potential issues
│   ├── ERROR (40) - Serious problems
│   └── CRITICAL (50) - Fatal errors
│
├── Configuration
│   ├── basicConfig() - Quick setup
│   ├── Handler configuration
│   └── Formatter configuration
│
└── Hierarchy
    ├── Parent loggers
    ├── Child loggers
    └── Propagation
```

---

## When to Use Each Level

| Level | Use Case |
|-------|----------|
| DEBUG | Variable values, function entry/exit |
| INFO | Normal operations, state changes |
| WARNING | Deprecated usage, potential issues |
| ERROR | Failures, exceptions |
| CRITICAL | System-level failures, data loss |

---

## Common Patterns

### 1. Basic Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

### 2. Application Logger
```python
class ApplicationLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)
```

### 3. Exception Logging
```python
try:
    risky_operation()
except Exception:
    logger.exception("Operation failed")  # Includes traceback
```

### 4. Library Logging
```python
# In library
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# In application
logging.basicConfig(level=logging.DEBUG)
```

### 5. Rotating File
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=1024 * 1024,  # 1MB
    backupCount=5,
)
```
