```python
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models

# Minimal Django setup for script to run standalone
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()


class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]


class Child(Parent):
    pass


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


def check_ordering():
    execute_from_command_line(['manage.py', 'makemigrations', '__main__', '--noinput'])
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])

    # Create test data
    Child.objects.create()
    Child.objects.create()
    Child.objects.create()

    # Fetch the query and check ordering
    query = str(Child.objects.all().query)
    expected_order = 'ORDER BY "myapp_parent"."id" DESC'
    if expected_order not in query:
        raise AssertionError(
            f"Query does not contain the expected ordering. Expected something like `{expected_order}`. Got: {query}"
        )


try:
    check_ordering()
except AssertionError as e:
    print_stacktrace(e)
    os._exit(1)  # Use os._exit here since sys.exit might be caught
else:
    print("No issues detected. Ordering works as expected.")
    os._exit(0)
```