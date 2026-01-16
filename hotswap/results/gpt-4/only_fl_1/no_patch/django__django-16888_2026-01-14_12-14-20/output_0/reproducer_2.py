# reproducerer.py
import os
import django
from django.core.management import execute_from_command_line
from django.conf import settings
from django.db import models
import decimal

# Setup minimal Django settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3"),}},
    INSTALLED_APPS=["__main__"],  # Register this module as an app
    TIME_ZONE="UTC",
    USE_TZ=True,
)

django.setup()

# Model definition
class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

# Initialize the database
execute_from_command_line(["manage.py", "migrate"])

# Exception stacktrace function
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

# Test function to trigger and handle the intended exception
def test_invalid_decimal_query():
    try:
        # Attempt to query a DecimalModel instance with dec_field value exceeding the max_digits
        DecimalModel.objects.get(dec_field='12345')
    except decimal.InvalidOperation as e:
        print_stacktrace(e)
        raise AssertionError("AssertionError: An InvalidOperation error occurred as expected due to max_digits limit.") from e
    except DecimalModel.DoesNotExist:
        pass  # If the model is not found, which is not the point of the test, ignore.
    else:
        # If no exception is raised, then it means the issue might have been resolved in a newer Django version
        print("No exception raised: The issue might have been fixed.")
        exit(0)

if __name__ == "__main__":
    test_invalid_decimal_query()
