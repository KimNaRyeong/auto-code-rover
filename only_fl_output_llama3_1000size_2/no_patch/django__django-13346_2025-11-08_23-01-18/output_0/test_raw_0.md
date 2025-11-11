Here is the reproducer script:

```python
import django
from django.db import models
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

class Reproducer(TestCase):
    def test_reproducer(self):
        class OurModel(models.Model):
            our_field = models.JSONField()

        for db in ['mysql', 'oracle', 'sqlite']:
            django.setup()
            try:
                first_filter = {'our_field__key__in': [0]}
                first_items = OurModel.objects.using(db).filter(**first_filter)
                self.assertEqual(len(first_items), 312)

                second_filter = {'our_field__key': 0}
                second_items = OurModel.objects.using(db).filter(**second_filter)
                self.assertEqual(len(second_items), 312)
            except AssertionError as e:
                print_stacktrace(e)
                raise
            finally:
                django.setup()

if __name__ == '__main__':
    try:
        Reproducer().test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)
```

This script sets up a Django test case, defines a model `OurModel` with a JSON field, and then runs two queries using the `__in` lookup on key transforms in different databases (MySQL, Oracle, SQLite). If the issue is present, it will raise an `AssertionError`, print the stack trace, and exit with code 1. If the issue is not present, it will print a success message and exit with code 0.