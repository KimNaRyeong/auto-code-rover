Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import django
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Q

# Set up Django project
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from myapp.models import MyModel  # Replace with your actual model name

def reproduce_issue():
    settings_module = __import__('settings')
    settings = settings_module.settings

    # Create a test database
    from django.db import connections
    conn = connections['legacy']
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE my_model (my_datetime_field datetime)")
    cursor.close()

    # Insert some data into the table
    dt = make_aware(datetime(2017, 7, 6, 20, 50))
    MyModel.objects.create(my_datetime_field=dt)

    # Try to filter by date
    try:
        result = MyModel.objects.filter(Q(my_datetime_field__date=dt.date()))
        if not result.exists():
            raise AssertionError("Filtering by date did not return any results")
    except Exception as e:
        print_stacktrace(e)
        raise

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

if __name__ == '__main__':
    reproduce_issue()
```

This script sets up a Django project, creates a test database, inserts some data into the table, and then tries to filter by date. If the filtering does not return any results, it raises an `AssertionError` with a stack trace.

Note that you'll need to replace `myapp.models.MyModel` with your actual model name.