Here is a standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
import django
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import DateTimeField
from django.db import models

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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.db import connection

TIME_ZONE = 'Europe/Paris'
USE_TZ = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'read_default_file': '....cnf'},
        'TIME_ZONE': TIME_ZONE,
    }
}

class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

def test_issue():
    dt = make_aware(datetime(2017, 7, 6, 20, 50))
    query = MyModel.objects.filter(my_datetime_field__date=dt.date())
    with connection.cursor() as cursor:
        cursor.execute(query.query)
        result = cursor.fetchone()
        if not result:
            raise AssertionError("Expected row found")

try:
    test_issue()
except AssertionError as e:
    print_stacktrace(e)
```

This script sets up a Django environment, defines a `MyModel` with a `DateTimeField`, and then runs a query that should return a row. If the query does not return a row, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the exception.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.