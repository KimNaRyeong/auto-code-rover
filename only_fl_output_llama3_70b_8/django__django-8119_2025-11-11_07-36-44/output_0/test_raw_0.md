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

class TestFilterExpressions(TestCase):
    def test_filter_expressions(self):
        try:
            # This should raise a TypeError if expressions are not allowed in .filter() calls
            MyModel.objects.filter(F('some_field').lower() == 'anssi')
            assert False, "Expected TypeError, but no exception was raised"
        except TypeError as e:
            print_stacktrace(e)
            raise AssertionError("Expressions are not allowed in .filter() calls") from e

if __name__ == "__main__":
    import sys
    try:
        TestFilterExpressions('test_filter_expressions').run()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
```
This script defines a test case that attempts to use an expression in a `.filter()` call. If the expression is not allowed, a `TypeError` should be raised. The script catches this exception and raises an `AssertionError` with a message indicating that expressions are not allowed in `.filter()` calls.

If the issue is fixed and expressions are allowed in `.filter()` calls, the test case will pass and the script will exit with code 0.