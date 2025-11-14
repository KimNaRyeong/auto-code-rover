Here is the reproducer script:

```python
import os
from django.db import IntegrityError
from django.test import TestCase, override_settings
from .models import JsonFieldHasKeyTest

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

@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}})
class Reproducer(TestCase):
    def test_json_field_has_key(self):
        try:
            test = JsonFieldHasKeyTest(data={'foo': 'bar'})
            test.save()
            test2 = JsonFieldHasKeyTest(data={str(1111): 'bar'})
            test2.save()

            c1 = JsonFieldHasKeyTest.objects.filter(data__has_key='foo').count()
            c2 = JsonFieldHasKeyTest.objects.filter(data__has_key=str(1111)).count()  # Use str(1111) for SQLite

            self.assertEqual(c1, 1, "Should have found 1 entry with key 'foo'")
            self.assertEqual(c2, 0, "Should not have found any entries with key '1111'")

        except AssertionError as e:
            print_stacktrace(e)
            raise
        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    try:
        Reproducer().test_json_field_has_key()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(0)
```

This script creates a SQLite database and saves two test entries with JSON fields. It then runs the same query as in the original issue, but for both numeric and string keys. If the query finds an entry with the numeric key, it prints the stack trace and raises an `AssertionError`.