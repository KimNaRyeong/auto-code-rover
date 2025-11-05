Here is the reproducer script:

```python
import os
from django.db import models, connection
from django.test.utils import override_settings
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

class DecimalFieldTestCase(TestCase):
    @override_settings(DEBUG=True)
    def test_decimal_field(self):
        models.DecimalField(max_digits=1, decimal_places=0)  # Create a DecimalField

        foo = Foo.objects.create(a='', d=1)
        try:
            Foo.objects.filter(d__gt=0).get()
        except Exception as e:
            print_stacktrace(e)

        queries = connection.queries
        if len(queries) > 0 and 'SELECT' in queries[-1]['sql']:
            print(connection.queries[-1]['sql'])
        else:
            raise AssertionError("Expected a SELECT query")

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'model_fields.settings'
    from django.test.utils import setup_test_environment
    setup_test_environment()
    from django.test.runner import DiscoverRunner

    test_runner = DiscoverRunner(findfile=lambda x: True)
    failures, errors = test_runner.run_tests([__name__])
    if failures or errors:
        print_stacktrace(Exception(f"Failed tests: {failures}"))
        exit(1)
    else:
        print("All tests passed")
        exit(0)

if __name__ == 'model_fields.test_decimalfield':
    DecimalFieldTestCase()
```

This script creates a `DecimalField` and then runs the test cases. If any of the queries are not SELECT queries, it raises an `AssertionError`.