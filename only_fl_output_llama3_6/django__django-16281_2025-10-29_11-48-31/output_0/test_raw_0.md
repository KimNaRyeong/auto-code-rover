Here is the reproducer script:

```python
import os
import django
from django.db import IntegrityError, OperationalError
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from django.db.models import ManyToManyField
from django.db.models.base import ModelBase

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

    class Bar(models.Model):
        pass

    class Foo(models.Model):
        bar = models.ManyToManyField('Bar', blank=True)

    execute_from_command_line(['manage.py', 'makemigrations', 'app'])
    execute_from_command_line(['manage.py', 'migrate'])

    class Bar(models.Model):
        pass

    class Foo(models.Model):
        bar = models.ManyToManyField('Foo', blank=True)

    execute_from_command_line(['manage.py', 'migrate'])

    try:
        User.objects.create()
    except (IntegrityError, OperationalError) as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up a Django project and models, runs the necessary migrations, changes the ManyToManyField type to 'Foo', runs the migrations again, and then attempts to create a user. If an OperationalError or IntegrityError is raised during this process, it prints the stack trace and raises an AssertionError with a message indicating that the issue was reproduced.