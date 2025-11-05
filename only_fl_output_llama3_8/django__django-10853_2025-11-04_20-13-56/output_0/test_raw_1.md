Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.db.models.functions.window import RowNumber
from django.db.models import F, Window

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
    try:
        # Set up Django environment
        os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
        django.setup()

        # Create a test model
        class MyModel(models.Model):
            pass

        # Annotate the model with a window function
        MyModel.objects.annotate(rn=Window(expression=RowNumber(), order_by=[F('pk')]))

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected OperationalError")

if __name__ == "__main__":
    main()
```

This script sets up a Django environment, creates a test model, and attempts to annotate the model with a window function. If an `OperationalError` is raised (which should happen if you're using SQLite 3.21.0 or earlier), it prints the stack trace and raises an `AssertionError`.