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
            assert False, "Expected an exception"
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue is still present")

if __name__ == "__main__":
    from django.test.runner import DiscoverRunner
    runner = DiscoverRunner()
    runner.run_tests([ReproducerTestCase])
```
This script assumes that you have a Django project set up with a model `MyModel` and a field `some_field`. If the issue is present, it will raise an `AssertionError` with a stack trace. If the issue is fixed, it will exit with code 0.

Please note that this script uses the Django test framework to run the test case. You may need to modify the script to fit your specific project setup.