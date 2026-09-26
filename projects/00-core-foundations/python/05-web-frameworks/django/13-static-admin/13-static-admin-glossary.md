# Django 13: Static Files & Admin Styling — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Static files | CSS, JS, images served without server-side rendering | admin CSS bundle |
| STATIC_ROOT | Single directory `collectstatic` assembles for production | `/var/www/static/` |
| collectstatic | Management command gathering all apps' static files | deploy step |
| STATICFILES_FINDERS | Ordered lookup: filesystem dirs, then per-app static/ | override mechanism |
| AppDirectoriesFinder | Finder checking each installed app's `static/` folder | admin's own assets |
| Template override | Shadowing an admin template via mirrored path + blocks | `templates/admin/base_site.html` |
| Branding block | The `branding` block rendering the admin header identity | site name + logo |

---

## Alphabetical Glossary

### AppDirectoriesFinder

**Definition:** Staticfiles finder that searches the `static/` subdirectory
of every installed app, in app order. How the admin's own assets resolve —
and what your earlier-ordered files override.

**Example:**
```python
# admin CSS found here last, so your copy wins if present earlier
```

**Related concepts:** STATICFILES_FINDERS, Static files

---

### Branding block

**Definition:** The `{% block branding %}` region of the admin base template
rendering the site name and logo. The standard one-block customization.

**Example:**
```html
{% block branding %}<h1 id="site-name">My Custom Admin</h1>{% endblock %}
```

**Related concepts:** Template override

---

### collectstatic

**Definition:** Management command copying every app's static files into
`STATIC_ROOT` for production serving. A deploy step, never a dev habit.

**Example:**
```bash
python manage.py collectstatic --noinput
```

**Related concepts:** STATIC_ROOT, Static files

---

### STATICFILES_FINDERS

**Definition:** Ordered list of finders resolving static file lookups.
Earlier entries win, which is the entire override mechanism.

**Example:**
```python
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
```

**Related concepts:** AppDirectoriesFinder, Template override

---

### STATIC_ROOT

**Definition:** The single directory collecting all static assets for the
production web server. Never edited by hand; always rebuilt by collectstatic.

**Example:**
```bash
# nginx serves STATIC_ROOT; Django never touches it at request time
```

**Related concepts:** collectstatic, Static files

---

### Static files

**Definition:** Assets served as-is (CSS, JavaScript, images). Django finds
them via finders in development and serves them pre-collected in production.

**Example:**
```python
# myapp/static/admin/css/custom.css
```

**Related concepts:** STATIC_ROOT, collectstatic

---

### Template override

**Definition:** Replacing an admin template by creating the same relative
path under your app's `templates/` directory, extending the original and
overriding only the blocks you change.

**Example:**
```html
{% extends "admin/base_site.html" %}
```

**Related concepts:** Branding block, STATICFILES_FINDERS

---

## Related Concepts

- **Template inheritance**: `extends` + `block`, the DRY mechanism behind overrides
- **Whitenoise/nginx**: production static serving in front of Django
- **Admin**: Django's built-in internal data-management UI

## Key Takeaways

1. Finders order is the override mechanism for both CSS and templates.
2. collectstatic is a deploy step; STATIC_ROOT is build output.
3. Brand the admin; build customer UI in your own views.
