```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.utils import timezone

# Define a bare minimum settings configuration
settings.configure(
    DEBUG=True,
    USE_TZ=True,
    TIME_ZONE='Europe/Paris',  # App's timezone
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'test_db',  # Make sure to adjust this to your actual database
            'USER': 'root',  # Adjust as per your database user
            'PASSWORD': '',  # Adjust as per your database password
            'HOST': 'localhost',  # Adjust as per your database host
            'PORT': '',  # Adjust as per your database port
            'TIME_ZONE': 'Europe/Paris',  # Database timezone
        }
    },
    INSTALLED_APPS=[
        '__main__',  # Allows us to define models directly in this script
    ]
)

django.setup()

# Model definition
class MyModel(models.Model):
    my_datetime_field = models.DateTimeField()

    class Meta:
        app_label = '__main__'


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
    # Ensuring tables are created
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(MyModel)

    try:
        # Date to test with
        dt = timezone.make_aware(timezone.datetime(2017, 7, 6, 20, 50))
        
        # Creating a sample record matching the test date
        MyModel.objects.create(my_datetime_field=dt)

        # Test: Querying with datetime should find the record
        assert MyModel.objects.filter(my_datetime_field=dt).exists(), "Record should be found with datetime"

        # Test: Querying with date should also find the record, but it doesn't
        assert MyModel.objects.filter(my_datetime_field__date=dt.date()).exists(), "Record should be found with date"
    
    except AssertionError as e:
        print_stacktrace(e)
        os._exit(1)  # Make sure the process exits with an error code

if __name__ == "__main__":
    main()
```