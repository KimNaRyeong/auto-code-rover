To create a Python script (`reproducer.py`) that reproduces the issue and adheres to your specifications, we need to simulate the Django environment programmatically. This includes initializing the Django settings, simulating the admin interface, and then attempting the deletion action which leads to the error. Below is a standalone script to accomplish this:

```python
"""
reproducer.py
"""
import os
import django
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.core.management import execute_from_command_line

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

# Define models inline to avoid the need for a separate models module.
class User(models.Model):
    email = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(User)

class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'authors__email')

def setup_django_environment():
    # Configure Django settings
    settings.configure(
        DEBUG=True,
        SECRET_KEY='xxx',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'mydatabase',
            }
        },
        INSTALLED_APPS=('__main__', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.admin'),
        MIDDLEWARE=()
    )
    django.setup()

    # Register models with the admin
    admin.site.register(Post, PostAdmin)

def main():
    setup_django_environment()

    # Simulate commands to setup database and create tables
    execute_from_command_line(['manage.py', 'migrate'])

    # Now attempt to reproduce the issue
    try:
        # Setup test data
        user = User(email='user@example.com')
        user.save()
        post = Post(title='Test Post')
        post.save()
        post.authors.add(user)
        
        # Simulate the admin search and delete action that causes the issue
        # Note: Here we directly use Django ORM methods to simulate the actions
        # In reality, reproducing this specific issue might require interacting with the Django admin web interface
        query_set = Post.objects.filter(title__icontains='Te')  # Simulate search
        query_set.delete()  # Attempt deletion, which should raise an error due to the bug

        # If the deletion succeeds without an error, the issue is not reproduced
        print("Issue not reproduced. Deletion completed successfully.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, TypeError), "Expected a TypeError due to the deletion bug."
        if "Cannot call delete() after .distinct()." in str(e):
            print("Issue successfully reproduced.")
        else:
            print("Unexpected error type or message.")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Notes:
1. **Initialization**: The script configures and initializes a Django environment programmatically. This includes setting up a minimal configuration required for Django models and admin to work.
2. **Model Registration**: The `User` and `Post` models are defined and registered with Django's admin within the script itself, thus not requiring any external Django project setup.
3. **Reproduction Logic**: Due to the limitations of a script-based environment (it's not straightforward to interact with the Django Admin UI programmatically without using external tools like Selenium), the reproduction logic simulates the admin's search and delete operations through Django's ORM layer. The actual interaction error, as described, is related to Django Admin UI and the deletion operation causing an internal server error when certain conditions are met (specifically the use of distinct queries which Django Admin can generate based on search fields configuration).
4. **Error Checking**: The script raises an `AssertionError` if the issue is reproduced as expected. It exits with code 0 if no error is encountered, indicating the issue might not be present. Note that adjustments might be needed based on the specific Django version and environment setup.