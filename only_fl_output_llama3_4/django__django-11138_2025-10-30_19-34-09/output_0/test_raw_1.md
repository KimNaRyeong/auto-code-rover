Here is the reproducer script:

```python
import os
from django.db import connection
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

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
    settings_module = __import__('settings')
    settings = settings_module.settings

    # Set up the database
    connection.settings_dict['TIME_ZONE'] = 'Europe/Paris'
    connection.settings_dict['USE_TZ'] = True

    # Create a test model instance
    dt = make_aware(datetime(2017, 7, 6, 20, 50))
    MyModel.objects.create(my_datetime_field=dt)

    try:
        # Perform the date lookup
        result = MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()
        if not result:
            raise AssertionError("Date lookup failed")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up a Django project, creates a test model instance with a datetime field, and then performs the date lookup. If the date lookup fails (i.e., no result is found), it raises an `AssertionError`. The script also prints the stack trace of the exception if one occurs.