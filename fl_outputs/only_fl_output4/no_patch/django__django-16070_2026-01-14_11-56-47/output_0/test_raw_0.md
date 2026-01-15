```python
import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.exceptions import FieldError

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    INSTALLED_APPS=("__main__",),  # This script is the app
    ROOT_URLCONF="__main__",
)

django.setup()

class SomeRelatedModel(models.Model):
    name = models.CharField(max_length=100)

class SomeModel(models.Model):
    some_foreign_key = models.ForeignKey(SomeRelatedModel, on_delete=models.CASCADE)

try:
    # Reproducer starts here
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

    try:
        SomeModel.objects.all().order_by("some_foreign_key__non_existing_field")

        # If no error is raised, the issue exists
        raise AssertionError("Order by non-existing related field should not work silently")

    except FieldError as e:
        print("Proper FieldError raised, issue not present.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```