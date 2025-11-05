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
    setup_test_environment()
    
    from reproducer.models import Post, User
    from django.contrib import admin
    
    class PostAdmin(admin.ModelAdmin):
        search_fields = ("title", "authors__email")
    
    admin.site.register(Post, PostAdmin)
    
    post = Post(title="Test Post", authors=User(email="test@example.com"))
    post.save()
    
    # Open the admin site and perform a search
    from django.test.client import RequestFactory
    factory = RequestFactory()
    request = factory.get('/admin/post/post/?q=Te')
    request.user = admin.helpers.AdminUser()
    
    # Select the post and delete it
    response = admin.site.admin_view(PostAdmin.changelist_view)(request)
    data = {'action': 'delete_selected', '_selected_action': 'delete_selected'}
    request = factory.post('/admin/post/post/?q=Te', data)
    response = admin.site.admin_view(PostAdmin.response_action)(request, queryset=post.objects.all())
    
    # Check if the issue is present
    if 'Cannot call delete() after .distinct()' in str(response):
        raise AssertionError("Issue is present")
    
except ImproperlyConfigured:
    print("Error: DJANGO_SETTINGS_MODULE is not set", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

finally:
    teardown_test_environment()
    connection.creation = BaseDatabaseCreation(connection)

print("Issue is fixed")
sys.exit(0)
```
This script sets up a Django test environment, creates a `Post` model with a many-to-many field `authors`, registers it to the admin site, and performs a search and deletion action. If the issue is present, it raises an `AssertionError`. If not, it prints "Issue is fixed" and exits with code 0.

Note that you need to create a `reproducer` directory in the same directory as this script, and inside it, create a `settings.py` file with the following content:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'reproducer',
]

SECRET_KEY = 'mysecretkey'
```
Replace the database settings with your own.

Run the script using `python3 reproducer.py`.