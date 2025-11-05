Here is the reproducer script:

```python
import os
from django.db import IntegrityError, OperationalError
from django.core.management import execute_from_command_line
from django.conf import settings
from django.apps import apps
from django.db.models import Model
from django.db.models.fields.related import ManyToManyField
from django.db.models.signals import post_migrate

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

def reproduce_issue():
    class Bar(Model):
        pass

    class Foo(Model):
        bar = ManyToManyField('self', blank=True)

    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])

        class Bar(Model):
            pass

        class Foo(Model):
            bar = ManyToManyField('Foo', blank=True)

        execute_from_command_line(['manage.py', 'migrate'])

        try:
            foo = Foo()
            foo.bar.add(foo)
            foo.save()
        except (IntegrityError, OperationalError) as e:
            print_stacktrace(e)
            raise AssertionError("Issue not fixed")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script creates the models, runs the migrations, and then tries to save a Foo instance with a ManyToManyField pointing to itself. If an OperationalError or IntegrityError is raised during this process, it prints the stack trace and raises an AssertionError.