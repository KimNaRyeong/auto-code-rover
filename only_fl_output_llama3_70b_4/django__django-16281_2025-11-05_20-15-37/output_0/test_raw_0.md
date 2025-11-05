Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.conf import settings
from django.core.management import call_command
from django.db import models
from django.test.utils import get_runner

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=['app']
)

class Bar(models.Model):
    pass

class Foo(models.Model):
    bar = models.ManyToManyField('Bar', blank=True)

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
    # Create initial migration
    call_command('makemigrations', 'app')
    call_command('migrate')

    # Change type of the ManyToManyField to Foo
    class Foo(models.Model):
        bar = models.ManyToManyField('Foo', blank=True)

    # Create new migration
    call_command('makemigrations', 'app')
    call_command('migrate')

    # Try to add a Foo instance through the admin interface
    from django.test.client import RequestFactory
    from django.contrib.admin.sites import AdminSite
    from app.admin import FooAdmin

    request_factory = RequestFactory()
    admin_site = AdminSite()

    foo_admin = FooAdmin(Foo, models.Model)
    admin_site.register(Foo, foo_admin)

    data = {'bar': []}
    request = request_factory.post('/admin/app/foo/add/', data)
    request.user = get_runner(settings).get_test_user()

    try:
        response = foo_admin.add_view(request)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")
except SystemExit:
    pass

print("Issue is fixed")
sys.exit(0)
```
This script creates a Django project with two models, `Bar` and `Foo`, and an admin interface for `Foo`. It then changes the target of the `ManyToManyField` from `Bar` to `Foo`, runs the migrations, and tries to add a new `Foo` instance through the admin interface. If the issue is present, it catches the exception, prints the stack trace using the provided function, and raises an `AssertionError`. If the issue is fixed, it simply prints "Issue is fixed" and exits with code 0.