Here is the reproducer script:

```python
import os
from django.db import models
from django.contrib import admin
from django.urls import path
from django.test import TestCase, Client
from django.conf import settings
from django.core.exceptions import AssertionError

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
    from models import Post, User
    from admin import PostAdmin

    class ReproducerTestCase(TestCase):
        def setUp(self):
            self.client = Client()
            self.post = Post(title="Test", authors=[User(email="test@example.com")])
            self.post.save()

        def test_reproducer(self):
            response = self.client.get('/admin/post/')
            self.assertEqual(response.status_code, 200)

            response = self.client.post('/admin/post/', {'q': 'Te'})
            self.assertEqual(response.status_code, 302)

            response = self.client.get('/admin/post/?q=Test')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/admin/post/post/1/delete/')
            if response.status_code != 200:
                raise AssertionError("Deletion failed with status code {}".format(response.status_code))
except Exception as e:
    print_stacktrace(e)
    raise
```

This script sets up a Django project with the given models and admin configuration. It then runs a test case that reproduces the issue: it creates a post, searches for it using the search bar, selects the post, and then tries to delete it. If the deletion fails with an Internal Server Error (500), the script prints the stack trace of the error and raises an `AssertionError`.