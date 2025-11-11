Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db.models import String, ManyToManyField
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydatabase',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'reproducer',  # our app
    ],
)

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User")

class User(models.Model):
    email = models.EmailField(unique=True)

class PostAdmin(ModelAdmin):
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
    from django.core.management import execute_from_command_line
    execute_from_command_line(['reproducer', 'migrate'])

    # Create a post with an author
    from reproducer.models import Post, User
    user = User(email="user@example.com")
    user.save()
    post = Post(title="My Post")
    post.save()
    post.authors.add(user)

    # Search for the post and delete it
    from django.contrib.admin.sites import AdminSite
    admin.site = AdminSite()
    request = setup_test_environment().request
    request.method = 'POST'
    request.POST = {'action': 'delete_selected', '_selected_action': ['1']}
    changelist_view = PostAdmin(Post, admin.site).changelist_view
    try:
        changelist_view(request)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    reproduce_issue()
```
This script sets up a Django project with the required models and admin configuration, creates a post with an author, searches for the post, and then tries to delete it. If the issue is present, it will raise an `AssertionError` with a stack trace of the error.

To run this script, save it as `reproducer.py` in the root directory of your project, and execute it with `python3 reproducer.py`.