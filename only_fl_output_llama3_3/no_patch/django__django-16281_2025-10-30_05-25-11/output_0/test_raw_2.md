Here is the reproducer script:

```python
import os
from django.db import IntegrityError
from django.core.management import execute_from_command_line
from django.db.utils import OperationalError
from django.db.models import ManyToManyField
from django.contrib.auth.models import User
from django.db import models
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_migrations():
    os.system('python manage.py makemigrations app')
    os.system('python manage.py migrate')

def reproduce_issue():
    try:
        run_migrations()
        from app.models import Foo, Bar
        class Bar(models.Model):
            pass
        class Foo(models.Model):
            bar = models.ManyToManyField('Bar', blank=True)
        run_migrations()
        user = User.objects.create_user('testuser', 'testemail@example.com', 'testpassword')
        foo = Foo(bar=[Bar()])
        foo.save()
    except OperationalError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script runs the migrations, creates the models, and then tries to save a `Foo` object with a many-to-many relationship. If an `OperationalError` is raised during this process, it prints the stack trace and raises an `AssertionError`.