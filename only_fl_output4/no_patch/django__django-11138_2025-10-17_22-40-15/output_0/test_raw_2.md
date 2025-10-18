To create a standalone Python file named `reproducer.py` that correctly reproduces the described issue and adheres to your execution requirements, including error handling and output formatting using the provided `print_stacktrace` function, follow this revised structure.

This version assumes that the Django environment setup, database configurations, and model definitions are correctly placed within a Django project structure. It’s tailored to spotlight the specific timezone-aware date querying issue with Django ORM when using MySQL, SQLite, or Oracle as the database backend.

```python
# reproducer.py
import os
import django
import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone

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

def setup_environment():
    # Minimal Django settings required for the script to run.
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
            }
        },
        USE_TZ=True,
        TIME_ZONE='Europe/Paris',
        INSTALLED_APPS=[
            '__main__',  # This script contains the model, so it's considered an app by Django.
        ],
    )

    django.setup()

class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

    class Meta:
        app_label = '__main__'

def main():
    setup_environment()

    # Creating the tables necessary for our model. In a real project, Django's migrate command would usually do this.
    from django.db import connection
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(MyModel)

    # Deleting any existing entries for cleanliness
    MyModel.objects.all().delete()

    # Example date to work with
    example_datetime = timezone.make_aware(datetime.datetime(2017, 7, 6, 20, 50))
    
    # Inserting a new MyModel instance using the example datetime
    instance = MyModel.objects.create(my_datetime_field=example_datetime)
    instance.save()

    # Attempting to retrieve the instance based on the datetime field
    assert MyModel.objects.filter(my_datetime_field=example_datetime).exists(), "Datetime-based filter failed."

    # Attempting to retrieve the instance based on the date part of the datetime field
    try:
        assert MyModel.objects.filter(my_datetime_field__date=example_datetime.date()).exists(), "Date-based filter failed."
        print("No issue detected. Exiting with code 0.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

Execute this script with `python3 reproducer.py` in the root directory of a Django project. This script now takes care to establish a minimal Django environment programmatically, define a test model, and set up a SQLite database to store the data. It first tests if it can insert and then retrieve a `MyModel` instance based on a timezone-aware datetime. Subsequently, it tries to retrieve the instance based on the date alone. When the second retrieval fails due to the identified issue, it catches the `AssertionError` and outputs a stack trace using the provided `print_stacktrace` function.