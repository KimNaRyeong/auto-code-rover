# reproducer.py

import os
import django
from django.conf import settings
from django.db import models, OperationalError
from django.db.models import F, Window
from django.db.models.functions import Lag
from django.core.management import execute_from_command_line

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

# Configure Django settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # current file as the app
    ),
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Define the model
class LagTest(models.Model):
    modified = models.DateField()
    data = models.FloatField()
    amount = models.DecimalField(decimal_places=4, max_digits=7)

    class Meta:
        app_label = '__main__'

# Attempt to reproduce the issue
def main():
    # Apply migrations
    execute_from_command_line(['manage.py', 'makemigrations', '__main__'])
    execute_from_command_line(['manage.py', 'migrate'])

    # Create a lag window function query
    w = Window(
        expression=Lag('amount', 7),
        partition_by=[F('modified')],
        order_by=F('modified').asc()
    )

    try:
        # Triggering the query, expecting it to fail on SQLite with the specific OperationalError
        qs = LagTest.objects.annotate(w=w)
        list(qs)  # Force query execution
        # If this point is reached without error, the issue might have been fixed
        print("No OperationalError encountered. The issue seems to be fixed.")
        exit(0)
    except OperationalError as e:
        print_stacktrace(e)
        assert "near \"OVER\": syntax error" in str(e), "Unexpected OperationalError encountered."
        # The assertion will fail if the error message does not match, indicating a different problem

if __name__ == '__main__':
    try:
        main()
    except AssertionError as error:
        print(f"AssertionError: {error}")
        print_stacktrace(error)
        exit(1)  # Non-zero exit code for failure in reproducing the exact issue
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)
        exit(1)  # General failure code
