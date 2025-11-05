Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.contrib import admin
from django.urls import path
from django.test.utils import setup_test_environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')

django.setup()

models.py:
class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User", related_name="posts")

class User(models.Model):
    email = models.EmailField(unique=True)

admin.py:
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")

reproducer.py:
import os
import sys
from django.core.management import execute_from_command_line
from reproducer.models import Post, User
from reproducer.admin import PostAdmin

def main():
    try:
        execute_from_command_line([os.path.join('reproducer', 'manage.py'), 'runserver'])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

This script sets up a Django project, defines the models and admin interface as described in the issue description, runs the development server, and catches any exceptions that occur. If an exception occurs, it prints the stack trace using the provided function and exits with code 1.