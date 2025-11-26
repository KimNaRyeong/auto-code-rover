Here is the `reproducer.py` file to reproduce the issue:
```
import os
from django.db import models
from django.test.utils import CaptureQueriesContext

class ParentModel(models.Model):
    id = models.BigIntegerField(primary_key=True)

class ChildModel(ParentModel):
    pass

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import django
    django.setup()

    with CaptureQueriesContext(connection='default') as ctx:
        ChildModel(id=1).save(force_insert=True)
        queries = [q['sql'] for q in ctx.captured_queries]

    if len(queries) != 2 or not (queries[0].startswith('INSERT INTO "app_parentmodel"') and queries[1].startswith('INSERT INTO "app_childmodel"')):
        raise AssertionError("force_insert flag is not respected on the parent model")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

exit(0)
```
This script defines the `ParentModel` and `ChildModel` using Django's ORM, sets up a test database connection, and then saves an instance of `ChildModel` with `force_insert=True`. It captures the SQL queries executed during this process using `CaptureQueriesContext`.

The script then checks if the captured queries match the expected behavior: two INSERT statements, one for each model. If not, it raises an `AssertionError` with a detailed stack trace.

If the issue is fixed, the script will exit with code 0.