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
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'reproducer',  # our test app
    ],
)

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = ManyToManyField(User)

class PostAdmin(admin.ModelAdmin):
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

def main():
    setup_test_environment()
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE reproducer_post (id SERIAL PRIMARY KEY, title VARCHAR(255) NOT NULL);")
    cursor.execute("INSERT INTO reproducer_post (title) VALUES ('Test Post');")
    cursor.execute("INSERT INTO auth_user (email) VALUES ('test@example.com');")
    cursor.execute("CREATE TABLE reproducer_post_authors (post_id INTEGER NOT NULL, user_id INTEGER NOT NULL, PRIMARY KEY (post_id, user_id));")
    cursor.execute("INSERT INTO reproducer_post_authors (post_id, user_id) VALUES (1, 1);")

    from django.contrib.admin.sites import AdminSite
    admin.site = AdminSite()

    try:
        from django.test.client import RequestFactory
        rf = RequestFactory()
        request = rf.post('/admin/post/post/?q=Te', {'action': 'delete_selected'})
        request.user = User.objects.get(email='test@example.com')
        PostAdmin(Post, admin.site).delete_queryset(request, Post.objects.all())
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")
    else:
        print("Issue is fixed")

if __name__ == "__main__":
    main()
```
This script creates a test database with a `Post` model and an admin interface for it. It then inserts some data into the database and tries to delete all posts using the admin interface. If the issue is present, it will raise an `AssertionError` with a stack trace of the error.