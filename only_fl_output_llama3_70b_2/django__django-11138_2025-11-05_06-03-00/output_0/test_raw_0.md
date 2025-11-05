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
                'read_default_file': '....cnf',
            },
            'TIME_ZONE': 'Europe/Paris',
        },
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': '....cnf',
            },
        }
    }
)

setup_test_environment()

# Create the table
with connection.cursor() as cursor:
    cursor.execute("CREATE TABLE my_model (my_datetime_field datetime)")

# Insert a row
MyModel.objects.create(my_datetime_field=datetime(2017, 7, 6, 20, 50))

dt = make_aware(datetime(2017, 7, 6, 20, 50))
try:
    assert MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a Django project with the specified settings, creates a model and inserts a row into the database. It then tries to filter the model by date using the `__date` lookup, which should work according to the documentation. If the assertion fails, it prints the stack trace of the issue and exits with code 1. If the issue is fixed, the script exits with code 0.