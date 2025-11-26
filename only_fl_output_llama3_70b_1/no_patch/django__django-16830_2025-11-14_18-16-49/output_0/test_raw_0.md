Here is the `reproducer.py` file that reproduces the issue:
```
import os
from django.db import models
from django.test.utils import CaptureQueriesContext

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import django
django.setup()

class ParentModel(models.Model):
    id = models.BigIntegerField(primary_key=True)

class ChildModel(ParentModel):
    pass

def main():
    with CaptureQueriesContext(connection='default') as ctx:
        child = ChildModel(id=1)
        child.save(force_insert=True)
        queries = [q['sql'] for q in ctx.captured_queries]
        assert len(queries) == 2, "Expected 2 queries, got {}".format(len(queries))
        assert 'UPDATE' not in queries[0], "UPDATE query should not be present"
    print("Issue is fixed!")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

```
This script defines the `ParentModel` and `ChildModel` using Django's ORM, and then creates a `ChildModel` instance with `id=1`. It uses the `CaptureQueriesContext` to capture the SQL queries executed during the `save` operation.

The script asserts that there should be exactly 2 queries executed (the INSERT into the child table and the INSERT into the parent table), and that the first query should not be an UPDATE. If these assertions fail, it raises an `AssertionError`, prints the stack trace using the provided function, and exits with code 1.

If the issue is fixed, the script will print "Issue is fixed!" and exit with code 0.