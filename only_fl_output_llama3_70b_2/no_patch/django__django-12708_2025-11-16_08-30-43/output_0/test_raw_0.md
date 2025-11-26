Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys

from django.db import models
from django.core.management import call_command

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

from reproducer import settings

try:
    # Create the models
    class MyModel(models.Model):
        field1 = models.IntegerField()
        field2 = models.IntegerField()

        class Meta:
            unique_together = (('field1', 'field2'),)
            index_together = (('field1', 'field2'),)

    # Make migrations
    call_command('makemigrations', verbosity=0, interactive=False)
    call_command('migrate', verbosity=0, interactive=False)

    # Try to delete the index_together
    MyModel._meta.index_together = ()
    call_command('makemigrations', verbosity=0, interactive=False)
    call_command('migrate', verbosity=0, interactive=False)

    # If we reach this point, it means the issue is fixed
    print("Issue is fixed!")
    sys.exit(0)

except Exception as e:
    print_stacktrace(e)
    assert False, "Issue is present"
```
This script creates a Django project with a single model that has both `unique_together` and `index_together` constraints on the same fields. It then tries to delete the `index_together` constraint using migrations.

If the issue is present, the script will raise an `AssertionError` with a stack trace of the error. If the issue is fixed, the script will print "Issue is fixed!" and exit with code 0.