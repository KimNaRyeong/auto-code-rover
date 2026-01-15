Based on the provided requirements and to address the error in the previous attempt, I am providing a revised standalone Python script, `reproducer.py`. This script is specifically designed to demonstrate the issue with Django models as described, and it correctly configures Django settings inline, allowing it to run without dependencies on external Django project settings.

```python
# reproducer.py
import sys
from django.conf import settings
from django.core.management import call_command
from django.db import models
from django.apps import apps


def setup_django_environment():
    settings.configure(
        INSTALLED_APPS=[
            '__main__',  # Include this script as an app
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        USE_TZ=True,
    )
    apps.populate(settings.INSTALLED_APPS)
    call_command('migrate', verbosity=0)


class Parent(models.Model):
    name = models.CharField(max_length=256)


class ProxyParent(Parent):
    class Meta:
        proxy = True


class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    many_to_many_field = models.ManyToManyField(
        to=Parent,
        through="ManyToManyModel",
        through_fields=['child', 'parent'],
        related_name="something"
    )


class ManyToManyModel(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='+')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='+')
    second_child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, default=None)


def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def check_issue():
    try:
        # Trigger Django's system check framework explicitly, mimicking `manage.py check`
        call_command('check')
    except Exception as e:
        # If an exception occurs, print the stack trace and ensure it matches the expected issue
        print_stacktrace(e)
        assert str(e) == "unhashable type: 'list'", "The issue was expected to be an unhashable type error."
        sys.exit(1)  # Exit with error to indicate the issue exists
    print("No issue detected. The problem seems to be fixed.")
    sys.exit(0)  # Exit with success as the issue is fixed or not present


if __name__ == '__main__':
    setup_django_environment()
    check_issue()
```

This script integrates the `print_stacktrace` function as requested and sets up an in-memory Django environment, allowing it to be run standalone. It defines the necessary models to reproduce the issue described and attempts to execute Django's system checks. If the issue is present—an `TypeError` is raised due to the unhashable type—it prints a detailed stack trace. The script exits with code `0` if the issue is not detected, indicating a potential fix, otherwise it exits with code `1`.