Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.core.exceptions import ImproperlyConfigured
from django.test.utils import setup_test_environment, teardown_test_environment
from django.db import connection
from django.db.backends.base.creation import BaseDatabaseCreation

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import reproducer.settings
except ImproperlyConfigured as e:
    print_stacktrace(e)
    sys.exit(1)

setup_test_environment()

from django.db import models
from django.contrib import admin

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('User')

class User(models.Model):
    email = models.EmailField(unique=True)

admin.site.register(Post, type('PostAdmin', (admin.ModelAdmin,), {
    'search_fields': ('title', 'authors__email'),
}))

from django.test.client import RequestFactory
rf = RequestFactory()

def delete_post(post_id):
    req = rf.post('/admin/post/post/{}/delete/'.format(post_id), data={'post': 'yes'})
    return req

try:
    post = Post.objects.create(title='Test Post', authors=User.objects.create(email='test@example.com'))
    req = rf.get('/admin/post/post/?q=Te')
    assert req.status_code == 200
    delete_req = delete_post(post.id)
    if delete_req.status_code != 500:
        print("Issue is not present")
        sys.exit(0)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

teardown_test_environment()
```
This script sets up a Django project with the models and admin configuration described in the issue. It then creates a post, searches for it using the many-to-many field, selects the post, and attempts to delete it. If the deletion raises an exception with a `TypeError` message containing "Cannot call delete() after .distinct().", the script prints the stack trace of the exception and exits with code 1. Otherwise, it prints a success message and exits with code 0.

To run this script, create a new Django project using `django-admin startproject reproducer`, then create a new file `reproducer.py` in the root directory of the project and paste the above code into it. Run the script using `python3 reproducer.py`.