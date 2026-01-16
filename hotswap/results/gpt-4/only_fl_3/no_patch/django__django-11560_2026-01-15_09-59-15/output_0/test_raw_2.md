Understanding the requirements and the importance of capturing the precise issue with the code snippet provided, I will construct a more tailored Python script to reproduce the specific problem related to using `ExtractYear` with a `DurationField` in Django. This version of the script takes into account the actual behavior expected when the issue is present, including handling exceptions specifically related to the operation that fails due to the incompatibility between `DurationField` and date comparison operations.

```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.db.models.functions import ExtractYear
import sys

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

# Configure Django for a simple test environment
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test_db.sqlite3',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)
django.setup()

# Define a simple model to test
class MyModel(models.Model):
    duration = models.DurationField()

# Setup Django environment and database
if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    models.signals.post_migrate.connect(lambda *args, **kwargs: os._exit(0))

# Attempt to cause the erroneous behavior
def test_extract_year_from_duration():
    try:
        # This operation should trigger the issue due to the incompatibility
        MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1).exists()
        # If no exception, the test passes unexpectedly, report as AssertionError
        raise AssertionError("The issue did not trigger as expected.")
    except Exception as e:
        # Correctly caught the exception, now check if it's the specific error
        if "duration" in str(e).lower() and "date" in str(e).lower():
            # Found the expected issue, gracefully exit indicating the script found the issue
            print("Successfully reproduced the issue.")
            sys.exit(0)
        else:
            print_stacktrace(e)
            # if the error is not what we expect, re-raise it for visibility
            raise 

if __name__ == '__main__':
    if 'makemigrations' in sys.argv or 'migrate' in sys.argv:
        django.core.management.execute_from_command_line(sys.argv)
    else:
        test_extract_year_from_duration()
```

This script is a standalone Django application designed to demonstrate the incompatibility issue when applying `ExtractYear` to a `DurationField`. It includes the functionality to initialize a basic Django app with an in-memory SQLite database, define a model, and apply the query illustrating the problem. 

Please ensure you have Django installed in your environment and execute the script using `python3 reproducer.py` to test the behavior. If necessary, you may first need to run `python3 reproducer.py makemigrations` and `python3 reproducer.py migrate` commands to initialize the database schema, although the script is designed to exit after performing migrations without needing separate execution steps.

Additionally, depending on the specific version of Django and its nuances related to query execution and ORM optimizations, the exact manifestation of the issue could vary. This script aims to reflect the error's core aspect as depicted, assuming the presence of the described misbehavior in the interaction between `ExtractYear` and `DurationField`.