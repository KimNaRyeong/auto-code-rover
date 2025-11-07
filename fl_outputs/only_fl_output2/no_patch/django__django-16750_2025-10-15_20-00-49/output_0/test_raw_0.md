```python
import os
import sys
from django.conf import settings
from django.db import models
from django.db.models.functions import Chr
from django.db.models import Value, CharField

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

# Settings for Django to run standalone scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',
    ),
    USE_TZ=True,
)

models.signals.post_migrate.connect(
    lambda **kwargs: [print("Migration completed."), sys.exit()],
    weak=False
)

class Author(models.Model):
    name = models.CharField(max_length=100)

try:
    from django.core.management import execute_from_command_line

    execute_from_command_line(['manage.py', 'migrate'])

    # Attempt to annotate an Author object with a character representation of a number
    try:
        Author.objects.annotate(first_letter=Chr(Value(77)))
        raise AssertionError("The issue is expected to raise ValueError but did not.")
    except ValueError as ve:
        print_stacktrace(ve)
        # Asserting specific error message for clarity. Modify as needed based on actual error observed.
        assert str(ve) == "invalid literal for int() with base 10: 'M'"
        sys.exit(0)  # Exit successfully if the expected issue occurs
    except AssertionError as ae:
        # Reraise the AssertionError if the issue does not occur as expected.
        raise ae
    except Exception as e:
        print("An unexpected error occurred.", file=sys.stderr)
        print_stacktrace(e)
        sys.exit(1)

except Exception as e:
    print("Failed to run migrations or annotate.", file=sys.stderr)
    print_stacktrace(e)
    sys.exit(1)
```