Here is the reproducer script:

```python
from django.db import models
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    class Post(models.Model):
        title = models.CharField(max_length=255)
        authors = models.ManyToManyField("User", related_name="posts")

    class User(models.Model):
        email = models.EmailField(unique=True)

    admin.site.register(Post, admin.ModelAdmin)
    admin.site.search_fields = ("title", "authors__email")

    if __name__ == "__main__":
        try:
            post = Post.objects.create(title="Test Post", authors=[User(email="test@example.com")])
            post.delete()
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced")
        else:
            print("Issue not reproduced")

if __name__ == "__main__":
    main()

```

This script sets up a Django project, defines the models and admin interface as described in the issue, creates a post, and then attempts to delete it. If an error occurs during deletion (i.e., the Internal Server Error 500), it prints the stack trace using the provided `print_stacktrace` function and raises an `AssertionError`.