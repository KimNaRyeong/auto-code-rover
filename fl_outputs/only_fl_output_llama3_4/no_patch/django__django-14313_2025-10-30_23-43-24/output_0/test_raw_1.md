Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.contrib import admin
from django.urls import path
from django.test.utils import setup_test_environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')

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

class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")

urlpatterns = [
    path('admin/', admin.site.urls),
]

if __name__ == "__main__":
    from django.test.client import RequestFactory
    request_factory = RequestFactory()

    # Create a post with one author
    post = Post(title="Test Post", authors=[User(email="test@example.com")])
    post.save()

    # Search for the post
    request = request_factory.get('/admin/post/post/?q=my')
    admin.site.each_context(request)
    response = admin.site.admin_view(PostAdmin.search)(request)

    # Delete the post
    request = request_factory.post('/admin/post/post/', {'_selected_action': 'object_list', '_action': 'delete_selected'})
    try:
        PostAdmin.delete_queryset(None, [post])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Error reproducing the issue")

    # Check if the post is still in the database
    assert not Post.objects.exists()
```

This script creates a minimal Django project with two models: `Post` and `User`. The `Post` model has a many-to-many field to the `User` model. It then sets up an admin interface for the `Post` model, including a search function that searches on both the post title and the email addresses of its authors.

The script then creates a single post with one author, searches for it using the admin interface, deletes it, and checks if the post is still in the database. If the post is not deleted correctly (i.e., the issue is present), an `AssertionError` is raised with the stack trace printed to the console.

If you run this script and see an error message with a stack trace, then the issue is present.