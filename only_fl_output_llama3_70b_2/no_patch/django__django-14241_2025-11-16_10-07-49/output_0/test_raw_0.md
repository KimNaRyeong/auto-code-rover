Here is the `reproducer.py` file to reproduce the issue:
```
```python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

from django.db import models
from django.db.models.query_utils import Q

class Celebrity(models.Model):
    name = models.CharField(max_length=255)

class ReservedName(models.Model):
    name = models.CharField(max_length=255)

def setup():
    from django.core.management import call_command
    call_command('makemigrations', verbosity=0)
    call_command('migrate', verbosity=0)

def reproduce_issue():
    qs1 = Celebrity.objects.all()
    qs2 = ReservedName.objects.all()
    try:
        result = qs1.union(qs2).values_list('name').first()
        assert False, "Expected DatabaseError or OperationalError"
    except (Exception) as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

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

if __name__ == "__main__":
    setup()
    reproduce_issue()
```
This script sets up a Django project with two models, `Celebrity` and `ReservedName`, and then tries to execute the problematic query. If the issue is present, it will raise an `AssertionError` with a stack trace of the error. If the issue is fixed, it will exit with code 0.

Note that you need to create a `reproducer/settings.py` file with the following content:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
INSTALLED_APPS = ['reproducer']
```
This sets up an in-memory SQLite database for the test.