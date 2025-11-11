Here is the `reproducer.py` file to reproduce the issue:
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

def main():
    settings.configure(
        USE_TZ=True,
        TIME_ZONE='Europe/Paris',
        DATABASES={
            'legacy': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {
                    'read_default_file': os.devnull,  # Replace with your MySQL config file
                },
                'TIME_ZONE': 'Europe/Paris',
            },
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {
                    'read_default_file': os.devnull,  # Replace with your MySQL config file
                },
            }
        }
    )

    setup_test_environment()

    MyModel.objects.create(my_datetime_field=datetime(2017, 7, 6, 20, 50))

    dt = make_aware(datetime(2017, 7, 6, 20, 50))
    assert MyModel.objects.filter(my_datetime_field=dt).exists(), "Filter by datetime works"

    try:
        assert MyModel.objects.filter(my_datetime_field__date=dt.date()).exists(), "Filter by date fails"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script sets up a Django project with two databases, creates a model with a datetime field, and inserts a record. It then tests filtering by datetime and date, expecting the latter to fail due to the issue described.

To run this script, save it as `reproducer.py` in the root directory of your project, replace `os.devnull` with the path to your MySQL config file, and execute it with `python3 reproducer.py`. If the issue is present, the script will raise an `AssertionError`, print a stack trace, and exit with code 1. If the issue is fixed, the script will exit with code 0.