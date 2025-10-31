Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import connection
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

def main():
    settings.configure({
        'USE_TZ': True,
        'TIME_ZONE': 'Europe/Paris',
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {'read_default_file': '/path/to/cnf'},
                'TIME_ZONE': 'Europe/Paris'
            }
        }
    })

    from django.db import connection
    cursor = connection.cursor()

    dt = timezone.make_aware(datetime(2017, 7, 6, 20, 50))
    query = "SELECT (1) AS `a` FROM `my_model` WHERE DATE(CONVERT_TZ(`my_model`.`my_datetime_field`, 'UTC', 'Europe/Paris')) = '%s' LIMIT 1;" % dt.date().isoformat()
    cursor.execute(query)
    result = cursor.fetchone()

    if not result:
        raise AssertionError("Expected row to be found")

if __name__ == '__main__':
    try:
        main()
    except (AssertionError, ImproperlyConfigured) as e:
        print_stacktrace(e)
        exit(1)

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

This script sets up a Django project with the given settings, creates a cursor to the database, executes the query that reproduces the issue, and raises an `AssertionError` if no row is found. The stack trace of the exception is printed using the provided function.

Note that you need to replace `'my_model'` with your actual model name in the script.