Here is the reproducer script:

```python
import django
from django.db import models
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

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

class IssueReproducer(TestCase):
    def test_issue(self):
        class OurModel(models.Model):
            our_field = models.JSONField()

        # Set the DJANGO_SETTINGS_MODULE environment variable
        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

        try:
            first_filter = {'our_field__key__in': [0]}
            first_items = OurModel.objects.filter(**first_filter)
            if len(first_items) != 0:
                raise AssertionError("Expected no items, but got {}".format(len(first_items)))

            second_filter = {'our_field__key': 0}
            second_items = OurModel.objects.filter(**second_filter)
            if len(second_items) != 312:
                raise AssertionError("Expected 312 items, but got {}".format(len(second_items)))
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)
        else:
            print("Issue not present. Exiting with code 0.")
            exit(0)

if __name__ == '__main__':
    try:
        issue_reproducer = IssueReproducer()
        issue_reproducer.test_issue()
    except ImproperlyConfigured as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)
```

This script sets the DJANGO_SETTINGS_MODULE environment variable before running the test, which should allow it to properly configure Django and run the test.