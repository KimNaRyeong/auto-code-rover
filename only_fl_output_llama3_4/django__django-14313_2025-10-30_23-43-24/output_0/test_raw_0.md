Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

django.setup()

models.py:
class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User", related_name="posts")

class User(models.Model):
    email = models.EmailField(unique=True)

admin.py:
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")
```

```python
# reproducer.py
import os
import django
from django.db import models
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

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
    from .models import Post
    from .admin import admin

    # Create a test database and populate it with some data
    models.Model._meta.db = 'test'
    models.Model._meta.app_label = 'test_project'

    post1 = Post(title='Test Post 1', authors=[User(email='user1@example.com')])
    post2 = Post(title='Test Post 2', authors=[User(email='user2@example.com')])

    # Save the posts to the database
    post1.save()
    post2.save()

    # Open the admin page and delete one of the posts
    response = admin.site.get_response(HttpResponse, path='/admin/post/')
    response.render()

    # Search for a term in the search box
    search_term = 'Test'
    response = admin.site.get_response(HttpResponse, path=f'/admin/post/?q={search_term}')
    response.render()

    # Select the post and delete it
    response = admin.site.get_response(HttpResponse, path='/admin/post/post/1/delete/')
    response.render()
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Error reproducing the issue")

print("Issue not reproduced")
exit(0)
```

This script creates a test database and populates it with two posts. It then opens the admin page, searches for a term in the search box, selects one of the posts, and deletes it. If an error occurs during this process, it prints the stack trace and raises an `AssertionError`.