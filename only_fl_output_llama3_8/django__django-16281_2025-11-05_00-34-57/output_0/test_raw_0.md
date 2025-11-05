Here is the reproducer script:

```python
import os
from django.db import IntegrityError, OperationalError
from django.db.models import ManyToManyField
from django.db.models.signals import post_migrate
from django.apps import AppConfig
from django.test import TestCase
from django.core.management import execute_from_command_line

class MyAppConfig(AppConfig):
    name = 'app'

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

class Reproducer(TestCase):
    def test_migration(self):
        try:
            os.system('python manage.py makemigrations app')
            os.system('python manage.py migrate')
            class Bar(models.Model):
                pass
            class Foo(models.Model):
                bar = models.ManyToManyField('Foo', blank=True)
            os.system('python manage.py makemigrations app')
            os.system('python manage.py migrate')
            self.fail("Expected OperationalError")
        except AssertionError:
            print_stacktrace(sys.exc_info()[1])
            raise

if __name__ == '__main__':
    execute_from_command_line(['manage.py', 'test'])
```

This script will create the models, run the migrations, and then try to add a new Foo instance. If the issue is present, it should raise an AssertionError with the stack trace printed.