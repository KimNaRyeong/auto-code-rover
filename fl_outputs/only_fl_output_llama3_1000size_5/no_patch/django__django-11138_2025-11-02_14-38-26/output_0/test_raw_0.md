Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import django
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Q

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

django.setup()

from myapp.models import MyModel  # Replace with your actual model

def reproduce_issue():
    settings_module = __import__('settings')
    settings = settings_module.settings

    use_tz = settings.USE_TZ
    time_zone = settings.TIME_ZONE
    databases = settings.DATABASES

    if not use_tz:
        raise AssertionError("USE_TZ must be True to reproduce the issue")

    # Create a test model instance with a datetime field
    my_model_instance = MyModel(my_datetime_field=make_aware(datetime(2017, 7, 6, 20, 50)))
    my_model_instance.save()

    # Perform date lookup query
    result = MyModel.objects.filter(Q(my_datetime_field__date=my_model_instance.my_datetime_field.date()))
    if not result.exists():
        raise AssertionError("Date lookup query should return at least one result")

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
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

This script sets up a Django project, creates a test model instance with a datetime field, and then performs a date lookup query. If the query does not return at least one result, it raises an `AssertionError` and prints the stack trace using the provided function.

Note that you'll need to replace `myapp.models.MyModel` with your actual model name and import statement.