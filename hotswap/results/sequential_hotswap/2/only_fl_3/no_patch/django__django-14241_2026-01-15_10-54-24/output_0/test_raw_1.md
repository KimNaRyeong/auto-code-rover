Below is the `reproducer.py` script that aims to reproduce the described Django QuerySet issue. This script attempts to run the problematic query and checks for an `AssertionError` if the issue is present. Before running this script, ensure your Django environment is set up correctly, including the necessary models `Celebrity` and `ReservedName` in your Django project, and your database is properly migrated.

```python
import os
import django
from django.core.exceptions import FieldError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from your_app.models import Celebrity, ReservedName  # Adjust this import to your project structure

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

def test_union_query():
    try:
        qs1 = Celebrity.objects.all()
        qs2 = ReservedName.objects.all()
        result = qs1.union(qs2).values_list('name').first()
        print(f"Query successful, result: {result}")
        # Assuming the incorrect behavior is an exception, change as needed for the actual behavior
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The union query did not work as expected.")

if __name__ == '__main__':
    try:
        test_union_query()
    except AssertionError as e:
        print(f"Assertion error: {e}")
        exit(1)  # Exit with a non-zero code to indicate failure
    except FieldError as e:
        # This except block can be adjusted based on the specific error Django throws for the scenario
        print("Detected potential issue with queryset union:")
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed without issue.")
        exit(0)
```

**Notes:**

1. Replace `your_project.settings` with the import path of your Django project settings.
2. Replace `your_app.models` with the actual import path where your `Celebrity` and `ReservedName` models are defined.
3. This script assumes that the issue will raise an exception that can be caught. Depending on the specifics of the issue (e.g., an inaccurate query result rather than an exception), you might need to adjust the error handling logic.
4. Ensure that the Django environment is properly set up for this script to run, including the necessary models and database migrations.