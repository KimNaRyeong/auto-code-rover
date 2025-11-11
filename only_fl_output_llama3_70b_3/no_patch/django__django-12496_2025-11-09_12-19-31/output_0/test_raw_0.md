Here is the `reproducer.py` file to reproduce the issue:
```
import os
import sys
from django.db import models
from django.test.utils import setup_test_environment
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    },
    INSTALLED_APPS=['app'],
)

from django.test.runner import DiscoverRunner

setup_test_environment()

class Parent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()

class Child(Parent):
    body = models.TextField()

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
    from django.core.management import call_command
    call_command('makemigrations', 'app')
    call_command('migrate')

    child = Child.objects.create()
    queries = len(connection.queries)

    if queries > 3:  # expected queries: 2 (insert into parent and child)
        raise AssertionError("Extra query detected")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a Django project with a custom primary key on the `Parent` model, creates a `Child` object, and checks if more than 3 queries are executed. If an extra query is detected, it raises an `AssertionError` with a stack trace of the issue.