Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from datetime import datetime
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db.backends.mysql.base import DatabaseWrapper
from django.db.models import DateTimeField, Model
from django.db import connection

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

class MyModel(Model):
    my_datetime_field = DateTimeField()

MyModel.objects.create(my_datetime_field=datetime(2017, 7, 6, 20, 50))

dt = datetime(2017, 7, 6, 20, 50)
dt_aware = dt.replace(tzinfo=settings.TIME_ZONE)

try:
    assert MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a Django project with the specified settings, creates a model and an instance of that model, and then tries to filter on the date part of the datetime field. If the assertion fails (i.e., the issue is present), it prints the stack trace and exits with code 1. If the assertion passes (i.e., the issue is fixed), it exits with code 0.