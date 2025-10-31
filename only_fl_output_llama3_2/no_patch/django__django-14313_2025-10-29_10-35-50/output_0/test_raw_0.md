Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.core.exceptions import AssertionError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')

django.setup()

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User", related_name="posts")

class User(models.Model):
    email = models.EmailField(unique=True)

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
    from django.db.models import Q
    from django.contrib.admin.utils import NestedObjects

    class PostAdmin(admin.ModelAdmin):
        search_fields = ("title", "authors__email")

    admin.site.register(Post, PostAdmin)

    # Create some test data
    post1 = Post(title="Post 1", authors=[User(email="user1@example.com")])
    post2 = Post(title="Post 2", authors=[User(email="user2@example.com")])

    post1.save()
    post2.save()

    # Search for a post and then delete it
    response = admin.site.urls.get('post', 'post/')(HttpResponse())
    response.write('<html><body><form action="/admin/post/post/" method="get"><input type="text" name="q"></form></body></html>')
    response.write('<script>window.onload = function() { document.querySelector("form").submit(); }</script>')

    admin.site.urls.get('post', 'post/')(response)

except AssertionError as e:
    print_stacktrace(e)
    exit(0)
else:
    print("Issue not present")
    exit(1)
```

This script should be run in the root directory of your project. It will create some test data, search for a post and then delete it. If the issue is present, it will raise an `AssertionError` with the stack trace printed to the console.