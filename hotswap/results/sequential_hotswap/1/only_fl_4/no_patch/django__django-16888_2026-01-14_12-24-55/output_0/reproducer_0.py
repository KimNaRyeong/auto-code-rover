import decimal
import os
import django
from django.conf import settings
from django.db import models

# Define settings for the Django app
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        '__main__',
    ),
    USE_TZ=True,
)

django.setup()


# Definition of the model associated with the issue
class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)


# to print stack trace of the issue
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


# Main section to create the table and perform the query that triggers the issue.
if __name__ == '__main__':
    from django.core.management import call_command
    from django.db.utils import OperationalError

    call_command('migrate')

    try:
        # Performing the operation that should raise an error if the issue is present.
        DecimalModel.objects.get(dec_field='12345')
        assert False, "The issue did not occur."
    except decimal.InvalidOperation as e:
        # If the specific exception occurs, the issue is present.
        print_stacktrace(e)
        raise AssertionError("The issue is present.")
    except DecimalModel.DoesNotExist:
        # If the object is not found, which means the DecimalField check is passing,
        # then the issue is considered fixed.
        print("No issue found, test passed.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "An unexpected error occurred."
