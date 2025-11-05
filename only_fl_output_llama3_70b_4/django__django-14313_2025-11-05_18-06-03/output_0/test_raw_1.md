Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
```python
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db.models import String, ManyToManyField
from django.contrib import admin
from django.contrib.auth.models import User

# Set up Django project and app
settings.configure(
    DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "test_db"}},
    INSTALLED_APPS=("django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes"),
)

# Define models
class Post(models.Model):
    title = String(max_length=255)
    authors = ManyToManyField(User)

# Create admin interface
class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")

admin.site.register(Post, PostAdmin)

# Set up test environment
setup_test_environment()

# Create a test user and post
User.objects.create_user("testuser", "test@example.com", "password")
post = Post(title="Test Post", authors=User.objects.all())

# Run the admin interface
from django.test.client import RequestFactory

rf = RequestFactory()
request = rf.get("/admin/post/post/?q=my")

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

try:
    admin.site.each_context(request)
    post.delete()
except TypeError as e:
    if "Cannot call delete() after .distinct()" in str(e):
        print_stacktrace(e)
        raise AssertionError("Issue is present")
    else:
        raise

print("Issue is fixed")
sys.exit(0)
```
This script sets up a Django project and app, defines the `Post` model with a many-to-many field to `User`, creates an admin interface for the `Post` model, and then runs the admin interface to reproduce the issue. If the issue is present, it prints the stack trace and raises an `AssertionError`. If the issue is fixed, it prints "Issue is fixed" and exits with code 0.

To run this script, save it as `reproducer.py` in the root directory of your project, then execute it with `python3 reproducer.py`.