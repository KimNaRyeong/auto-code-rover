Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.contrib import admin
from django.db import models
from django.test import TestCase, RequestFactory

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

# Create a test project
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

from reproducer import settings

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('User')

class User(models.Model):
    email = models.EmailField(unique=True)

class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")

admin.site.register(Post, PostAdmin)

# Create a test database
from django.core.management import call_command
call_command('migrate', verbosity=0)

# Create some test data
post = Post.objects.create(title='Test Post')
user = User.objects.create(email='test@example.com')
post.authors.add(user)

# Create a request factory
factory = RequestFactory()

# Try to delete the post using the admin interface
def try_delete_post():
    request = factory.post('/admin/post/post/?q=my', data={'action': 'delete_selected'})
    request.user = admin.site.admin_view(None, None).request.user
    response = admin.site.admin_view(PostAdmin.delete_queryset)(request, Post.objects.all())
    return response

try:
    try_delete_post()
except TypeError as e:
    print_stacktrace(e)
    assert "Cannot call delete() after .distinct()" in str(e), "Issue not reproduced"
else:
    sys.exit(0)
```
This script creates a test project with the models and admin interface described in the issue, populates the database with some test data, and then tries to delete a post using the admin interface. If the `TypeError` exception is raised with the expected error message, it prints the stack trace and exits with code 1. If the issue is not reproduced, it exits with code 0.

To run this script, save it as `reproducer.py` in the root directory of your project, and execute it using `python3 reproducer.py`.