 Here is a standalone Python script that reproduces the issue:

```python
from django.db import connection, models

class MyModel(models.Model):
    pass

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    with connection.cursor() as cursor:
        cursor.execute("CREATE TEMPORARY TABLE mymodel (id serial primary key)")
        cursor.execute("INSERT INTO mymodel DEFAULT VALUES")
        cursor.execute("INSERT INTO mymodel DEFAULT VALUES")
        cursor.execute("INSERT INTO mymodel DEFAULT VALUES")

    MyModel.objects.annotate(my_column=models.Value('asdf')).order_by('my_column').values_list('id')
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue present")
```

When executed with `python3 reproducer.py`, the script will create a temporary table in the database, insert some dummy data, and then execute the query that causes the issue. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed to the console. If the issue is fixed, the script will exit with code 0.