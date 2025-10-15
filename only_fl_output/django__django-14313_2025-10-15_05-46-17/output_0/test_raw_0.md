```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.core.management import call_command
from django.core.exceptions import ImproperlyConfigured

def setup_django_environment():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        INSTALLED_APPS=('__main__',)
    )
    try:
        django.setup()
    except ImproperlyConfigured as e:
        print("Django setup failed:", e)

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User", related_name="posts")

class User(models.Model):
    email = models.CharField(max_length=255)

class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")

def add_test_data():
    user = User.objects.create(email="user@example.com")
    post = Post.objects.create(title="Test Post")
    post.authors.add(user)

def main():
    setup_django_environment()
    
    # Register models with admin
    admin.site.register(Post, PostAdmin)
    
    # Migrate database
    call_command('migrate', '--noinput')
    
    # Add test data
    add_test_data()
    
    # Perform the test
    try:
        post_query = Post.objects.filter(title__startswith="Te")
        post_query.delete()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present") from e
    else:
        print("Issue is fixed. Exiting with code 0.")
        exit(0)

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