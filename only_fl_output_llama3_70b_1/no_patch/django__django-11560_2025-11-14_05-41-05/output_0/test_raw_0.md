Here is the `reproducer.py` file that reproduces the issue:
```
import os
from django.db import models
from django.db.models.functions import ExtractYear
from django.test import TestCase

class MyModel(models.Model):
    duration = models.DurationField()

def setup_test_db():
    from django.core.management import call_command
    call_command('migrate', verbosity=0)

def test_extract_year_lookup():
    MyModel(duration='1 00:00:00').save()
    try:
        MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")
    else:
        print("Issue is fixed")

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import reproducer.settings
    setup_test_db()
    test_extract_year_lookup()

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
```
This script sets up a test database, defines the `MyModel` with a `DurationField`, and then tries to execute the problematic query. If the query raises a `ValueError`, it prints the stack trace using the provided function and raises an `AssertionError`. If the query succeeds, it prints "Issue is fixed" and exits with code 0.

Note that you'll need to create a `reproducer` directory with a `settings.py` file containing the necessary Django settings for this script to work.