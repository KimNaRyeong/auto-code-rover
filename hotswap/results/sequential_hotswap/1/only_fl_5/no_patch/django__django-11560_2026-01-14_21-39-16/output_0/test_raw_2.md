Given the explanation and the aim to directly reproduce the reported issue with a `DurationField` in Django, we'll write a script that attempts to annotate `MyModel` objects using `ExtractYear` on a `DurationField`, which according to the description, should fail and provide insight into the problem. This updated approach ensures the query actually executes by forcing the evaluation of the queryset, catching the exception to confirm the issue.

```python
import os
import sys
from django.conf import settings

# Setup the minimal Django environment
def setup_django_environment():
    settings.configure(
        SECRET_KEY='a_very_secret_key',
        INSTALLED_APPS=('__main__',),  # Current file is the app
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',  # Using in-memory database for simplicity
            }
        },
    )

    # Prepare the environment
    from django.core.management import call_command
    from django.apps import apps
    apps.populate(settings.INSTALLED_APPS)
    call_command('migrate', verbosity=0)

setup_django_environment()

from django.db import models
from django.db.models.functions import ExtractYear

# Define model after setting up Django to avoid issues
class MyModel(models.Model):
    duration = models.DurationField()

from django.db import connection

# Main logic to reproduce the issue and handle assertion
def main():
    # Make sure Django's model system is ready
    if not models.Model.check.__test__:  # Remove in Django 3.2+
        setup_django_environment()

    # Usually, you'd create some instances here, but since the issue is at the query level,
    # we won't need actual instances to reproduce the error

    try:
        # Forcing the query to run by converting it to a list
        list(MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1))

        # If the program reaches this point, the issue was not reproduced
        print("The issue was not reproduced.")
    
    except Exception as e:
        print_stacktrace(e)
        assert "interval are not comparable with dates" in str(e), "The expected issue was not encountered."

# Support function to print detailed traceback
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

if __name__ == '__main__':
    main()
```

Explanation:
- We first set up a minimal Django environment within our script. This is crucial because Django models require a configured environment to interact with the database and perform ORM operations.
- We define a simple model `MyModel` with a `DurationField`, mirroring the scenario described in the issue.
- In the main logic, we use the Django ORM to annotate `MyModel` objects using `ExtractYear` on the duration field and filter based on the annotation. To ensure the queryset is evaluated and the database is actually queried, we wrap the queryset with `list()`. It's this evaluation that should trigger the error as described.
- If the specific error occurs, it will be caught, and the provided `print_stacktrace` function will output detailed information about the error, helping to confirm the nature of the issue.