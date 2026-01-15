Below is a standalone Python file named `reproducer.py` which aims to reproduce the described issue. This script sets up a minimal Django environment programmatically, defines models using multi-table inheritance and includes an `ordering` Meta option that utilises a query expression as stated in the issue. When executed, it attempts to trigger the issue and will raise an `AssertionError` if the problem persists or exist with code 0 if it's resolved:

```python
import os
import sys
from django.conf import settings
from django.db import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure Django Settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=('__main__',),
)

# Import necessary Django components after settings are configured
from django.apps import apps
apps.populate(settings.INSTALLED_APPS)

from django.core.management import call_command
from django.db.models import F

# Utility function to print stack trace
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

# Define models
class Parent(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = [F('name').asc(nulls_first=True)]

class Child(Parent):
    age = models.IntegerField()

# Django setup
from django.setup import setup
setup()

try:
    # Create tables
    call_command('migrate', verbosity=0)

    # Try to reproduce the issue
    Child.objects.create(name='John Doe', age=30)
    children = Child.objects.all()
    assert list(children), "Query should not fail."

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("No issue detected.")
    sys.exit(0)
```

Make sure before running this script, you have Django installed in your environment. You can install Django using pip:

```bash
pip install django
```

This script follows the description as closely as possible, considering the constraints of creating minimal, self-contained code. It should be executed in a directory where it is permissible to create a `db.sqlite3` file, as it does not clean up after itself for simplicity's sake.