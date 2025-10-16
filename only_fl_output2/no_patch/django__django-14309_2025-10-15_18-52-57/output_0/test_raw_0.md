Certainly! Based on the problem description, below is a standalone Python script named `reproducer.py`. This script is designed to reproduce the issue specified, adhering to the condition that an `AssertionError` should be raised if the issue exists, and a clear stack trace of the issue should be displayed. It assumes the presence of a Django project setup, so you need to have Django installed and a model named `Book` available in your project's models.

```python
import os
import django
from django.db.models import Exists, Q
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from your_app.models import Book  # Make sure to replace 'your_app' with the actual app name containing your 'Book' model

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

class TestEmptyQExistsCombination(TestCase):
    def test_combine_negated(self):
        try:
            q = Q() & ~Exists(Book.objects.all())
            assert q.negated, "The combination of an empty Q object with a negated exists lookup did not maintain its negation."
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEmptyQExistsCombination)
    unittest.TextTestRunner().run(suite)
```

Note:
1. Please replace `'your_project.settings'` with the actual path to your Django project settings.
2. Replace `'your_app.models'` with the actual path to your app containing the `Book` model.

This script executes a unit test that attempts to combine an empty `Q` object with a negated `Exists` lookup. If the object's negated status is not `True` as expected, an `AssertionError` will be raised, triggering the `print_stacktrace(e)` function to output a clear traceback. When executed in a properly set up Django environment (with a `Book` model available), this script will raise an exception if the issue described is present, providing detailed information about the failure point.