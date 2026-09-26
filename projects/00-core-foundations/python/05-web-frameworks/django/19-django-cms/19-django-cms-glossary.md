# Django 19: Django CMS — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Django CMS | Editor-friendly content layer on Django | marketing site |
| Page tree | Hierarchical page structure driving URLs | /blog/2026/post |
| Placeholder | Named template slot editors fill with plugins | `{% placeholder "body" %}` |
| Plugin | Reusable content block: model + template | testimonial, gallery |
| Toolbar | In-place editing bar for staff users | draft/publish buttons |
| treebeard | Efficient tree storage backing the page hierarchy | page moves stay cheap |
| sekizai | Collects per-plugin JS/CSS blocks into the page | plugin asset injection |
| CMS_TEMPLATES | Page-shape registry editors choose from | base, blog, landing |

---

## Alphabetical Glossary

### CMS_TEMPLATES

**Definition:** Settings registry mapping template files to editor-visible
page shapes. One entry per genuinely different layout.

**Example:**
```python
CMS_TEMPLATES = [("base.html", "Base"), ("blog.html", "Blog Page")]
```

**Related concepts:** Placeholder, Page tree

---

### Django CMS

**Definition:** Open-source content management system built on Django:
visual editing, plugins, multilingual trees, versioning, permissions.

**Example:**
```python
# pip install django-cms — editors publish without deploys
```

**Related concepts:** Placeholder, Plugin, Toolbar

---

### Page tree

**Definition:** The hierarchy of CMS pages; URLs, navigation (via `menus`),
and permissions follow it. Managed by treebeard for cheap moves.

**Example:**
```python
# /products/widget/ mirrors its position in the tree
```

**Related concepts:** treebeard, CMS_TEMPLATES

---

### Placeholder

**Definition:** A named slot in a CMS template that editors fill with plugin
instances. Developers define slots; editors own what goes in them.

**Example:**
```html
{% placeholder "sidebar" %}
```

**Related concepts:** Plugin, CMS_TEMPLATES

---

### Plugin

**Definition:** A reusable content block: a Django model for storage plus a
template for rendering, registered via a plugin class. New content types
without new views.

**Example:**
```python
class TestimonialPlugin(CMSPluginBase):
    model = Testimonial
    render_template = "plugins/testimonial.html"
```

**Related concepts:** Placeholder, Toolbar

---

### sekizai

**Definition:** Library collecting JavaScript/CSS blocks from individual
plugins into the page head/foot. Each plugin declares assets; sekizai
assembles them without duplicates.

**Example:**
```html
{% render_block "js" %}  <!-- gallery plugin's script lands here -->
```

**Related concepts:** Plugin

---

### Toolbar

**Definition:** The in-place editing interface for staff: draft, preview,
publish, version history, and permission-gated actions per page.

**Example:**
```python
# 'cms.middleware.toolbar.ToolbarMiddleware' enables it
```

**Related concepts:** Django CMS, Plugin

---

### treebeard

**Definition:** Django library for efficient tree storage (materialized path
et al.) backing the CMS page hierarchy. Moves and inserts stay cheap.

**Example:**
```python
# dragging a page with 200 children reorders without N+1 writes
```

**Related concepts:** Page tree

---

## Related Concepts

- **Versioning**: content history without git, free with the CMS
- **LANGUAGES**: setting driving multilingual page trees
- **Wagtail**: the main Django-CMS alternative (different editing model)

## Key Takeaways

1. Structure in code (placeholders, plugins), content with editors.
2. Toolbar + versioning + permissions are the free wins.
3. Page-shaped + editor-driven = CMS; app behavior = hand-build.
