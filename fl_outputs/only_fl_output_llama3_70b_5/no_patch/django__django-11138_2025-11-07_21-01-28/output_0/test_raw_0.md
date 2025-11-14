Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
import sys
from datetime import datetime
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db.backends.mysql.base import DatabaseWrapper
from django.db.models import DateTimeField, Model

# Set up Django environment
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

# Create a test model
class MyModel(Model):
    my_datetime_field = DateTimeField()

# Create the database tables
DatabaseWrapper(settings.DATABASES['legacy']).create_table(MyModel._meta.db_table, [])

# Insert a test row
from django.db import connection
cursor = connection.cursor()
cursor.execute("INSERT INTO my_model (my_datetime_field) VALUES ('2017-07-06 20:50:00')")
connection.commit()

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    dt = datetime(2017, 7, 6, 20, 50)
    assert MyModel.objects.filter(my_datetime_field=dt).exists()
    dt_date = dt.date()
    assert MyModel.objects.filter(my_datetime_field__date=dt_date).exists()  # This should raise an AssertionError
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a Django environment with the specified settings, creates a test model and inserts a row into the database. It then tries to filter the model instances using a datetime object and its date component. If the issue is present, it should raise an `AssertionError` when filtering by the date component, which will be caught and printed with a stack trace.