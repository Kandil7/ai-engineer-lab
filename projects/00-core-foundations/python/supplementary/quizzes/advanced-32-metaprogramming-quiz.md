# Advanced Python Quiz 32 — Metaprogramming

**Course:** AI Engineer — Core Foundations · Python
**Level:** Advanced · **Topic:** 32 — Metaprogramming
**Questions:** 20 (6 Easy · 9 Medium · 5 Hard)
**Time:** 30 minutes

---

## Instructions

- Each question has exactly **one** correct answer (A–D).
- **Code-output questions** show code; choose the output.
- Answers and explanations are at the end — do the quiz **before** reading the key.
- Score yourself: `Score Tracking` section at the end.

---

## Questions

### Easy

**1. What does `__init_subclass__` do?**

A) It is called automatically when a subclass of the defining class is created
B) It must be called manually to register a subclass
C) It replaces `__init__` for all instances
D) It is a metaclass

**2. Which mechanism auto-registers subclasses WITHOUT a metaclass?**

A) `__init_subclass__`
B) `__new__`
C) `type.__mro__`
D) `__setattr__`

**3. What does `__set_name__` give a descriptor?**

A) The name of the owner class's module
B) The attribute name the descriptor is bound to
C) The descriptor's method resolution order
D) The instance's `__dict__`

**4. What is the danger of `eval(user_input)`?**

A) It is slow for large inputs
B) It executes arbitrary code — remote code execution if input is untrusted
C) It only works with integers
D) It raises `NameError` for strings

**5. Which is the safe replacement for `eval(name + "()")`?**

A) `exec(name + "()")`
B) `getattr(module, name)()` with a whitelist
C) A dispatch table `{name: callable}`
D) `ast.literal_eval(name)`

**6. What does `importlib.import_module("math")` return?**

A) A string with the module's source
B) The `math` module object (cached across calls)
C) A new module object on every call
D) A dict of the module's functions

### Medium

**7. Given:**

```python
class Registry:
    _r = {}

    def __init_subclass__(cls, **kwargs):
        Registry._r[cls.__name__] = cls


class A(Registry):
    pass


class B(A):
    pass


print(sorted(Registry._r))
```

**What is the output?**

A) `['A']`
B) `['A', 'B']`
C) `['Registry', 'A']`
D) `['B']`

**8. With `from __future__ import annotations`, what is `inspect.signature(fn).parameters["x"].annotation` at runtime?**

A) The actual type object (`int`)
B) The string `"int"`
C) `None`
D) `inspect.Parameter.empty`

**9. Which call resolves string annotations to real types?**

A) `inspect.getsource(fn)`
B) `typing.get_type_hints(fn)`
C) `ast.parse(fn)`
D) `fn.__annotations__.values()`

**10. Given `describe()` with `type_map = {str: "string", int: "integer"}`, what is `describe` of `def f(docs: list[str], top_k: int = 5) -> None` (with `__future__` annotations resolved)?**

A) `"docs": {"type": "array"}`, `"top_k": {"type": "integer", "default": 5}`
B) `"docs": {"type": "string"}`, `"top_k": {"type": "integer", "default": 5}`
C) `"docs": {"type": "list"}`, `"top_k": {"type": "integer"}`
D) `"docs": {}`, `"top_k": {"type": "integer", "default": 5}`

**11. What is the primary purpose of the `@tool` pattern in agent frameworks?**

A) To make functions run faster
B) To register a callable and derive its JSON schema for LLM function calling
C) To encrypt tool outputs
D) To replace `__init__` with a registry

**12. What is a dispatch table?**

A) A dict mapping names to callables, used instead of `eval`
B) A list of exceptions a function can raise
C) A metaclass for table classes
D) An `ast` node type

**13. What does `ast.parse(source)` allow that `exec(source)` does not?**

A) Execution with a timeout
B) Analysis of code as data WITHOUT executing it
C) Faster execution
D) Bytecode compilation

**14. Why is monkey-patching dangerous in production?**

A) It is slow
B) It is invisible (not in the source), breaks on refactors, and patches do not compose
C) It requires a metaclass
D) It only works on classes, not instances

**15. In the class-decorator example, `@with_repr` on `class Chunk`:**

A) Replaces the class with a function
B) Receives the class, modifies it (adds `__repr__`), and returns it
C) Is called once per instance
D) Requires a metaclass

### Hard

**16. Given:**

```python
def make_point(name):
    return type(name, (), {"x": 0, "y": 0})


PointA = make_point("PointA")
PointB = make_point("PointB")
p = PointA()
p.x = 5
print(PointA is PointB, PointB().x)
```

**What is the output?**

A) `True 5`
B) `False 0`
C) `True 0`
D) `False 5`

**17. With the `@tool` registry, why must tool-name resolution use `TOOLS[name]` and NEVER `eval`?**

A) Dict lookup is faster
B) Model output is untrusted — `eval` would execute arbitrary code chosen by the model
C) `eval` cannot call functions with arguments
D) `TOOLS` only holds schemas

**18. In `schema_for`, why check `getattr(annotation, "__origin__", None) is list`?**

A) `list[str]` is a subscripted generic whose origin is `list`
B) To catch `TypeError` from `get_type_hints`
C) `list` annotations are always strings
D) To skip `self` parameters

**19. Which ordering of mechanisms is the recommended preference (simplest first)?**

A) metaclass → `__init_subclass__` → class decorator → plain function
B) plain function → class decorator → `__init_subclass__` → metaclass
C) `type()` factory → metaclass → plain function
D) `__set_name__` → metaclass → `eval`

**20. A plugin system loads modules from a directory. Which combination is the correct design?**

A) `eval(open(path).read())` for each plugin
B) `importlib.import_module(name)` + subclasses registering via `__init_subclass__` + dispatch table for tool names
C) `exec` all plugin sources at startup
D) A metaclass per plugin file

---

## Score Tracking

| Section | Count | Your Score |
|---------|-------|------------|
| Easy (Q1–6) | 6 | /6 |
| Medium (Q7–15) | 9 | /9 |
| Hard (Q16–20) | 5 | /5 |
| **Total** | **20** | **/20** |

**Rating:** 18–20 → Ready to build tool frameworks · 14–17 → Review sections 4.1–4.6 · <14 → Re-read the lecture, especially the `@tool` pattern and the `eval` dangers.

---

## Answer Key

**1. A** — `__init_subclass__` fires automatically when a subclass is created.
*Distractors:* B requires manual calls, C confuses it with `__init__`, D is a different mechanism.

**2. A** — `__init_subclass__` on the base class registers subclasses without a metaclass.
*Distractors:* B is instance creation, C is MRO access, D is attribute setting.

**3. B** — `__set_name__(owner, name)` tells the descriptor which attribute it is bound to.
*Distractors:* A/C/D are not what the hook provides.

**4. B** — `eval` runs arbitrary code; untrusted input = RCE.
*Distractors:* A is a minor concern, C is false, D is false (strings evaluate fine).

**5. C** — A dispatch table `{name: callable}` is the explicit, safe replacement.
*Distractors:* A is the same hazard, B still needs a whitelist but the canonical answer is the table, D only handles literals.

**6. B** — `importlib.import_module` returns the module; Python caches it so repeated calls return the same object.
*Distractors:* A is `inspect.getsource`, C is false (cached), D is wrong type.

**7. B** — `__init_subclass__` runs for `B` too, even though `B` subclasses `A` (which subclasses `Registry`) — the hook is inherited.
*Distractors:* A would miss B, C wrongly includes the base, D misses A.

**8. B** — With `from __future__ import annotations`, annotations are strings at runtime.
*Distractors:* A is the resolved type, C/D are not what happens.

**9. B** — `typing.get_type_hints` resolves string annotations to real types.
*Distractors:* A gets source, C parses code, D still shows strings.

**10. A** — `list[str]` maps to `"array"` via `__origin__`, `int` with default 5 → `{"type": "integer", "default": 5}`.
*Distractors:* B wrong mapping, C no such JSON type, D misses the `list` mapping.

**11. B** — The `@tool` decorator registers the callable and derives its JSON schema for LLM calling.
*Distractors:* A/C are unrelated, D confuses with `__init__`.

**12. A** — A dict mapping names to callables, the safe alternative to `eval`.
*Distractors:* B/C/D are unrelated concepts.

**13. B** — `ast.parse` builds a tree you can analyze without executing.
*Distractors:* A/exec, C false, D is `compile`'s job.

**14. B** — Invisible, breaks on refactor, and patches conflict.
*Distractors:* A false, C false, D false (works on instances too).

**15. B** — A class decorator receives the class, modifies it, returns it.
*Distractors:* A would be wrong decorator style, C confuses with instance decorators, D false.

**16. B** — Each `type()` call creates a distinct class (`False`), and `PointB().x` is the fresh default `0` (`p.x = 5` only affects `p`).
*Distractors:* A/C get identity wrong, D gets the shared-state wrong.

**17. B** — Model output is untrusted; `eval` would execute code chosen by the model (RCE).
*Distractors:* A true but not the point, C false, D false (it holds callables too).

**18. A** — `list[str].__origin__` is `list`; that is how subscripted generics are detected.
*Distractors:* B/C/D are not the reason.

**19. B** — Simplest first: plain function → class decorator → `__init_subclass__` → metaclass.
*Distractors:* A reverses it, C omits the simple options, D includes `eval`.

**20. B** — `importlib` for loading, `__init_subclass__` for registration, dispatch tables for names.
*Distractors:* A/C execute arbitrary plugin code (RCE), D is overkill per file.
