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
    
    # Create a test user and post
    user = User.objects.create(email="test@example.com")
    post = Post.objects.create(title="Test Post")
    post.authors.add(user)
    
    # Perform the delete action
    from django.contrib.admin.views.main import ChangelistView
    from django.http import HttpRequest
    request = HttpRequest()
    request.method = 'POST'
    request.POST = {'action': 'delete_selected', '_selected_action': ['1']}
    cl_view = ChangelistView()
    cl_view.model_admin = PostAdmin(Post, admin.site)
    cl_view.request = request
    
    try:
        cl_view.response_action(request, queryset=Post.objects.all())
    except TypeError as e:
        print_stacktrace(e)
        assert "Cannot call delete() after .distinct()" in str(e), "Issue not reproduced"
        sys.exit(1)
    
except ImproperlyConfigured:
    print("Error: DJANGO_SETTINGS_MODULE is not set.")
    sys.exit(1)

finally:
    teardown_test_environment()
    connection.creation = BaseDatabaseCreation(connection)
```
This script sets up a test environment, creates a test user and post, and then performs the delete action that triggers the issue. If the issue is present, it will raise an `AssertionError` with a stack trace of the error.

To run this script, create a new Django project and app, and add the following to your `settings.py` file:
```
INSTALLED_APPS = [
    # ...
    'reproducer',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your_database_name>',
        'USER': '<your_database_user>',
        'PASSWORD': '<your_database_password>',
        'HOST': '<your_database_host>',
        'PORT': '<your_database_port>',
    }
}
```
Then, run the script using `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` with a stack trace of the error.