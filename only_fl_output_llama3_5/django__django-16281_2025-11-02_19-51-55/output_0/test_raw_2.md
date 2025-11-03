Here is the reproducer script:

```python
import os
import django
from django.db import IntegrityError
from django.core.management import execute_from_command_line
from django.conf import settings
from django.db.models import Model
from django.db import models

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
    settings.configure()
    django.setup()

    os.system('python manage.py makemigrations app')
    os.system('python manage.py migrate')

    class Bar(models.Model):
        pass

    class Foo(models.Model):
        bar = models.ManyToManyField(Bar, blank=True)

    os.system('python manage.py makemigrations app')
    os.system('python manage.py migrate')

    try:
        Foo.objects.create()
    except IntegrityError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

    if 'app' not in settings.INSTALLED_APPS:
        raise AssertionError("Issue fixed")

if __name__ == "__main__":
    reproduce_issue()
```

This script should be placed in the root directory of your Django project.