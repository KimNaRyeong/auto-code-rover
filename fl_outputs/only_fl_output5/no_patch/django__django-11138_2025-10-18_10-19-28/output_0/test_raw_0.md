Here is a `reproducer.py` file that you can use to reproduce the stated issue. Ensure that your Django project settings are configured appropriately for this script to run, particularly the `DATABASES` setting as illustrated in the issue description.

```python
# reproducer.py
import os
import datetime
from django.conf import settings
from django.utils import timezone
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
import django
django.setup()

from your_app.models import MyModel  # Update this import according to your actual model

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
    settings.configure()
    execute_from_command_line(["manage.py", "migrate"])  # Ensure DB is up to date

    # Set up test environment
    test_date = datetime.datetime(2017, 7, 6, 20, 50)
    tz = timezone.get_default_timezone()  # You might need to adjust this
    dt = timezone.make_aware(test_date, tz)

    # Ensure the data is there for our test
    MyModel.objects.create(my_datetime_field=dt)

    try:
        # The following filter should return True, indicating the object exists
        exists_without_lookup = MyModel.objects.filter(my_datetime_field=dt).exists()
        assert exists_without_lookup, "Object with exact datetime does not exist."
        
        # The filter with the __date lookup that should also return True
        exists_with_date_lookup = MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()
        assert exists_with_date_lookup, "Object with datetime converted to date does not exist."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred. See stack trace for more information.")
```

Before running the script, there are a few things you need to adjust:

1. Replace `"your_project.settings"` with the path to your Django project's settings module.
2. Replace `"your_app.models"` and `MyModel` with the actual path to your Django model.
3. Depending on your Django project setup, you might need to adjust the timezone handling with `timezone.get_default_timezone()` to match the time zone used in your project.

This script performs the following actions:

- It configures the Django environment and database (assumes migrations are properly set up for `MyModel`).
- It creates a new model instance with a specified datetime.
- It attempts to verify if the object exists using two methods: directly by datetime and by converting the datetime to a date.

- If the assertions fail (indicating the issue is present), it will print a stack trace.
- If the script runs without errors, it means the issue is not observed under the test conditions.