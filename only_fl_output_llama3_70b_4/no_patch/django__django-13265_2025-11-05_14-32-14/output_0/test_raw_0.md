Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys

from django.db import models
from django.core.management import call_command

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

# Create a new Django project
os.system("django-admin startproject reproducer_project")
os.chdir("reproducer_project")

# Create a new app
os.system("python manage.py startapp posts")

# Define the models
with open("posts/models.py", "w") as f:
    f.write("""
from django.db import models

class Look(models.Model):
    pass

class LookImage(models.Model):
    look = models.ForeignKey('Look', on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(blank=True, max_length=10000, null=True)
    image = models.ImageField(max_length=2000, upload_to='')
    deleted = models.DateTimeField(editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'look_image'
        order_with_respect_to = 'look'
        indexes = [
            models.Index(fields=['look', '_order']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
""")

# Make migrations
call_command("makemigrations", "posts")
call_command("migrate")

try:
    # Apply the migration that raises the error
    call_command("migrate", "posts", "0002")
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present") from e

print("Issue is fixed")
sys.exit(0)
```
This script creates a new Django project, app, and models, then applies the migrations that reproduce the issue. If the issue is present, it raises an `AssertionError` with a stack trace of the error. If the issue is fixed, it prints "Issue is fixed" and exits with code 0.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.