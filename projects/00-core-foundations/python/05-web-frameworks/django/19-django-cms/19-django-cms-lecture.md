# Django Lecture 19: Django CMS (Content Management on Django)

## 🎯 Topic Overview

Django CMS puts an editor-friendly content layer on top of Django: pages
edited in place with a toolbar, content composed from plugins, and multiple
languages from the same page tree. This lecture covers the architecture
(pages, plugins, placeholders), the setup surface (apps, middleware,
templates, languages), and the decision that matters most — when a CMS beats
hand-built views and when it becomes the constraint. Reference-only: Django
is not installed by default.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the page tree, placeholders, and plugin model
2. List the required apps and middleware and state what each contributes
3. Configure CMS templates and multi-language settings
4. Build a custom plugin (model + rendering) from scratch
5. State the versioning, permissions, and SEO properties editors get for free
6. Decide CMS vs hand-built views from content-churn and editor-skill criteria

---

## 1. Architecture: Pages, Placeholders, Plugins

A CMS page is a node in a tree (URLs follow the tree). Each page renders a
template containing **placeholders** — named slots editors fill. **Plugins**
are the content blocks dropped into slots: text, images, custom models.
Developers define placeholders and plugin types; editors compose pages from
them. That split is the whole value proposition: code owns structure, editors
own content, and neither deploys to do the other's job.

## 2. Setup Surface

```python
INSTALLED_APPS = [
    'cms', 'menus', 'treebeard', 'sekizai',
    'djangocms_text_ckeditor',
]
MIDDLEWARE = [
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.PageAccessMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
]
CMS_TEMPLATES = [('base.html', 'Base'), ('blog.html', 'Blog Page')]
LANGUAGES = [('en', 'English'), ('es', 'Spanish')]
```

Each entry earns its place: `menus` renders navigation from the tree,
`treebeard` stores the page hierarchy efficiently, `sekizai` collects per-plugin
JS/CSS blocks, the middleware trio wires user, access control, and the
in-place toolbar. After install: `migrate`, `createsuperuser`, `runserver` —
pages are then created through the toolbar, not the shell.

## 3. Custom Plugins

A plugin is a model plus rendering. The pattern never varies:

```python
# models.py — what the plugin stores
class Testimonial(CMSPlugin):
    author = models.CharField(max_length=100)
    quote = models.TextField()

# cms_plugins.py — how it renders and edits
class TestimonialPlugin(CMSPluginBase):
    model = Testimonial
    render_template = "plugins/testimonial.html"
```

Editors get a form for free from the model fields; the template controls
output. New content type, no new views, no deploy to publish words.

## 4. What Editors Get for Free

Versioning (content history without git), role-based permissions (who may
publish vs draft), multi-language page trees from `LANGUAGES`, and
SEO-friendly URLs inherited from the tree structure. Price: the CMS owns page
routing and rendering conventions — custom interactive behavior fights the
framework instead of riding it.

## 5. CMS vs Hand-Built: The Decision

Choose the CMS when non-developers publish often, content is page-shaped, and
multiple languages multiply the work. Hand-build when content is
data-shaped (dashboards, feeds, app UI), interactions are custom, or
developers are the only authors. The wrong choice in either direction costs
months: editors filing tickets for text changes, or developers fighting page
routing for app behavior.

---

## 3. Common Mistakes

### Editing content via shell instead of the toolbar
```python
# WRONG - creates pages nobody can edit or version
# from cms.api import create_page  # for scripts/migrations only

# RIGHT - editors use the toolbar; the API is for automation
```

### One template for everything
```python
# WRONG - CMS_TEMPLATES = [('base.html', 'Everything')]
# RIGHT - a template per page shape: base, blog, landing
CMS_TEMPLATES = [('base.html', 'Base'), ('blog.html', 'Blog Page')]
```

### Skipping the plugin layer (hardcoding content in templates)
Content frozen in templates means a deploy per typo — the exact cost the CMS
exists to eliminate. If editors can't change it, it shouldn't be a template
string; make it a plugin.

---

## 4. Best Practices

1. One **template per page shape**, named for editors not developers
2. Model plugin **content**, template plugin **presentation** — never mix
3. Keep **permissions** tight: draft vs publish roles from day one
4. Plan **languages** before the first page (tree structure follows)
5. Put custom behavior in **plugins**, not template hacks
6. Version **templates in git**, content in the CMS — each where it belongs
7. Test plugin rendering with **unit tests** like any view

---

## 5. Practice Exercises

### Exercise 1: Plugin From Scratch
Build the Testimonial plugin above end to end: model, plugin class,
template, and a page showing two testimonials.

### Exercise 2: Multilingual Page
Add Spanish to `LANGUAGES`, translate one page, and verify URL routing serves
both versions with the toolbar language switcher.

### Exercise 3: The Decision Memo
For a hypothetical client blog with weekly posts in two languages, write the
one-page CMS-vs-hand-built decision with content-churn and editor-skill
evidence.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Page tree | URLs and hierarchy from tree structure (treebeard) |
| Placeholder | Named slot editors fill; developers define |
| Plugin | Model + template content block; no views needed |
| Toolbar | In-place editing, versioning, permissions |
| Decision | Editors + page-shaped + multilingual = CMS; app behavior = hand-build |
