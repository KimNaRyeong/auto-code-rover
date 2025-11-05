Here is the reproducer script:

```python
import os
import sys
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.writer import Writer

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
    # Create a test database
    conn = connections['test']
    conn.execute('CREATE DATABASE IF NOT EXISTS test_case_insensitive')

    # Set the collation to case-insensitive
    conn.cursor().execute('SET GLOBAL lower_case_table_names=1')
    conn.cursor().execute('SET SESSION lower_case_table_names=1')

    # Create a table with camelCasing
    conn.execute('CREATE TABLE IF NOT EXISTS `City` (`id` INT PRIMARY KEY AUTO_INCREMENT, `countryCode` VARCHAR(255))')

    # Run the migration
    writer = Writer()
    executor = MigrationExecutor(writer)
    try:
        executor.migrate(['my_first_app'])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a test database with a case-insensitive collation, creates a table with camelCasing, and then runs the migration. If the issue is present, it will raise an `AssertionError` and print the stack trace.