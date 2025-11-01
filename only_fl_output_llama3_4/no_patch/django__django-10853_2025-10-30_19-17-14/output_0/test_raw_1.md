Here is the reproducer script:

```python
import sqlite3
from django.db import models, connection
from django.db.models.functions.window import RowNumber
from django.db.utils import OperationalError

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
        conn = sqlite3.connect(":memory:")
        c = conn.cursor()
        c.execute("CREATE TABLE t0(x INTEGER PRIMARY KEY, y TEXT)")
        c.execute("INSERT INTO t0 VALUES (1, 'aaa'), (2, 'ccc'), (3, 'bbb')")
        c.execute("SELECT x, y, row_number() OVER (ORDER BY y) AS row_number FROM t0 ORDER BY x")
    except OperationalError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script connects to a temporary SQLite database, creates a table and inserts some data. Then it attempts to execute a SQL query that uses window functions. If the query fails due to SQLite not supporting window functions (which is the case for versions prior to 3.25.0), it prints the stack trace and raises an `AssertionError`.