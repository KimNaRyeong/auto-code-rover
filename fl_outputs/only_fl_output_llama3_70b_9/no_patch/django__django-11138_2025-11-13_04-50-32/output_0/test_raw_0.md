Here is the `reproducer.py` script to reproduce the issue:
```python
import os
import sys
from datetime import datetime
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db import connection, models
from django.utils.timezone import make_aware

class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

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

settings.configure(
    USE_TZ=True,
    TIME_ZONE='Europe/Paris',
    DATABASES={
        'legacy': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {'read_default_file': ''},
            'TIME_ZONE': 'Europe/Paris',
        },
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {'read_default_file': ''},
        }
    }
)

setup_test_environment()

# Create the table
with connection.cursor() as cursor:
    cursor.execute('CREATE TABLE my_model (my_datetime_field datetime)')

# Insert a row with the desired datetime
dt = make_aware(datetime(2017, 7, 6, 20, 50))
MyModel.objects.create(my_datetime_field=dt)

try:
    # This should return True, but returns False due to the issue
    assert MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a Django project with the specified settings, creates a table and inserts a row with a datetime value. It then tries to filter on the date part of the datetime field using the `__date` lookup, which should return True but returns False due to the issue. If the assertion fails, it prints the stack trace and exits with code 1. If the assertion passes, it exits with code 0.