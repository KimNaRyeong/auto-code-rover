import os
import django
from django.conf import settings
from django.db import models
from django.db.models.expressions import RawSQL

# Minimal settings necessary for the script to run.
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        '__main__',
    ],
    USE_TZ=True,
)

django.setup()

# Define models
class BaseItem(models.Model):
    title = models.CharField(max_length=32)
    class Meta:
        app_label = '__main__'

class Item(BaseItem):
    class Meta:
        app_label = '__main__'

# Create the necessary tables
from django.core.management import call_command
call_command('migrate', interactive=False, verbosity=0)

# Function to print stacktrace
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

def run_test():
    try:
        # Attempt to reproduce the issue
        queryset = Item.objects.all()
        queryset = queryset.annotate(title2=RawSQL("SELECT title FROM __main__baseitem", ()))
        count = queryset.count()  # This should raise an error if the issue exists
        
        # If the above statement did not raise an OperationalError, the issue is fixed
        print("The issue is fixed. Exiting with code 0.")
        exit(0)
        
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present") from e

if __name__ == '__main__':
    run_test()
