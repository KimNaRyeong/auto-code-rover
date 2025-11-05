Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
import sys
from datetime import datetime
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db import connection, models
from django.utils.timezone import make_aware, get_default_timezone

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

def setup_django():
    settings.configure(
        USE_TZ=True,
        TIME_ZONE='Europe/Paris',
        DATABASES={
            'legacy': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {
                    'read_default_file': os.devnull,
                },
                'TIME_ZONE': 'Europe/Paris',
            },
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {
                    'read_default_file': os.devnull,
                },
            }
        }
    )
    setup_test_environment()

def main():
    setup_django()
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
This script sets up a Django project with the specified settings, creates a model instance with a datetime field, and then tries to filter by both the datetime and date. If the filtering by date fails (which is the issue being reproduced), it prints a stack trace of the error and exits with code 1.