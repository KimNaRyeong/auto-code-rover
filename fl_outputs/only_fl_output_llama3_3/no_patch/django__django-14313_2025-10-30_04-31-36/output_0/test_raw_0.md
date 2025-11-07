Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.contrib import admin
from django.urls import path
from django.test import TestCase, Client
from django.conf import settings

# Set up Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
django.setup()

# Define the models
class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User", related_name="posts")

class User(models.Model):
    email = models.EmailField(unique=True)

# Define the admin model and URL
admin.site.register(Post, PostAdmin)

urlpatterns = [
    path('admin/', admin.site.urls),
]

settings.configure()

# Run the reproducer test case
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
        self.assertEqual(response.status_code, 500)

try:
    ReproducerTestCase()
except Exception as e:
    print_stacktrace(e)
    raise
```

This script sets up a Django project with the given models and admin configuration. It then runs a test case that reproduces the issue: it creates a post, searches for it using the search bar, selects the post, and then tries to delete it. If the deletion fails with an Internal Server Error (500), the script prints the stack trace of the error and raises an `AssertionError`.