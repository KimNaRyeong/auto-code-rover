Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.db.models import Q
from django.db.backends.sqlite3.client import DatabaseClient
from django.test.utils import CaptureStandardOutput, CaptureStderr
from django.core.management.base import BaseCommand

class PredictionData(models.Model):
    data = models.JSONField()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
    django.setup()
    
    # Create a test database
    from django.db.backends.sqlite3.client import DatabaseClient
    client = DatabaseClient()
    client.create_test_db(verbosity=0)

    # Create the model
    PredictionData.objects.create(data={'value': True})

    # Run the query and check the result
    try:
        results = list(PredictionData.objects.values_list('data', 'data__value'))
        assert all(isinstance(x[1], bool) for x in results)
    except AssertionError as e:
        print_stacktrace(e)
        raise

    os._exit(0)

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

if __name__ == "__main__":
    main()
```

This script sets up a test Django project, creates the model and some data, runs the query, and checks that the result is as expected. If the result is not as expected (i.e., if the values are integers instead of booleans), it prints the stack trace and raises an `AssertionError`.