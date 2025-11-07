Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys

from django.conf import settings
from django.db import models
from django.db.models import Count, F

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth'
    ]
)

from django.test.utils import setup_test_environment
setup_test_environment()

class Thing(models.Model):
    pass

class Related(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)

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

def main():
    Thing.objects.create()
    rs = [Related.objects.create(thing=Thing.objects.get()) for _ in range(2)]

    qs = Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc')

    try:
        assert len(qs) == 1, "QuerySet aggregation is broken"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```
This script sets up a Django test environment with an in-memory SQLite database, creates the necessary models and data, and then runs the problematic query. If the issue is present, it raises an `AssertionError` with a stack trace of the issue. If the issue is fixed, the script exits with code 0.

Please note that you need to have Django installed in your Python environment for this script to work.