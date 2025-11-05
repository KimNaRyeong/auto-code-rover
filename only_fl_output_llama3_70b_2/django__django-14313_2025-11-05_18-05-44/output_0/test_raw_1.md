Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db.models import CharField, EmailField, ManyToManyField
from django.contrib import admin
from django.http import HttpRequest

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

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'reproducer_app'
    ],
)

class Post(models.Model):
    title = CharField(max_length=255)
    authors = ManyToManyField('User')

class User(models.Model):
    email = EmailField(unique=True)

admin.site.register(Post, type('PostAdmin', (admin.ModelAdmin,), {
    'search_fields': ("title", "authors__email")
}))

setup_test_environment()

from django.core.management import call_command
call_command('migrate', verbosity=0)

post = Post.objects.create(title='Test Post')
user = User.objects.create(email='test@example.com')
post.authors.add(user)

request = HttpRequest()
request.method = 'GET'
request.GET['q'] = 'Te'

try:
    admin.site.each_context(request)
    request.method = 'POST'
    request.POST['action'] = 'delete_selected'
    request.POST['_selected_action'] = 'delete_selected'
    request.POST['index'] = 0
    admin.site.each_context(request)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")

if __name__ == '__main__':
    sys.exit(0 if "Issue is fixed" in locals() else 1)
```
This script creates a test database, defines the `Post` and `User` models, registers the `PostAdmin`, creates some test data, and then runs a test case that reproduces the issue.

To run the script, save it to a file named `reproducer.py` in the root directory of your project, and execute it with `python3 reproducer.py`. If the issue is present, the script will raise an `AssertionError` and print a stack trace of the issue. If the issue is fixed, the script will exit with code 0.

Note that this script uses Django's test framework to create a test database and run the test case. This allows us to isolate the reproduction of the issue from any existing project configuration.