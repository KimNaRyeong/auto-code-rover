Here is the reproducer script:

```python
import os
from django.db import models
from django.contrib import admin
from django.urls import path
from django.test.utils import setup_test_environment
from django.core.management import execute_from_command_line
from django.conf import settings

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

# Set up Django environment for testing
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
setup_test_environment()

try:
    # Create the models
    models_file_path = 'models.py'
    with open(models_file_path, 'w') as f:
        f.write("""
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User", related_name="posts")

class User(models.Model):
    email = models.EmailField(unique=True)
""")

    # Create the admin
    admin_file_path = 'admin.py'
    with open(admin_file_path, 'w') as f:
        f.write("""
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")
""")

    # Create the urls
    urls_file_path = 'urls.py'
    with open(urls_file_path, 'w') as f:
        f.write("""
from django.urls import path
from .admin import admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
]
""")

    # Run the Django app
    execute_from_command_line(['manage.py', 'runserver'])

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script creates a new Django project, defines the models and admin configuration, and then runs the Django development server. If an `AssertionError` is raised during this process, it prints the stack trace using the provided function and exits with code 1.