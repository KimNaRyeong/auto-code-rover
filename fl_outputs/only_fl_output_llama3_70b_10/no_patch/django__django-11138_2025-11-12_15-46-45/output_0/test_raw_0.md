Here is the `reproducer.py` file to reproduce the issue:
```
import os
import sys
from datetime import datetime
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db import connection, models
from django.utils.timezone import make_aware, timezone

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
                'read_default_file': '',  # Replace with your MySQL config file
            },
            'TIME_ZONE': 'Europe/Paris',
        },
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': '',  # Replace with your MySQL config file
            },
        }
    }
)

setup_test_environment()

class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

MyModel.objects.create(my_datetime_field=datetime(2017, 7, 6, 20, 50))

dt = make_aware(datetime(2017, 7, 6, 20, 50))
try:
    assert MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a Django project with the specified settings and creates a model with a datetime field. It then creates an instance of the model with a specific datetime value.

The script then tries to filter the model instances using a date lookup, which should return `True` if the issue is fixed. If the assertion fails, it prints the stack trace of the error and exits with code 1. If the assertion passes, it exits with code 0.

Note that you'll need to replace the `read_default_file` options with your actual MySQL config file path.