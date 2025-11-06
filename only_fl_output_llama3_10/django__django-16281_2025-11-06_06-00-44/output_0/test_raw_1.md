Here is the `reproducer.py` script that reproduces the issue:

```python
import os
from django.db import IntegrityError
from django.core.exceptions import OperationalError
from django.core.management.commands.makemigrations import CommandError
from django.core.management.commands.migrate import CommandError
from django.test.utils import CaptureHandler

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
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()

    from app.models import Bar, Foo

    try:
        # Create models
        class Bar(models.Model):
            pass
        class Foo(models.Model):
            bar = models.ManyToManyField(Bar, blank=True)

        # Migrate
        os.system('./manage.py makemigrations app')
        os.system('./manage.py migrate')

        # Change type of the ManyToManyField to Foo
        class Bar(models.Model):
            pass
        class Foo(models.Model):
            bar = models.ManyToManyField('Foo', blank=True)

        # Migrate (see above)
        os.system('./manage.py makemigrations app')
        os.system('./manage.py migrate')

        # Add a new Foo instance
        foo = Foo()
        try:
            foo.save()
        except OperationalError as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced")
    except (CommandError, IntegrityError) as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up a Django project and models, runs the necessary migrations, changes the type of the ManyToManyField to Foo, runs the migrations again, and attempts to add a new Foo instance. If an OperationalError is raised during this process, it prints the stack trace and raises an AssertionError with the message "Issue reproduced".