Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.contrib import admin
from django.db import models
from django.test import TestCase

# Define models
class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User")

class User(models.Model):
    email = models.EmailField(unique=True)

# Define admin interface
class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")

admin.site.register(Post, PostAdmin)

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    # Create test database
    os.environ["DJANGO_SETTINGS_MODULE"] = "reproducer.settings"
    from django.core.management import execute_from_command_line
    execute_from_command_line(["", "migrate"])

    # Create test data
    user = User(email="test@example.com")
    user.save()
    post = Post(title="Test Post")
    post.save()
    post.authors.add(user)

    # Try to delete the post using the admin interface
    from django.test.client import RequestFactory
    rf = RequestFactory()
    request = rf.post("/admin/post/post/?q=Te", data={"action": "delete_selected"})
    request.user = TestCase()

    try:
        from django.contrib.admin.sites import AdminSite
        admin_site = AdminSite()
        response = admin_site.login(request)
        response = admin_site.delete_selected(request, Post.objects.all())
        assert False, "Expected an error"
    except Exception as e:
        print_stacktrace(e)
        if isinstance(e, TypeError) and str(e).startswith("Cannot call delete() after .distinct()."):
            raise AssertionError("Issue is present")
        else:
            print("Unexpected error:", file=sys.stderr)
            print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```
This script defines the models and admin interface, creates a test database, adds some test data, and then tries to delete the post using the admin interface. If the issue is present, it raises an `AssertionError` with a stack trace of the error. If the issue is fixed, it exits with code 0.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.