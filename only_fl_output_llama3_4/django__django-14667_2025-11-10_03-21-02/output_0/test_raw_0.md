Here is the reproducer script:

```python
import django
from django.db.models import Q
from django.test.utils import CaptureQueriesMade

def main():
    try:
        with CaptureQueriesMade() as queries:
            Company.objects.only("name").defer("name")
            if len(queries) != 1 or any(query.query for query in queries):
                raise AssertionError("Expected only 'id' column to be selected, but got unexpected columns.")
        
        with CaptureQueriesMade() as queries:
            Company.objects.only("name", "country").defer("name")
            if len(queries) != 1 or any(query.query for query in queries) or not all(column in ["company.id", "company.name", "company.country"] for query in queries):
                raise AssertionError("Expected only 'id' and 'country' columns to be selected, but got unexpected columns.")
        
        print("Test passed. No unexpected columns were selected.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    django.setup()
    main()

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

```

This script uses Django's `CaptureQueriesMade` to capture the queries executed during the test. It then checks if the expected columns are selected and raises an `AssertionError` if not. The `print_stacktrace` function is used to print the stack trace of the error.