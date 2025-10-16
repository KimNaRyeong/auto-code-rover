```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models, connection
from django.core.management import execute_from_command_line

# Dynamically configure the Django settings with the minimum necessary configuration
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()


class Foo(models.Model):
    a = models.CharField(max_length=10)
    d = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = '__main__'


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


def run_tests():
    # Create table for Foo model
    execute_from_command_line(['manage.py', 'migrate'])

    # Test cases
    Foo.objects.create(a='', d=1)
    assert Foo.objects.filter(d__gt=0).exists(), "AssertionError: Case 00 failed"
    print("Test case 00 passed")

    Foo.objects.create(a='', d=0)
    assert Foo.objects.annotate(
        x=models.Value(1, output_field=models.DecimalField(max_digits=1, decimal_places=0))
    ).filter(x__gt=0).exists(), "AssertionError: Case 01 failed"
    print("Test case 01 passed")

    try:
        Foo.objects.create(a='', d=0)
        assert Foo.objects.annotate(
            x=models.ExpressionWrapper(
                models.Value(1),
                output_field=models.DecimalField(max_digits=1, decimal_places=0),
            )
        ).filter(x__gt=0).exists(), "AssertionError: Case 02 failed"
    except AssertionError as e:
        print("Test case 02 failed with AssertionError")
        print_stacktrace(e)
        raise

    try:
        Foo.objects.create(a='', d=1)
        assert Foo.objects.annotate(
            x=models.Case(models.When(a='', then=models.F('d')))
        ).filter(x__gt=0).exists(), "AssertionError: Case 03 failed"
    except AssertionError as e:
        print("Test case 03 failed with AssertionError")
        print_stacktrace(e)
        raise

    print("All test cases passed")


if __name__ == '__main__':
    try:
        run_tests()
    finally:
        # Clean up the SQLite database file
        os.remove(os.path.join(os.getcwd(), 'db.sqlite3'))
```

This standalone Python script, `reproducer.py`, aims to replicate the issue as described by dynamically setting up a Django environment, defining a model `Foo`, and running test cases that reproduce the having issues with `DecimalField` on SQLite when used with `Case()` and `ExpressionWrapper()`. It is designed to be self-contained so that running `python3 reproducer.py` in the root project directory attempts to reproduce the issue, capturing an `AssertionError` where the problem lies and printing the stack trace of the issue for cases where errors are expected to occur due to the described problem.