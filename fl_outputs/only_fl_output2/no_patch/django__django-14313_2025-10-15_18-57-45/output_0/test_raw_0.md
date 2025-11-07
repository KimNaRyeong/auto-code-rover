To create a `reproducer.py` script that sets up the necessary Django environment, models, and admin configuration to reproduce the mentioned issue and print a detailed stack trace, follow the script below. This script assumes you have Django installed and a Postgres database ready for connection. Update the database settings as per your Postgres configuration:

```python
"""
reproducer.py
"""

import os
import django
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.db import models
from django.conf import settings
from django.contrib import admin


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


def setup_django_environment():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

    settings.configure(
        DATABASES=DATABASES,
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.admin",
            "__main__",  # Allow the Post and User models to be recognized by Django.
        ],
        MIDDLEWARE=[],
        ROOT_URLCONF=__name__,
    )

    try:
        django.setup()
    except ImproperlyConfigured as e:
        print("Django setup failed:", e)
        exit(1)


# Models definition
class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User", related_name="posts")


class User(models.Model):
    email = models.CharField(max_length=255)


# Admin
class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")


try:
    setup_django_environment()

    # Registering models to the admin
    admin.site.register(Post, PostAdmin)
    admin.site.register(User)

    # Prepare the database
    call_command('migrate', interactive=False, verbosity=0)

    # Create sample data
    user = User.objects.create(email="testuser@example.com")
    post = Post.objects.create(title="Example Post")
    post.authors.add(user)

    # Try to reproduce the error described
    try:
        assert Post.objects.count() == 1, "Setup failed, there should be exactly one Post instance."
        Post.objects.all().delete()
        print("Issue not reproduced, exited with code 0.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "AssertionError when issue is present."

except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

### Notes:
- Update `DATABASES` configuration with your Postgres database credentials.
- This script directly interacts with the database and tries to delete a `Post` instance. The deletion part should trigger the error if the issue exists.
- If the issue is fixed, it will simply print a successful message. If not, it will try to print a detailed stack trace using the provided function.
- Remember to create a database that matches the provided credentials and ensure the user has the necessary permissions.
- Use a virtual environment and ensure Django is installed (`pip install django`) before running this script.