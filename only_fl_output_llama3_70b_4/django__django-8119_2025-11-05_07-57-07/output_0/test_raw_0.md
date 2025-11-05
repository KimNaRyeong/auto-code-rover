Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
from django.db.models import F, Q
from django.test import TestCase

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

class ReproducerTestCase(TestCase):
    def test_filter_expression(self):
        try:
            # This should raise an error if the issue is present
            MyModel.objects.filter(F('some_field').lower() == 'anssi')
            # If no error is raised, it means the issue is fixed
            print("Issue is fixed!")
            exit(0)
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue is still present")

class MyModel(models.Model):
    some_field = models.CharField(max_length=255)

if __name__ == "__main__":
    import django
    django.setup()
    from django.db import models

    ReproducerTestCase('test_filter_expression').debug()
```
This script defines a `ReproducerTestCase` that attempts to use an expression in a `.filter()` call. If the issue is present, this should raise an error, which will be caught and printed with a stack trace using the provided `print_stacktrace` function. If no error is raised, it means the issue is fixed, and the script will exit with code 0.

To run the script, save it to a file named `reproducer.py` in the root directory of your project, then execute it with `python3 reproducer.py`.