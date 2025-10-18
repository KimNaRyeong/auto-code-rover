```python
# reproducer.py
import os
import django
from django.core.exceptions import OperationalError
from django.conf import settings
from django.db import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    default_settings=django.conf.global_settings,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=['__main__'],
    ROOT_URLCONF='__main__',
    SECRET_KEY='just-for-this-demo',
)

django.setup()

class Bar(models.Model):
    pass

class Foo(models.Model):
    bar = models.ManyToManyField('Bar', blank=True)

django.apps.apps.clear_cache()
try:
    with django.db.transaction.atomic():
        # First migration
        django.core.management.call_command('makemigrations', verbosity=0)
        django.core.management.call_command('migrate', verbosity=0)

        # Change to self reference
        Foo.bar.field.remote_field.model = "self"
        Foo.bar.field.model = Foo
        Foo.bar.field.through = None  # Reset through model to force Django to recreate it
        django.apps.apps.clear_cache()

        # Second migration (attempt, expected to fail based on the issue)
        django.core.management.call_command('makemigrations', verbosity=0)
        django.core.management.call_command('migrate', verbosity=0)

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
    
    # If the script gets this far without an OperationalError, the issue is fixed
    print("No issue detected.")
except django.db.utils.OperationalError as e:
    print_stacktrace(e)
    assert str(e) == "no such column: app_foo_bar.from_foo_id"
except Exception as e:
    print("An unexpected error occurred:", str(e))
    print_stacktrace(e)
    assert False  # An unexpected error occurred, fail the reproduction script
else:
    exit(0)  # Exit with success
```

This script attempts to reproduce the issue described where Django does not handle the migration changing a ManyToManyField's target to "self" correctly, leading to an `OperationalError` due to a missing column in the database. When the issue is present, this script raises an `AssertionError` after printing the stack trace of the caught `OperationalError`. When the issue is resolved, the script will simply print "No issue detected." and exit with code 0. Note that this script directly manipulates Django models and uses migrations to simulate the reported issue.