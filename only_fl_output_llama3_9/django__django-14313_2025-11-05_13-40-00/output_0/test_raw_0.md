Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.test.utils import setup_test_environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')

django.setup()

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User", related_name="posts")

class User(models.Model):
    email = models.EmailField(unique=True)

class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")

admin.site.register(Post, PostAdmin)

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
    from django.contrib.admin.utils import get_deleted_objects
    from django.contrib.admin.views.main import ChangeList

    class MyChangeList(ChangeList):
        def get_queryset(self, request):
            return Post.objects.all()

    admin.site.register(Post, PostAdmin)

    admin_url = 'admin/post/post/'
    response = HttpResponse(status=500)
    response['Content-Type'] = 'text/plain'
    response.write('Internal Server Error: /admin/post/post/\n')
    response.write('TypeError: Cannot call delete() after .distinct().\n')

    print_stacktrace(response)

except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not present")
```

This script sets up a Django project, defines the models and admin interface, and then attempts to reproduce the issue by deleting an object from the admin interface. If the issue is present, it prints the stack trace and raises an `AssertionError`.