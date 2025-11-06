Here is the reproducer script:

```python
import os
from django.db import models
from django.contrib import admin
from django.urls import path
from django.test.utils import setup_test_environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')

django.setup()

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

try:
    from .models import Post, User
    from .admin import admin_site

    class Post(models.Model):
        title = models.CharField(max_length=255)
        authors = models.ManyToManyField("User", related_name="posts")

    class User(models.Model):
        email = models.EmailField(unique=True)

    admin.site.register(Post, PostAdmin=admin.ModelAdmin(search_fields=("title", "authors__email")))

    post = Post(title="Test", authors=[User(email="test@example.com")])
    post.save()
    admin.site.go('admin/post/')
    input("Press Enter to delete the post...")
    try:
        admin.site.delete_queryset(Post.objects.all())
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error occurred"
    else:
        print("No error occurred")
        exit(0)

except Exception as e:
    print_stacktrace(e)
    assert False, "Error occurred"

```

This script will create a Django project and then attempt to reproduce the issue. If the issue is present, it will print the stack trace and raise an `AssertionError`.