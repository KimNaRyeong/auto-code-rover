Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
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
            'OPTIONS': {
                'read_default_file': '',
            },
            'TIME_ZONE': 'Europe/Paris',
        },
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': '',
            },
        }
    }
)

setup_test_environment()

# Create the database tables
connection.creation.create_all()

# Create a test record
MyModel(my_datetime_field=datetime(2017, 7, 6, 20, 50)).save()

dt = make_aware(datetime(2017, 7, 6, 20, 50))
try:
    assert MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a Django project with the specified settings, creates a test model and record, and then tries to filter on the date part of the datetime field using the `__date` lookup. If the issue is present, it will raise an `AssertionError`, print the stack trace, and exit with code 1. If the issue is fixed, it will exit with code 0.