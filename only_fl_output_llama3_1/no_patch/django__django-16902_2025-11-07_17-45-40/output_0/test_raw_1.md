Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import Right, Length

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

def reproduce_issue():
    try:
        from django.db import connection
        cursor = connection.cursor()
        query = "SELECT RIGHT('hello', 0) AS result"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        if result != '':
            raise AssertionError("RIGHT function on Oracle and SQLite returns improper value when the length is zero.")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    print("Issue not present. Exiting with code 0.")
    exit(0)
```

This script tries to execute a query that uses the RIGHT function on Oracle and SQLite databases. If the result is not an empty string, it raises an AssertionError and prints the stack trace.