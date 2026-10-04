# Django Quiz

## Topic Overview
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the "batteries included" philosophy, providing tools for authentication, database ORM, URL routing, templates, and more. This quiz covers Django's core concepts and common patterns.

**Difficulty:** Beginner to Intermediate
**Questions:** 20
**Time:** ~25 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What is Django primarily used for?**

A) Data analysis
B) Building web applications
C) Machine learning
D) Desktop applications

**Correct Answer:** B
**Explanation:** Django is a high-level Python web framework for building secure, maintainable web applications. It follows the MVC (Model-View-Controller) pattern, called MVT in Django.

---

### Question 2 [Easy]
**What does MVT stand for in Django?**

A) Model-View-Template
B) Model-View-Controller
C) Module-View-Template
D) Model-View-Transaction

**Correct Answer:** A
**Explanation:** Django uses the MVT pattern: Models (data), Views (business logic), and Templates (presentation). It's similar to MVC but with templates instead of views.

---

### Question 3 [Easy]
**How do you create a new Django project?**

A) `django-admin startproject project_name`
B) `django create project_name`
C) `django init project_name`
D) `pip install django`

**Correct Answer:** A
**Explanation:** `django-admin startproject` creates a new Django project with the standard directory structure. Then use `python manage.py startapp` to create apps within it.

---

### Question 4 [Easy]
**What is a Django app?**

A) A mobile application
B) A modular component that handles specific functionality
C) The main project
D) A template file

**Correct Answer:** B
**Explanation:** Django apps are modular components that handle specific features (e.g., blog, authentication, payments). A project contains multiple apps, each with its own models, views, and URLs.

---

### Question 5 [Medium]
**How do you define a model in Django?**

A) By creating a class that inherits from `django.db.models.Model`
B) By writing SQL directly
C) By creating a JSON file
D) By using decorators

**Correct Answer:** A
**Explanation:** Django models are Python classes that inherit from `Model`. Each class attribute represents a database field, and Django automatically creates the database table.

```python
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

---

### Question 6 [Medium]
**What does `python manage.py migrate` do?**

A) Moves files to production
B) Applies database migrations to create/update tables
C) Backs up the database
D) Transfers data between databases

**Correct Answer:** B
**Explanation:** `migrate` applies pending migrations to the database, creating tables and modifying schema. Always run `makemigrations` first to create migration files.

---

### Question 7 [Medium]
**What is the purpose of `urls.py` in Django?**

A) To configure database connections
B) To map URLs to views
C) To define models
D) To create templates

**Correct Answer:** B
**Explanation:** `urls.py` defines URL patterns that map URL paths to view functions. Django uses the `urlpatterns` list with `path()` or `re_path()` functions.

```python
from django.urls import path
from . import views

urlpatterns = [
    path("articles/", views.article_list, name="article_list"),
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
]
```

---

### Question 8 [Easy]
**What is the Django admin interface?**

A) A command-line tool
B) A built-in web interface for managing data
C) A database management tool
D) A file manager

**Correct Answer:** B
**Explanation:** Django provides a built-in admin interface that automatically generates a web-based UI for managing your data. It's highly customizable and great for content management.

---

### Question 9 [Medium]
**How do you create a superuser in Django?**

A) `python manage.py createsuperuser`
B) `python manage.py createadmin`
C) `python manage.py adduser`
D) `python manage.py superuser`

**Correct Answer:** A
**Explanation:** `createsuperuser` creates an admin user with full permissions. You'll be prompted for username, email, and password. This user can access the admin interface.

---

### Question 10 [Medium]
**What is the Django ORM?**

A) Object-Relational Mapping for database operations
B) Online Resource Manager
C) Output Rendering Module
D) Object Request Mapper

**Correct Answer:** A
**Explanation:** The ORM (Object-Relational Mapping) lets you interact with the database using Python objects instead of raw SQL. It supports multiple databases (PostgreSQL, MySQL, SQLite).

---

### Question 11 [Easy]
**What does `python manage.py runserver` do?**

A) Runs the production server
B) Starts the development server
C) Compiles the project
D) Runs database migrations

**Correct Answer:** B
**Explanation:** `runserver` starts Django's lightweight development server (default port 8000). It auto-reloads on code changes. Never use it in production.

---

### Question 12 [Medium]
**What is a Django template?**

A) A database schema
B) An HTML file with template tags for dynamic content
C) A Python script
D) A CSS file

**Correct Answer:** B
**Explanation:** Django templates are HTML files with special syntax (`{{ variable }}`, `{% tag %}`) for dynamic content. They support inheritance, filters, and custom tags.

---

### Question 13 [Medium]
**How do you render a template in a view?**

A) `return render(request, 'template.html', context)`
B) `return template('template.html')`
C) `return HttpResponse(template)`
D) `render_template('template.html')`

**Correct Answer:** A
**Explanation:** The `render()` shortcut combines template loading, context processing, and HttpResponse creation. It's the standard way to return rendered templates.

---

### Question 14 [Medium]
**What is `settings.py` used for?**

A) Project configuration (database, installed apps, middleware, etc.)
B) User settings
C) Template settings only
D) Database queries

**Correct Answer:** A
**Explanation:** `settings.py` contains all project configuration: database settings, installed apps, middleware, templates, static files, security settings, and more.

---

### Question 15 [Hard]
**What is middleware in Django?**

A) Software that processes requests/responses globally
B) Database middleware
C) Template middleware
D) File middleware

**Correct Answer:** A
**Explanation:** Middleware is a framework of hooks into Django's request/response processing. It can do security checks, session management, CSRF protection, and more.

---

### Question 16 [Easy]
**How do you create a Django app?**

A) `python manage.py startapp app_name`
B) `django-admin startapp app_name`
C) Both A and B
D) `python manage.py createapp app_name`

**Correct Answer:** C
**Explanation:** Both commands create a new Django app. `manage.py startapp` is used within a project, while `django-admin startapp` can create standalone apps.

---

### Question 17 [Medium]
**What is the purpose of `models.py` in a Django app?**

A) To define the database schema
B) To handle HTTP requests
C) To create templates
D) To configure URLs

**Correct Answer:** A
**Explanation:** `models.py` defines your data models as Python classes. Each model maps to a database table, and fields define columns with types and constraints.

---

### Question 18 [Medium]
**What is Django REST Framework (DRF)?**

A) A library for building REST APIs with Django
B) A framework for RESTful services
C) Both A and B
D) A testing framework

**Correct Answer:** A
**Explanation:** Django REST Framework is a powerful toolkit for building Web APIs. It provides serializers, viewsets, authentication, and browsable API interface.

---

### Question 19 [Hard]
**What is `select_related()` used for in Django ORM?**

A) Selecting related objects efficiently with JOIN
B) Selecting database tables
C) Filtering related data
D) Joining strings

**Correct Answer:** A
**Explanation:** `select_related()` performs a SQL JOIN to fetch related objects in a single query, preventing the N+1 query problem. Use it for ForeignKey and OneToOneField relationships.

---

### Question 20 [Medium]
**What does `python manage.py shell` do?**

A) Opens a Python shell with Django environment loaded
B) Opens a system shell
C) Runs a script
D) Compiles the project

**Correct Answer:** A
**Explanation:** `manage.py shell` opens an interactive Python shell with Django's settings and models loaded. This lets you interact with your models and test queries directly.

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | B |
| 2 | A |
| 3 | A |
| 4 | B |
| 5 | A |
| 6 | B |
| 7 | B |
| 8 | B |
| 9 | A |
| 10 | A |
| 11 | B |
| 12 | B |
| 13 | A |
| 14 | A |
| 15 | A |
| 16 | C |
| 17 | A |
| 18 | A |
| 19 | A |
| 20 | A |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered Django basics! |
| 14-17 | Proficient - Strong foundation, ready for advanced topics |
| 10-13 | Developing - Good start, practice more |
| 6-9 | Beginner - Review Django fundamentals |
| 0-5 | Novice - Start with Django tutorial |

---

*Quiz created for AI Engineer Lab - Python Foundations*
