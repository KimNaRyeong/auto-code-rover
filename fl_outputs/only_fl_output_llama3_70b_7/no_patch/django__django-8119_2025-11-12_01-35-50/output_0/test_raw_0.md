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
            MyModel.objects.filter(F('some_field').lower() == 'anssi')
            self.fail("Expected TypeError")
        except TypeError as e:
            print_stacktrace(e)
            raise AssertionError("Expressions in filter calls are not supported")

if __name__ == "__main__":
    from django.test.runner import DiscoverRunner
    runner = DiscoverRunner()
    runner.run_tests([ReproducerTestCase])
```
This script defines a Django test case that attempts to use an expression in a `.filter()` call. If the issue is present, it will raise a `TypeError`, which we catch and re-raise as an `AssertionError` with a stack trace. If the issue is fixed, the test will pass and exit with code 0.

Note: You'll need to replace `MyModel` with an actual Django model class that has a field named `some_field`.