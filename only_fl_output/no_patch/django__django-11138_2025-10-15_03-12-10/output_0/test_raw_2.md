To write a `reproducer.py` that effectively reproduces the issue described, while integrating Django settings properly to avoid `ImproperlyConfigured` errors, you'll have to set up a minimal Django environment within the script. This means configuring Django settings on the fly and simulating model queries meaningfully.

Below is a fully self-contained script that sets up the necessary Django environment, mocks a model and database interaction, and attempts to demonstrate the timezone issue with date lookups explicitly. This script raises an `AssertionError` when the behavior doesn't align with expectations, indicating the presence of the described issue.

```python
import os
import sys
import django
from django.conf import settings
from django.db import models
from django.utils import timezone

# Define minimal Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    INSTALLED_APPS=(
        '__main__',  # Include this script as an app
    ),
    TIME_ZONE='Europe/Paris',
    USE_TZ=True,
)

# Initialize Django
django.setup()

# Define a mock model to simulate database interactions
class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

    class Meta:
        app_label = '__main__'

# Helper function to print a formatted traceback
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

# Main function to perform the actions described in the issue
def main():
    # Simulate saving an object into the database
    MyModel.objects.create(my_datetime_field=timezone.make_aware(timezone.datetime(2017, 7, 6, 20, 50)))

    # Perform a date lookup that should logically succeed
    dt = timezone.make_aware(timezone.datetime(2017, 7, 6, 20, 50))
    exists_using_datetime = MyModel.objects.filter(my_datetime_field=dt).exists()

    # Perform a date lookup using `__date` that exposes the issue
    exists_using_date_lookup = MyModel.objects.filter(my_datetime_field__date=dt.date()).exists()

    # Assertion to verify if the issue is present
    try:
        assert exists_using_datetime == exists_using_date_lookup, "Timezone handling issue detected with date lookups."
    except AssertionError as e:
        print_stacktrace(e)
        raise
    
    print("No issue detected with timezone handling in date lookups.")

if __name__ == '__main__':
    try:
        main()
    except AssertionError:
        os._exit(1)  # Exit with a non-zero status code to indicate failure
    
    os._exit(0)  # Exit with a zero status code to indicate success
```

This script dynamically configures Django to use an in-memory SQLite database, which simplifies the demonstration without worrying about setting up a real MySQL or any other database. However, it should accurately reproduce the timezone issue in question within Django's ORM system by comparing direct datetime lookups with date-based lookups.

To run this script, execute `python3 reproducer.py` in a terminal. This assumes you have a Python environment with Django installed. The script should exit with code 0 if the issue is fixed or non-zero if the issue is present, per your instructions.