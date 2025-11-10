Here is the reproducer script:

```python
import os
from django.db import models
from django.apps import apps
from django.test.utils import setup_test_environment, teardown_test_environment

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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'myapp.settings'
    setup_test_environment()

    from django.db.models import Q
    from django.test import TestCase

    class TestIssue(TestCase):
        def test_issue(self):
            from myapp.models import Parent, Child

            parent = Parent()
            parent.save()

            child = Child(parent_ptr_id=parent.pk)
            child.save()

            query = Child.objects.all().order_by('-pk')
            self.assertEqual(list(query), [child])

    try:
        TestIssue('test_issue').test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    teardown_test_environment()

if __name__ == "__main__":
    main()
```

This script sets up a test environment, defines the models and runs the test. If the issue is present (i.e., the query is not ordered by "-pk" in descending order), it prints the stack trace and exits with code 1.