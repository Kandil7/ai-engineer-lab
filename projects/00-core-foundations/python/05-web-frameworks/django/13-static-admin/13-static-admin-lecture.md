# Django Lecture 13: Static Files & Admin Styling

## 🎯 Topic Overview

The Django admin ships its own CSS, JS, and images — and every real project
rebrands it. This lecture covers where admin static files live, how
`collectstatic` assembles them for production, and the two customization
paths: overriding admin CSS and overriding admin templates. Reference-only:
Django is not installed by default, so run these commands only in an env
with Django present.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Locate the admin's static files inside `django/contrib/admin/static/admin/`
2. Explain what `collectstatic` does and why production needs it
3. Override admin styles with a custom CSS file in the static lookup path
4. Override admin templates via `templates/admin/` with block inheritance
5. State when theming stops being worth it (hint: user-facing UI belongs outside admin)

---

## 1. Where Admin Static Files Live

The admin is a Django app like any other, so its assets live under its own
`static/` directory: `django/contrib/admin/static/admin/` holds the CSS, JS,
and images every admin page loads. In development Django serves these
directly; in production a web server does, which is why `collectstatic`
exists — one command gathering every app's static files into `STATIC_ROOT`:

```bash
python manage.py collectstatic   # development files -> STATIC_ROOT for serving
```

## 2. Custom Admin CSS

### Static lookup order

`STATICFILES_FINDERS` decides where Django looks: `FileSystemFinder` checks
`STATICFILES_DIRS` first, then `AppDirectoriesFinder` checks each app's
`static/` folder. Your override wins by appearing earlier in that order:

```python
# settings.py — your app's static dir is found before the admin's own files
STATICFILES_DIRS = [BASE_DIR / "static"]
```

### The override pattern

```css
/* myapp/static/admin/css/custom.css — loaded after admin CSS, so it wins */
#header {
    background-color: #2c3e50;
}
#branding h1 a {
    color: #ecf0f1;
}
```

## 3. Custom Admin Templates

For structural changes (branding, layout, extra blocks), override templates
by mirroring the admin's template path inside your app:

```
myapp/templates/admin/base_site.html   # shadows django/contrib/admin/templates/admin/base_site.html
```

```html
{% extends "admin/base_site.html" %}
{% block title %}{{ title }} | My Site Admin{% endblock %}
{% block branding %}
<h1 id="site-name">
    <a href="{% url 'admin:index' %}">My Custom Admin</a>
</h1>
{% endblock %}
```

Template inheritance (`extends` + `block`) means you override one block, not
the whole page — the same DRY principle as view templates.

## 4. Knowing When to Stop

Admin theming has a ceiling: CSS tweaks and branding are cheap, rebuilding
admin workflows is not. If the "customization" list includes custom
dashboards, role-specific layouts, or customer-facing pages, that UI belongs
in your own views and templates — the admin stays an internal tool.

---

## 3. Common Mistakes

### Static files work locally, 404 in production
`collectstatic` was never run, or the web server doesn't serve `STATIC_ROOT`:
```bash
# WRONG - dev-only assumption
# (no collectstatic, DEBUG=False, whitenoise/nginx unconfigured)

# RIGHT - production static pipeline
python manage.py collectstatic --noinput   # STATIC_ROOT populated at deploy
```

### Override has no effect
The custom CSS loads before the admin's, or the template path is wrong:
```python
# WRONG - file at myapp/static/custom.css (wrong path, never found)
# WRONG - templates/myapp/base_site.html (missing the admin/ segment)

# RIGHT - mirror the exact admin-relative paths
# myapp/static/admin/css/custom.css
# myapp/templates/admin/base_site.html
```

### Editing Django's own static files in place
Changes vanish on the next `pip install --upgrade django`. Override through
the lookup path; never patch `site-packages`.

---

## 4. Best Practices

1. Keep admin styling to **branding** (logo, colors, title) — cheap and durable
2. Mirror **exact admin-relative paths** for every override
3. Run `collectstatic` in **CI/deploy**, never by hand on the server
4. Keep secrets out of CSS/JS — static files are **public by design**
5. Version custom admin assets (querystring or hashed names) to **beat browser cache**
6. Put customer-facing UI in **your own views**, not the admin
7. Test overrides with `DEBUG=False` locally before deploying

---

## 5. Practice Exercises

### Exercise 1: Brand the Admin
Create `myapp/static/admin/css/custom.css` changing the header color and
branding text color. Verify the override wins over default admin CSS.

### Exercise 2: Template Override
Write `myapp/templates/admin/base_site.html` extending the default, changing
the title suffix and branding block. Confirm the stock admin still renders.

### Exercise 3: Production Check
Run `collectstatic` into a fresh `STATIC_ROOT` and list the output proving
both admin defaults and your overrides were collected.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Admin static | Lives in `django/contrib/admin/static/admin/` |
| collectstatic | Gathers all apps' static files into `STATIC_ROOT` for production |
| CSS override | Same relative path in your app wins via finder order |
| Template override | Mirror path under `templates/admin/`, extend + block |
| Ceiling | Brand the admin; build real UI in your own views |
